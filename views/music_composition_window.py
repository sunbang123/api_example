import tkinter as tk
from controllers.music_controller import MusicController
import asyncio
import pygame
import os

class MusicCompositionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Music Generator")

        self.api_key_label = tk.Label(self, text="GPT API Key:")
        self.api_key_label.grid(row=0, column=0, padx=5, pady=5)
        self.api_key_entry = tk.Entry(self, show='*')
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=5)

        self.keyword_label = tk.Label(self, text="Keyword:")
        self.keyword_label.grid(row=1, column=0, padx=5, pady=5)
        self.keyword_entry = tk.Entry(self)
        self.keyword_entry.grid(row=1, column=1, padx=5, pady=5)

        self.key_signature_label = tk.Label(self, text="Key Signature(ex: C Major):")
        self.key_signature_label.grid(row=2, column=0, padx=5, pady=5)
        self.key_signature_entry = tk.Entry(self)
        self.key_signature_entry.grid(row=2, column=1, padx=5, pady=5)

        self.generate_button = tk.Button(self, text="Generate Music", command=self.generate_music)
        self.generate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.save_button = tk.Button(self, text="Save Music", command=self.save_music)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.play_button = tk.Button(self, text="Play Music", command=self.play_music)
        self.play_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.controller = MusicController(self)
        pygame.mixer.init()

    def get_api_key(self):
        return self.api_key_entry.get()

    def get_keyword(self):
        return self.keyword_entry.get()

    def get_key_signature(self):
        return self.key_signature_entry.get()

    def generate_music(self):
        asyncio.run(self.async_generate_music())

    async def async_generate_music(self):
        await self.controller.generate_music()

    def save_music(self):
        self.controller.save_music()

    def play_music(self):
        file_path = 'output/generated_music.mid'
        if os.path.exists(file_path):
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        else:
            print("Generate and save music first before playing.")