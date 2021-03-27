#!/usr/bin/env python
# coding: utf-8

# # <center>0verlay </center>
# Overlay need extra channel alpha 
#  

# Backgroung Image

# In[13]:


import cv2
import imutils
import numpy as np


def overlay_transparent(background_img, img_to_overlay_t, x, y):

    bg_img = background_img.copy()
    
    # Extract the alpha mask of the RGBA image, convert to RGB 
    b,g,r,a = cv2.split(img_to_overlay_t)
    overlay_color = cv2.merge((b,g,r))

    # Apply some simple filtering to remove edge noise
    mask = cv2.medianBlur(a,5)

    h, w, _ = overlay_color.shape
    roi = bg_img[y:y+h, x:x+w]

    # Black-out the area behind the logo in our original ROI
    img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))

    # Mask out the logo from the logo image.
    img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)

    # Update the original image with our new ROI
    bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

    return bg_img


# filled image  (main img, overlayImg, possition(x,y))
def overlay100(l_img, s_img, offset):

    (x_offset,y_offset)= offset

    s_img = cv2.cvtColor(s_img, cv2.COLOR_BGR2BGRA)

    y1, y2 = y_offset, y_offset + s_img.shape[0]
    x1, x2 = x_offset, x_offset + s_img.shape[1]

    alpha_s = s_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                                  alpha_l * l_img[y1:y2, x1:x2, c])
        
    return l_img