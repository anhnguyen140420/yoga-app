import cv2
import numpy as np
import math
import function.build_ddnet as ddnet
from keras.models import load_model

C = ddnet.Config()
DD_Net = ddnet.build_DD_Net(C)
DD_Net.summary()
labels = ['Vòng tay', 'Squats','Chéo tay']

sequence = []
sentence = []
predictions = []
threshold = 0.7

def preLoadWeight(self):
    global DD_Net
    DD_Net.load_weights(self.recogdatafile)

def Recognize(sequence):
    global DD_Net, C, labels, sentence, predictions, threshold
    X_test_rt_1, X_test_rt_2 = ddnet.data_generator_rt(sequence, C)
    res = DD_Net.predict([X_test_rt_1, X_test_rt_2])[0]
    #print(labels[np.argmax(res)])
    predictions.append(np.argmax(res))
    if np.unique(predictions[-10:])[0]==np.argmax(res): 
        if res[np.argmax(res)] > threshold: 
            
            if len(sentence) > 0: 
                if labels[np.argmax(res)] != sentence[-1]:
                    sentence.append(labels[np.argmax(res)])
            else:
                sentence.append(labels[np.argmax(res)])

    if len(sentence) > 5: 
        sentence = sentence[-5:]
        
    # img = 255 * np.zeros((480, 480, 3), dtype=np.uint8)
    data = []
    for num, prob in enumerate(res*100):
        prob = round(prob)
        data.append(prob)

    return data