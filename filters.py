import math

from PIL import Image
from kernels import *

def get_pixel(image, row, col):
    return image["pixels"][row*image["width"] + col]

def set_pixel(image, row, col, color):
    image["pixels"][row*image["width"] + col] = color

def apply_per_pixel(image, func):
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"],
    }

    for row in range(image["height"]):
        for col in range(image["width"]):
       
            color = get_pixel(image, row, col)
            new_color = func(color)
            set_pixel(result, row, col, new_color)
         
    return result

def inverted(image):
    return apply_per_pixel(image, lambda color: 255-color)

def wrap(image, padded_image, row, col):
    if row == 0 and col == 0 :
        
        return get_pixel(image, image["height"] - 1, image["width"] - 1)
    
    elif (row == 0 and col == padded_image["width"] + 1):
        return get_pixel(image, image["height"] - 1, 0)
        

    elif (row == padded_image["height"] + 1 and col == 0):
        return get_pixel(image, 0, image["width"] - 1)
        
    
    elif (row == padded_image["height"] + 1 and col == padded_image["width"] + 1):
        return get_pixel(image, 0,0)
   
    elif row == 0 :
      
        return get_pixel(image, image["height"] - 1, col -1)
        
    
    elif row == padded_image["height"] + 1:
        return get_pixel(image, 0, col -1)
        
    elif col == 0:
        return get_pixel(image, row - 1, image["width"] - 1)
        
    elif col == padded_image["width"] + 1:
        return get_pixel(image, row - 1, 0)

def extend(image, padded_image, row, col):
    if row == 0 and col == 0 :
        return get_pixel(image, 0,0)
    
    elif (row == 0 and col == padded_image["width"] + 1):
        return get_pixel(image, 0, image["width"] - 1)

    elif (row == padded_image["height"] + 1 and col == 0):
        return get_pixel(image, image["height"] - 1, 0)
    
    elif (row == padded_image["height"] + 1 and col == padded_image["width"] + 1):
        return get_pixel(image, image["height"] - 1, image["width"] - 1)

    elif row == 0 :

        return get_pixel(image, 0, col -1)
    
    elif row == padded_image["height"] + 1:
        return get_pixel(image, image["height"] - 1, col -1)
    
    elif col == 0:
        return get_pixel(image, row - 1, 0)
    
    elif col == padded_image["width"] + 1:
        return get_pixel(image, row - 1, image["width"] - 1)
   
def boundary_behaviour(boundary):
    if boundary == "zero":
        return lambda *args: 0
    elif boundary == "extend":
        return extend
    elif boundary == "wrap":
        return wrap
    return None

def pad_image_num(image,boundary,num = 1):

    func = boundary_behaviour(boundary)
    
    if func == None:
        raise Exception()
    
    def pad_image(image):
        padded_image = {
            "height": image["height"],
            "width": image["width"],
            "pixels": []
        }
        
        for row in range(image["height"] + 2):
            for col in range(image["width"] + 2):
                if (col == 0 or col == padded_image["width"] + 1) or (row == 0 or row == padded_image["height"] + 1) :
                    padded_image["pixels"].append(func(image, padded_image, row, col))
                else:
                    padded_image["pixels"].append(get_pixel(image, row - 1, col - 1))
        
        padded_image["height"] += 2
        padded_image["width"] += 2
        return padded_image
    
    for _ in range(num):
        image = pad_image(image)
        
    return image

def get_target_pixels(image, n):
    target = []
    for row in range(n, image["height"] - n):
        for col in range(n, image["width"] - n):
            target.append((row, col))
    return target

def get_neighboring_pixels(target, n, img):
    neighbors = []
    x,y = target

    for i in range(x - n, x + n + 1):
        for j in range(y - n, y + n + 1): 
            neighbors.append(get_pixel(img,i,j))
  
    return neighbors


def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of "zero", "extend", or "wrap", return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with "height", "width", and "pixels" keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    """
    def multiply(n,m):
        ans = 0
        for i, j in zip(n,m):
            ans += i*j
        return ans

    n = kernel["height"] // 2
    padded_image = pad_image_num(image,boundary_behavior, n)
    targets = get_target_pixels(padded_image, n)

    new_image = {
        "height": padded_image["height"],
        "width": padded_image["width"],
        "pixels": padded_image["pixels"].copy()
    }
    
    
    for target in targets:
    
        neighbors = get_neighboring_pixels(target, n, padded_image)
        new_color = multiply(kernel["pixels"], neighbors)
        set_pixel(new_image, *target, new_color)
  
    return remove_layers(new_image, n)


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    for row in range(image["height"]):
        for col in range(image["width"]):
            current = get_pixel(image,row,col)
            if current < 0:
                set_pixel(image, row,col,0)
            elif current > 255:
                set_pixel(image, row, col, 255)
            else:
                set_pixel(image, row, col, int(current))

def average_img(image):
    kernel = average
    result = {"height":image["height"],
              "width":image["width"],
              "pixels":image["pixels"]}
    for i in range(10):
        result =correlate(result, kernel, "wrap")
        save_greyscale_image(result,f"{i}.png")

    return result

def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    def box_blur(n):
        return {
            "height":n,
            "width":n,
            "pixels": [ 1 / math.pow(n,2) for _ in range(int(math.pow(n,2)))]
        }
    kernel = box_blur(kernel_size)

    result = {"height":image["height"],
              "width":image["width"],
              "pixels":image["pixels"]}
    
    result = correlate(result, kernel, "wrap")

    round_and_clip_image(result)

    return result

def sharpen(image, kernel_size):
    result = {"height":image["height"],
              "width":image["width"],
              "pixels":[]}
    
    blurred_image = blurred(image, kernel_size)
    for image_pixel, blurred_pixel in zip(image["pixels"],blurred_image["pixels"]):
        new_color = 2*image_pixel - blurred_pixel
        result["pixels"].append(new_color)
    
    return result

def test(image,size):
    for i in range(5):
        blurred_img = blurred(image, size)
        sharpened_img = sharpen(image,size)
        #save_greyscale_image(blurred_img, f"blurred{i+1}.png")
        save_greyscale_image(sharpened_img, f"sharpened{i+1}.png")
def remove_layers(image, n):
    result = {"height":image["height"],
              "width":image["width"],
              "pixels":image["pixels"]}
    
    def remove_layer(image):
        rows = image["height"] - 2
        cols = image["width"] - 2
        resized_img = {
            "height": rows,
            "width":cols,
            "pixels":[]
        }
        for row in range(1,rows+1):
            for col in range(1, cols +1):
                resized_img["pixels"].append(get_pixel(image,row,col))
        
        return resized_img
    
    for i in range(n):
        result = remove_layer(result)
    
    return result


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
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
    by the "mode" parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()

def main():
    path = "test_images/"

    img = load_greyscale_image(path+"pattern.png")

    test(img,3)
    #save_greyscale_image(inverted_img, "x.png")

if __name__ == "__main__":
    main()

