# This script generates a PDF with images from a relative folder ('./images') arranged on A4 pages.
# Each page holds up to 9 images (3x3 grid) with exact dimensions (63mm x 88mm), thin white gaps (0.5mm) between cards as cutting guidelines, and crop marks at corners.
# It supports common image formats: .png, .jpg, .jpeg, .gif, .bmp, .tiff.
# To use: Place your images in a folder named 'images' in the same directory as this script.
# The script will print the list of loaded images to the console for verification.
# New: Interactive Y/N prompt to specify multiple copies of images (e.g., for lands or tokens).
# New: Prompt at the beginning to enter the output PDF file name.
# Requirements: pip install reportlab pillow

import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def load_images_from_folder(folder_path):
    """
    Load all supported image files from the given folder into a dictionary (filename: image) and print them for verification.
    """
    supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    image_dict = {}
    print(f"Scanning folder: {os.path.abspath(folder_path)}")
    for file_name in sorted(os.listdir(folder_path)):  # Sorted for consistent order
        if file_name.lower().endswith(supported_extensions):
            full_path = os.path.join(folder_path, file_name)
            try:
                img = Image.open(full_path)
                image_dict[file_name] = img
                print(f"Loaded: {file_name}")
            except Exception as e:
                print(f"Failed to load '{file_name}': {e}")
    if not image_dict:
        print("No images loaded.")
    return image_dict

def get_user_multiples(image_dict):
    """
    Interactive prompt to specify multiple copies of images.
    Returns a list of images with duplicates based on user input.
    """
    images_list = list(image_dict.values())  # Start with one copy of each

    while True:
        response = input("Do you want to specify multiple copies for any images (e.g., lands or tokens)? (Y/N): ").strip().upper()
        if response == 'N':
            break
        elif response != 'Y':
            print("Invalid input. Please enter Y or N.")
            continue

        while True:
            file_name = input("Enter the image file name (e.g., 'forest.png'): ").strip()
            if file_name not in image_dict:
                print(f"File '{file_name}' not found in the images folder. Try again.")
                continue

            try:
                quantity = int(input(f"How many copies of '{file_name}' do you want in total? (Enter a number >=1): ").strip())
                if quantity < 1:
                    raise ValueError
            except ValueError:
                print("Invalid quantity. Must be an integer >=1.")
                continue

            # Add (quantity - 1) additional copies (since one is already in the list)
            img = image_dict[file_name]
            images_list.extend([img] * (quantity - 1))
            print(f"Added {quantity - 1} extra copies of '{file_name}'.")

            another = input("Add multiples for another image? (Y/N): ").strip().upper()
            if another != 'Y':
                break

    return images_list

def main():
    # Prompt for output PDF file name at the beginning
    output_file = input("Enter the name for the output PDF file (e.g., my_proxies.pdf): ").strip()
    if not output_file:
        output_file = "proxies_with_thin_gaps_and_cropmarks.pdf"  # Default if empty
    if not output_file.lower().endswith('.pdf'):
        output_file += '.pdf'  # Ensure it ends with .pdf

    # Relative folder path (folder named 'images' in the same directory as this script)
    folder_path = "./images"

    # Load images from folder into a dict (will print the list to console)
    image_dict = load_images_from_folder(folder_path)

    if not image_dict:
        print("No valid images found in the folder. Exiting.")
        return

    # Get user input for multiples and build the final list
    images = get_user_multiples(image_dict)

    # PDF setup
    card_width = 63 * mm
    card_height = 88 * mm
    a4_width = 210 * mm
    a4_height = 297 * mm
    num_cols = 3
    num_rows = 3
    gap_x = 0.5 * mm  # Thin white gap between columns (guideline for cutting)
    gap_y = 0.5 * mm  # Thin white gap between rows (guideline for cutting)
    crop_length = 5 * mm  # Length of crop marks

    # Calculate total used dimensions and margins
    total_width = num_cols * card_width + (num_cols - 1) * gap_x
    total_height = num_rows * card_height + (num_rows - 1) * gap_y
    margin_x = (a4_width - total_width) / 2
    margin_y = (a4_height - total_height) / 2

    c = canvas.Canvas(output_file, pagesize=(a4_width, a4_height))

    for idx, img in enumerate(images):
        if idx > 0 and idx % (num_cols * num_rows) == 0:
            c.showPage()

        pos = idx % (num_cols * num_rows)
        col = pos % num_cols
        row = pos // num_cols

        x = margin_x + col * (card_width + gap_x)
        y = a4_height - margin_y - (row + 1) * card_height - row * gap_y  # y from bottom, adjusted for gaps

        # Draw crop marks (thin solid black lines at corners for outer guidance)
        c.setLineWidth(0.2)  # Thin line for guidance
        
        # Bottom-left corner
        c.line(x - crop_length, y, x, y)  # Horizontal
        c.line(x, y - crop_length, x, y)  # Vertical
        
        # Bottom-right corner
        c.line(x + card_width, y, x + card_width + crop_length, y)  # Horizontal
        c.line(x + card_width, y - crop_length, x + card_width, y)  # Vertical
        
        # Top-left corner
        c.line(x - crop_length, y + card_height, x, y + card_height)  # Horizontal
        c.line(x, y + card_height, x, y + card_height + crop_length)  # Vertical
        
        # Top-right corner
        c.line(x + card_width, y + card_height, x + card_width + crop_length, y + card_height)  # Horizontal
        c.line(x + card_width, y + card_height, x + card_width, y + card_height + crop_length)  # Vertical

        # Draw image (after crop marks)
        c.drawInlineImage(img, x, y, width=card_width, height=card_height)

    c.save()
    print(f"PDF generated: {output_file}")

if __name__ == "__main__":
    main()