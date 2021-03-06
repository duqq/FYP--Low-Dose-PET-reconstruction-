import numpy as np
import glob
import h5py
from keras.layers import Input, Conv2D, Activation, BatchNormalization, MaxPooling2D, Conv2DTranspose, concatenate, Reshape, Dropout, Add, UpSampling2D
from keras.models import Model, load_model
from keras.utils import np_utils, to_categorical
from keras import callbacks
from keras.optimizers import SGD
from keras.callbacks import LearningRateScheduler
from keras import regularizers
from keras import metrics
import keras.backend as K
from keras.utils import plot_model
from PIL import Image
from keras.utils import plot_model
from keras.preprocessing.image import ImageDataGenerator 
np.random.seed(12345)  # for reproducibility
 
###################################### MODEL DEFINATION START ######################################
## Input data dimensions ##
width = 256
height = 256
inputs = Input(shape=(height,width,6)) 
fracDO = 0.2
kerReg = 0.0
## Stage 1 ##
C1_1        = Conv2D(64, kernel_size=3, strides=1, padding='same')(inputs)
C1_1        = BatchNormalization(center=False, scale=False)(C1_1)
C1_1        = Activation('relu')(C1_1)
C1_2        = Conv2D(64, kernel_size=3, strides=1, padding='same')(C1_1)
C1_2        = BatchNormalization(center=False, scale=False)(C1_2)
C1_2        = Activation('relu')(C1_2)
C1_3        = Conv2D(64, kernel_size=3, strides=1, padding='same')(C1_2)
C1_3        = BatchNormalization(center=False, scale=False)(C1_3)
C1_3        = Activation('relu')(C1_3)
C1_pool     = MaxPooling2D(pool_size=(2, 2), strides=2)(C1_3)
## Stage 2 ##
C2_1        = Conv2D(128, kernel_size=3, strides=1, padding='same')(C1_pool)
C2_1        = BatchNormalization(center=False, scale=False)(C2_1)
C2_1        = Activation('relu')(C2_1)
C2_2        = Conv2D(128, kernel_size=3, strides=1, padding='same')(C2_1)
C2_2        = BatchNormalization(center=False, scale=False)(C2_2)
C2_2        = Activation('relu')(C2_2)
C2_3        = Conv2D(128, kernel_size=3, strides=1, padding='same')(C2_2)
C2_3        = BatchNormalization(center=False, scale=False)(C2_3)
C2_3        = Activation('relu')(C2_3)
C2_pool     = MaxPooling2D(pool_size=(2, 2), strides=2)(C2_3)
## Stage 3 ##
C3_1        = Conv2D(256, kernel_size=3, strides=1, padding='same')(C2_pool)
C3_1        = BatchNormalization(center=False, scale=False)(C3_1)
C3_1        = Activation('relu')(C3_1)
C3_2        = Conv2D(256, kernel_size=3, strides=1, padding='same')(C3_1)
C3_2        = BatchNormalization(center=False, scale=False)(C3_2)
C3_2        = Activation('relu')(C3_2)
C3_3        = Conv2D(256, kernel_size=3, strides=1, padding='same')(C3_2)
C3_3        = BatchNormalization(center=False, scale=False)(C3_3)
C3_3        = Activation('relu')(C3_3)
C3_pool     = MaxPooling2D(pool_size=(2, 2), strides=2)(C3_3)
## Stage 4 ##
C4_1        = Conv2D(512, kernel_size=3, strides=1, padding='same')(C3_pool)
C4_1        = BatchNormalization(center=False, scale=False)(C4_1)
C4_1        = Activation('relu')(C4_1)
C4_2        = Conv2D(512, kernel_size=3, strides=1, padding='same')(C4_1)
C4_2        = BatchNormalization(center=False, scale=False)(C4_2)
C4_2        = Activation('relu')(C4_2)
C4_3        = Conv2D(512, kernel_size=3, strides=1, padding='same')(C4_2)
C4_3        = BatchNormalization(center=False, scale=False)(C4_3)
C4_3        = Activation('relu')(C4_3)
C4_pool     = MaxPooling2D(pool_size=(2, 2), strides=2)(C4_3)
## Stage 5 ##
C5_1        = Conv2D(1024, kernel_size=3, strides=1, padding='same')(C4_pool)
C5_1        = BatchNormalization(center=False, scale=False)(C5_1)
C5_1        = Activation('relu')(C5_1)
C5_2        = Conv2D(1024, kernel_size=3, strides=1, padding='same')(C5_1)
C5_2        = BatchNormalization(center=False, scale=False)(C5_2)
C5_2        = Activation('relu')(C5_2)
C5_3        = Conv2D(1024, kernel_size=3, strides=1, padding='same')(C5_2)
C5_3        = BatchNormalization(center=False, scale=False)(C5_3)
C5_3        = Activation('relu')(C5_3)

## Stage 6 Decoder ##
C4D_UpSamp      = Conv2DTranspose(512, kernel_size=2, strides=2, padding='same')(C5_3)
C4D_Conct       = concatenate([C4D_UpSamp, C4_3], axis=-1)
C4D_1           = Conv2D(512, kernel_size=3, strides=1, padding='same')(C4D_Conct)
C4D_1           = BatchNormalization(center=False, scale=False)(C4D_1)
C4D_1           = Dropout(fracDO)(C4D_1)
C4D_1           = Activation('relu')(C4D_1)
C4D_2           = Conv2D(512, kernel_size=3, strides=1, padding='same')(C4D_1)
C4D_2           = BatchNormalization(center=False, scale=False)(C4D_2)
C4D_2           = Dropout(fracDO)(C4D_2)
C4D_2           = Activation('relu')(C4D_2)

## Stage 7 Decoder ##
C3D_UpSamp      = Conv2DTranspose(256, kernel_size=2, strides=2, padding='same')(C4D_2)
C3D_Conct       = concatenate([C3D_UpSamp, C3_3], axis=-1)
C3D_1           = Conv2D(256, kernel_size=3, strides=1, padding='same')(C3D_Conct)
C3D_1           = BatchNormalization(center=False, scale=False)(C3D_1)
C3D_1           = Dropout(fracDO)(C3D_1)
C3D_1           = Activation('relu')(C3D_1)
C3D_2           = Conv2D(256, kernel_size=3, strides=1, padding='same')(C3D_1)
C3D_2           = BatchNormalization(center=False, scale=False)(C3D_2)
C3D_2           = Dropout(fracDO)(C3D_2)
C3D_2           = Activation('relu')(C3D_2)

## Stage 8 Decoder ##
C2D_UpSamp      = Conv2DTranspose(128, kernel_size=2, strides=2, padding='same')(C3D_2)
C2D_Conct       = concatenate([C2D_UpSamp, C2_3], axis=-1)
C2D_1           = Conv2D(128, kernel_size=3, strides=1, padding='same')(C2D_Conct)
C2D_1           = BatchNormalization(center=False, scale=False)(C2D_1)
C2D_1           = Dropout(fracDO)(C2D_1)
C2D_1           = Activation('relu')(C2D_1)
C2D_2           = Conv2D(128, kernel_size=3, strides=1, padding='same')(C2D_1)
C2D_2           = BatchNormalization(center=False, scale=False)(C2D_2)
C2D_2           = Dropout(fracDO)(C2D_2)
C2D_2           = Activation('relu')(C2D_2)

## Stage 9 Decoder ##
C1D_UpSamp      = Conv2DTranspose(64, kernel_size=2, strides=2, padding='same')(C2D_2)
C1D_Conct       = concatenate([C1D_UpSamp, C1_3], axis=-1)
C1D_1           = Conv2D(64, kernel_size=3, strides=1, padding='same')(C1D_Conct)
C1D_1           = BatchNormalization(center=False, scale=False)(C1D_1)
C1D_1           = Dropout(fracDO)(C1D_1)
C1D_1           = Activation('relu')(C1D_1)
C1D_2           = Conv2D(64, kernel_size=3, strides=1, padding='same')(C1D_1)
C1D_2           = BatchNormalization(center=False, scale=False)(C1D_2)
C1D_2           = Dropout(fracDO)(C1D_2)
C1D_2           = Activation('relu')(C1D_2)

## Stage 9 Decoder ##
C00D_1          = Conv2D(1, kernel_size=1, strides=1, padding='same')(C1D_2)

model           = Model(inputs=inputs, outputs=C00D_1)
###################################### MODEL DEFINATION END ######################################
## Data Generator using file located in pathVal##
def generate_valData(path, batchSize):
    while 1:
        fname = glob.glob(path)
        numFile = len(fname)
        assert(numFile>0), "No files in the folder"
	for n in range(0,numFile):
            fh5 = h5py.File(fname[n],'r')
            data = np.array(fh5["data"])
            SLC = data.shape[0]
	    c = 0
            for nBatch in range(0,SLC-7,2):
                x = np.transpose(data[nBatch:nBatch+batchSize,:,:],(1,2,0))
                x = x[None, :, :,: ]
		x = np.float32(x)
                yield x


    
####### define paths ########
pathVal   = '/home/ajfer6/ab57/anthony-PET/FinalTests/Testing/*.h5'
weightpath  = "/home/ajfer6/ab57/anthony-PET/FinalTests/TestUnetL2GD/model-203.hdf5"


## load weights into new model ##
model.load_weights(weightpath)
print("Loaded model from disk")
X = generate_valData(pathVal, 6)

## model predict ##
print ('Prediction Started')
stepsp = 120
prediction = model.predict_generator(X,steps=stepsp)

## output stored as a h5 file ##
hf = h5py.File('del.h5', 'w')
## dataset name ##
hf.create_dataset('data', data=prediction)
print ('Prediction Completed')



