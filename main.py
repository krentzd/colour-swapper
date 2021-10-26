import imageio
import numpy as np
from skimage.color import rgb2hsv, hsv2rgb
import glob
import os
from magicgui import magicgui
from napari.layers import Image
import napari

@magicgui(
    call_button='Apply',
    img={'label': 'Pick an Image'},
    hue_from={'widget_type': 'FloatSlider', 'max': 1},
    hue_range={'widget_type': 'FloatSlider', 'max': 0.2},
    hue_to={'widget_type': 'FloatSlider', 'max': 1},
    # dropdown={"choices": ['first', 'second', 'third']},
)
def swap_colours(img: Image, hue_from, hue_range, hue_to) -> 'napari.types.ImageData':
    img_hsv = rgb2hsv(img.data)
    img_hue = img_hsv[:,:,0]
    # hue_val, hue_range = hue_from
    hue_val = hue_from

    if hue_val > 1 and hue_to > 1:
        hue_val = hue_val / 360
        hue_to = hue_to / 360
        hue_range = hue_range / 360

    hue_upper = hue_val + hue_range
    hue_lower = hue_val - hue_range

    if hue_lower < 0:
        hue_lower = (hue_val - hue_range) % 1
        img_hue[img_hue > hue_lower] = hue_to
        img_hue[img_hue < hue_upper] = hue_to
    elif hue_upper > 1:
        hue_upper = (hue_val + hue_range) % 1
        img_hue[img_hue > hue_lower] = hue_to
        img_hue[img_hue < hue_upper] = hue_to
    else:
        img_hue[np.logical_and(img_hue < hue_upper, img_hue > hue_lower)] = hue_to

    img_hsv[:,:,0] = img_hue

    return hsv2rgb(img_hsv)

viewer = napari.Viewer()
viewer.window.add_dock_widget(swap_colours, area='right')
napari.run()
