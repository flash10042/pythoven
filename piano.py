import numpy as np
import pygame as pg
import argparse
from os import path


class Piano():
	def __init__(self, samplerate=44100, amplitude=8192, decay=3, note_value=2.5):
		"""
		Initialize pygame mixer, read file with keybindings, generate sound waves
		"""
		pg.mixer.init(samplerate, channels=2)

		self.SAMPLERATE = samplerate
		self.AMPLITUDE = amplitude
		self.DECAY = decay
		self.NOTE_VALUE = note_value

		self.notes = [
					'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3',
					'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4',
					'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5'
				]

		base_freq = np.array([[261.63, 523.25, 788.35, 1051.027, 2118.91]]).T
		ampl = np.array([[amplitude, amplitude/2, amplitude/4, amplitude/8, amplitude/16]]).T
		sounds = list()
		for n in range(-12, 24):
			freq = base_freq * 2 ** (n / 12)
			data = np.linspace(0, self.NOTE_VALUE, int(self.SAMPLERATE*self.NOTE_VALUE))
			data = (ampl * np.sin(2 * np.pi * freq * data) / np.exp(self.DECAY*data))
			data = np.sum(data, axis=0).astype(np.int16)
			data = data.reshape(-1, 1)
			data = np.concatenate([data, data], axis=1)
			sounds.append(pg.sndarray.make_sound(data))
		with open(path.join('utils', 'pianokeys.mapping')) as f:
			self.keys = f.read().split('\n')
		self.key_note = dict(zip(self.keys, sounds))
		self.pressed = {key: False for key in self.keys}


	def play_note(self, key):
		self.key_note[key].stop()
		self.key_note[key].play()


	def start_playing(self, notes_file=''):
		pg.init()

		icon = pg.image.load(path.join('utils', 'icon.png'))
		pg.display.set_icon(icon)
		pg.display.set_caption("Virtual Piano")

		if not notes_file:
			SIZE = (973, 282)
			self.notes_file = notes_file
		else:
			SIZE = (973, 482)
			pg.font.init()

		self.screen = pg.display.set_mode(SIZE)
		self.screen.fill((20, 11, 10))
		bg = pg.image.load(path.join('utils', "keys.png")).convert()
		self.screen.blit(bg, (0, SIZE[1]-282))

		if notes_file:
			self.WIDTH = 400
			self.HEIGHT = 150
			self.LEFT = (SIZE[0]-self.WIDTH)//2
			self.TOP = (SIZE[1]-282-self.HEIGHT)//2

			self.RECT = pg.Rect(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT)
			pg.draw.rect(self.screen, (245, 241, 230), self.RECT)

			self.CURRENT_COLOR = (0, 0, 0)
			self.OTHER_COLOR = (122, 122, 122)
			self.FONT = pg.font.Font(None, 22)

		pg.display.flip()

		if not notes_file:
			while True:
				event = pg.event.wait()
				if event.type in [pg.KEYDOWN, pg.KEYUP]:
					if event.key == pg.K_ESCAPE:
						pg.quit()
						quit()
					current_key = pg.key.name(event.key)

				if event.type == pg.KEYDOWN and current_key in self.key_note.keys():
					self.play_note(current_key)
		else:
			sheet = self.load_notes(notes_file)
			self.SPACE_BETWEEN = self.WIDTH // len(sheet[0]) - 7

			current_idx = 0
			self.display_notes(sheet, current_idx)

			while True:
				event = pg.event.wait()
				if event.type in [pg.KEYDOWN, pg.KEYUP]:
					if event.key == pg.K_ESCAPE:
						pg.quit()
						quit()
					current_key = pg.key.name(event.key)

				if event.type == pg.KEYDOWN and current_key in self.key_note.keys():
					self.play_note(current_key)
					self.pressed[current_key] = True

				if event.type == pg.KEYUP and current_key in self.key_note.keys():
					self.pressed[current_key] = False
					if not any(self.pressed.values()):
						current_idx = self.display_notes(sheet, current_idx + 1)


	def load_notes(self, notes_file):
		parsed = list()
		note_key = dict(zip(self.notes, self.keys))
		with open(notes_file) as file:
			lines = file.read().split('\n')[:-1]
			for line in lines:
				parsed_line = list()
				for chord in line.split():
					res = ''
					for note in chord.split('.'):
						res += note_key[note]
					parsed_line.append(res)
				parsed.append(parsed_line)
		return parsed


	def display_notes(self, notes, current):
		pg.draw.rect(self.screen, (245, 241, 230), self.RECT)
		if len(notes):
			if current >= len(notes[0]):
				current = 0
				notes.pop(0)
			if not len(notes):
				pg.display.update(self.RECT)
				return 0

			left = self.LEFT + self.SPACE_BETWEEN
			for i in range(len(notes[0])):
				color = self.OTHER_COLOR
				if current == i: color = self.CURRENT_COLOR
				note = self.FONT.render(notes[0][i], True, color)
				self.screen.blit(note, (left, self.TOP + self.HEIGHT//3))
				left += self.SPACE_BETWEEN + 5*len(notes[0][i])

			if len(notes) > 1:
				left = self.LEFT + self.SPACE_BETWEEN
				for i in range(len(notes[1])):
					note = self.FONT.render(notes[1][i], True, self.OTHER_COLOR)
					self.screen.blit(note, (left, self.TOP + self.HEIGHT//3*2))
					left += self.SPACE_BETWEEN + 5*len(notes[1][i])

			pg.display.update(self.RECT)

			return current
		else:
			pg.display.update(self.RECT)
			return 0


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Virtual piano with Python')

	parser.add_argument(
		'-n', '--notes',
        default='',
        help='(Optional) File with notes to play')

	args = parser.parse_args()

	piano = Piano()
	piano.start_playing(args.notes)
