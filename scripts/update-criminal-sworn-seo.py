from pathlib import Path
import re


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, found {count}")
    return text.replace(old, new, 1)


# 1) Criminal record source markdown
p = Path("content/criminal-record-certificate.md")
text = p.read_text(encoding="utf-8")
repls = [
    ('title: "Справка о несудимости для ВНЖ номада в Испании"', 'title: "Справка о несудимости для Испании: апостиль, перевод и Госуслуги"'),
    ('description: "Как получить справку о несудимости в России для первичной подачи на ВНЖ цифрового кочевника в Испании: апостиль, jurado перевод и выдача по доверенности."', 'description: "Как оформить справку о несудимости для Испании: апостиль, присяжный перевод, Госуслуги, получение через представителя и требования для ВНЖ."'),
    ('# Справка о несудимости для ВНЖ цифрового кочевника в Испании', '# Справка о несудимости для Испании'),
    ('<p class="lead">Применимо для первичной подачи на ВНЖ цифрового кочевника в Испании <mark style="background-color: #dff1ff; color: inherit; white-space: nowrap;">по контракту</mark> или <mark style="background-color: #dff1ff; color: inherit; white-space: nowrap;">по найму</mark>.</p>', '<p class="lead">Справка о несудимости требуется для ряда процедур ВНЖ в Испании, в том числе для Digital Nomad Visa. Ниже — как получить российскую справку, поставить апостиль, сделать присяжный перевод и учесть требования UGE.</p>'),
]
for old, new in repls:
    text = replace_once(text, old, new, f"criminal md {old[:32]}")

marker = "## Что требует UGE\n"
quick = """## Коротко

- Для российской справки, используемой в пакете DNV, нужен бумажный оригинал с апостилем.
- Справка и апостиль переводятся на испанский у присяжного переводчика — *traductor jurado*.
- Для DNV UGE проверяет страны проживания за последние 2 года; отдельная декларация об отсутствии судимости охватывает 5 лет.
- Электронный PDF с Госуслуг без апостиля не заменяет комплект с бумажной справкой и апостилем.

"""
text = replace_once(text, marker, quick + marker, "criminal md quick block")
p.write_text(text, encoding="utf-8")


# 2) Criminal record rendered HTML
p = Path("docs/criminal-record-certificate.html")
text = p.read_text(encoding="utf-8")
repls = [
    ('<title>Справка о несудимости для ВНЖ номада в Испании</title>', '<title>Справка о несудимости для Испании: апостиль, перевод и Госуслуги</title>'),
    ('<meta name="description" content="Справка о несудимости для визы и ВНЖ цифрового кочевника в Испании: за какой период нужна, исключения UGE, апостиль, присяжный перевод и страны проживания.">', '<meta name="description" content="Как оформить справку о несудимости для Испании: апостиль, присяжный перевод, Госуслуги, получение через представителя и требования для ВНЖ.">'),
    ('<meta property="og:title" content="Справка о несудимости для ВНЖ номада в Испании">', '<meta property="og:title" content="Справка о несудимости для Испании: апостиль, перевод и Госуслуги">'),
    ('<meta property="og:description" content="Справка о несудимости для визы и ВНЖ цифрового кочевника в Испании: за какой период нужна, исключения UGE, апостиль, присяжный перевод и страны проживания.">', '<meta property="og:description" content="Как оформить справку о несудимости для Испании: апостиль, присяжный перевод, Госуслуги, получение через представителя и требования для ВНЖ.">'),
    ('<meta property="article:modified_time" content="2026-09-30">', '<meta property="article:modified_time" content="2026-10-05">'),
    ('<meta name="twitter:title" content="Справка о несудимости для ВНЖ номада в Испании">', '<meta name="twitter:title" content="Справка о несудимости для Испании: апостиль, перевод и Госуслуги">'),
    ('<meta name="twitter:description" content="Справка о несудимости для визы и ВНЖ цифрового кочевника в Испании: за какой период нужна, исключения UGE, апостиль, присяжный перевод и страны проживания.">', '<meta name="twitter:description" content="Как оформить справку о несудимости для Испании: апостиль, присяжный перевод, Госуслуги, получение через представителя и требования для ВНЖ.">'),
    ('"headline": "Справка о несудимости для ВНЖ цифрового кочевника в Испании"', '"headline": "Справка о несудимости для Испании: апостиль, перевод и Госуслуги"'),
    ('"description": "Справка о несудимости для визы и ВНЖ цифрового кочевника в Испании: за какой период нужна, исключения UGE, апостиль, присяжный перевод и страны проживания."', '"description": "Как оформить справку о несудимости для Испании: апостиль, присяжный перевод, Госуслуги, получение через представителя и требования для ВНЖ."'),
    ('"dateModified": "2026-09-30"', '"dateModified": "2026-10-05"'),
    ('<h1>Справка о несудимости для ВНЖ цифрового кочевника в Испании</h1>', '<h1>Справка о несудимости для Испании</h1>'),
    ('<p class="lead">Применимо для первичной подачи на ВНЖ цифрового кочевника в Испании <mark style="background-color: #dff1ff; color: inherit; white-space: nowrap;">по контракту</mark> или <mark style="background-color: #dff1ff; color: inherit; white-space: nowrap;">по найму</mark>.</p>', '<p class="lead">Справка о несудимости требуется для ряда процедур ВНЖ в Испании, в том числе для Digital Nomad Visa. Ниже — как получить российскую справку, поставить апостиль, сделать присяжный перевод и учесть требования UGE.</p>'),
]
for old, new in repls:
    text = replace_once(text, old, new, f"criminal html {old[:36]}")

html_marker = "        <h2>Справка и декларация о несудимости</h2>\n"
quick_html = """        <section>
          <h2>Коротко</h2>
          <ul class="check-list">
            <li>Для российской справки, используемой в пакете DNV, нужен бумажный оригинал с апостилем.</li>
            <li>Справка и апостиль переводятся на испанский у присяжного переводчика — <em>traductor jurado</em>.</li>
            <li>Для DNV UGE проверяет страны проживания за последние 2 года; отдельная декларация об отсутствии судимости охватывает 5 лет.</li>
            <li>Электронный PDF с Госуслуг без апостиля не заменяет комплект с бумажной справкой и апостилем.</li>
          </ul>
        </section>

"""
text = replace_once(text, html_marker, quick_html + html_marker, "criminal html quick block")
p.write_text(text, encoding="utf-8")


# 3) Sworn translation rendered HTML
p = Path("docs/sworn-translation.html")
text = p.read_text(encoding="utf-8")
repls = [
    ('<title>Хурадо-перевод с русского на испанский | Traductor jurado</title>', '<title>Присяжный переводчик в Испании: перевод с русского | Traductor jurado</title>'),
    ('<meta name="description" content="Присяжный перевод (traducción jurada) с русского на испанский для визы и ВНЖ в Испании: где найти traductor jurado, как запросить перевод и проверить оформление.">', '<meta name="description" content="Как найти присяжного переводчика с русского на испанский в Испании: официальный реестр MAEUEC, электронная подпись, формат, сроки и требования к traducción jurada.">'),
    ('<meta property="og:type" content="website">', '<meta property="og:type" content="article">'),
    ('<meta property="og:title" content="Хурадо-перевод с русского на испанский | Traductor jurado">', '<meta property="og:title" content="Присяжный переводчик в Испании: перевод с русского | Traductor jurado">'),
    ('<meta property="og:description" content="Присяжный перевод (traducción jurada) с русского на испанский для визы и ВНЖ в Испании: где найти traductor jurado, как запросить перевод и проверить оформление.">', '<meta property="og:description" content="Как найти присяжного переводчика с русского на испанский в Испании: официальный реестр MAEUEC, электронная подпись, формат, сроки и требования к traducción jurada.">'),
    ('<meta property="article:modified_time" content="2026-09-30">', '<meta property="article:modified_time" content="2026-10-05">'),
    ('<meta name="twitter:title" content="Хурадо-перевод с русского на испанский | Traductor jurado">', '<meta name="twitter:title" content="Присяжный переводчик в Испании: перевод с русского | Traductor jurado">'),
    ('<meta name="twitter:description" content="Присяжный перевод (traducción jurada) с русского на испанский для визы и ВНЖ в Испании: где найти traductor jurado, как запросить перевод и проверить оформление.">', '<meta name="twitter:description" content="Как найти присяжного переводчика с русского на испанский в Испании: официальный реестр MAEUEC, электронная подпись, формат, сроки и требования к traducción jurada.">'),
    ('"headline": "Хурадо-перевод с русского на испанский"', '"headline": "Присяжный перевод в Испании с русского на испанский"'),
    ('"description": "Присяжный перевод (traducción jurada) с русского на испанский для визы и ВНЖ в Испании: где найти traductor jurado, как запросить перевод и проверить оформление."', '"description": "Как найти присяжного переводчика с русского на испанский в Испании: официальный реестр MAEUEC, электронная подпись, формат, сроки и требования к traducción jurada."'),
    ('"dateModified": "2026-09-30"', '"dateModified": "2026-10-05"'),
    ('<h1>Хурадо-перевод с русского на испанский</h1>', '<h1>Присяжный перевод в Испании — traductor jurado</h1>'),
    ('<p class="lead">Traducción jurada — официальный перевод, выполненный присяжным переводчиком, назначенным Министерством иностранных дел Испании (MAEUEC). Такой перевод имеет официальный характер и принимается испанскими административными органами.</p>', '<p class="lead">Traducción jurada — официальный присяжный перевод, выполненный переводчиком, назначенным Министерством иностранных дел Испании (MAEUEC). Такой перевод используется для иностранных документов при подаче на ВНЖ и в других административных процедурах в Испании.</p>'),
    ('<h2>Где искать переводчика</h2>', '<h2>Как найти присяжного переводчика</h2>'),
    ('<h2>Как сократить время на хурадо-перевод</h2>', '<h2>Как сократить время на присяжный перевод</h2>'),
    ('<p>Чтобы сократить время на хурадо-перевод, можно не ждать, пока будет готов весь пакет документов.', '<p>Чтобы сократить время на присяжный перевод, можно не ждать, пока будет готов весь пакет документов.'),
]
for old, new in repls:
    text = replace_once(text, old, new, f"sworn html {old[:36]}")

sworn_marker = "        <section>\n          <h2>Как найти присяжного переводчика</h2>\n"
useful = """        <section>
          <h2>Что проверить перед заказом перевода</h2>
          <div class="table-wrap">
            <table>
              <thead><tr><th>Что проверить</th><th>Что важно</th></tr></thead>
              <tbody>
                <tr><td>Язык</td><td>Для российских документов нужен перевод с русского на испанский.</td></tr>
                <tr><td>Статус переводчика</td><td>Переводчик должен быть в официальном реестре MAEUEC как <em>traductor-intérprete jurado</em> для русского языка.</td></tr>
                <tr><td>Формат</td><td>Уточните заранее, нужен бумажный экземпляр или подойдет электронный PDF.</td></tr>
                <tr><td>Электронная подпись</td><td>Для электронной подачи лучше заранее запросить версию с электронной подписью переводчика.</td></tr>
                <tr><td>Полный документ</td><td>Если есть апостиль, переводчику нужно отправлять документ вместе с апостилем — переводятся оба.</td></tr>
                <tr><td>Цена и срок</td><td>Запросите стоимость и срок у нескольких переводчиков до отправки оригиналов.</td></tr>
              </tbody>
            </table>
          </div>
        </section>

"""
text = replace_once(text, sworn_marker, useful + sworn_marker, "sworn visible table")
p.write_text(text, encoding="utf-8")


# 4) Shared sidebar label
p = Path("partials/sidebar.html")
text = p.read_text(encoding="utf-8")
text = replace_once(text, '<a href="/docs/sworn-translation.html">Хурадо-перевод</a>', '<a href="/docs/sworn-translation.html">Присяжный перевод</a>', "sidebar sworn label")
p.write_text(text, encoding="utf-8")


# 5) Sitemap lastmod values
p = Path("sitemap.xml")
text = p.read_text(encoding="utf-8")
for url in [
    "https://ola-espanola.github.io/docs/criminal-record-certificate.html",
    "https://ola-espanola.github.io/docs/sworn-translation.html",
]:
    pattern = rf'(<loc>{re.escape(url)}</loc>\s*<lastmod>)([^<]+)(</lastmod>)'
    text, n = re.subn(pattern, rf'\g<1>2026-10-05\g<3>', text, count=1)
    if n != 1:
        raise SystemExit(f"sitemap: URL not found {url}")
p.write_text(text, encoding="utf-8")
