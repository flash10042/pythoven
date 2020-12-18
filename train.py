import numpy as np
from os import path, listdir

import tensorflow as tf
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dense, Reshape, TimeDistributed, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import RMSprop

# FOLDER WITH TRAINING DATA
FOLDER = 'samples'

TIME = 10
NOTES = 88
LENGTH = 20

ENCODED_SHAPE = 200
EPOCHS = 2000

MODEL_NAME = 'composer.h5'

# GET TRAINING DATA

x = list()
for file in listdir(FOLDER):
    sample = np.load(path.join(FOLDER, file))
    sample = sample[:-(len(sample)%(TIME*LENGTH))]
    sample = sample.reshape(-1, TIME, NOTES)
    data = list()
    for i in range(LENGTH, sample.shape[0]):
        sliced = sample[i-LENGTH:i]
        data.append(sliced)
    data = np.array(data)
    if data.ndim != 4:
        continue
    x.append(data)
x = np.vstack(x)
del sample
del data

# MODEL

encoder_input = Input((LENGTH, TIME, NOTES))
X = Reshape((LENGTH, -1))(encoder_input)
X = TimeDistributed(Dense(100, activation='relu'))(X)
X = Dropout(0.1)(X)
X = Flatten()(X)
X = Dense(ENCODED_SHAPE)(X)
X = BatchNormalization()(X)

encoder = Model(encoder_input, X, name='encoder')

decoder_input = Input(ENCODED_SHAPE)
X = Dense(100*LENGTH)(decoder_input)
X = Dropout(0.1)(X)
X = Reshape((LENGTH, -1))(X)
X = TimeDistributed(Dense(64*TIME))(X)
X = Dropout(0.1)(X)
X = Reshape((LENGTH, TIME, -1))(X)
decoder_output = TimeDistributed(Dense(88, activation='sigmoid'))(X)

decoder = Model(decoder_input, decoder_output, name='decoder')

autoenc = Input((LENGTH, TIME, NOTES))
encoded = encoder(autoenc)
decoded = decoder(encoded)

autoencoder = Model(autoenc, decoded)
autoencoder.compile(RMSprop(0.001), loss='binary_crossentropy')


# TRAINING

autoencoder.fit(x, x, batch_size=256, epochs=EPOCHS, use_multiprocessing=True)

autoencoder.save(MODEL_NAME)

# FOR DISCOVERING PURPOSE

encoder_preds = encoder.predict(x)
means = encoder_preds.mean(axis=0)
vars = encoder_preds.var(axis=0)
distr = np.vstack((means, vars))
np.save('distrs.npy', distr)
