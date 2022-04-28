import os

import numpy as np

from autoencoder import VAE


LEARNING_RATE = 0.0005
BATCH_SIZE = 2
EPOCHS = 150

SPECTROGRAMS_PATH = "./clear_numpy/"
SPECTROGRAMS_PATH_MIXED = "./mixed_numpy/"


def load_fsdd(spectrograms_path):
    x_train = []
    for root, _, file_names in os.walk(spectrograms_path):
        for file_name in sorted(file_names, key=lambda x: (x.split("_")[1])): #TODO: copiar esta linea al repo real
            print(file_name)
            file_path = os.path.join(root, file_name)
            spectrogram = np.load(file_path) # (n_bins, n_frames, 1)
            x_train.append(spectrogram)
    x_train = np.array(x_train)
    x_train = x_train[..., np.newaxis] # -> (3000, 256, 64, 1)
    return x_train


def train(x_train,y_train, learning_rate, batch_size, epochs):
    autoencoder = VAE(
        input_shape=(256, 259, 1),
        conv_filters=(512, 256, 128, 64, 32),
        conv_kernels=(3, 3, 3, 3, 3),
        conv_strides=(2, 2, 2, 2, (2, 1)),
        latent_space_dim=128
    )
    autoencoder.summary()
    autoencoder.compile(learning_rate)
    autoencoder.train(x_train,y_train, batch_size, epochs)
    return autoencoder


if __name__ == "__main__":
    y_train = load_fsdd(SPECTROGRAMS_PATH)
    x_train = load_fsdd(SPECTROGRAMS_PATH_MIXED)
    print(x_train.shape)
    #reshape xtrain to (7,256,64,1)
    x_train = x_train[:,:,:259,:]
    y_train = y_train[:,:,:259,:]
    #add padding shape [2,256,259,1] to [2,256,272,1]
    
    print(x_train.shape)
    print(y_train.shape)
    autoencoder = train(x_train,y_train, LEARNING_RATE, BATCH_SIZE, EPOCHS)
    autoencoder.save("model")