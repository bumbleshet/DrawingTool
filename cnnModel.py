import numpy as np
from keras.preprocessing import image
from keras.models import load_model
import itertools
import matplotlib.pyplot as plt

model = load_model('cnnModel.hdf5')

def prepare_image(img, show=False):
    img_array_expanded_dims = np.expand_dims(img, axis=0)
    img_copy = img_array_expanded_dims.copy()
    img_copy = img_copy.astype(np.float32)
    img_copy /= 255.

    if show:
        plt.imshow(img_array_expanded_dims[0])                           
        plt.axis('off')
        plt.show()

    return img_copy

def predict_class(img):
    preprocessed_image = prepare_image(img, False)
    y_prob = model.predict(preprocessed_image) 
    print(y_prob)
    y_classes = y_prob.argmax(axis=-1)
    print(y_classes)
    predicted_label = ['M1', 'M10', 'M11', 'M12', 'M13', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'
                       ,'M9']
    print(predicted_label[y_classes[0]])
    return predicted_label[y_classes[0]]
