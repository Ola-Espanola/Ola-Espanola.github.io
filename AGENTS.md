# Ola Espanola

## Workspace

- Actual Git checkout: `C:\ola-espanola`.
- The site deploys from `main` through GitHub Pages: `https://ola-espanola.github.io/`.
- The task workspace may contain a mirrored ChatGPT project and a staging copy. Treat `sources/` in that mirror as read-only. Make changes in the repository or staging copy, then commit and push only the intended files.

## Site structure

- Public pages are static HTML: `index.html`, `docs/*.html`, and `blog/*.html`.
- Each public guide and blog page has a Markdown source in `content/`. When changing page content, update the matching HTML and Markdown files together.
- Images and CSS are in `assets/`.
- `Doc/` contains working materials. Keep it in Git, but never link to it from public pages or expose it in navigation.
- Do not delete, move, or replace source images and working materials unless the user explicitly asks.

## Publishing

- Before a substantive content change, show the proposed wording to the user and wait for approval. A direct request to make the stated change counts as approval.
- Do not publish a new blog post before the user explicitly approves its final text and image.
- Before publishing, check the diff and HTML structure. After pushing, confirm that GitHub Pages serves the new page.
- Preserve unrelated changes in a dirty working tree.

## Writing style

- Audience: primarily Russian applicants for Spain's digital nomad residence permit.
- Write clearly, briefly, and practically. Avoid bureaucratic, promotional, and newspaper-like language.
- Explain Spanish terms only when they help; do not overload a reader with terminology.
- Use Russian descriptions for source links. Prefer official sources for legal or procedural claims.
- Brand: `Ola Española`. Telegram: `https://t.me/ola_espana`.
- In every main guide or blog article, place the Telegram contact block immediately after the heading. Do not repeat it at the bottom. Do not add it to link pages or other reference-only pages.

## Document guides

- Keep the document table and the example package in the same order as the corresponding submission-form screenshot.
- For the current contract-work guide: contracts, public company documents, qualifications/official experience, criminal record, and social-security certificates use `jurado перевод`; bank statements, invoices, and client letters use `Простой перевод`; forms prepared for the application use `Нет (заполняется на испанском)` or `Нет (сразу на испанском)`.
- For the employee guide, keep the same format and form order. `Nóminas` use `Простой перевод`; medical insurance is `Нет (оформляется в Испании)`; the social-security coverage certificate is `Апостиль + jurado перевод`.
- Do not add generic caveats that conflict with the actual form or existing guidance. Verify uncertain document requirements against the official UGE instruction before changing them.
