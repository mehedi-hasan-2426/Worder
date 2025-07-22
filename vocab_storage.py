# Handles vocabulary file loading and saving
import json
import os
import config

def load_vocab():
    if os.path.exists(config.VOCAB_FILE):
        try:
            with open(config.VOCAB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_vocab(vocab):
    try:
        with open(config.VOCAB_FILE, "w", encoding="utf-8") as f:
            json.dump(vocab, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return str(e)
    return None
