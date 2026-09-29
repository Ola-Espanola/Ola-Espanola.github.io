# Cloudflare Pages draft

Отдельная заготовка для будущего Cloudflare Pages-проекта.

Сейчас она намеренно не предназначена для индексации:
- исходники лежат внутри `/Doc/`, который закрыт текущим корневым `robots.txt` основного GitHub Pages-сайта;
- `index.html` содержит `noindex,nofollow`;
- локальный `robots.txt` запрещает обход всего будущего Cloudflare-сайта.

Перед публичным запуском на Cloudflare:
1. заменить `noindex,nofollow` на `index,follow`;
2. заменить `Disallow: /` в `robots.txt` на `Allow: /`;
3. после получения окончательного `*.pages.dev` адреса добавить абсолютную строку `Sitemap:` в `robots.txt`;
4. при необходимости синхронизировать `sitemap.xml` с актуальным sitemap основного сайта.

`Doc/cloudflare-site/sitemap.xml` уже содержит URL основного сайта `https://ola-espanola.github.io/` и предназначен для теста cross-site sitemap.
