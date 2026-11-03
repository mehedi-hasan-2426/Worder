# Simple German Vocabulary Trainer

Dependency maintenance: [Renovate](renovate.json) is prepared, but needs its
[GitHub App](https://github.com/apps/renovate) installed for this repository.
There is currently no tracked dependency manifest, so the inline `pip install`
command below is not automatically updated. Supported manifests added later are
discovered automatically. Routine PRs are grouped weekly; vulnerability PRs bypass
the schedule and release-age delay. All updates require manual review.

A desktop app to help you learn and practice German vocabulary. Add new words, review them in flashcard mode, and manage your vocabulary list easily.

## Features
- Add new German words and their meanings
- Prevents duplicate entries (case-insensitive)
- Practice mode: flashcard-style review
- Delete words from your list
- Vocabulary is saved in a local JSON file
- Scrollable word list for large vocabularies

## How to Run
1. Install requirements: `pip install customtkinter`
2. Run the app: `python main.py`

## Project Structure
- `main.py` — Main application logic
- `vocab_ui.py` — UI layout and widgets
- `vocab_storage.py` — File handling for vocabulary
- `config.py` — Configuration (window size, file names, etc.)
