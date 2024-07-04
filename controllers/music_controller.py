import asyncio
from models.keyword_processor import analyze_keyword
from models.music_generator import generate_music
from models.music_generator import detect_dissonance
from models.music_generator import correct_dissonance
from models.music_generator import ensure_complete_measures
from models.music_generator import add_cadence
from models.music_generator import save_midi_file

class MusicController:
    def __init__(self, view):
        self.view = view
        self.music_sequence = None
        self.chord_progression = None

    async def generate_music(self):
        api_key = self.view.get_api_key()
        keyword = self.view.get_keyword()
        key_signature = self.view.get_key_signature()

        analysis_result = await analyze_keyword(keyword, api_key)
        self.music_sequence, self.chord_progression = generate_music(analysis_result, key_signature)

        # Detect and correct dissonances
        dissonances = detect_dissonance(self.music_sequence, self.chord_progression, key_signature)
        self.music_sequence = correct_dissonance(self.music_sequence, dissonances, self.chord_progression)

        # Ensure the last measure is complete
        measure_length = 4  # Assume a 4/4 time signature, adjust as needed
        total_length = len(self.music_sequence)
        self.music_sequence = ensure_complete_measures(self.music_sequence, measure_length, total_length)

        # Add a cadence to finish the music
        self.music_sequence = add_cadence(self.music_sequence, key_signature)

        print("Music generated, corrected, and finalized successfully.")

    def save_music(self):
        if self.music_sequence and self.chord_progression:
            file_path = 'output/generated_music.mid'
            save_midi_file(self.music_sequence, self.chord_progression, self.view.get_key_signature(), file_path)
            print(f"Music saved as {file_path}")
        else:
            print("Generate music first before saving.")