from pathlib import Path
import json

DATE='2026-09-30'
STYLE='''    <style>\n      .seo-footer { margin-top: 54px; padding-top: 24px; border-top: 1px solid var(--line); color: var(--muted); font-size: 14px; line-height: 1.65; }\n      .seo-footer h2 { margin: 0 0 14px; color: var(--muted); font-size: 18px; }\n      .seo-footer p { margin: 10px 0; }\n      .seo-footer a { color: var(--nav); }\n    </style>\n'''

articles = {
'nalogi-cifrovogo-kochevnika-ispania.html': {
 'title':'Налоги цифрового кочевника в Испании 2026: autónomo, IRPF и Бекхэм',
 'desc':'Налоги цифрового кочевника в Испании в 2026 году: IRPF, взносы autónomo, работа в найме, режим Бекхэма, стартовые льготы и примеры расчётов.',
 'headline':'Налоги цифрового кочевника в Испании: сколько остается после налогов и соцстраха',
 'url':'https://ola-espanola.github.io/blog/nalogi-cifrovogo-kochevnika-ispania.html',
 'footer_h':'Налоги цифрового кочевника и ВНЖ в Испании',
 'footer_p1':'Налоговая нагрузка цифрового кочевника в Испании зависит от формата работы, дохода, состава семьи и доступных льгот. Для предварительной оценки можно использовать <a href="../docs/tax-calculator.html">налоговый калькулятор</a>, а требования к минимальному доходу для самого ВНЖ собраны на странице <a href="../docs/eligibility.html">Кому подходит ВНЖ</a>.',
 'footer_p2':'Если вы готовите подачу, используйте полный список документов <a href="../docs/cuenta-ajena.html">для работы в найме</a> или <a href="../docs/contract-work.html">для работы по контракту</a>. Общий порядок получения визы и ВНЖ разобран в <a href="../docs/digital-nomad-spain-guide.html">полном гайде по цифровому кочевнику в Испании</a>.'
},
'statistika-nomadov-ispania.html': {
 'title':'Статистика ВНЖ цифровых кочевников в Испании: 2023–2025',
 'desc':'Статистика ВНЖ цифровых кочевников в Испании за 2023–2025 годы: сколько разрешений выдано, рост программы, заявители из России, США и других стран.',
 'headline':'Сколько ВНЖ цифровых кочевников выдаёт Испания: статистика Digital Nomad',
 'url':'https://ola-espanola.github.io/blog/statistika-nomadov-ispania.html',
 'footer_h':'Статистика ВНЖ цифровых кочевников в Испании',
 'footer_p1':'Статистика показывает масштаб программы Digital Nomad в Испании и динамику выдачи разрешений. Для практической подготовки к подаче смотрите <a href="../docs/digital-nomad-spain-guide.html">полный гайд по визе и ВНЖ цифрового кочевника</a> и актуальные <a href="../docs/eligibility.html">требования к заявителю и доходу</a>.',
 'footer_p2':'Полные списки документов разделены по рабочему сценарию: <a href="../docs/cuenta-ajena.html">работа в найме</a>, <a href="../docs/contract-work.html">работа по контракту</a> и <a href="../docs/family-member.html">член семьи</a>.'
}
}

for fn,cfg in articles.items():
    p=Path('blog')/fn
    s=p.read_text(encoding='utf-8')
    import re
    s=re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{cfg["desc"]}">', s, count=1)
    s=re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{cfg["desc"]}">', s, count=1)
    s=re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{cfg["desc"]}">', s, count=1)
    marker='    <meta name="twitter:card" content="summary">'
    if 'article:modified_time' not in s:
        s=s.replace(marker, f'    <meta property="article:modified_time" content="{DATE}">\n'+marker, 1)
    if 'name="twitter:title"' not in s:
        s=s.replace(marker, marker+f'\n    <meta name="twitter:title" content="{cfg["title"]}">\n    <meta name="twitter:description" content="{cfg["desc"]}">', 1)
    if '"@type": "Article"' not in s:
        schema='    <script type="application/ld+json">\n'+json.dumps({
          '@context':'https://schema.org','@type':'Article','headline':cfg['headline'],
          'description':cfg['desc'],'mainEntityOfPage':cfg['url'],
          'publisher':{'@type':'Organization','name':'Ola Española','url':'https://ola-espanola.github.io/'},
          'dateModified':DATE,'inLanguage':'ru'
        }, ensure_ascii=False, indent=2)+'\n    </script>\n'
        s=s.replace('    <!-- structured:breadcrumbs -->',schema+'    <!-- structured:breadcrumbs -->',1)
    if '.seo-footer {' not in s:
        s=s.replace('  </head>',STYLE+'  </head>',1)
    if 'class="seo-footer"' not in s:
        footer=f'''\n        <section class="seo-footer" aria-label="Дополнительная информация">\n          <h2>{cfg['footer_h']}</h2>\n          <p>{cfg['footer_p1']}</p>\n          <p>{cfg['footer_p2']}</p>\n        </section>\n'''
        pos=s.rfind('      </article>')
        if pos<0: raise RuntimeError(fn+' article close')
        s=s[:pos]+footer+s[pos:]
    p.write_text(s,encoding='utf-8')

# Blog index
p=Path('blog/index.html'); s=p.read_text(encoding='utf-8')
old_title='Блог о визе номада и переезде в Испанию | Ola Española'
new_title='Блог о визе и ВНЖ цифрового кочевника в Испании | Ola Española'
desc='Блог о визе и ВНЖ цифрового кочевника в Испании: налоги, налоговые режимы, статистика выдачи разрешений и практические материалы для номадов.'
s=s.replace(old_title,new_title)
s=s.replace('Статьи о визе номада и ВНЖ цифрового кочевника в Испании: налоги, практика и статистика.',desc)
s=s.replace('Блог о визе номада и ВНЖ цифрового кочевника в Испании','Блог о визе и ВНЖ цифрового кочевника в Испании')
s=s.replace('Практические разборы о визе номада и ВНЖ цифрового кочевника в Испании: налоги и статистика.','Практические статьи о визе и ВНЖ цифрового кочевника в Испании: налоги, работа в найме и как autónomo, статистика выдачи разрешений и другие материалы для номадов.')
s=s.replace('В блоге Ola Española публикуются практические материалы о жизни цифрового кочевника в Испании: налоги, работа как autónomo или по найму, статистика выдачи ВНЖ и изменения, которые важны после переезда.','В блоге Ola Española публикуются практические материалы о жизни цифрового кочевника в Испании: налоги, работа как autónomo или по найму, статистика выдачи ВНЖ и другие материалы для номадов.')
marker='    <meta name="twitter:card" content="summary">'
if 'name="twitter:title"' not in s:
    s=s.replace(marker,marker+f'\n    <meta name="twitter:title" content="{new_title}">\n    <meta name="twitter:description" content="{desc}">',1)
else:
    import re
    s=re.sub(r'<meta name="twitter:title" content="[^"]*">',f'<meta name="twitter:title" content="{new_title}">',s,count=1)
    s=re.sub(r'<meta name="twitter:description" content="[^"]*">',f'<meta name="twitter:description" content="{desc}">',s,count=1)
if '"@type": "CollectionPage"' not in s:
    schema='    <script type="application/ld+json">\n'+json.dumps({
      '@context':'https://schema.org','@type':'CollectionPage','name':'Блог о визе и ВНЖ цифрового кочевника в Испании',
      'description':desc,'url':'https://ola-espanola.github.io/blog/','inLanguage':'ru',
      'isPartOf':{'@type':'WebSite','name':'Ola Española','url':'https://ola-espanola.github.io/'}
    },ensure_ascii=False,indent=2)+'\n    </script>\n'
    s=s.replace('    <!-- structured:breadcrumbs -->',schema+'    <!-- structured:breadcrumbs -->',1)
if '.seo-footer {' not in s:
    s=s.replace('  </head>',STYLE+'  </head>',1)
if 'class="seo-footer"' not in s:
    footer='''\n        <section class="seo-footer" aria-label="О блоге Ola Española">\n          <h2>Блог о визе и ВНЖ цифрового кочевника в Испании</h2>\n          <p>В блоге Ola Española публикуются практические материалы о жизни цифрового кочевника в Испании: налоги, работа как autónomo или по найму, статистика выдачи ВНЖ и другие материалы для номадов.</p>\n          <p>Для подготовки документов используйте <a href="../docs/digital-nomad-spain-guide.html">полный гайд по визе и ВНЖ цифрового кочевника</a>, а также списки документов <a href="../docs/cuenta-ajena.html">для работы в найме</a>, <a href="../docs/contract-work.html">для работы по контракту</a> и <a href="../docs/family-member.html">для члена семьи</a>.</p>\n        </section>\n'''
    pos=s.rfind('      </section>')
    if pos<0: raise RuntimeError('blog index section close')
    s=s[:pos]+footer+s[pos:]
p.write_text(s,encoding='utf-8')

print('Updated blog SEO')