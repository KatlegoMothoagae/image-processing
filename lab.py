"""
6.101 Lab 2:
Image Processing 2
"""

#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image
from filters import * 

# VARIOUS FILTERS

def separate_color_image(image):
    red , green, blue= {}, {}, {}
    
    for color in [red,green, blue]:
        color["height"] = image["height"]
        color["width"] = image["width"]
        color["pixels"] = []

    for pixel in image["pixels"]:
        red["pixels"].append(pixel[0])
        green["pixels"].append(pixel[1])
        blue["pixels"].append(pixel[2])
    
    return red, green, blue

def combine_color_image(red, green, blue):
    color_image = {
        "height": red["height"],
        "width": red["width"],
        "pixels": []
    }
    for red_pixel, green_pixel, blue_pixel in zip(red["pixels"], green["pixels"], blue["pixels"]):
        color_image["pixels"].append((red_pixel, green_pixel, blue_pixel))
    
    return color_image

def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def apply_filter(image):
        red, green, blue = separate_color_image(image)
        red, green, blue = filt(red),filt(green),filt(blue)
        return combine_color_image(red, green, blue)

    return apply_filter
 


def make_blur_filter(kernel_size):
    return lambda image: blurred(image, kernel_size)


def make_sharpen_filter(kernel_size):
    raise lambda image: sharpen(image, kernel_size)

def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def apply_filters(image):
        for filter in filters:
            print(filter)
            image = filter(image)
            print(image)
        print("done")
        return image

    return apply_filters

    
    



# SEAM CARVING

# Main Seam Carving Implementation


def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image. Returns a new image.
    """
    result = result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"]
    }
    # print(f"before: {result}")
    for i in range(20):
        grey = greyscale_image_from_color_image(result)
        # print(f"after {result}")
        energy = compute_energy(grey)
        cem = cumulative_energy_map(energy)
        seam = minimum_energy_seam(cem)
    
        result = image_without_seam(result, seam)
        
        save_color_image(result,f"color_{i}.png")
 
    return result
# Optional Helper Functions for Seam Carving


def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"][::]
    }

    func = lambda r, g, b: round(0.299*r + 0.587*g + 0.114 * b)
    result = apply_per_pixel(result, func)

    return result


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
 
    return edge_detection(grey) 


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    result = result = {
        "height": energy["height"],
        "width": energy["width"],
        "pixels": energy["pixels"]
    }

    for row in range(energy["height"]):
        for col in range(energy["width"]):
            color = get_pixel(energy, row, col)
            if row > 0:
                if col == 0:
                    adj1 = get_pixel(energy, row - 1, col)
                    adj2 = get_pixel(energy, row - 1, col + 1)
              
                    new_color = color + min(adj1, adj2)

                elif col == energy["width"] -1:
                    adj1 = get_pixel(energy, row - 1, col)
                    adj2 = get_pixel(energy, row - 1, col - 1)
           
                    new_color = color + min(adj1, adj2)
                
                else:
                    adj1 = get_pixel(energy, row - 1, col)
                    adj2 = get_pixel(energy, row - 1, col - 1)
                    adj3 = get_pixel(energy, row - 1, col + 1)
                    new_color = color + min(adj1, adj2, adj3)
            else:
                new_color = get_pixel(energy, row, col)
                
            
            set_pixel(result, row, col, new_color)
    print(result)
    return result


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    
    minimum = get_pixel(cem, cem["height"] - 1, 0)
    
    for col in range(cem["width"]):
        if minimum > (get_pixel(cem, cem["height"] - 1, col)):
            minimum = get_pixel(cem, cem["height"] - 1, col)
            pos = col

    path = [(cem["height"] - 1,pos)]

    for row in range(cem["height"] - 1, 0, -1):
        minimum = math.inf

        if pos == 0:
            adj1 = get_pixel(cem, row - 1, pos)
            adj2 = get_pixel(cem, row - 1, pos + 1)
            minimum, pos  = min((adj1, pos),(adj2,pos + 1), key = lambda x: x[0])
       
        elif pos == cem["width"] -1:
            adj1 = get_pixel(cem, row - 1, pos)
            adj2 = get_pixel(cem, row - 1, pos - 1)
            minimum, pos  = min((adj1, pos),(adj2,pos - 1), key = lambda x: x[0])

        else:
            adj1 = get_pixel(cem, row - 1, pos - 1)
            adj2 = get_pixel(cem, row - 1, pos)
            adj3 = get_pixel(cem, row - 1, pos + 1)
            minimum, pos  = min((adj1, pos - 1),(adj2,pos),(adj3,pos + 1), key = lambda x: x[0])
    
        path.append((row - 1, pos))

        #print(n)     
    print(path)
    return path




def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    result = {
        "height": image["height"],
        "width": image["width"] - 1,
        "pixels": []
    }
    for row in range(image["height"]):
        for col in range(image["width"]):
            if (row,col) not in seam:
                print(get_pixel(image,row,col))
                result["pixels"].append(get_pixel(image,row,col))
    
    return result



def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    
    img = load_color_image("test_images/twocats.png")

    result = seam_carving(img,2)
    # img = greyscale_image_from_color_image(img)
    # save_greyscale_image(img, "test_grey.png")
    # energy = compute_energy(result)
    # save_greyscale_image(energy, "test_energy.png")
    # cumulative = cumulative_energy_map(energy)
    # minimum_energy_seam(cumulative)
    # save_greyscale_image(result, "test_cumulative_energy.png")
 
    print("done")


