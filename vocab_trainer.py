
import customtkinter as ctk
import json
import os
import random
import config
import tkinter as tk

class VocabTrainer(ctk.CTk):
    def set_message(self, text, text_color=None, duration=10000):
        self.message_label.configure(text=text)
        if text_color:
            self.message_label.configure(text_color=text_color)
        if hasattr(self, '_message_after_id') and self._message_after_id:
            self.after_cancel(self._message_after_id)
        self._message_after_id = self.after(duration, lambda: self.message_label.configure(text=""))
    def __init__(self):
        super().__init__()
        self.title(config.APP_TITLE)
        self.geometry(config.WINDOW_GEOMETRY)
        self.vocab = {}
        self.practice_words = []
        self.practice_index = 0
        self.practice_mode = False
        self.create_widgets()
        self.load_vocab()

    def create_widgets(self):
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.pack(pady=10)
        self.word_label = ctk.CTkLabel(self.entry_frame, text="German Word:")
        self.word_label.grid(row=0, column=0, padx=5, pady=5)
        self.word_entry = ctk.CTkEntry(self.entry_frame, width=150)
        self.word_entry.grid(row=0, column=1, padx=5, pady=5)
        self.meaning_label = ctk.CTkLabel(self.entry_frame, text="Meaning:")
        self.meaning_label.grid(row=1, column=0, padx=5, pady=5)
        self.meaning_entry = ctk.CTkEntry(self.entry_frame, width=150)
        self.meaning_entry.grid(row=1, column=1, padx=5, pady=5)
        self.add_button = ctk.CTkButton(self.entry_frame, text="Add", command=self.add_word)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.message_label = ctk.CTkLabel(self, text="")
        self.message_label.pack(pady=5)
        self.practice_button = ctk.CTkButton(self, text="Practice Mode", command=self.enter_practice_mode)
        self.practice_button.pack(pady=5)
        
        self.listbox_frame = ctk.CTkFrame(self.entry_frame)
        self.listbox_frame.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky="ew")
        self.word_listbox = tk.Listbox(self.listbox_frame, height=6, width=22, exportselection=False)
        self.word_listbox.pack(side="left", fill="y")
        self.listbox_scrollbar = tk.Scrollbar(self.listbox_frame, orient="vertical", command=self.word_listbox.yview)
        self.listbox_scrollbar.pack(side="right", fill="y")
        self.word_listbox.config(yscrollcommand=self.listbox_scrollbar.set)
        self.word_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.delete_button = ctk.CTkButton(self.entry_frame, text="Delete", command=self.delete_word)
        self.delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.practice_frame = ctk.CTkFrame(self)
        self.practice_word_label = ctk.CTkLabel(self.practice_frame, text="", font=("Arial", 18))
        self.practice_word_label.pack(pady=10)
        self.show_meaning_button = ctk.CTkButton(self.practice_frame, text="Show Meaning", command=self.show_meaning)
        self.show_meaning_button.pack(pady=5)
        self.meaning_display_label = ctk.CTkLabel(self.practice_frame, text="", font=("Arial", 16))
        self.meaning_display_label.pack(pady=5)
        self.next_button = ctk.CTkButton(self.practice_frame, text="Next", command=self.next_word)
        self.next_button.pack(pady=5)
        self.exit_practice_button = ctk.CTkButton(self.practice_frame, text="Exit Practice Mode", command=self.exit_practice_mode)
        self.exit_practice_button.pack(pady=5)


    def on_listbox_select(self, event):
        selection = self.word_listbox.curselection()
        if selection:
            value = self.word_listbox.get(selection[0])
            self.word_entry.delete(0, ctk.END)
            self.word_entry.insert(0, value)

    def refresh_word_listbox(self):
        self.word_listbox.delete(0, "end")
        for word in sorted(self.vocab.keys(), key=lambda w: w.lower()):
            self.word_listbox.insert("end", word)

    def delete_word(self):
        selection = self.word_listbox.curselection()
        if selection:
            word = self.word_listbox.get(selection[0])
            lower_words = {w.lower(): w for w in self.vocab}
            if word.lower() in lower_words:
                orig = lower_words[word.lower()]
                del self.vocab[orig]
                self.save_vocab()
                self.refresh_word_listbox()
                if self.word_entry.get().strip().lower() == orig.lower():
                    self.word_entry.delete(0, ctk.END)
                self.set_message(f'Deleted: {orig}', text_color="red")
                return
        self.set_message("Select a valid word to delete.", text_color="orange")
    
    def add_word(self):
        word = self.word_entry.get().strip()
        meaning = self.meaning_entry.get().strip()
        if not word or not meaning:
            self.set_message("Please enter both word and meaning.", text_color="red")
            return
        lower_words = {w.lower(): w for w in self.vocab}
        if word.lower() in lower_words:
            orig = lower_words[word.lower()]
            self.set_message(f'Already exists: {orig} = {self.vocab[orig]}', text_color="orange")
        else:
            self.vocab[word] = meaning
            self.save_vocab()
            self.set_message(f'Added: {word} = {meaning}', text_color="green")
            self.word_entry.delete(0, ctk.END)
            self.meaning_entry.delete(0, ctk.END)
            self.refresh_word_listbox()

    def save_vocab(self):
        try:
            with open(config.VOCAB_FILE, "w", encoding="utf-8") as f:
                json.dump(self.vocab, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.set_message(f"Error saving: {e}", text_color="red")

    def load_vocab(self):
        if os.path.exists(config.VOCAB_FILE):
            try:
                with open(config.VOCAB_FILE, "r", encoding="utf-8") as f:
                    self.vocab = json.load(f)
            except Exception:
                self.vocab = {}
        else:
            self.vocab = {}

        if hasattr(self, 'word_listbox'):
            self.refresh_word_listbox()

    def enter_practice_mode(self):
        if not self.vocab:
            self.set_message("No words to practice.", text_color="red")
            return
        self.practice_mode = True
        self.practice_words = list(self.vocab.keys())
        random.shuffle(self.practice_words)
        self.practice_index = 0
        self.entry_frame.pack_forget()
        self.practice_button.pack_forget()
        self.message_label.pack_forget()
        self.practice_frame.pack(pady=10)
        self.show_practice_word()

    def show_practice_word(self):
        if not self.practice_words:
            self.practice_word_label.configure(text="No words available.")
            self.meaning_display_label.configure(text="")
            return
        word = self.practice_words[self.practice_index]
        self.practice_word_label.configure(text=word)
        self.meaning_display_label.configure(text="")

    def show_meaning(self):
        word = self.practice_words[self.practice_index]
        meaning = self.vocab.get(word, "")
        self.meaning_display_label.configure(text=meaning)

    def next_word(self):
        if not self.practice_words:
            return
        self.practice_index = (self.practice_index + 1) % len(self.practice_words)
        self.show_practice_word()

    def exit_practice_mode(self):
        self.practice_frame.pack_forget()
        self.entry_frame.pack(pady=10)
        self.practice_button.pack(pady=5)
        self.message_label.pack(pady=5)
        self.practice_mode = False

if __name__ == "__main__":
    app = VocabTrainer()
    app.mainloop()
