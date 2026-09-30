# Cloudflare Pages landing

Отдельная индексируемая посадочная страница Ola Española на Cloudflare Pages.

Текущий адрес:
- `https://ola-espanola.pages.dev/`

Назначение:
- дополнительная точка входа из поиска;
- ссылки на основной сайт `https://ola-espanola.github.io/` и ключевые материалы;
- отдельная верификация и индексация Cloudflare Pages-домена.

SEO-настройки:
- `index.html` открыт для индексации и имеет self-canonical на `https://ola-espanola.pages.dev/`;
- `robots.txt` разрешает обход и указывает `self-sitemap.xml`;
- `self-sitemap.xml` содержит индексируемую Cloudflare-страницу;
- `sitemap.xml` — синхронизированная копия sitemap основного сайта с URL `ola-espanola.github.io`;
- файл ключа IndexNow размещается в корне Cloudflare Pages для отдельной отправки `pages.dev` URL.

Основной сайт и Cloudflare-страница не должны быть буквальными дублями: Cloudflare остаётся короткой посадочной страницей, которая ведёт на подробные материалы основного сайта.
