#!/usr/bin/env node
'use strict';

// Run before committing. The browser only receives the generated HTML.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');

const ASSET_VERSION = crypto.createHash('sha256')
  .update(fs.readFileSync(path.join(root, 'assets/css/styles.css')))
  .update(fs.readFileSync(path.join(root, 'assets/js/metrika.js')))
  .digest('hex')
  .slice(0, 10);

function publicPages() {
  const pages = ['index.html'];
  for (const directory of ['docs', 'blog']) {
    for (const entry of fs.readdirSync(path.join(root, directory), { withFileTypes: true })) {
      if (entry.isFile() && entry.name.endsWith('.html')) pages.push(`${directory}/${entry.name}`);
    }
  }
  return pages.sort();
}

function template(name, context, stack = []) {
  if (!/^[a-z-]+$/.test(name) || stack.includes(name)) throw new Error(`Invalid or recursive partial: ${name}`);
  let html = fs.readFileSync(path.join(root, 'partials', `${name}.html`), 'utf8').replace(/\r\n/g, '\n').trimEnd();
  // Conditional blocks occupy whole lines; nesting is deliberately unsupported.
  html = html.replace(/^\{\{#(\w+)\}\}\n([\s\S]*?)^\{\{\/\1\}\}(?:\n|$)/gm, (_, flag, body) => {
    let enabled;
    if (flag === 'guide') enabled = context.guide;
    else if (/^blog[1-9]\d*$/.test(flag)) enabled = context.blogItems >= Number(flag.slice(4));
    else throw new Error(`Unknown condition in ${name}: ${flag}`);
    return enabled ? body : '';
  });
  html = html.replace(/^([ \t]*)\{\{>([a-z-]+)\}\}$/gm, (_, indent, partial) =>
    template(partial, context, [...stack, name]).split('\n').map(line => indent + line).join('\n'));
  html = html.replace(/\{\{(\w+)\}\}/g, (_, key) => {
    if (!Object.hasOwn(context, key)) throw new Error(`Unknown value in ${name}: ${key}`);
    return String(context[key]);
  });
  if (html.includes('{{') || html.includes('}}')) throw new Error(`Unresolved template syntax in ${name}`);
  return html;
}

function destination(url) {
  if (!url.startsWith('/') || url.startsWith('//')) return null;
  const [, pathname, suffix] = url.match(/^([^?#]*)(.*)$/);
  const file = pathname.endsWith('/') ? `${pathname}index.html` : pathname;
  return { file: file.slice(1), suffix };
}

function linksForPage(html, page) {
  html = html.replace(/<a\b[^>]*>/g, tag => {
    const url = tag.match(/\bhref="([^"]*)"/)?.[1];
    const target = url && destination(url);
    const classes = tag.match(/\bclass="([^"]*)"/)?.[1].split(/\s+/) || [];
    if (!target || target.file !== page || classes.includes('brand')) return tag;
    if (!classes.includes('active')) classes.push('active');
    tag = /\bclass="/.test(tag)
      ? tag.replace(/\bclass="[^"]*"/, `class="${classes.join(' ')}"`)
      : tag.replace('<a', `<a class="${classes.join(' ')}"`);
    if (!/\baria-current=/.test(tag)) tag = tag.replace(/>$/, ' aria-current="page">');
    return tag;
  });
  return html.replace(/\b(href|src)="([^"]*)"/g, (attribute, name, url) => {
    const target = destination(url);
    if (!target) return attribute;
    const relative = path.posix.relative(path.posix.dirname(page), target.file);
    return `${name}="${relative}${target.suffix}"`;
  });
}

function versionAssets(html) {
  return html
    .replace(/((?:\/|(?:\.\.\/)*)assets\/css\/styles\.css)(?:\?v[^\"'\s>]*)?/g, `$1?v=${ASSET_VERSION}`)
    .replace(/((?:\/|(?:\.\.\/)*)assets\/js\/metrika\.js)(?:\?v[^\"'\s>]*)?/g, `$1?v=${ASSET_VERSION}`);
}

function updatePage(source, page) {
  const eol = source.includes('\r\n') ? '\r\n' : '\n';
  const normalized = source.replace(/\r\n/g, '\n');
  const block = /^([ \t]*)<!-- shared:([a-z-]+)(?: ([a-z0-9-]+))? -->\n([\s\S]*?)^[ \t]*<!-- \/shared:\2 -->/gm;
  const matches = [...normalized.matchAll(block)];
  const kinds = matches.map(match => match[2]);
  const headers = kinds.filter(kind => kind === 'header' || kind === 'calculator-header');
  if (headers.length !== 1) throw new Error(`${page}: expected one shared header`);
  const sidebarCount = kinds.filter(kind => kind === 'sidebar').length;
  if (sidebarCount !== 1) throw new Error(`${page}: unexpected number of sidebars`);
  const outside = normalized.replace(block, '');
  if (/<!--\s*\/?shared:/.test(outside) || /<(?:header|aside)\b[^>]*class="(?:site-header|calculator-header|sidebar)"/.test(outside)) {
    throw new Error(`${page}: malformed shared markers or unmarked layout`);
  }
  const result = normalized.replace(block, (whole, indent, kind, variant, body) => {
    if (/<!--\s*\/?shared:/.test(body)) throw new Error(`${page}: nested shared markers`);
    if (!['header', 'calculator-header', 'sidebar'].includes(kind)) throw new Error(`${page}: unknown shared block ${kind}`);
    if (kind === 'sidebar' ? !/^(guide|blog-\d+)$/.test(variant || '') : variant !== undefined) {
      throw new Error(`${page}: invalid variant for ${kind}`);
    }
    const context = {
      brandClass: kind === 'calculator-header' ? ' calculator-brand' : '',
      sidebarLabel: variant === 'guide' ? 'Разделы гида' : 'Разделы сайта',
      guide: variant === 'guide',
      blogItems: variant?.startsWith('blog-') ? Number(variant.slice(5)) : 0,
    };
    const rendered = linksForPage(template(kind, context), page).split('\n').map(line => indent + line).join('\n');
    return `${indent}<!-- shared:${kind}${variant ? ` ${variant}` : ''} -->\n${rendered}\n${indent}<!-- /shared:${kind} -->`;
  });
  return versionAssets(result).replace(/\n/g, eol);
}

function main() {
  const args = process.argv.slice(2);
  if (args.some(arg => arg !== '--check') || args.length > 1) throw new Error('Usage: node scripts/update-layout.cjs [--check]');
  // Validate and render every page before writing any file.
  const pages = publicPages();
  const changes = [];
  for (const page of pages) {
    const filename = path.join(root, page);
    const before = fs.readFileSync(filename, 'utf8');
    const after = updatePage(before, page);
    if (before !== after) changes.push({ page, filename, after });
  }
  if (args.includes('--check')) {
    if (changes.length) {
      console.error(`Outdated shared layout in ${changes.length} page(s):\n${changes.map(change => change.page).join('\n')}\nRun: node scripts/update-layout.cjs`);
      process.exitCode = 1;
    } else console.log(`Shared layout is up to date in all ${pages.length} pages.`);
    return;
  }
  for (const change of changes) fs.writeFileSync(change.filename, change.after);
  console.log(`Updated ${changes.length} of ${pages.length} pages. Generated HTML is ready for local viewing and Git.`);
}

try {
  main();
} catch (error) {
  console.error(`Layout update failed: ${error.message}`);
  process.exitCode = 1;
}
