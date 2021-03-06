import numpy as np
# from keras.preprocessing import image
from keras.models import load_model
import itertools
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.io import imread
from skimage.morphology import convex_hull_image


model = load_model('cnn_model2_512.hdf5')

def rm_white_space(img, Image):
    isAddPadding = True
    im1 = 1 - rgb2gray(np.array(img))
    threshold = 0.5
    im1[im1 <= threshold] = 0
    im1[im1 > threshold] = 1
    chull = convex_hull_image(im1)
    imageBox = Image.fromarray((chull*255).astype(np.uint8)).getbbox()
    cropped = Image.fromarray(np.array(img)).crop(imageBox)
    width, height = cropped.size
    if(width>=height):
        isAddPadding = False
    print(isAddPadding)
    return cropped, isAddPadding

def prepare_image(img, show=False):
    img_array_expanded_dims = np.expand_dims(img, axis=0)
    img_copy = img_array_expanded_dims.copy()
    img_copy = img_copy.astype(np.float32)
    img_copy /= 255.
    
    if show:
        plt.imshow(img_copy[0])   
        print(img_copy[0].shape)                        
        plt.axis('off')
        plt.show()

    return img_copy

def predict_class(img):
    preprocessed_image = prepare_image(img)
    y_prob = model.predict(preprocessed_image) 
    print(y_prob)
    y_classes = y_prob.argmax(axis=-1)
    print(y_classes)
    predicted_label = [1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8
                       ,9]
    print(predicted_label[y_classes[0]])
    return predicted_label[y_classes[0]]

def add_white_border(img, Image):
    old_size = img.size
    new_size = (250, 250)
    new_im = Image.new("RGB", new_size, "white")   
    new_im.paste(img, ((new_size[0]-old_size[0])//2,
                        ((new_size[1]-old_size[1])//2)))
    return new_im