# Telegram knowledge base

Compact export for internal retrieval and manual search. This folder is intentionally not linked from the public site navigation or sitemap. The repository robots.txt also disallows /Doc/.

Important: this is not access control. If a file is in the public GitHub Pages branch, it can still be opened by direct URL or through GitHub.

## Included

- topics/*.md - recent high-signal messages by topic, newest first.
- qa_best.compact.jsonl - compact question/answer pairs.
- knowledge_messages.compact.001.jsonl / knowledge_messages.compact.002.jsonl - compact high-signal message set split into two parts.
- topic_summary.csv - topic counters by chat.
- processing_report.json - processing counts and skip reasons.
- tools/process_nomad_exports.py - script used to generate the processed export.
- manifest.json - file list and counts for this compact bundle.

## Excluded

- clean_messages.jsonl / clean_messages.csv - too large and noisy for git.
- qa_candidates.jsonl - broad noisy candidate layer.
- knowledge_messages.csv - duplicate of JSONL data.

## Compact JSONL fields

knowledge_messages.compact.001.jsonl and knowledge_messages.compact.002.jsonl:
- ts - timestamp
- chat - source chat folder
- author - message author
- text - message text
- topics - assigned topics
- source - source export path
- id - Telegram message id
- reply_to - replied message id, when present
- links - links, when present
- score - usefulness score

qa_best.compact.jsonl:
- q / a - question and answer
- qt / at - question and answer timestamps
- qa / aa - question and answer authors
- chat - source chat folder
- topics - assigned topics
- source_q / source_a - source export paths
- qid / aid - source message ids
- links - answer links, when present
- score - QA quality score
