from pathlib import Path


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, found {count}")
    return text.replace(old, new, 1)


# Markdown source
p = Path("content/nalogi-cifrovogo-kochevnika-ispania.md")
text = p.read_text(encoding="utf-8")

md_replacements = [
    (
        "![График налоговой нагрузки autónomo без стартовых льгот](../assets/images/blog/2_autonomo_graph.png)",
        "![График налоговой нагрузки autónomo без стартовых льгот](../assets/images/blog/2_autonomo_graph.png)\n\n_Налоговая нагрузка обычного autónomo в Испании в 2026 году: IRPF и взносы Seguridad Social при разном месячном доходе. Расчёт для одного заявителя без детей в Comunitat Valenciana._",
        "markdown regular autonomo caption",
    ),
    (
        "![График налоговой нагрузки autónomo со стартовыми льготами](../assets/images/blog/4_autonomo_graph_benefit.png)",
        "![График налоговой нагрузки autónomo со стартовыми льготами](../assets/images/blog/4_autonomo_graph_benefit.png)\n\n_Налоговая нагрузка нового autónomo в Испании в 2026 году со стартовыми льготами: сниженная cuota и reducción 20% при выполнении условий. Расчёт для одного заявителя без детей в Comunitat Valenciana._",
        "markdown benefit autonomo caption",
    ),
    (
        "![График налоговой нагрузки при работе по найму](../assets/images/blog/6_ajena_graph.png)",
        "![График налоговой нагрузки при работе по найму](../assets/images/blog/6_ajena_graph.png)\n\n_Налоговая нагрузка при работе по найму в Испании в 2026 году: IRPF при отсутствии отдельного испанского социального взноса. Расчёт для одного заявителя без детей в Comunitat Valenciana._",
        "markdown employee caption",
    ),
]

for old, new, label in md_replacements:
    text = replace_once(text, old, new, label)

p.write_text(text, encoding="utf-8")


# Rendered HTML
p = Path("blog/nalogi-cifrovogo-kochevnika-ispania.html")
text = p.read_text(encoding="utf-8")

html_replacements = [
    (
        '''          <figure class="article-hero">\n            <img src="../assets/images/blog/2_autonomo_graph.png" alt="График налоговой нагрузки autónomo без стартовых льгот">\n          </figure>''',
        '''          <figure class="article-hero">\n            <img src="../assets/images/blog/2_autonomo_graph.png" alt="График налоговой нагрузки autónomo без стартовых льгот">\n            <figcaption>Налоговая нагрузка обычного autónomo в Испании в 2026 году: IRPF и взносы Seguridad Social при разном месячном доходе. Расчёт для одного заявителя без детей в Comunitat Valenciana.</figcaption>\n          </figure>''',
        "html regular autonomo caption",
    ),
    (
        '''          <figure class="article-hero">\n            <img src="../assets/images/blog/4_autonomo_graph_benefit.png" alt="График налоговой нагрузки autónomo со стартовыми льготами">\n          </figure>''',
        '''          <figure class="article-hero">\n            <img src="../assets/images/blog/4_autonomo_graph_benefit.png" alt="График налоговой нагрузки autónomo со стартовыми льготами">\n            <figcaption>Налоговая нагрузка нового autónomo в Испании в 2026 году со стартовыми льготами: сниженная cuota и reducción 20% при выполнении условий. Расчёт для одного заявителя без детей в Comunitat Valenciana.</figcaption>\n          </figure>''',
        "html benefit autonomo caption",
    ),
    (
        '''          <figure class="article-hero">\n            <img src="../assets/images/blog/6_ajena_graph.png" alt="График налоговой нагрузки при работе по найму">\n          </figure>''',
        '''          <figure class="article-hero">\n            <img src="../assets/images/blog/6_ajena_graph.png" alt="График налоговой нагрузки при работе по найму">\n            <figcaption>Налоговая нагрузка при работе по найму в Испании в 2026 году: IRPF при отсутствии отдельного испанского социального взноса. Расчёт для одного заявителя без детей в Comunitat Valenciana.</figcaption>\n          </figure>''',
        "html employee caption",
    ),
]

for old, new, label in html_replacements:
    text = replace_once(text, old, new, label)

style_anchor = "      .seo-footer { margin-top: 54px; padding-top: 24px; border-top: 1px solid var(--line); color: var(--muted); font-size: 14px; line-height: 1.65; }"
style_new = "      .article-hero figcaption { margin-top: 10px; color: var(--muted); font-size: 14px; line-height: 1.55; text-align: left; }\n" + style_anchor
text = replace_once(text, style_anchor, style_new, "figcaption style")

p.write_text(text, encoding="utf-8")
