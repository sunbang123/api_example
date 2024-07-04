from midiutil import MIDIFile
import numpy as np

# 간단한 스케일 및 코드 정의
MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10]
CHORDS = {
    "I": [0, 4, 7],
    "ii": [2, 5, 9],
    "iii": [4, 7, 11],
    "IV": [5, 9, 0],
    "V": [7, 11, 2],
    "vi": [9, 0, 4],
    "vii°": [11, 2, 5],
    "I7": [0, 4, 7, 10],
    "IV7": [5, 9, 0, 2],
    "V7": [7, 11, 2, 5]
}
COMMON_CHORD_PROGRESSIONS = [
    ["I", "V", "vi", "IV"],
    ["ii", "V", "I", "vi"],
    ["I", "vi", "IV", "V"],
    ["I", "IV", "V", "IV"],
    ["vi", "IV", "I", "V"],
]


def get_scale(key_signature):
    root, scale_type = key_signature.split()
    semitone_map = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10,
                    'B': 11}
    root_semitone = semitone_map[root]
    scale = MAJOR_SCALE if scale_type == 'major' else MINOR_SCALE
    return [(note + root_semitone) % 12 for note in scale]


def generate_music(info, key_signature):
    scale_notes = get_scale(key_signature)
    chord_progression = COMMON_CHORD_PROGRESSIONS[np.random.choice(len(COMMON_CHORD_PROGRESSIONS))]

    # 마르코프 체인을 위한 전환 행렬 초기화
    transition_matrix = np.zeros((12, 12))

    # 전환 행렬을 생성 (여기서는 단순히 임의의 확률로 초기화)
    for i in range(12):
        transition_matrix[i] = np.random.dirichlet(np.ones(12), size=1)

    # 초기 음 설정
    current_note = np.random.choice(scale_notes)
    generated_notes = [current_note]

    for _ in range(49):  # 50개의 음을 생성
        next_note_probs = transition_matrix[current_note]
        next_note = np.random.choice(range(12), p=next_note_probs)

        # 조표에 맞게 변환
        while next_note not in scale_notes:
            next_note = (next_note + 1) % 12

        generated_notes.append(next_note)
        current_note = next_note

    return generated_notes, chord_progression


def harmonize_chord_progression(chord_progression, key_signature):
    harmonized_progression = []
    scale_notes = get_scale(key_signature)

    for chord in chord_progression:
        if chord in CHORDS:
            harmonized_progression.append(chord)
        else:
            # 기본 코드 진행 외에 텐션 코드 등을 추가
            harmonized_progression.append(chord + "7")

    return harmonized_progression


def detect_dissonance(generated_notes, chord_progression, key_signature):
    scale_notes = get_scale(key_signature)
    dissonances = []

    for i, note in enumerate(generated_notes):
        current_chord = CHORDS[chord_progression[i % len(chord_progression)]]
        if note % 12 not in current_chord:
            dissonances.append((i, note))

    return dissonances

def correct_dissonance(generated_notes, dissonances, chord_progression):
    for index, note in dissonances:
        current_chord = CHORDS[chord_progression[index % len(chord_progression)]]
        closest_note = min(current_chord, key=lambda x: abs(x - (note % 12)))
        generated_notes[index] = (generated_notes[index] // 12) * 12 + closest_note

    return generated_notes


def ensure_complete_measures(generated_notes, measure_length, total_length):
    # Measure length can be considered as the length of one measure in ticks or time units
    remainder = total_length % measure_length

    if remainder != 0:
        padding_length = measure_length - remainder
        generated_notes.extend([0] * padding_length)  # Pad with silence (or rests)

    return generated_notes


def add_cadence(generated_notes, key_signature):
    # Add a perfect cadence (V-I) at the end
    scale_notes = get_scale(key_signature)
    root = scale_notes[0]
    fifth = scale_notes[4]
    generated_notes.append(fifth)  # Add V
    generated_notes.append(root)  # Add I
    return generated_notes

def save_midi_file(sequence, chord_progression, key_signature, file_path, melody_track=None):
    melody_track = 0
    harmony_track = 1
    channel = 0
    chord_time = 0  # 코드의 시작 시간
    chord_duration = 4  # 코드의 길이
    melody_time = 0  # 멜로디의 시작 시간
    melody_duration = 1  # 멜로디 음의 길이
    tempo = 120  # BPM
    volume = 100  # 볼륨

    midi = MIDIFile(2)  # 두 개의 트랙을 가진 MIDI 파일 생성
    midi.addTempo(melody_track, 0, tempo)
    midi.addTempo(harmony_track, 0, tempo)

    # 코드 진행 반복
    num_repeats = len(sequence) // (len(chord_progression) * chord_duration) + 1
    harmonized_progression = harmonize_chord_progression(chord_progression, key_signature)
    for _ in range(num_repeats):
        for chord in harmonized_progression:
            notes = [note + 48 for note in CHORDS[chord]]
            for note in notes:
                midi.addNote(harmony_track, channel, note, chord_time, chord_duration, volume)
            chord_time += chord_duration

    # 멜로디 추가 (옥타브를 높여서 연주)
    for pitch in sequence:
        midi.addNote(melody_track, channel, pitch + 72, melody_time, melody_duration,
                     volume)  # MIDI 피치는 60을 더해 C4로 설정, 72를 더해 한 옥타브 높임
        melody_time += melody_duration

    # 코드 진행과 멜로디가 동시에 끝나도록 패딩 추가
    if chord_time > melody_time:
        for pitch in sequence[-(chord_time - melody_time):]:
            midi.addNote(melody_track, channel, pitch + 72, melody_time, melody_duration, volume)
            melody_time += melody_duration

    with open(file_path, "wb") as output_file:
        midi.writeFile(output_file)