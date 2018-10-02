import cv2
import time
import utils

from PIL import Image
from asciimatics.screen import Screen

ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
ASCII_CHARS = ASCII_CHARS[::-1]

'''
method resize():
    - takes as parameters the image, and the final width
    - resizes the image into the final width while maintaining aspect ratio
'''
def resize(image, new_width=100):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image
'''
method grayscalify():
    - takes an image as a parameter
    - returns the grayscale version of image
'''
def grayscalify(image):
    return image.convert('L')

'''
method modify():
    - replaces every pixel with a character whose intensity is similar
'''
def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)

'''
method do():
    - does all the work by calling all the above functions
'''
def do(image, new_width=100):
    image = resize(image)
    image = grayscalify(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    # Construct the image from the character list
    new_image = [pixels[index:index+new_width] for index in range(0, len_pixels, new_width)]

    return '\n'.join(new_image)

'''
method runner():
    - takes as parameter the image path and runs the above code
    - handles exceptions as well
    - provides alternative output options
'''
def runner(path):
    image = None
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in",path)
        #print(e)
        return
    image = do(image)

    # To print on console
    print(image)

    # Else, to write into a file
    # Note: This text file will be created by default under
    #       the same directory as this python file,
    #       NOT in the directory from where the image is pulled.
    f = open('img.txt','w')
    f.write(image)
    f.close()

'''
def play():
    - Reads video from VideoCapture object cap
    - And prints on the console screen provided by asciimatics
    - Used asciimatics to overwrite lines at the same place
'''
def play(stdscr, cap, playback_speed=1):
    stdscr.clear()

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / fps
    delay = delay / playback_speed

    retv, frame = cap.read()
    while retv:
        img = Image.fromarray(frame)
        ascii_img_row_wise = do(img).split('\n')
        rows = len(ascii_img_row_wise)
        
        # need to print line by line because print_at does not respect '\n'
        for i in range(0, rows):
            stdscr.print_at(ascii_img_row_wise[i], 0, i)

        stdscr.refresh()
        time.sleep(delay)

        retv, frame = cap.read()

'''
method play_video_wrapper():
    - loads VideoCapture object and checks if video can be read
    - accepts video file path and playback_speed (float)
'''
def play_video_wrapper(path, playback_speed):
    cap = cv2.VideoCapture(path)

    if cap.isOpened():

        Screen.wrapper(play, arguments=(
            cap, playback_speed))

        cap.release()
    else:
        print("Could not read video file.")

'''
method main():
    - reads input from console
    - profit
'''
if __name__ == '__main__':
    import sys
    import urllib.request

    if len(sys.argv) < 3:
        print("Incorrect input format.")
        print("Syntax 1: python asciify.py -i IMAGE_FILE")
        print("Syntax 2: python asciify.py -v VIDEO_FILE")
        print("Syntax 3: python asciify.py -v VIDEO_FILE PLAYBACK_SPEED")
        sys.exit(-1)

    if sys.argv[1] not in ['-i', '-v']:
        print("Invalid switch. Use -i for image and -v for video.")
        sys.exit(-1)
    
    path = utils.resolve(sys.argv[2])
    if sys.argv[1] == '-i':
        runner(path)
    else:
        try:
            playback_speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1
            play_video_wrapper(path, playback_speed)
        except ValueError:
            print("Invalid playback speed:", sys.argv[3])
            sys.exit(-1)
