import cv2
import numpy as np
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog
import subprocess
import os

# Constants
IMAGE_SIZE = (100, 100)
ASCII_FILE_NAME = "ascii_art.txt"

def resize_image(image, size):
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)

def calculate_brightness(image):
    return np.mean(image, axis=2, dtype=int)

def assign_ascii_values(brightness_values, ascii_vals_brightness):
    return [
        [ascii_vals_brightness[(low, high)] for val in row for low, high in ascii_vals_brightness.keys() if
         val >= low and val <= high]
        for row in brightness_values
    ]

def generate_ascii(image_path):
    # Read the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error reading the image file: {image_path}")
        return

    # Resize the image
    image = resize_image(image, IMAGE_SIZE)

    # Calculate brightness values
    brightness_values = calculate_brightness(image)

    # ASCII characters
    ascii_vals = [' ', '`','^','"',',',':',';','I','l','!','i','~','+','_','-','?',']',
            '[','}','{','1',')','(','|','/','t','f','j','r','x','n','u','v','c','z',
            'X','Y','U','J','C','L','Q','0','O','Z','m','w','q','p','d','b','k','h',
            'a','o','*','#','M','W','&','8','%','B','@','$']

    ascii_vals_brightness = {}
    val = 0
    increment = 255 // len(ascii_vals)

    for x in ascii_vals:
        ascii_vals_brightness[(val, val + increment)] = x
        val += increment + 1

    # Assign ASCII values to the image
    ascii_image = assign_ascii_values(brightness_values, ascii_vals_brightness)

    # Determine the line ending based on the operating system
    if os.name == 'posix':  # Unix-like systems (Linux, macOS)
        line_ending = '\n'
    elif os.name == 'nt':   # Windows
        line_ending = '\r\n'
    else:
        line_ending = '\n'   # Default to '\n' for other systems

    # Convert ASCII art to a string with platform-specific line endings
    ascii_str = line_ending.join(["".join(row) for row in ascii_image])

    # Save ASCII art to a text file with newline='' to handle universal newline support
    with open(ASCII_FILE_NAME, "w", newline='') as file:
        file.write(ascii_str)

    # Open the command prompt and print the ASCII art
    cmd_command = f"cmd /c notepad {ASCII_FILE_NAME}"
    subprocess.run(cmd_command, shell=True)

    # Clean up: Optionally delete the temporary file
    os.remove(ASCII_FILE_NAME)

def on_drop(event):
    # Extract the file path from the dropped event data
    file_path = event.data.strip('{}')
    
    # Generate ASCII art only if the file path is not empty
    if file_path:
        generate_ascii(file_path)

def ask_for_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_path:
        generate_ascii(file_path)

# Create the main application window
root = TkinterDnD.Tk()

# Set up the window properties
root.title("ASCII Art Generator")
root.geometry("400x200")

# Allow the root window to accept drops
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Create a label for dropping files (optional)
label = tk.Label(root, text="Drop an image file or click to choose", font=("Helvetica", 14))
label.pack(pady=50)

# Alternatively, you can use a button to open a file dialog
button = tk.Button(root, text="Choose Image", command=ask_for_file)
button.pack()

# Start the Tkinter event loop
root.mainloop()