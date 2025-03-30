import os

image_folder = r"C:\Users\rosie\OneDrive\Pictures\touchdesigner"

image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

print(f"Looking for images in: {image_folder}")
print(f"Found images: {image_files}")


def switch_image(index):
    movie_file_in = op('moviefilein1')  
    movie_file_in.par.file = image_folder  

    if 0 <= index < len(image_files):
        print(f"Switching to image {index + 1}: {image_files[index]}")
        movie_file_in.par.index = index
    else:
        print("Index out of range.")


def start_image_switching():
    delay = 1.0  
    for i in range(len(image_files)):
        run(f"switch_image({i})", delayFrames=int(i * delay * 60)) 

start_image_switching()