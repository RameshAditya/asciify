from PIL import Image


class asciify:
    def __init__(self,img_path,width=100):
        self.img=img_path
        self.asciified_image=""
        self.ASCII_CHARS = ['@', '#', 'S', '%', '0', '*', '+', ';', ':', ',', ' ']
        self.convert(self.img,int(width))

    '''
    method resize():
        - takes as parameters the image, and the final width
        - resizes the image into the final width while maintaining aspect ratio
    '''
    def _resize(self,image, new_width):
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
    def _grayscalify(self,image):
        return image.convert('L')

    '''
    method modify():
        - replaces every pixel with a character whose intensity is similar
    '''
    def _modify(self,image, buckets=25):
        initial_pixels = list(image.getdata())
        new_pixels = [self.ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
        return ''.join(new_pixels)

    '''
    method imageFetcher():
        - returns image from web annd stores it at path

    '''
    def imageFetcher(self,url):
        import urllib.request
        urllib.request.urlretrieve(url, "asciify.jpg")
        path = "asciify.jpg"
        return path

    '''
    method convert():
        - does all the work by calling all the above functions
    '''
    def convert(self,path, new_width):
        image = None
        if path.startswith('http://') or path.startswith('https://'):
            path=self.imageFetcher(path)
        try:
            image = Image.open(path)
        except Exception:
            print("Unable to find image in",path)
      
            return
    
        image = self._resize(image,new_width)
        image = self._grayscalify(image)

        pixels = self._modify(image)
        len_pixels = len(pixels)

        # Construct the image from the character list
        new_image = [pixels[index:index+new_width] for index in range(0, len_pixels, new_width)]

        self.asciified_image='\n'.join(new_image)
        
    '''
    method img_to_file():
        - saves asciified image to a file takes parameter fileName
    '''
  
    def img_to_file(self,fileName):
        # Note: This text file will be created by default under
        #       the same directory as this python file,
        #       NOT in the directory from where the image is pulled.
        

        f = open(fileName,'w')
        f.write(self.asciified_image)
        f.close()
    
    '''
    method printToConsole()"
        - prints the output on console
    '''

    def printToConsole(self):
        # To print on console
        print(self.asciified_image)
    '''
    method getAsciifiedImage():
        - returns asciified image
    '''

    def getAsciifiedImage(self):
        return self.asciified_image


 
if __name__ == '__main__':
    import sys
    try:
        ob=asciify(sys.argv[1],sys.argv[2])
    except:
        ob=asciify(sys.argv[1])
    ob.printToConsole()
