from PIL import Image
import os

# all images in folder are in the gitignore

session_folder = "Session #1"
targeted_folder = ""
og_folder_dir = "fly_training_images/original_data/" + session_folder + "/" + targeted_folder

new_session_folder_dir = "fly_training_images/augmented_data/flip_top_bottom/" + session_folder 
new_targeted_folder_dir = new_session_folder_dir + "/" + targeted_folder
# Load the image
#mg = Image.open("augmented_data/acrylic fly comparison.png")

if not os.path.exists(new_session_folder_dir):
    os.mkdir(new_session_folder_dir)

if not os.path.exists(new_targeted_folder_dir):
    os.mkdir(new_targeted_folder_dir)

cnt = 0
for images in os.listdir(og_folder_dir):
    if images.endswith(".jpg"):
        print(images)
        
        img_path = og_folder_dir + "/" + images
        img = Image.open(img_path)
        
        flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
        flipped_img.save(new_targeted_folder_dir + "/" + images)
        
        
    

# # Flip the image vertically
# flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)

# # Save the flipped image
# flipped_img.save("flipped_image.png")



