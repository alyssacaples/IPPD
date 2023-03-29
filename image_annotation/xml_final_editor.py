import ast
import os
import sys
import xml.etree.ElementTree as ET

for child in root:
    print(child)


path = "/content/drive/MyDrive/Training_Session/train"
folder = "train"
filename = "1_.jpg"
# for xml in xml_files:
#     filename = xml[-4:] + ".jpg"
#     counter = counter + 1
#     if counter > 55:
#         google_collab_file_path = "/content/drive/MyDrive/Training_Session/validate"
#         folder = "validate"

# ET.SubElement(root, "folder").set = folder
# ET.SubElement(root, "filename").set = filename
# ET.SubElement(root, "path").set = path



# new_root = ET.Element("annotation")
# ET.SubElement(new_root, "folder").text = folder
# ET.SubElement(new_root, "filename").text = filename
# ET.SubElement(new_root, "path").text = path
# ET.SubElement(new_root, "source").set = ET.SubElement(root, "size")
# ET.SubElement(new_root, "size").set = ET.SubElement(root, "size")
# ET.SubElement(new_root, "segmented").set = ET.SubElement(root, "segmented")


old_tree = ET.parse("C:\\Users\\seba1\\Downloads\\1.xml")
old_root = old_tree.getroot()

image_folder_name = "train"
google_collab_file_path = "/content/drive/MyDrive/Training_Session/train"

for child in old_root.iter("annotation"):
    print(child.attrib["name"])

    counter = counter + 1
    # if counter > :
    #     google_collab_file_path = "/content/drive/MyDrive/Training_Session/train"
    #     image_folder_name = "train"
    
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
    path.text = google_collab_file_path #saved_path + filename_title

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
    # if cnt > 1:
    #     break
print("total picture count: ", cnt)

tree = ET.ElementTree(new_root)
output_xml_name = "C:\\Users\\seba1\\Downloads\\1_.xml"
ET.indent(tree, "    ")
tree.write(output_xml_name, encoding="utf-8", xml_declaration=False)