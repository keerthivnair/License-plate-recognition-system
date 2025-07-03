#!/usr/bin/env python
# coding: utf-8

# In[1]:


from skimage.filters import threshold_otsu
from skimage.io import imread
import matplotlib.pyplot as plt


# In[2]:


car_image = imread('./car.jpeg',as_gray=True)
print(car_image.shape)


# In[13]:


# Convert to [0, 255] and uint8 for easier interpretation
gray_car_image = (car_image * 255).astype("uint8")

# Apply Otsu's threshold
threshold_value = threshold_otsu(gray_car_image)
binary_car_image = (gray_car_image > threshold_value).astype("uint8") * 255

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(gray_car_image, cmap="gray")
ax1.set_title("Grayscale")
ax1.axis("off")

ax2.imshow(binary_car_image, cmap="gray")
ax2.set_title("Otsu Binary")
ax2.axis("off")

plt.show()


# In[ ]:




