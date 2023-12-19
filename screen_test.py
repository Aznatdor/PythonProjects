import tkinter as tk
from PIL import ImageGrab, Image
import pytesseract

# Initialize Tkinter
root = tk.Tk()
root.title("Simple Paint")

# Create a canvas to draw on
canvas = tk.Canvas(root, width=500, height=500, bg='white')
canvas.pack()

# Variables to store mouse position
prev_x, prev_y = None, None

# Function to draw lines
def draw(event):
    global prev_x, prev_y
    if prev_x and prev_y:
        canvas.create_line(prev_x, prev_y, event.x, event.y, width=2)
    prev_x, prev_y = event.x, event.y

def clear_previous(event):
    global prev_x, prev_y
    prev_x, prev_y = None, None

# Bind mouse events
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", clear_previous)

# Function to save the canvas content as an image
def save_image():
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).save('drawn_image.png')

# Create a button to save the image
save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack()

# Function to perform OCR on the saved image
def perform_ocr():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    img = Image.open('drawn_image.png')
    text = pytesseract.image_to_string(img)
    print(text)

# Create a button to perform OCR on the saved image
ocr_button = tk.Button(root, text="Perform OCR", command=perform_ocr)
ocr_button.pack()

# Run the Tkinter main loop
root.mainloop()