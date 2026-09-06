from __future__ import annotations

import argparse
import csv
import html
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


MESSAGE_START_RE = re.compile(
    r'<div class="message (?P<class>[^"]+)" id="(?P<id>[^"]+)">',
    re.IGNORECASE,
)
DATE_RE = re.compile(
    r'<div class="pull_right date details" title="(?P<dt>\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}) UTC(?P<tz>[+-]\d{2}:\d{2})">',
    re.IGNORECASE,
)
FROM_RE = re.compile(r'<div class="from_name">\s*(?P<value>.*?)\s*</div>', re.IGNORECASE | re.DOTALL)
TEXT_RE = re.compile(r'<div class="text">\s*(?P<value>.*?)\s*</div>', re.IGNORECASE | re.DOTALL)
HEADER_RE = re.compile(
    r'<div class="page_header">.*?<div class="text bold">\s*(?P<value>.*?)\s*</div>',
    re.IGNORECASE | re.DOTALL,
)
REPLY_RE = re.compile(
    r'<div class="reply_to details">\s*In reply to <a\s+[^>]*href="(?P<href>[^"]+)"',
    re.IGNORECASE | re.DOTALL,
)
LINK_RE = re.compile(r'<a\s+[^>]*href="(?P<href>[^"]+)"', re.IGNORECASE)


TOPICS = {
    "prodlenie": [
        "продлен",
        "продле",
        "renovar",
        "renovacion",
        "пролонг",
        "residencia",
    ],
    "dnv_general": [
        "digital nomad",
        "цифров",
        "номад",
        "dnv",
        "виза кочев",
        "кочевник",
    ],
    "uge_status": [
        "uge",
        "silencio",
        "silencio administrativo",
        "requerimiento",
        "resolucion",
        "aprobado",
        "odisea",
        "mercurio",
    ],
    "tie_nie_huella": [
        "tie",
        "nie",
        "tarjeta",
        "huella",
        "отпечат",
        "полици",
        "policia",
        "lote",
        "cita",
        "запись",
        "tasa",
        "790",
    ],
    "documents": [
        "справк",
        "апостил",
        "перевод",
        "присяж",
        "certificado",
        "сертификат",
        "документ",
        "легализ",
    ],
    "income_work": [
        "доход",
        "зарплат",
        "контракт",
        "договор",
        "работодатель",
        "клиент",
        "autonomo",
        "autonom",
        "фриланс",
        "ип",
    ],
    "taxes": [
        "налог",
        "hacienda",
        "irpf",
        "beckham",
        "modelo",
        "деклара",
        "резидент",
        "tax",
    ],
    "bank_insurance": [
        "банк",
        "счет",
        "счёт",
        "выписк",
        "страхов",
        "seguro",
        "sanitas",
        "adeslas",
        "asisa",
    ],
    "family": [
        "семья",
        "супруг",
        "супруга",
        "дети",
        "ребен",
        "ребён",
        "pareja",
        "matrimonio",
    ],
    "consulate_entry": [
        "консульств",
        "виза",
        "въезд",
        "шенген",
        "испания въех",
        "visado",
        "consulado",
    ],
    "digital_tools": [
        "certificado digital",
        "clave",
        "cl@ve",
        "firma",
        "autofirma",
        "электрон",
    ],
}

NOISE_EXACT = {
    "",
    "+",
    "++",
    "-",
    ".",
    "..",
    "...",
    "ок",
    "окей",
    "okay",
    "ok",
    "да",
    "нет",
    "неа",
    "ага",
    "угу",
    "спасибо",
    "спс",
    "спасибо!",
    "спасибо.",
    "благодарю",
    "понял",
    "поняла",
    "ясно",
    "понятно",
    "добрый день",
    "здравствуйте",
    "привет",
    "👍",
    "🙏",
}

NOISE_PATTERNS = [
    re.compile(r"^[\W_]{1,8}$", re.UNICODE),
    re.compile(r"^(ха)+$", re.IGNORECASE),
    re.compile(r"^спасибо[!. )]*$", re.IGNORECASE),
    re.compile(r"^большое спасибо[!. )]*$", re.IGNORECASE),
]

QUESTION_RE = re.compile(
    r"(\?|подскажите|скажите|кто знает|можно ли|нужно ли|как\b|где\b|куда\b|сколько\b|какой\b|какая\b|какие\b|что делать|есть ли)",
    re.IGNORECASE,
)
OFF_TOPIC_RE = re.compile(
    r"(немного не по теме|не по теме|оффтоп|offtopic|офтоп|аренд[ауы]|купальный сезон|пригород|барсы|море|пляж)",
    re.IGNORECASE,
)


@dataclass
class ParsedMessage:
    chat_folder: str
    chat_title: str
    file: str
    message_id: str
    classes: str
    dt: str | None
    timestamp: str | None
    author: str | None
    text: str
    links: list[str]
    media: list[str]
    reply_to: str | None
    is_service: bool
    is_joined: bool
    topics: list[str]
    is_question: bool
    usefulness_score: int
    skip_reason: str | None


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "br":
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def get_text(self) -> str:
        value = "".join(self.parts)
        value = html.unescape(value)
        value = value.replace("\xa0", " ")
        value = re.sub(r"[ \t\r\f\v]+", " ", value)
        value = re.sub(r"\n\s+", "\n", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        return value.strip()


def html_to_text(fragment: str) -> str:
    parser = TextExtractor()
    parser.feed(fragment)
    return parser.get_text()


def strip_html(fragment: str) -> str:
    return html_to_text(fragment)


def message_file_sort_key(path: Path) -> int:
    if path.name == "messages.html":
        return 1
    match = re.fullmatch(r"messages(\d+)\.html", path.name)
    if match:
        return int(match.group(1))
    return 999999


def iter_message_blocks(source: str) -> Iterable[tuple[re.Match[str], str]]:
    matches = list(MESSAGE_START_RE.finditer(source))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        yield match, source[match.start() : end]


def parse_dt(block: str) -> tuple[str | None, str | None]:
    match = DATE_RE.search(block)
    if not match:
        return None, None
    raw = f"{match.group('dt')} UTC{match.group('tz')}"
    dt = datetime.strptime(match.group("dt"), "%d.%m.%Y %H:%M:%S")
    return raw, dt.strftime("%Y-%m-%dT%H:%M:%S")


def detect_topics(text: str, chat_title: str) -> list[str]:
    haystack = text.lower()
    topics = []
    for topic, terms in TOPICS.items():
        if any(term.lower() in haystack for term in terms):
            topics.append(topic)
    return topics


def normalize_id(message_id: str) -> str:
    return message_id.removeprefix("message")


def parse_reply(block: str) -> str | None:
    match = REPLY_RE.search(block)
    if not match:
        return None
    href = html.unescape(match.group("href"))
    target = href.split("#")[-1]
    target = target.removeprefix("go_to_")
    return target if target else href


def extract_links(block: str) -> tuple[list[str], list[str]]:
    links: list[str] = []
    media: list[str] = []
    for match in LINK_RE.finditer(block):
        href = html.unescape(match.group("href"))
        if href.startswith(("photos/", "files/", "video_files/", "voice_messages/")):
            media.append(href)
        elif href.startswith("#") or "#go_to_message" in href:
            continue
        else:
            links.append(href)
    return sorted(set(links)), sorted(set(media))


def score_message(text: str, links: list[str], media: list[str], reply_to: str | None, topics: list[str], is_question: bool) -> int:
    score = 0
    length = len(text)
    if length >= 20:
        score += 1
    if length >= 80:
        score += 1
    if length >= 250:
        score += 1
    if links:
        score += 1
    if media and text:
        score += 1
    if reply_to:
        score += 1
    if topics:
        score += min(3, len(topics))
    if is_question:
        score += 2
    return score


def skip_reason(text: str, links: list[str], media: list[str], is_service: bool, score: int) -> str | None:
    compact = text.strip().lower()
    compact = re.sub(r"\s+", " ", compact)
    if is_service:
        return "service"
    if not text and not links and not media:
        return "empty"
    if compact in NOISE_EXACT and not links and not media:
        return "short_ack"
    if any(pattern.match(compact) for pattern in NOISE_PATTERNS) and not links and not media:
        return "punctuation_or_reaction"
    if len(compact) < 12 and not links and not media:
        return "too_short"
    if len(compact) < 30 and score < 2 and not links and not media:
        return "low_information"
    if score == 0:
        return "low_information"
    return None


def parse_chat(chat_dir: Path) -> tuple[list[ParsedMessage], Counter]:
    html_files = sorted(chat_dir.glob("messages*.html"), key=message_file_sort_key)
    chat_title = chat_dir.name
    messages: list[ParsedMessage] = []
    stats: Counter = Counter()
    last_author: str | None = None

    for html_file in html_files:
        source = html_file.read_text(encoding="utf-8", errors="replace")
        header_match = HEADER_RE.search(source)
        if header_match:
            chat_title = strip_html(header_match.group("value")) or chat_title

        for start, block in iter_message_blocks(source):
            classes = start.group("class")
            message_id = start.group("id")
            is_service = "service" in classes.split()
            is_joined = "joined" in classes.split()
            raw_dt, timestamp = parse_dt(block)
            from_match = FROM_RE.search(block)
            author = strip_html(from_match.group("value")) if from_match else None
            if author:
                last_author = author
            elif is_joined:
                author = last_author

            text_match = TEXT_RE.search(block)
            text = html_to_text(text_match.group("value")) if text_match else ""
            links, media = extract_links(block)
            reply_to = parse_reply(block)
            topics = detect_topics(text, chat_title)
            is_question = bool(QUESTION_RE.search(text))
            score = score_message(text, links, media, reply_to, topics, is_question)
            reason = skip_reason(text, links, media, is_service, score)

            stats["raw_messages"] += 1
            if reason:
                stats[f"skipped_{reason}"] += 1
            else:
                stats["kept_messages"] += 1
            if is_service:
                stats["service_messages"] += 1
            if is_joined:
                stats["joined_messages"] += 1
            if reply_to:
                stats["reply_messages"] += 1
            if media:
                stats["messages_with_media"] += 1
            if links:
                stats["messages_with_links"] += 1
            if is_question:
                stats["question_like_messages"] += 1

            messages.append(
                ParsedMessage(
                    chat_folder=chat_dir.name,
                    chat_title=chat_title,
                    file=html_file.name,
                    message_id=message_id,
                    classes=classes,
                    dt=raw_dt,
                    timestamp=timestamp,
                    author=author,
                    text=text,
                    links=links,
                    media=media,
                    reply_to=reply_to,
                    is_service=is_service,
                    is_joined=is_joined,
                    topics=topics,
                    is_question=is_question,
                    usefulness_score=score,
                    skip_reason=reason,
                )
            )
    return messages, stats


def as_dict(message: ParsedMessage) -> dict:
    return {
        "chat_folder": message.chat_folder,
        "chat_title": message.chat_title,
        "file": message.file,
        "message_id": message.message_id,
        "message_num": normalize_id(message.message_id),
        "timestamp": message.timestamp,
        "telegram_datetime": message.dt,
        "author": message.author,
        "text": message.text,
        "links": message.links,
        "media": message.media,
        "reply_to": message.reply_to,
        "topics": message.topics,
        "is_question": message.is_question,
        "usefulness_score": message.usefulness_score,
        "source_path": str(Path(message.chat_folder) / message.file),
    }


def write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build_reply_pairs(kept: list[ParsedMessage]) -> list[dict]:
    by_id: dict[str, dict[str, ParsedMessage]] = defaultdict(dict)
    by_num: dict[str, dict[str, ParsedMessage]] = defaultdict(dict)
    for message in kept:
        by_id[message.chat_folder][message.message_id] = message
        by_num[message.chat_folder][normalize_id(message.message_id)] = message

    pairs: list[dict] = []

    for message in kept:
        if not message.reply_to:
            continue
        parent = by_id[message.chat_folder].get(message.reply_to) or by_num[message.chat_folder].get(normalize_id(message.reply_to))
        if not parent:
            continue
        if not parent.text or not message.text:
            continue

        question_first = parent.is_question or "?" in parent.text
        if not question_first:
            continue
        answer_score = message.usefulness_score + len(message.text) // 120
        if answer_score < 3:
            continue
        pairs.append(
            {
                "chat_title": message.chat_title,
                "chat_folder": message.chat_folder,
                "question_message_id": parent.message_id,
                "answer_message_id": message.message_id,
                "question_timestamp": parent.timestamp,
                "answer_timestamp": message.timestamp,
                "question_author": parent.author,
                "answer_author": message.author,
                "topics": sorted(set(parent.topics + message.topics)),
                "question": parent.text,
                "answer": message.text,
                "answer_links": message.links,
                "answer_media": message.media,
                "source_question": str(Path(parent.chat_folder) / parent.file),
                "source_answer": str(Path(message.chat_folder) / message.file),
            }
        )
    pairs.sort(key=lambda row: (row.get("answer_timestamp") or "", row.get("chat_title") or ""), reverse=True)
    return pairs


def qa_quality_score(row: dict) -> int:
    question = row["question"]
    answer = row["answer"]
    topics = row["topics"]
    score = 0
    if len(question) >= 30:
        score += 1
    if len(answer) >= 60:
        score += 2
    if len(answer) >= 180:
        score += 1
    if topics:
        score += min(3, len(topics))
    if row["answer_links"]:
        score += 1
    if row["answer_media"]:
        score += 1
    if row["chat_folder"] == "Закрытый_чат_Продление_2026-09-06":
        score += 2
    if "prodlenie" in topics:
        score += 2
    if "uge_status" in topics:
        score += 1
    if row["answer_timestamp"] and row["answer_timestamp"] >= "2026-01-01":
        score += 2
    elif row["answer_timestamp"] and row["answer_timestamp"] >= "2025-01-01":
        score += 1
    return score


def is_best_qa(row: dict) -> bool:
    question = row["question"].strip()
    answer = row["answer"].strip()
    if not row["topics"]:
        return False
    if OFF_TOPIC_RE.search(question) or OFF_TOPIC_RE.search(answer):
        return False
    if len(question) < 20 or len(answer) < 45:
        return False
    if answer.lower() in NOISE_EXACT:
        return False
    if answer.count("?") and len(answer) < 120:
        return False
    return qa_quality_score(row) >= 6


def build_knowledge_messages(kept: list[ParsedMessage]) -> list[dict]:
    messages = []
    for message in kept:
        if not message.topics:
            continue
        if OFF_TOPIC_RE.search(message.text):
            continue
        if message.usefulness_score < 3:
            continue
        if len(message.text) < 40 and not message.links and not message.media:
            continue
        row = as_dict(message)
        if message.chat_folder == "Закрытый_чат_Продление_2026-09-06":
            row["source_priority"] = 3
        elif "prodlenie" in message.topics or "uge_status" in message.topics:
            row["source_priority"] = 2
        else:
            row["source_priority"] = 1
        messages.append(row)
    messages.sort(
        key=lambda row: (
            row["source_priority"],
            row["timestamp"] or "",
            row["usefulness_score"],
        ),
        reverse=True,
    )
    return messages


def write_topic_files(output_dir: Path, kept: list[ParsedMessage]) -> dict[str, int]:
    topic_dir = output_dir / "topics"
    topic_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for topic in sorted(TOPICS):
        topic_messages = [
            message
            for message in kept
            if topic in message.topics and message.timestamp and message.usefulness_score >= 3
        ]
        topic_messages.sort(key=lambda message: message.timestamp or "", reverse=True)
        topic_messages = topic_messages[:300]
        counts[topic] = len(topic_messages)
        lines = [
            f"# {topic}",
            "",
            "Most recent useful messages first. Source paths are relative to C:\\Projects\\Nomad.",
            "",
        ]
        for message in topic_messages:
            body = message.text.replace("\n", "\n  ")
            lines.extend(
                [
                    f"## {message.timestamp} | {message.chat_title} | {message.author or 'unknown'}",
                    "",
                    f"Source: {message.chat_folder}/{message.file}#{message.message_id}",
                    "",
                    body,
                    "",
                ]
            )
            if message.links:
                lines.append(f"Links: {', '.join(message.links)}")
                lines.append("")
        (topic_dir / f"{topic}.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return counts


def write_readme(
    output_dir: Path,
    root: Path,
    chat_stats: dict[str, Counter],
    kept: list[ParsedMessage],
    knowledge_rows: list[dict],
    pairs: list[dict],
    best_pairs: list[dict],
    topic_counts: dict[str, int],
) -> None:
    total_raw = sum(stats["raw_messages"] for stats in chat_stats.values())
    total_kept = sum(stats["kept_messages"] for stats in chat_stats.values())
    skipped = total_raw - total_kept
    latest = max((message.timestamp for message in kept if message.timestamp), default="")
    earliest = min((message.timestamp for message in kept if message.timestamp), default="")
    topic_summary = Counter(topic for message in kept for topic in message.topics)

    lines = [
        "# Nomad Telegram Export - Processed",
        "",
        f"Source folder: `{root}`",
        f"Generated from current local exports without modifying the originals.",
        "",
        "## Output files",
        "",
        "- `clean_messages.jsonl`: useful normalized messages, one JSON object per line.",
        "- `clean_messages.csv`: compact spreadsheet-friendly view of useful messages.",
        "- `knowledge_messages.jsonl`: stricter high-signal subset for future answers.",
        "- `knowledge_messages.csv`: spreadsheet-friendly view of the high-signal subset.",
        "- `qa_candidates.jsonl`: broad likely question-answer pairs reconstructed from Telegram replies.",
        "- `qa_best.jsonl`: stricter Q/A candidates suitable for first-pass retrieval.",
        "- `topic_summary.csv`: topic counters by chat.",
        "- `topics/*.md`: recent useful messages per topic, newest first.",
        "- `processing_report.json`: detailed counts and skip reasons.",
        "",
        "## Totals",
        "",
        f"- Raw message blocks: {total_raw}",
        f"- Kept useful messages: {total_kept}",
        f"- High-signal knowledge messages: {len(knowledge_rows)}",
        f"- Skipped low-value/service blocks: {skipped}",
        f"- Broad likely Q/A pairs: {len(pairs)}",
        f"- Best Q/A candidates: {len(best_pairs)}",
        f"- Kept date range: {earliest} to {latest}",
        "",
        "## Main topics in kept messages",
        "",
    ]
    for topic, count in topic_summary.most_common():
        lines.append(f"- {topic}: {count}")
    lines.extend(["", "## Per-chat processing"])
    for chat, stats in sorted(chat_stats.items()):
        lines.extend(
            [
                "",
                f"### {chat}",
                "",
                f"- Raw: {stats['raw_messages']}",
                f"- Kept: {stats['kept_messages']}",
                f"- Service: {stats['service_messages']}",
                f"- Joined messages: {stats['joined_messages']}",
                f"- Reply messages: {stats['reply_messages']}",
                f"- Question-like messages: {stats['question_like_messages']}",
            ]
        )
    lines.extend(["", "## Topic files"])
    for topic, count in sorted(topic_counts.items()):
        lines.append(f"- `topics/{topic}.md`: {count}")
    (output_dir / "README.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=r"C:\Projects\Nomad")
    parser.add_argument("--output", default="processed_nomad")
    args = parser.parse_args()

    root = Path(args.source)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_messages: list[ParsedMessage] = []
    chat_stats: dict[str, Counter] = {}
    for chat_dir in sorted([path for path in root.iterdir() if path.is_dir()]):
        messages, stats = parse_chat(chat_dir)
        all_messages.extend(messages)
        chat_stats[chat_dir.name] = stats

    kept = [message for message in all_messages if message.skip_reason is None]
    kept.sort(key=lambda message: (message.timestamp or "", message.chat_title, message.message_id), reverse=True)
    kept_rows = [as_dict(message) for message in kept]

    write_jsonl(output_dir / "clean_messages.jsonl", kept_rows)
    csv_rows = [
        {
            "timestamp": row["timestamp"],
            "chat_title": row["chat_title"],
            "author": row["author"],
            "topics": ";".join(row["topics"]),
            "is_question": row["is_question"],
            "usefulness_score": row["usefulness_score"],
            "text": row["text"],
            "links": ";".join(row["links"]),
            "media": ";".join(row["media"]),
            "source": f"{row['chat_folder']}/{row['file']}#{row['message_id']}",
        }
        for row in kept_rows
    ]
    write_csv(
        output_dir / "clean_messages.csv",
        csv_rows,
        ["timestamp", "chat_title", "author", "topics", "is_question", "usefulness_score", "text", "links", "media", "source"],
    )

    pairs = build_reply_pairs(kept)
    write_jsonl(output_dir / "qa_candidates.jsonl", pairs)
    best_pairs = []
    for pair in pairs:
        if is_best_qa(pair):
            pair = dict(pair)
            pair["qa_quality_score"] = qa_quality_score(pair)
            best_pairs.append(pair)
    best_pairs.sort(
        key=lambda row: (
            row["qa_quality_score"],
            row.get("answer_timestamp") or "",
        ),
        reverse=True,
    )
    write_jsonl(output_dir / "qa_best.jsonl", best_pairs)

    knowledge_rows = build_knowledge_messages(kept)
    write_jsonl(output_dir / "knowledge_messages.jsonl", knowledge_rows)
    write_csv(
        output_dir / "knowledge_messages.csv",
        [
            {
                "timestamp": row["timestamp"],
                "source_priority": row["source_priority"],
                "chat_title": row["chat_title"],
                "author": row["author"],
                "topics": ";".join(row["topics"]),
                "is_question": row["is_question"],
                "usefulness_score": row["usefulness_score"],
                "text": row["text"],
                "links": ";".join(row["links"]),
                "media": ";".join(row["media"]),
                "source": f"{row['chat_folder']}/{row['file']}#{row['message_id']}",
            }
            for row in knowledge_rows
        ],
        ["timestamp", "source_priority", "chat_title", "author", "topics", "is_question", "usefulness_score", "text", "links", "media", "source"],
    )

    topic_counts = write_topic_files(output_dir, kept)

    topic_rows = []
    for chat in sorted(chat_stats):
        chat_messages = [message for message in kept if message.chat_folder == chat]
        counter = Counter(topic for message in chat_messages for topic in message.topics)
        for topic in sorted(TOPICS):
            topic_rows.append({"chat": chat, "topic": topic, "kept_messages": counter[topic]})
    write_csv(output_dir / "topic_summary.csv", topic_rows, ["chat", "topic", "kept_messages"])

    report = {
        "source": str(root),
        "output": str(output_dir.resolve()),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "totals": {
            "raw_messages": len(all_messages),
            "kept_messages": len(kept),
            "knowledge_messages": len(knowledge_rows),
            "skipped_messages": len(all_messages) - len(kept),
            "qa_candidates": len(pairs),
            "qa_best": len(best_pairs),
        },
        "chat_stats": {chat: dict(stats) for chat, stats in sorted(chat_stats.items())},
        "skip_reasons": dict(Counter(message.skip_reason for message in all_messages if message.skip_reason)),
        "topic_counts": dict(Counter(topic for message in kept for topic in message.topics)),
    }
    (output_dir / "processing_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_readme(output_dir, root, chat_stats, kept, knowledge_rows, pairs, best_pairs, topic_counts)

    print(json.dumps(report["totals"], ensure_ascii=False, indent=2))
    print(str(output_dir.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
