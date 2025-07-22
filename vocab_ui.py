# Handles all UI widget creation and layout
import customtkinter as ctk
import tkinter as tk

DEFAULT_FONT = ("Segoe UI", 14)
LARGE_FONT = ("Segoe UI", 18, "bold")

class VocabUI:
    def __init__(self, master, add_word_cb, delete_word_cb, select_word_cb, enter_practice_cb):
        self.master = master
        self.add_word_cb = add_word_cb
        self.delete_word_cb = delete_word_cb
        self.select_word_cb = select_word_cb
        self.enter_practice_cb = enter_practice_cb
        self.create_widgets()

    def create_widgets(self):
        self.entry_frame = ctk.CTkFrame(self.master)
        self.entry_frame.pack(pady=10)

        self.word_label = ctk.CTkLabel(self.entry_frame, text="German Word:", font=DEFAULT_FONT)
        self.word_label.grid(row=0, column=0, padx=5, pady=5)
        self.word_entry = ctk.CTkEntry(self.entry_frame, width=250, height=40, font=DEFAULT_FONT)
        self.word_entry.grid(row=0, column=1, padx=5, pady=5)

        self.meaning_label = ctk.CTkLabel(self.entry_frame, text="Meaning:", font=DEFAULT_FONT)
        self.meaning_label.grid(row=1, column=0, padx=5, pady=5)
        self.meaning_entry = ctk.CTkEntry(self.entry_frame, width=250, height=40, font=DEFAULT_FONT)
        self.meaning_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = ctk.CTkButton(self.entry_frame, text="Add", font=DEFAULT_FONT, command=self.add_word_cb)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.message_label = ctk.CTkLabel(self.master, text="", font=DEFAULT_FONT)
        self.message_label.pack(pady=5)

        self.practice_button = ctk.CTkButton(self.master, text="Practice Mode", font=DEFAULT_FONT, command=self.enter_practice_cb)
        self.practice_button.pack(pady=5)

        self.listbox_frame = ctk.CTkFrame(self.entry_frame)
        self.listbox_frame.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky="ew")
        self.word_listbox = tk.Listbox(self.listbox_frame, height=10, width=30, font=DEFAULT_FONT, exportselection=False)
        self.word_listbox.pack(side="left", fill="y")
        self.listbox_scrollbar = tk.Scrollbar(self.listbox_frame, orient="vertical", command=self.word_listbox.yview)
        self.listbox_scrollbar.pack(side="right", fill="y")
        self.word_listbox.config(yscrollcommand=self.listbox_scrollbar.set)
        self.word_listbox.bind("<<ListboxSelect>>", self.select_word_cb)
        self.delete_button = ctk.CTkButton(self.entry_frame, text="Delete", font=DEFAULT_FONT, command=self.delete_word_cb)
        self.delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)


        self.practice_frame = ctk.CTkFrame(self.master)
        self.practice_word_label = ctk.CTkLabel(self.practice_frame, text="", font=LARGE_FONT)
        self.practice_word_label.pack(pady=10)
        self.show_meaning_button = ctk.CTkButton(self.practice_frame, text="Show Meaning", font=DEFAULT_FONT)
        self.show_meaning_button.pack(pady=5)
        self.meaning_display_label = ctk.CTkLabel(self.practice_frame, text="", font=DEFAULT_FONT)
        self.meaning_display_label.pack(pady=5)
        self.next_button = ctk.CTkButton(self.practice_frame, text="Next", font=DEFAULT_FONT)
        self.next_button.pack(pady=5)
        self.exit_practice_button = ctk.CTkButton(self.practice_frame, text="Exit Practice Mode", font=DEFAULT_FONT)
        self.exit_practice_button.pack(pady=5)
