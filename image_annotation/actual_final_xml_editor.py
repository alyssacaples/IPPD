import os
import shutil

path_to_folder = "C:\\Users\\seba1\\Downloads\\Training_Dataset_Actual\\Session-5-OFF\\"
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
S1: [1 - ] - 69
S2-CFF: [70 - ] - 145
S2-OFF: [146 - ] - 220
S3-CFF: [221 - ] - 300
S3-OFF: [301 - ] - 375
S4.1-MFF: [376 - ] - 450
S4.2-MFF: [451 - ] - 525
S5-CFF: [526 - ] - 560
S5-OFF: [561 - ] - 595
'''

# Partition into directories

# 1. Create directories
# train_dir = os.path.join(path_to_img, "train")
# os.mkdir(train_dir)
# val_dir = os.path.join(path_to_img, "validate")
# os.mkdir(val_dir)


# 2. Partition train and validate
# val = int(len(folder)*.2) - 1
# train = len(folder) - val

# 3. Rename files and place in corresponding directories
xml_files = []
img_files = []

for f in folder:
    if f[-4:] == ".xml":
        xml_files.append(f)
    else:
        img_files.append(f)

counter = 0
google_collab_file_path = "/content/drive/MyDrive/Training_Session/train"
folder = "train"
for xml in xml_files:
    filename = xml[-4:] + ".jpg"
    counter = counter + 1
    if counter > 55:
        google_collab_file_path = "/content/drive/MyDrive/Training_Session/validate"
        folder = "validate"
    


    # if i <= train:
    #     shutil.move(new_img_name, train_dir)
    # else:
    #     shutil.move(new_img_name, val_dir)

    # if i <= val:
    #     shutil.move(new_img_name, val_dir)
    # else:
    #     shutil.move(new_img_name, train_dir)
    