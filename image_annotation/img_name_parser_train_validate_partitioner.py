import os
import shutil
import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-f', '--folder_path', type=str,
                    help='path to folder of annotated images with corresponding .xml file')
parser.add_argument('-v', '--num_validation', type=str,
                    help='the number from images for validation set')
parser.add_argument('-p', '--prefix_name', type=str,
                    help='the new name of the file')

args = parser.parse_args()

path_to_folder = args.folder_path
folder = os.listdir(path_to_folder)

'''
Normal:
S1: 0 - [56 - 69]
S2-CFF: 70 - [131 - 145]
S2-OFF: 146 - [206 - 220]
S3-CFF: 221 - [286 - 300]
S3-OFF: 301 - [362 - 375]
S4.1-MFF: 376 - [437 - 450]
S4.2-MFF: 451 - [512 - 525]
S5-CFF: 526 - [555 - 560]
S5-OFF: 561 - [590 - 595]
'''

'''
Augmented:
S1: [1 - 14] - 69
S2-CFF: [70 - 85] - 145
S2-OFF: [146 - 201] - 220
S3-CFF: [221 - 236] - 300
S3-OFF: [301 - 315] - 375
S4.1-MFF: [376 - 390] - 450
S4.2-MFF: [451 - 505] - 525
S5-CFF: [526 - 532] - 560
S5-OFF: [561 - 567] - 595
'''

# Partition into directories

# 1. Establish final image directory
google_colab_file_path = "/content/drive/MyDrive/Training_Session/"


# 2. Partition train and validate
val = args.num_validation
train = len(folder) - val

# 3. Rename files and place in corresponding directories
xml_files = []
img_files = []

for f in folder:
    if f[-4:] == ".xml":
        xml_files.append(f)
    else:
        img_files.append(f)

# Iterate through files
i = 0
folder_text = "train"
prefix = args.prefix_name
counter = 0
for xml in xml_files:
    counter = counter + 1
    if  counter > train:
        folder_text = "validate"

    for img in img_files:
        if xml[:-4] == img[:-4]:
            # Change img name
            new_img_name = prefix + "_" + str(counter) + ".jpg"
            new_img_path_name = path_to_folder + new_img_name
            os.rename(path_to_folder + img, new_img_path_name)
            print(new_img_path_name)
            print(img)

            # Change xml file name
            new_xml_path_name = path_to_folder + "_" + str(counter) + ".xml"
            os.rename(path_to_folder + xml, new_xml_path_name)
            print(new_xml_path_name)
            print(xml)

            # Modify xml file
            tree = ET.parse(new_xml_path_name)
            root = tree.getroot()
            folder = root.find("folder").text = folder_text
            filename = root.find("filename").text = new_img_name
            path = root.find("path").text = google_collab_file_path + folder_text
            tree.write(new_xml_path_name)