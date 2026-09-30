from pathlib import Path

p = Path('docs/tax-calculator.html')
s = p.read_text(encoding='utf-8')

# Core SEO wording
s = s.replace(
    '<title>Налоги цифрового кочевника в Испании 2026 — калькулятор IRPF</title>',
    '<title>Калькулятор налогов цифрового кочевника в Испании 2026 — IRPF и autónomo</title>',
    1,
)
s = s.replace(
    '<meta name="description" content="Налоги цифрового кочевника в Испании в 2026 году: калькулятор IRPF, взносов autónomo, чистого и минимального дохода для DNV.">',
    '<meta name="description" content="Калькулятор налогов цифрового кочевника в Испании на 2026 год: IRPF, взносы autónomo, чистый доход и минимальный доход для визы и ВНЖ DNV.">',
    1,
)
s = s.replace(
    '<h1>Налоги цифрового кочевника в Испании: калькулятор 2026</h1>',
    '<h1>Калькулятор налогов цифрового кочевника в Испании — 2026</h1>',
    1,
)
s = s.replace(
    '<p class="lead">Ориентировочно считает IRPF, взносы autónomo, чистый доход и минимальный доход для DNV с учетом семьи.</p>',
    '<p class="lead">Калькулятор ориентировочно считает IRPF, взносы autónomo, чистый доход и минимальный доход для визы и ВНЖ цифрового кочевника (DNV) с учетом состава семьи.</p>',
    1,
)

canonical = '    <link rel="canonical" href="https://ola-espanola.github.io/docs/tax-calculator.html">'
if 'property="og:title"' not in s:
    social = '''    <meta property="og:locale" content="ru_RU">\n    <meta property="og:site_name" content="Ola Española">\n    <meta property="og:type" content="website">\n    <meta property="og:title" content="Калькулятор налогов цифрового кочевника в Испании 2026 — IRPF и autónomo">\n    <meta property="og:description" content="Калькулятор налогов цифрового кочевника в Испании на 2026 год: IRPF, взносы autónomo, чистый доход и минимальный доход для визы и ВНЖ DNV.">\n    <meta property="og:url" content="https://ola-espanola.github.io/docs/tax-calculator.html">\n    <meta property="article:modified_time" content="2026-09-30">\n    <meta name="twitter:card" content="summary">\n    <meta name="twitter:title" content="Калькулятор налогов цифрового кочевника в Испании 2026">\n    <meta name="twitter:description" content="Расчёт IRPF, взносов autónomo, чистого дохода и минимального дохода для визы и ВНЖ цифрового кочевника в Испании.">'''
    s = s.replace(canonical, canonical + '\n' + social, 1)

if '"@type": "WebPage"' not in s:
    schema = '''    <script type="application/ld+json">\n    {\n      "@context": "https://schema.org",\n      "@type": "WebPage",\n      "name": "Калькулятор налогов цифрового кочевника в Испании — 2026",\n      "description": "Калькулятор налогов цифрового кочевника в Испании на 2026 год: IRPF, взносы autónomo, чистый доход и минимальный доход для визы и ВНЖ DNV.",\n      "url": "https://ola-espanola.github.io/docs/tax-calculator.html",\n      "dateModified": "2026-09-30",\n      "inLanguage": "ru",\n      "mainEntity": {\n        "@type": "WebApplication",\n        "name": "Калькулятор налогов цифрового кочевника в Испании",\n        "applicationCategory": "FinanceApplication",\n        "operatingSystem": "Web"\n      }\n    }\n    </script>\n'''
    s = s.replace('    <!-- structured:breadcrumbs -->', schema + '    <!-- structured:breadcrumbs -->', 1)

if '.seo-footer{' not in s and '.seo-footer {' not in s:
    s = s.replace(
        '      @media(max-width:820px){.calculator-page{padding:28px 16px 52px}.result-grid{grid-template-columns:1fr}.dnv-status{grid-template-columns:1fr}.status-badge{justify-self:start}}',
        '      @media(max-width:820px){.calculator-page{padding:28px 16px 52px}.result-grid{grid-template-columns:1fr}.dnv-status{grid-template-columns:1fr}.status-badge{justify-self:start}}\n      .seo-footer{margin-top:54px;padding-top:24px;border-top:1px solid var(--line);color:var(--muted);font-size:14px;line-height:1.65}.seo-footer h2{margin:0 0 14px;color:var(--muted);font-size:18px}.seo-footer p{margin:10px 0}.seo-footer a{color:var(--nav)}',
        1,
    )

if 'class="seo-footer"' not in s:
    marker = '      </section>\n        </div>\n      </div>\n    </main>'
    footer = '''      </section>\n\n      <section class="seo-footer" aria-label="О калькуляторе налогов цифрового кочевника">\n        <h2>Калькулятор налогов цифрового кочевника в Испании</h2>\n        <p>Калькулятор помогает предварительно оценить IRPF, взносы autónomo и чистый доход при жизни в Испании, а также сравнить доход с минимальным порогом для визы и ВНЖ цифрового кочевника. Итог зависит от формата работы, состава семьи, автономного сообщества и доступных налоговых льгот.</p>\n        <p>Подробно о налоговой нагрузке и примерах расчётов читайте в статье <a href="../blog/nalogi-cifrovogo-kochevnika-ispania.html">Налоги цифрового кочевника в Испании</a>. Требования к минимальному доходу собраны на странице <a href="eligibility.html">Кому подходит ВНЖ</a>, а общий порядок оформления — в <a href="digital-nomad-spain-guide.html">полном гайде по визе и ВНЖ цифрового кочевника</a>.</p>\n      </section>\n        </div>\n      </div>\n    </main>'''
    if marker not in s:
        raise RuntimeError('footer insertion marker not found')
    s = s.replace(marker, footer, 1)

p.write_text(s, encoding='utf-8')

# Keep sitemap lastmod current if page is present.
sp = Path('sitemap.xml')
sm = sp.read_text(encoding='utf-8')
needle = '<loc>https://ola-espanola.github.io/docs/tax-calculator.html</loc>'
pos = sm.find(needle)
if pos >= 0:
    block_end = sm.find('</url>', pos)
    block = sm[pos:block_end]
    import re
    new_block = re.sub(r'<lastmod>[^<]+</lastmod>', '<lastmod>2026-09-30</lastmod>', block)
    sm = sm[:pos] + new_block + sm[block_end:]
    sp.write_text(sm, encoding='utf-8')

print('Updated calculator SEO')
