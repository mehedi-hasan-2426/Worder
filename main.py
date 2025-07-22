# Handles all business logic and app state
import customtkinter as ctk
import config
import vocab_storage
from vocab_ui import VocabUI
import random

class VocabApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(config.APP_TITLE)
        self.geometry(config.WINDOW_GEOMETRY)
        self.vocab = vocab_storage.load_vocab()
        self.practice_words = []
        self.practice_index = 0
        self.practice_mode = False
        self._message_after_id = None
        self.ui = VocabUI(self, self.add_word, self.delete_word, self.on_listbox_select, self.enter_practice_mode)
        self.refresh_word_listbox()
        self.ui.show_meaning_button.configure(command=self.show_meaning)
        self.ui.next_button.configure(command=self.next_word)
        self.ui.exit_practice_button.configure(command=self.exit_practice_mode)

    def set_message(self, text, text_color=None, duration=10000):
        self.ui.message_label.configure(text=text)
        if text_color:
            self.ui.message_label.configure(text_color=text_color)
        if self._message_after_id:
            self.after_cancel(self._message_after_id)
        self._message_after_id = self.after(duration, lambda: self.ui.message_label.configure(text=""))

    def refresh_word_listbox(self):
        self.ui.word_listbox.delete(0, "end")
        for word in sorted(self.vocab.keys(), key=lambda w: w.lower()):
            self.ui.word_listbox.insert("end", word)

    def on_listbox_select(self, event):
        selection = self.ui.word_listbox.curselection()
        if selection:
            value = self.ui.word_listbox.get(selection[0])
            self.ui.word_entry.delete(0, ctk.END)
            self.ui.word_entry.insert(0, value)

    def add_word(self):
        word = self.ui.word_entry.get().strip()
        meaning = self.ui.meaning_entry.get().strip()
        if not word or not meaning:
            self.set_message("Please enter both word and meaning.", text_color="red")
            return
        lower_words = {w.lower(): w for w in self.vocab}
        if word.lower() in lower_words:
            orig = lower_words[word.lower()]
            self.set_message(f'Already exists: {orig} = {self.vocab[orig]}', text_color="orange")
        else:
            self.vocab[word] = meaning
            vocab_storage.save_vocab(self.vocab)
            self.set_message(f'Added: {word} = {meaning}', text_color="green")
            self.ui.word_entry.delete(0, ctk.END)
            self.ui.meaning_entry.delete(0, ctk.END)
            self.refresh_word_listbox()

    def delete_word(self):
        selection = self.ui.word_listbox.curselection()
        if selection:
            word = self.ui.word_listbox.get(selection[0])
            lower_words = {w.lower(): w for w in self.vocab}
            if word.lower() in lower_words:
                orig = lower_words[word.lower()]
                del self.vocab[orig]
                vocab_storage.save_vocab(self.vocab)
                self.refresh_word_listbox()
                if self.ui.word_entry.get().strip().lower() == orig.lower():
                    self.ui.word_entry.delete(0, ctk.END)
                self.set_message(f'Deleted: {orig}', text_color="red")
                return
        self.set_message("Select a valid word to delete.", text_color="orange")

    def enter_practice_mode(self):
        if not self.vocab:
            self.set_message("No words to practice.", text_color="red")
            return
        self.practice_mode = True
        self.practice_words = list(self.vocab.keys())
        random.shuffle(self.practice_words)
        self.practice_index = 0
        self.ui.entry_frame.pack_forget()
        self.ui.practice_button.pack_forget()
        self.ui.message_label.pack_forget()
        self.ui.practice_frame.pack(pady=10)
        self.show_practice_word()

    def show_practice_word(self):
        if not self.practice_words:
            self.ui.practice_word_label.configure(text="No words available.")
            self.ui.meaning_display_label.configure(text="")
            return
        word = self.practice_words[self.practice_index]
        self.ui.practice_word_label.configure(text=word)
        self.ui.meaning_display_label.configure(text="")

    def show_meaning(self):
        word = self.practice_words[self.practice_index]
        meaning = self.vocab.get(word, "")
        self.ui.meaning_display_label.configure(text=meaning)

    def next_word(self):
        if not self.practice_words:
            return
        self.practice_index = (self.practice_index + 1) % len(self.practice_words)
        self.show_practice_word()

    def exit_practice_mode(self):
        self.ui.practice_frame.pack_forget()
        self.ui.entry_frame.pack(pady=10)
        self.ui.practice_button.pack(pady=5)
        self.ui.message_label.pack(pady=5)
        self.practice_mode = False

if __name__ == "__main__":
    app = VocabApp()
    app.mainloop()
