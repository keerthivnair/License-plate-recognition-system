#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import joblib
from skimage.io import imread
from skimage.filters import threshold_otsu


# In[7]:


letters = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
            'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z'
        ]


# In[12]:


def read_training_data(training_folder):
    image_data = []
    target_data = []

    for letter in letters:
        for each in letter:
            image_path = os.path.join(training_folder, letter, letter + '_' + str(each) + '.jpg')

            image_details = imread(image_path,as_gray=True)

            binary_image = image_details < threshold_otsu(image_details)

            flat_bin_img = binary_image.reshape(-1)

            image_data.append(flat_bin_img)
            target_data.append(letter)
    return np.array(image_data),np.array(target_data) 


def cross_validation(model,num_of_folds,train_data,train_label):

    accuracy_result = cross_val_score(model, train_data, train_label,
                                      cv=num_of_fold)

    print("Cross Validation Result for ", str(num_of_fold), " -fold")

    print(accuracy_result * 100) 

current_dir = os.path.dirname(os.path.realpath(__file__))

training_folder = os.path.join(current_dir,'training_data')

image_data,target_data = read_training_data(training_folder)

svc_model = SVC(kernel='linear', probability=True)

cross_validation(svc_model, 4, image_data, target_data)

svc_model.fit(image_data, target_data)

save_directory = os.path.join(current_dir,'model/svc/')

if not os.path.exists(save_directory):
    os.makedirs(save_directory)
joblib.dump(svc_model, save_directory+'/svc.pkl')    


# In[ ]:




