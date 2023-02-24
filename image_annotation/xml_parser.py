import xml.etree.ElementTree as ET
import numpy as np
import cv2
import matplotlib.pyplot as plt
import ast

# change file names here
base = "3_4_6"
xml_parse = "annotations" + base + ".xml"
img_filename = "Snap_Speed" + base + ".jpg"
output_filename = "annotated" + base + ".jpg"

tree = ET.parse(xml_parse)
root = tree.getroot()

def parse_line(line):
    individ = line.split(';')
    xy = []
    for each in individ:
        xy.append(np.array(each.split(','), dtype=np.float32))

    return np.array(xy)


def contour_identifier(image, output_img, output_color, lower, upper):
    #image = cv2.imread(img)
    lower = np.array(lower, dtype= "uint8")
    upper = np.array(upper, dtype= "uint8")
    
    mask = cv2.inRange(image, lower, upper)

    points = []
    height, width = mask.shape
    for x in range(height):
        for y in range(width):
            if(mask[x][y] == 255):
                points.append((y, x))

    points = np.array(points, dtype=object)

    for shape in points:
        #print(shape)
        shape = shape.reshape(-1,1,2)
        cv2.fillPoly(output_img, np.int32([shape]), color=(0, 255, 0))
    
    return output_img

f1_label = []
f2_label = []
f3_label = []
f4_label = []

for child in root.iter('polyline'):
    child_points = parse_line(child.attrib['points']) # this is a string
    
    if(child.attrib['label'] == 'f1'):
        f1_label.append(child_points)
        #print("f1")
    elif(child.attrib['label'] == 'f2'):
        f2_label.append(child_points)
        #print("f2")
    elif(child.attrib['label'] == 'f3'):
        f3_label.append(child_points)
        #print("f3")
    elif(child.attrib['label'] == 'f4'):
        f4_label.append(child_points)
        #np.concatenate((f4_label, child_points), axis=0)
        #print("f4")

#vect = np.vectorize(np.float)
f1_label = np.array(f1_label, dtype=object)
f2_label = np.array(f2_label, dtype=object)
f3_label = np.array(f3_label, dtype=object)
f4_label = np.array(f4_label, dtype=object)

img = cv2.imread(img_filename)
cpy_img = img.copy()

all_fill = np.array([[0, 0], [0,1200], [1200, 1200], [1200, 0]])
cv2.fillPoly(img,np.int32([all_fill]),color=(255, 0, 0) ) # fill everything w f1 color ebcause it is the background

# for shape in f1_label:

#     cv2.fillPoly(img, np.int32([shape]), color=(255, 0, 0))

for shape in f2_label:
    cv2.fillPoly(img, np.int32([shape]), color=(255, 255, 0))

lower = [155, 155, 155]
upper = [255, 255, 255]

img = contour_identifier(cpy_img, img, (0, 255, 0), lower, upper)

# for shape in f3_label:

#     cv2.fillPoly(img, np.int32([shape]), color=(0, 255, 0)) #white parts

for shape in f4_label:

    cv2.fillPoly(img, np.int32([shape]), color=(255, 0, 255))

cv2.imshow("filled polygon", img)

#wait for the user to press any key to 
#exit window
cv2.waitKey(0)
  
#Closing all open windows
cv2.destroyAllWindows()

cv2.imwrite(output_filename, img)

