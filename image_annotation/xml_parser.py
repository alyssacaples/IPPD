import xml.etree.ElementTree as ET

# import numpy as np
# import cv2
# import matplotlib.pyplot as plt
import ast
import os
import sys

#images must be inside the ippd github repo
#all images should be inside the image folder
image_folder_name = "Session1"  # where the images are located. CHANGE THIS TO YOUR IMAGE FOLDER NAME
xml_parse = "fly_image_set_1.xml" # this should later be based on image folder name # CHANGE THIS TO YOUR OUTPUT XML 

google_collab_file_path = "/content/drive/MyDrive/" + image_folder_name

xml_output_folder = image_folder_name + "_"+ "OutputXMLs" 
label_dictionary = {
    "caribbean": "Caribbean Fruit Fly",
    "med": "Mediterranean Fruit Fly",
    "oriental": "Oriental Fruit Fly",
}

print(xml_output_folder)
os.chdir("image_annotation") # inside the github
saved_path = os.getcwd() + "\\" + image_folder_name + "\\"

old_tree = ET.parse(xml_parse)
old_root = old_tree.getroot()

if not os.path.exists("XML_Output"):
    os.mkdir("XML_Output")

os.chdir("XML_Output") # where all xml files should go
if not os.path.exists(xml_output_folder):
    os.mkdir(xml_output_folder)

# change all xml files

os.chdir(xml_output_folder)
cnt = 0

for child in old_root.iter("image"):
    print(child.attrib["name"])
    xml_encoding = '<?xml version="1.0" encoding="utf-8"?>'

    filename_title = str(child.attrib["name"])
    # print(type(filename))
    # print(filename)

    # make a new file based on image name
    root = ET.Element("annotation")
    folder = ET.SubElement(root, "folder")
    folder.text = image_folder_name #google_collab_file_path #
    filename = ET.SubElement(root, "filename")
    filename.text = filename_title
    path = ET.SubElement(root, "path")
    path.text = google_collab_file_path#saved_path + filename_title

    source = ET.SubElement(root, "source")
    source.text = "Unknown"

    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    height = ET.SubElement(size, "height")
    depth = ET.SubElement(size, "depth")
    width.text = child.attrib["width"]
    height.text = child.attrib["height"]
    depth.text = "3"

    segmented = ET.SubElement(root, "segmented")
    segmented.text = "0"

    box_cnt = 0
    for box in child.findall("box"):
        object = ET.SubElement(root, "object")
        name = ET.SubElement(object, "name")
        name.text = label_dictionary.get(box.get("label"))

        print(google_collab_file_path)

        # unnecessary values
        pose = ET.SubElement(object, "pose")
        pose.text = "Unspecified"
        truncated = ET.SubElement(object, "truncated")
        truncated.text = "0"
        difficult = ET.SubElement(object, "difficult")

        # bounding box for each value
        bndbox = ET.SubElement(object, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = box.get("xtl")
        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = box.get("ytl")
        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text =  box.get("xbr")
        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = box.get("ybr")

        box_cnt = box_cnt + 1
        
    print(filename_title, "total box count: ", box_cnt)
    tree = ET.ElementTree(root)
    output_xml_name = filename_title[:-4] + "_output.xml"
    ET.indent(tree, "    ")
    tree.write(output_xml_name, encoding="utf-8", xml_declaration=True)

    cnt = cnt + 1
    # if cnt > 1:
    #     break
print("total picture count: ", cnt)
