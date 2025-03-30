import os

image_path = r"C:\Users\rosie\OneDrive\Pictures\touchdesigner\pink.png"  # change this to an actual image

movie_file_in = op('moviefilein1')
movie_file_in.par.file = image_path

null_top = op('null1')
null_top.inputConnectors[0].connect(movie_file_in)

print(f"Image loaded: {image_path}")
