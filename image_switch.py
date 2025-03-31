import os

image_folder = r"C:\Users\rosie\OneDrive\Pictures\touchdesigner"
movie_file_in = op('moviefilein2') 
index_storage = op('image_index_storage')

image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

if index_storage is not None and index_storage.numRows == 0:
    index_storage.appendRow(['0']) 

def switch_image():
    movie_file_in = op('moviefilein2') 
    index_storage = op('image_index_storage')

    if movie_file_in is None:
        print("ERROR: 'moviefilein2' TOP not found.")
        return

    if index_storage is None or index_storage.numRows == 0:
        print("ERROR: 'image_index_storage' Table DAT not found or empty.")
        return

    if not image_files:
        print("ERROR: No images found in the folder.")
        return

    current_index = int(index_storage[0, 0].val) if index_storage[0, 0] else 0
    new_index = (current_index + 1) % len(image_files)
    index_storage[0, 0] = str(new_index)
    movie_file_in.par.index = new_index  
    
    print(f"Switched to image index: {new_index} - {image_files[new_index]}")


def monitor_trigger():
    trigger_op = op('image_switch_trigger') 

    if trigger_op is not None:
        if trigger_op[0, 0] == 1: 
            switch_image()  
            trigger_op[0, 0] = 0 
        else:
            print("Waiting for trigger to switch images.")
    else:
        print("Error: Trigger operator not found.")

monitor_trigger()
