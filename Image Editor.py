## Hany Yacoub
import copy

#Red Blue Swap
#==========================================
# Purpose:
#   Swaps the red and blue components in an image
# Input Parameter(s):
#   A 3D matrix (list of lists of lists) representing an .bmp image
#   Each element of the matrix represents one row of pixels in the image
#   Each element of a row represents a single pixel in the image
#   Each pixel is represented by a list of three numbers between 0 and 255
#   in the order [red, green, blue]
# Return Value:
#   A 3D matrix of the same dimensions, with all colors inverted
#   (that is, for every pixel list, the first and last values have been
#   swapped.
#==========================================
def red_blue_swap(img_matrix):
    for i in img_matrix:
        for j in i:
                j[0], j[-1] = j[-1], j[0]
    return img_matrix

#Grayscale
#==========================================
# Purpose:
#   Converts an image to grayscale
# Input Parameter(s):
#   A 3D image matrix (see part 1)
# Return Value:
#   A 3D matrix of the same dimensions, where each pixel has all components
#   (red, green, blue) set to a value determined by the formula:
#       0.3*red + 0.59*green + 0.11*blue
#   and then truncated down to the nearest integer.
#==========================================
def grayscale(img_matrix):
    for i in img_matrix:
        for j in i:
            avg = int((j[0]*0.3 + j[1]*0.59 + j[2]*0.11))
            for k in range(len(j)):
                j[k] = avg
    return img_matrix

            
# Split
#==========================================
# Purpose:
#   Splits an image into four copies of itself, each with half the dimensions
#   of the original.  Computes each component of the output image's pixels by
#   taking the corresponding 2x2 square of pixels in the original and averaging
#   that component among those four pixels (truncating this average down to the
#   nearest integer).  See instructions for more details.
# Input Parameter(s):
#   A 3D image matrix. Width and height
#   of the image are both even, so that each 1 pixel in the output image
#   corresponds to one 2x2 square of pixels in the input.
# Return Value:
#   A 3D matrix of the same dimensions, with the transformation described above.
#==========================================

def split(img_matrix):
    new_image = copy.deepcopy(img_matrix)
    height = len(img_matrix)
    width = len(img_matrix[0])
    outputrow = []
    output = []
         
    for i in range(0, height, 2): #loops through each second pixel
        for j in range(0, width, 2):
            r = (new_image[i][j][0] + new_image[i][j+1][0] + new_image[i+1][j][0] + new_image[i+1][j+1][0]) // 4 
            g = (new_image[i][j][1] + new_image[i][j+1][1] + new_image[i+1][j][1] + new_image[i+1][j+1][1]) // 4
            b = (new_image[i][j][2] + new_image[i][j+1][2] + new_image[i+1][j][2] + new_image[i+1][j+1][2]) // 4

            new_pixel = [r,g,b]
            outputrow.append(new_pixel)
        output.append(outputrow) #creates list containing shrunk pixels
        outputrow = [] 
                      
    for k in range(len(output)): #uses shrunk image to place pixels in new positions
        for l in range(len(output[0])):
            img_matrix[k][l], img_matrix[k+height//2][l], img_matrix[k][l+width//2], img_matrix[k+height//2][l+width//2] = output[k][l], output[k][l], output[k][l], output[k][l]
            
    return img_matrix



# Helper functions to load in files.
#==========================================
# Purpose:
#   Compute the integer represented by a sequence of bytes
# Input Parameter(s):
#   A list of bytes (integers between 0 and 255), in big-endian order
# Return Value:
#   Integer value that the bytes represent
#==========================================
def big_end_to_int(ls):
    total = 0
    for ele in ls[::-1]:
        total *= 256
        total += ele
    return total

# .bmp conversion function
#==========================================
# Purpose:
#   Turns a .bmp file into a matrix of pixel values, performs an operation
#   on it, and then converts it back into a new .bmp file
# Input Parameter(s):
#   fname, a string representing a file name in the current directory
#   operation, a string representing the operation to be performed on the
#   image.  This can be one of 3 options: 'invert', 'grayscale',
#   or 'split'.
# Return Value:
#   None
#==========================================
def transform_image(fname,operation):
    #Open file in read bytes mode, get bytes specifying width/height
    fp = open(fname,'rb')
    data = list(fp.read())
    old_data = list(data)
    width = big_end_to_int(data[18:22])
    height = big_end_to_int(data[22:26])

    #Data starts at byte 54.  Create matrix of pixels, where each
    #pixel is a 3 element list [red,green,blue].
    #Starts in lower left corner of image.
    i = 54
    matrix = []
    for y in range(height):
        row = []
        for x in range(width):
            pixel = [data[i+2],data[i+1],data[i]]
            i += 3
            row.append(pixel)
        matrix.append(row)
        #Row size must be divisible by 4, otherwise padding occurs
        i += (2-i)%4
    fp.close()

    #Perform operation on the pixel matrix
    if operation == 'red_blue_swap':
        new_matrix = red_blue_swap(matrix[::-1])
    elif operation == 'grayscale':
        new_matrix = grayscale(matrix[::-1])
    elif operation == 'split':
        new_matrix = split(matrix[::-1])
    else:
        return
    new_matrix = new_matrix[::-1]
    #Write back to new .bmp file.
    #New file name is operation+fname
    i = 54
    for y in range(height):
        for x in range(width):
            pixel = tuple(new_matrix[y][x])
            data[i+2],data[i+1],data[i] = pixel
            i += 3
        i += (2-i)%4
    fp = open(operation+"_"+fname,'wb')
    fp.write(bytearray(data))
    fp.close()

