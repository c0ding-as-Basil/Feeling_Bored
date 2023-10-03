# Many thanks to Taylor Swift for being a great support through all her
# songs that I was listening to while working on this.

# ~ Basil

import math
from PIL import Image  # this is ONLY used to convert list to image and vice-versa
import os


# Function to read image and transform it into its corresponding 2D array
def image_to_2d_grayscale_array(img_path):
    image = Image.open(img_path)
    image = image.convert('L')  # Convert to grayscale
    width, height = image.size
    pixels = list(image.getdata())

    return [pixels[n * width:(n + 1) * width] for n in range(height)]


# Function to read 2D array of an image and convert it back to an actual image
def array_to_image(img_array):
    # Convert 2D list to 1D
    flat_list = [item for sublist in img_array for item in sublist]
    # Convert 1D list to Image
    image = Image.new('L', (len(img_array[0]), len(img_array)))
    image.putdata(flat_list)
    return image


# Function to perform bilinear interpolation (add other types of interpolations if you wish)
def bilinear_interpolation(x, y, img):
    x1, y1 = int(x), int(y)
    x2, y2 = min(x1 + 1, len(img[0]) - 1), min(y1 + 1, len(img) - 1)

    q11, q12, q21, q22 = img[y1][x1], img[y1][x2], img[y2][x1], img[y2][x2]

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1))


# Function to perform rotation using bilinear interpolation
def rotate_image(img, angle):
    height, width = len(img), len(img[0])
    rad = math.radians(angle)

    sin, cos = math.sin(rad), math.cos(rad)

    # Calculate dimensions of the new image to avoid cropping the sides
    new_width = int(abs(len(img) * sin) + abs(len(img[0]) * cos))
    new_height = int(abs(len(img) * cos) + abs(len(img[0]) * sin))

    new_img = [[0 for _ in range(new_width)] for _ in range(new_height)]
    mid_y = (new_height - 1) / 2
    mid_x = (new_width - 1) / 2

    for y in range(new_height):
        for x in range(new_width):
            old_x = (x - mid_x) * cos + (y - mid_y) * sin + width / 2
            old_y = - (x - mid_x) * sin + (y - mid_y) * cos + height / 2

            if 0 <= old_x < width and 0 <= old_y < height:
                # Just change this line if you wish to use other interpolation technique
                new_img[y][x] = bilinear_interpolation(old_x, old_y, img)

    return new_img


# Function to perform zoom using bilinear interpolation
def zoom_image(img, factor):
    if factor <= 0:
        raise ValueError("Zoom factor should be positive!")

    # Original dimensions
    height, width = len(img), len(img[0])

    # Midpoints which serve as zooming centers
    mid_x, mid_y = width // 2, height // 2

    # Create an empty image with the same dimensions as the original
    zoomed_img = [[0 for _ in range(width)] for _ in range(height)]

    for x in range(width):
        for y in range(height):
            # Offset by the center of the image
            x_offset = (x - mid_x) / factor
            y_offset = (y - mid_y) / factor

            # Map back to original image
            x_ = mid_x + x_offset
            y_ = mid_y + y_offset

            # make sure mapped coordinates are within image bounds
            if 0 <= x_ < width and 0 <= y_ < height:
                # Just change this line if you wish to use other interpolation technique
                zoomed_img[y][x] = bilinear_interpolation(x_, y_, img)

    return zoomed_img


def main():
    # Handle image path input
    validInput = False;
    while (not validInput):
        try:
            # There is a sample image in same directory called "Sample.png" (feel free to test on it)
            img_path = input("Enter the path to the image: ")
            img = image_to_2d_grayscale_array(img_path)
            validInput = True
        except:
            print("==> Failed to load the image. Make sure the path is correct.\n")

    print("==> Loaded Image of Dimensions: ", len(img), "x", len(img[0]), "\n")

    # Handle operation input
    validInput = False
    while(not validInput):
        try:
            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            choice = int(input("Choose operation:\n1. Zoom\n2. Rotate\n==> "))
            if choice == 1:
                factor = float(input("Enter zoom factor:\n==> "))
                result = zoom_image(img, factor)
                validInput = True
            elif choice == 2:
                angle = float(input("Enter rotation angle in degrees:\n==> "))
                result = rotate_image(img, angle)
                validInput = True
            else:
                print("==> Invalid Choice!")
        except:
            print("==> Invalid Input!")

    # convert the resultant array to image
    output_img = array_to_image(result)

    # Create a save path in the same directory as the program
    directory = os.path.dirname(os.path.abspath(__file__))  # get current directory
    save_path = os.path.join(directory, '../LovelyNunu/transformed_image.jpg')

    output_img.save(save_path)
    print("==> Transformed Image saved!")
    print("==> Transformed Image Dimensions:", len(result), "x", len(result[0]))
    # Uncomment the line below if you want to print the list itself of the transformed image
    # print("Transformed Image List:", result)


if __name__ == "__main__":
    main()