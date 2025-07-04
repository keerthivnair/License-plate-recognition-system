#!/usr/bin/env python
# coding: utf-8

# In[3]:


import importlib
import localization
importlib.reload(localization)
from skimage import measure
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from skimage.measure import regionprops


# In[4]:


from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import localization

# this gets all the connected regions and groups them together
label_image = measure.label(localization.binary_car_image)

# getting the maximum width, height and minimum width and height that a license plate can be
plate_dimensions = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
min_height, max_height, min_width, max_width = plate_dimensions
plate_objects_cordinates = []
plate_like_objects = []
fig, (ax1) = plt.subplots(1)
ax1.imshow(localization.gray_car_image, cmap="gray");

# regionprops creates a list of properties of all the labelled regions
for region in regionprops(label_image):
    if region.area < 50:
        #if the region is so small then it's likely not a license plate
        continue

    # the bounding box coordinates
    min_row, min_col, max_row, max_col = region.bbox
    region_height = max_row - min_row
    region_width = max_col - min_col
    # ensuring that the region identified satisfies the condition of a typical license plate
    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        plate_like_objects.append(localization.binary_car_image[min_row:max_row,
                                  min_col:max_col])
        plate_objects_cordinates.append((min_row, min_col,
                                              max_row, max_col))
        rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False)
        ax1.add_patch(rectBorder)
    # let's draw a red rectangle over those regions

plt.show()


# In[5]:


from skimage.measure import label, regionprops
from skimage.morphology import closing, square
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Label the binary image
label_image = measure.label(localization.binary_car_image)

# License plate size heuristics
min_height, max_height = 0.063* label_image.shape[0], 0.2 * label_image.shape[0]
min_width, max_width   = 0.13 * label_image.shape[1], 0.35 * label_image.shape[1]

plate_objects_coordinates = []
plate_like_objects = []

fig, ax1 = plt.subplots(1)
ax1.imshow(localization.binary_car_image, cmap="gray")

for region in regionprops(label_image):
    if region.area < 50:
        continue

    min_row, min_col, max_row, max_col = region.bbox
    region_height = max_row - min_row
    region_width = max_col - min_col

    # Normal case: region resembles plate
    if (min_height <= region_height <= max_height and
        min_width <= region_width <= max_width and
        region_width > region_height):

        plate_like_objects.append(localization.binary_car_image[min_row:max_row, min_col:max_col])
        plate_objects_coordinates.append((min_row, min_col, max_row, max_col))

        rectBorder = patches.Rectangle((min_col, min_row), region_width, region_height,
                                       edgecolor="red", linewidth=2, fill=False)
        ax1.add_patch(rectBorder)


    elif region_height >= min_height and region_width >= min_width:

        mini_height = int(max_height - min_height)
        mini_width = int(max_width - min_width)

        lh = min_row
        while lh + mini_height <= max_row:
            lw = min_col
            while lw + mini_width <= max_col:
                plate_like_objects.append(localization.binary_car_image[lh:lh+mini_height, lw:lw+mini_width])
                plate_objects_coordinates.append((lh, lw, lh+mini_height, lw+mini_width))

                rectBorder = patches.Rectangle((lw, lh), mini_width, mini_height,
                                               edgecolor="green", linewidth=1, fill=False)
                ax1.add_patch(rectBorder)

                lw += mini_width
            lh += mini_height

plt.show()


# In[30]:


num_plates = len(plate_like_objects)

# Set number of columns (adjustable)
cols = 4
# Compute rows needed to fit all images
rows = (num_plates + cols - 1) // cols  # same as math.ceil(num_plates / cols)

# Create one big figure with custom size
plt.figure(figsize=(12, 3 * rows))

# Plot each image manually using subplot
for i in range(num_plates):
    plt.subplot(rows, cols, i + 1)  # subplot index starts from 1
    plt.imshow(plate_like_objects[i], cmap='gray')
    plt.title(f"Plate {i}")
    plt.axis('off')

plt.tight_layout()
plt.show()


# In[ ]:




