#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
from skimage.measure import regionprops
from skimage import measure 
import numpy as np
import matplotlib.patches as patches
from skimage.transform import resize
import cca2


# In[11]:


license_plate = np.invert(cca2.plate_like_objects[22])

labelled_plate = measure.label(license_plate)

fig,ax1 = plt.subplots(1)
ax1.imshow(license_plate, cmap="gray")


# In[35]:


character_dimensions = (0.25*license_plate.shape[0], 0.60*license_plate.shape[0], 0.05*license_plate.shape[1], 0.15*license_plate.shape[1])
min_height, max_height, min_width, max_width = character_dimensions


# In[37]:


license_plate = np.invert(cca2.plate_like_objects[22])

labelled_plate = measure.label(license_plate)

fig,ax1 = plt.subplots(1)
ax1.imshow(license_plate, cmap="gray")
characters= []
counters = []
column_list= []

for region in regionprops(labelled_plate):
    y0,x0,y1,x1 = region.bbox
    region_height = y1-y0
    region_width = x1-x0


    if region_height >= min_height and region_height <=max_height and region_width>=min_width and region_width<=max_width:
        roi = license_plate[y0:y1, x0:x1]
        print('region height',region_height)
        print('region width',region_width)

        rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",
                                       linewidth=2, fill=False)
        ax1.add_patch(rect_border)

        resized_char = resize(roi, (20, 20))
        characters.append(resized_char)

        column_list.append(x0)

plt.show()




# In[ ]:




