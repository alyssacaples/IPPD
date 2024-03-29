import xml.etree.ElementTree as ET
import ast
import os
import sys

# All images should be inside the image folder
xml_parse = "XML_Input\\Augmented-5-OFF.xml" # this should later be based on image folder name # CHANGE THIS TO YOUR OUTPUT XML 

# Folder names
image_folder_name = "validate"
xml_output_folder = "Augmented-5-OFF_OutputXMLs" 
label_dictionary = {
    "caribbean": "Caribbean Fruit Fly",
    "medfly": "Mediterranean Fruit Fly",
    "oriental": "Oriental Fruit Fly",
}
print(xml_output_folder)
saved_path = os.getcwd() + "\\" + image_folder_name + "\\"

old_tree = ET.parse(xml_parse)
old_root = old_tree.getroot()

if not os.path.exists("XML_Output"):
    os.mkdir("XML_Output")

os.chdir("XML_Output") # where all xml files should go
if not os.path.exists(xml_output_folder):
    os.mkdir(xml_output_folder)

# Change all xml files
os.chdir(xml_output_folder)
cnt = 0

for child in old_root.iter("image"):
    print(child.attrib["name"])

    xml_encoding = '<?xml version="1.0" encoding="utf-8"?>'

    filename_title = str(child.attrib["name"])

    # make a new file based on image name
    root = ET.Element("annotation")
    folder = ET.SubElement(root, "folder")
    folder.text = image_folder_name 
    filename = ET.SubElement(root, "filename")
    filename.text = filename_title
    path = ET.SubElement(root, "path")
    path.text = saved_path + filename_title #google_collab_file_path #saved_path + filename_title

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

        #print(google_collab_file_path)

        # unnecessary values
        pose = ET.SubElement(object, "pose")
        pose.text = "Unspecified"
        truncated = ET.SubElement(object, "truncated")
        truncated.text = "0"
        difficult = ET.SubElement(object, "difficult")
        difficult.text = "0"

        # bounding box for each value
        bndbox = ET.SubElement(object, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = str(round(float(box.get("xtl"))))
        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = str(round(float(box.get("ytl"))))
        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text =  str(round(float(box.get("xbr"))))
        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = str(round(float(box.get("ybr"))))

        box_cnt = box_cnt + 1
        
    print(filename_title, "total box count: ", box_cnt)
    tree = ET.ElementTree(root)
    output_xml_name = filename_title[:-4] + ".xml"
    ET.indent(tree, "    ")
    tree.write(output_xml_name, encoding="utf-8", xml_declaration=False)

    cnt = cnt + 1
    if cnt > 1:
        break
print("total picture count: ", cnt)