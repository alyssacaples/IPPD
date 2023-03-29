import os
import shutil

path_to_folder = "C:\\Users\\seba1\\Downloads\\Augmented_Training_Set\\Augmented-5-OFF\\"
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

# 1. Create directories
# train_dir = os.path.join(path_to_img, "train")
# os.mkdir(train_dir)
# val_dir = os.path.join(path_to_img, "validate")
# os.mkdir(val_dir)


# 2. Partition train and validate
val = int(len(folder)*.2) - 1
train = len(folder) - val

# 3. Rename files and place in corresponding directories
xml_files = []
img_files = []

for f in folder:
    if f[-4:] == ".xml":
        xml_files.append(f)
    else:
        img_files.append(f)

name_counter = 560
i = 0
for xml in xml_files:
    name_counter = name_counter + 1
    i = i + 1
    for img in img_files:
        if xml[:-4] == img[:-4]:

            # Change img name
            new_img_name = path_to_folder + "a_" + str(name_counter) + ".jpg"
            os.rename(path_to_folder + img, new_img_name)
            print(new_img_name)
            print(img)

            # Change xml name
            new_xml_name = path_to_folder + "a_" + str(name_counter) + ".xml"
            os.rename(path_to_folder + xml, new_xml_name)
            print(new_xml_name)
            print(xml)


    # if i <= train:
    #     shutil.move(new_img_name, train_dir)
    # else:
    #     shutil.move(new_img_name, val_dir)

    # if i <= val:
    #     shutil.move(new_img_name, val_dir)
    # else:
    #     shutil.move(new_img_name, train_dir)
    