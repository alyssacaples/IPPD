import xml.etree.ElementTree as ET
import numpy as np
import cv2
import matplotlib.pyplot as plt
import ast
import os


os.chdir("image_annotation")

# change file names here
xml_parse = "fly_image_set_1.xml"

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

cnt = 0
for child in root.iter('image'):
    print(child.attrib["name"])
    
    filename_title = str(child.attrib["name"])
    # print(type(filename))
    # print(filename)
    
    # make a new file based on image name
    
    root = ET.Element("annotation")
    folder = ET.SubElement(root, "folder")
    filename = ET.SubElement(root, "filename")
    path = ET.SubElement(root, "path" )
    
    source = ET.SubElement(root, "source")
    size = ET.SubElement(root, "size")
    
    segmented = ET.SubElement(root, "segmented")
    object = ET.SubElement(root, "object")
    
    tree = ET.ElementTree(root)
    output_xml_name = filename_title[:-4] + "_output.xml"
    tree.write(output_xml_name)
    

    cnt = cnt + 1
    if cnt > 0:
        break
    
    
    
    
    #child_points = parse_line(child.attrib['points']) # this is a string
    
    # if(child.attrib['label'] == 'f1'):
    #     f1_label.append(child_points)
    #     #print("f1")
    # elif(child.attrib['label'] == 'f2'):
    #     f2_label.append(child_points)
    #     #print("f2")
    # elif(child.attrib['label'] == 'f3'):
    #     f3_label.append(child_points)
    #     #print("f3")
    # elif(child.attrib['label'] == 'f4'):
    #     f4_label.append(child_points)
    #     #np.concatenate((f4_label, child_points), axis=0)
        #print("f4")

print(cnt)
