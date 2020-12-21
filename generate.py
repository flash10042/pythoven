import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from parse_midi import sample2midi

THRESHOLD = 0.5
OUTPUT_NAME = 'generated.mid'

weights = np.load('distrs.npy')
autoencoder = load_model('composer.h5')
decoder = autoencoder.get_layer('decoder')

# TUNE THIS ARRAY TO CHANGE OUTPUT
data = np.random.normal(size=200)

sample = decoder.predict(np.expand_dims(data*weights[1]+weights[0], 0))
sample = (sample > THRESHOLD).astype(np.uint8)

sample2midi(sample.reshape(-1, sample.shape[-1]), OUTPUT_NAME)

print(f"Number of generated notes - {np.count_nonzero(sample)}")
