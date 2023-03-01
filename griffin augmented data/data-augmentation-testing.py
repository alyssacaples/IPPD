from PIL import Image

# Load the image
img = Image.open("image.jpg")

# Flip the image vertically
flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)

# Save the flipped image
flipped_img.save("flipped_image.jpg")
