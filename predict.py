import pandas as pd
import numpy as np
from keras.utils import np_utils
from keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import tensorflow as tf
from sklearn.metrics import accuracy_score

data=pd.read_csv('./DF_푸라닭.csv')

model = load_model('./review_predict.h5')
predict_score = model.predict_classes(data['review'])
pred_1 = list(map(np.argmax, predict_score))

print(pred_1)
