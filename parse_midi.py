import mido
import numpy as np
from os import path, listdir

MIDI_FOLDER = 'midies'
SAMPLES_FOLDER = 'samples'
LOWER_NOTE = 21
UPPER_NOTE = 108
NOTES_RANGE = UPPER_NOTE - LOWER_NOTE
TIME_STEP = 0.1
PPQ = 480
TEMPO = 500000


def midi2sample(filename):
	mid = mido.MidiFile(path.join(MIDI_FOLDER, filename))

	notes = dict()
	time = 0
	ppq = mid.ticks_per_beat
	i = 0

	for msg in mid:
		time += msg.time
		if msg.type == 'note_on':
			note = msg.note - LOWER_NOTE
			if note < 0 or note > NOTES_RANGE:
				print(f"CRAZY NOTES IN {filename}")
				print(msg.note)
				return
			if note not in notes:
				notes[note] = list()
			notes[note].append(time)
			i += 1

	sample = list()

	for note in notes:
		note2vec = np.eye(NOTES_RANGE+1, 1, -note).reshape(-1)
		for time in notes[note]:
			t = int(time / TIME_STEP)
			while len(sample) <= t:
				sample.append(np.zeros(NOTES_RANGE+1))
			sample[t] += note2vec

	return np.array(sample, dtype=np.uint8)


def sample2midi(sample, filename):
	file = mido.MidiFile(type=0)
	file.ticks_per_beat = PPQ
	track = mido.MidiTrack()
	file.tracks.append(track)

	time = 0
	last_time = 0
	step = int(mido.second2tick(TIME_STEP, PPQ, TEMPO))
	prev = [LOWER_NOTE]

	for timestep in sample:
		notes = np.nonzero(timestep)[0]
		if len(notes):
			delta = time - last_time
			off = prev[0] + LOWER_NOTE
			track.append(mido.Message('note_off', note=off, velocity=64, time=delta))
			if len(prev) > 1:
				for off in prev[1:]:
					note_off = off + LOWER_NOTE
					track.append(mido.Message('note_off', note=note_off, velocity=64, time=0))
			for note in notes:
				midi_note = note + LOWER_NOTE
				track.append(mido.Message('note_on', note=midi_note, velocity=64, time=0))
			last_time = time
			prev = notes
		time += step

	file.save(filename)


if __name__ == '__main__':
	for i, file in enumerate(listdir(MIDI_FOLDER)):
		sample = midi2sample(file)
		np.save(path.join(SAMPLES_FOLDER, str(i+1)), sample)