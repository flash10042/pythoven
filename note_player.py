import numpy as np
from scipy.io import wavfile
import pygame as pg


class Song():
	def __init__(self, BPM=60, SAMPLERATE=44100):
		self.SAMPLERATE = SAMPLERATE
		self.BPM = BPM
		self.AMPLITUDE = 6_000
		self.DECAY = 3

		self.note_freq = dict()
		notes = [
					'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2',
					'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3',
					'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4',
					'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5',
					'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6'
				]
		base_freq = 65.406
		for n, note in enumerate(notes):
			self.note_freq[note] = base_freq * 2 ** (n / 12)
		self.note_freq['*'] = 0


		self.song = np.array(list(), dtype=np.int16)


	def play(self):
		pg.mixer.init(channels=1)
		song = pg.sndarray.make_sound(self.song)
		song.play()
		input("Press Enter to exit")


	def generate_sound_array(self, note, value):
		freq = self.note_freq[note]
		note_duration = 60 / self.BPM / value
		data = np.linspace(0, note_duration, int(self.SAMPLERATE*note_duration))
		data = (self.AMPLITUDE * np.sin(2 * np.pi * freq * data) / np.exp(self.DECAY*data)).astype(np.int16)

		return data


	def append_sound(self, data, shift=0):
		assert shift >= 0

		if shift:
			shift_value = int(self.SAMPLERATE * 60 / self.BPM / shift)
			if len(data) >= shift_value:
				self.song[-shift_value:] += data[:shift_value]
				self.song = np.append(self.song, data[shift_value:])
			else:
				shift_end = shift_value - len(data)
				self.song[-shift_value:-shift_end] += data
		else:
			self.song = np.append(self.song, data)


	def generate_chord(self, chord_data):
		splited_chord = chord_data.split('_')
		notes = splited_chord[0].split('.')
		value = float(splited_chord[1])
		shift = float(splited_chord[2]) if len(splited_chord) >= 3 else 0
		data = self.generate_sound_array(notes[0], value)
		if len(notes) > 1:
			for note in notes[1:]:
				data += self.generate_sound_array(note, value)
		self.append_sound(data, shift)


	def generate_song(self, song_data):
		for chord in song_data:
			self.generate_chord(chord)


	def save_wav(self, name='song.wav'):
		wavfile.write(name, self.SAMPLERATE, self.song)


if __name__ == '__main__':
	song = Song(30)


	notes = 'E5_8 D#5_8 E5_8 D#5_8 E5_8 B4_8 D5_8 C5_8 A2_8 A4_4_8 E3_8_8 A3_8 '
	notes += 'C4_8 E4_8 A4_8 E2_8 B4_4_8 E3_8_8 G#3_8 E4_8 G#4_8 B4_8 A2_8 C5_4_8 '
	notes += 'E3_8_8 A4_8 E4_8 '
	notes += 'E5_8 D#5_8 E5_8 D#5_8 E5_8 B4_8 D5_8 C5_8 A2_8 A4_4_8 E3_8_8 A3_8 '
	notes += 'C4_8 E4_8 A4_8 E2_8 B4_4_8 E3_8_8 G#3_8 E4_8 G#4_8 B4_8 '
	copy = notes
	notes += 'A2_8 A4_4_8 E3_8_8 A3_8 '
	notes += copy
	notes += 'A4_8 A2_8_8 E3_8 A3_8 B4_8 C5_8 D5_8 '
	notes += 'C3_8 E5_6_8 G3_8_24 C4_8 G4_8 F5_8 E5_8'
	notes += ' G2_8 D5_6_8 G3_8_24 B3_8 F4_8 E5_8 D5_8'
	notes += ' A2_8 C5_6_8 E3_8_24 A3_8 E4_8 D5_8 C5_8'
	notes += ' B4_4 E2_8_4 E3_8_8 E4_8 E4_8 E5_8 E4_8'
	notes += ' E5_8 E5_8 E6_8 D#5_8 E5_8 D#5_8'
	notes += ' E5_8 D#5_8 E5_8 D#5_8 E5_8 D5_8'
	notes += copy
	notes += ' A2.A4_1'


	song.generate_song(notes.split())
	#song.save_wav()
	song.play()
