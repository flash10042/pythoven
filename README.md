# Pythoven

Different musical stuff with help of Python.

## Note Player (related file note_player.py)

It's a simple script that can take list of notes in format {note}{octave}_{duration} and play it or save to wav file. It's kinda boring and bad coded, but I don't have heart to delete it.

## Virtual Piano (related files piano.py, Unravel.notes and misc folder)

Program that allows you to play on a synth with help of your keybord. Also you can write a text file with ".notes" extension and with command

```
python piano.py --notes EXAMPLE.notes
```

launch your virtual piano with on-screen hints which key to press. 

In repository you can find little example of .notes file - Unravel.notes

## "Pythoven" Song Generator

A neural net trained on classical music to generate a new music.

Initially all training data was in midi format, so I wrote script parse_midi.py to convert .mid file to numpy array and vice versa.

Script train.py creates and trains autoencoder, then saves trained model to model.h5

Script generate.py takes decoder part of autoencoder and uses it to generate new music.

P.S. I tried to underfit the model, so it shouldn't generate just fully memorizied songs.

P.P.S. Maybe I'll try to train a GAN for this task and then create a new repository with neural nets only.
