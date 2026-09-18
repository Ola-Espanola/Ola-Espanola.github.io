'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const pages = ['index.html', ...['docs', 'blog'].flatMap(dir =>
  fs.readdirSync(path.join(root, dir)).filter(file => file.endsWith('.html')).map(file => `${dir}/${file}`))];
const read = (directory, file) => fs.readFileSync(path.join(directory, file), 'utf8');
const run = (directory, ...args) => spawnSync(process.execPath, [path.join(directory, 'scripts/update-layout.cjs'), ...args], { encoding: 'utf8', cwd: os.tmpdir() });
const snapshot = directory => Object.fromEntries(pages.map(file => [file, read(directory, file)]));
const contentOnly = html => html.replace(/^[ \t]*<!-- shared:([a-z-]+)[^\r\n]*-->\r?\n[\s\S]*?^[ \t]*<!-- \/shared:\1 -->/gm, '[shared layout]');
const blocks = html => [...html.matchAll(/<!-- shared:([a-z-]+)[^\r\n]*-->\r?\n([\s\S]*?)<!-- \/shared:\1 -->/g)].map(match => match[2]).join('\n');

function fixture(t) {
  const temporaryRoot = fs.realpathSync(os.tmpdir());
  const directory = fs.mkdtempSync(path.join(temporaryRoot, 'ola-layout-test-'));
  t.after(() => {
    const resolved = fs.realpathSync(directory);
    assert.equal(path.dirname(resolved), temporaryRoot);
    assert(path.basename(resolved).startsWith('ola-layout-test-'));
    fs.rmSync(resolved, { recursive: true, force: true });
  });
  fs.cpSync(path.join(root, 'partials'), path.join(directory, 'partials'), { recursive: true });
  fs.mkdirSync(path.join(directory, 'scripts'));
  fs.copyFileSync(path.join(root, 'scripts/update-layout.cjs'), path.join(directory, 'scripts/update-layout.cjs'));
  for (const file of pages) {
    fs.mkdirSync(path.dirname(path.join(directory, file)), { recursive: true });
    fs.copyFileSync(path.join(root, file), path.join(directory, file));
  }
  return directory;
}

test('committed HTML matches the common templates; --check never writes', () => {
  const before = snapshot(root);
  const result = run(root, '--check');
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(snapshot(root), before);
});

test('one edit reaches every header and sidebar, preserves article content and is repeatable', t => {
  const directory = fixture(t);
  const before = snapshot(directory);
  fs.writeFileSync(path.join(directory, 'partials/brand.html'), read(directory, 'partials/brand.html').replace('la Española</span>', 'la TEST</span>'));
  fs.writeFileSync(path.join(directory, 'partials/sidebar.html'), read(directory, 'partials/sidebar.html').replace('Полезные ссылки', 'TEST ссылки'));
  assert.equal(run(directory, '--check').status, 1);
  assert.deepEqual(snapshot(directory), before, '--check changed pages');
  const result = run(directory);
  assert.equal(result.status, 0, result.stderr);
  for (const file of pages) {
    const after = read(directory, file);
    assert(after.includes('la TEST</span>'), file);
    assert.equal(after.includes('TEST ссылки'), file !== 'docs/tax-calculator.html', file);
    assert.equal(contentOnly(after), contentOnly(before[file]), file);
    assert.equal(after.includes('\r\n'), before[file].includes('\r\n'), 'Line endings: ' + file);
  }
  const after = snapshot(directory);
  assert.equal(run(directory).status, 0);
  assert.deepEqual(snapshot(directory), after, 'Second update was not idempotent');
  assert.equal(run(directory, '--check').status, 0);
});

test('generated navigation works from disk and selects the current page', () => {
  for (const file of pages) {
    const html = read(root, file);
    const layout = blocks(html);
    for (const [, url] of layout.matchAll(/\b(?:href|src)="([^"]+)"/g)) {
      assert(!url.startsWith('/'), `${file}: non-local path ${url}`);
      assert(fs.existsSync(path.resolve(root, path.dirname(file), url)), `${file}: missing ${url}`);
    }
    const sidebar = layout.match(/<aside\b[\s\S]*?<\/aside>/)?.[0];
    if (!sidebar) {
      assert.equal(file, 'docs/tax-calculator.html');
      assert(layout.includes('brand calculator-brand'));
      continue;
    }
    const active = [...sidebar.matchAll(/<a\b([^>]+)>/g)].filter(([, attributes]) => /\bclass="[^"]*\bactive\b/.test(attributes));
    assert.equal(active.length, 1, file);
    const attributes = active[0][1];
    const href = attributes.match(/\bhref="([^"]+)"/)[1];
    assert.equal(path.posix.normalize(path.posix.join(path.posix.dirname(file), href)), file);
    assert(attributes.includes('aria-current="page"'), file);
  }
});

test('a missing marker aborts before writing any page', t => {
  const directory = fixture(t);
  fs.appendFileSync(path.join(directory, 'partials/header.html'), '\n<!-- updated -->\n');
  fs.writeFileSync(path.join(directory, 'index.html'), read(directory, 'index.html').replace('<!-- /shared:sidebar -->', ''));
  const before = snapshot(directory);
  const result = run(directory);
  assert.equal(result.status, 1);
  assert.match(result.stderr, /index\.html/);
  assert.deepEqual(snapshot(directory), before);
});

test('invalid template syntax aborts without changing generated files', t => {
  const directory = fixture(t);
  fs.appendFileSync(path.join(directory, 'partials/sidebar.html'), '\n{{misspelledValue}}\n');
  const before = snapshot(directory);
  const result = run(directory);
  assert.equal(result.status, 1);
  assert.match(result.stderr, /Unknown value.*misspelledValue/);
  assert.deepEqual(snapshot(directory), before);
});

test('a new page is discovered and gets its own active navigation', t => {
  const directory = fixture(t);
  fs.copyFileSync(path.join(directory, 'docs/cuenta-ajena.html'), path.join(directory, 'docs/example.html'));
  fs.writeFileSync(path.join(directory, 'partials/sidebar.html'), read(directory, 'partials/sidebar.html').replace('</aside>', '  <a href="/docs/example.html">Example</a>\n</aside>'));
  const result = run(directory);
  assert.equal(result.status, 0, result.stderr);
  const example = read(directory, 'docs/example.html');
  assert.match(example, /<a class="active" href="example\.html" aria-current="page">Example<\/a>/);
  assert.equal((example.match(/class="active"/g) || []).length, 1);
  assert.equal(run(directory, '--check').status, 0);
});
