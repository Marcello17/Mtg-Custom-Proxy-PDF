# MTG Proxy PDF Generator README

This Python script generates a printable PDF for Magic: The Gathering (MTG) card proxies (or any card-sized images) from images in a local folder. It arranges up to 9 cards per A4 page in a 3x3 grid, adds thin white gaps (1mm) between cards for cutting guidelines, and includes crop marks at the corners for precise trimming. The cards are sized exactly at 63mm x 88mm (standard MTG dimensions).

Features:
- Loads images from a `./images` folder in the same directory as the script.
- Interactive prompts to customize the output PDF name and specify multiple copies of images (e.g., for lands or tokens).
- Supports common image formats: PNG, JPG, JPEG, GIF, BMP, TIFF.
- Automatically handles multi-page PDFs if there are more than 9 images (including duplicates).

## Installation Instructions

1. **Python Requirement**: Ensure you have Python 3 installed (version 3.6+ recommended). You can download it from [python.org](https://www.python.org/downloads/).

2. **Install Dependencies**: Open a terminal or command prompt and run the following command to install the required libraries:
   ```
   pip3 install reportlab pillow
   ```
   - `reportlab`: For generating the PDF.
   - `pillow`: For loading and handling images.

   Note: No additional packages are needed, and you don't need internet access after installation.

## Setup and Usage

1. **Prepare Your Images**:
   - Create a folder named `images` in the same directory as the script file (e.g., if the script is `customPrintProxy.py`, place the `images` folder next to it).
   - Copy your MTG card images (or proxy images) into the `./images` folder. For example:
     - `forest.png` (for a basic land)
     - `soldier_token.jpg` (for a token)
     - Any other card images.
   - The script will scan this folder automatically and list the loaded images when run.

2. **Run the Script**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing the script (e.g., `cd path/to/your/script`).
   - Execute the script:
     ```
     python3 customPrintProxy.py
     ```
   - The script runs interactively, prompting you for inputs (see "Example Prompts" below).
   - After completion, the PDF will be saved in the current directory with the name you specified.

3. **Printing and Cutting**:
   - Print the generated PDF on A4 cardstock (200-300gsm recommended) at 100% scale (no scaling or "fit to page").
   - Use the thin white gaps between cards as guidelines to cut in the center (provides tolerance).
   - Align cuts with crop marks for outer edges to ensure exact 63mm x 88mm sizes.
   - Optional: Use a corner rounder for rounded edges like real MTG cards.

## Example Prompts and Workflow

When you run the script, it will interact with you via the console. Here's an example of what the prompts look like and how to respond:

```
Enter the name for the output PDF file (e.g., my_proxies.pdf): my_deck_proxies.pdf

Scanning folder: /path/to/your/project/images
Loaded: forest.png
Loaded: lightning_bolt.jpg
Loaded: soldier_token.png

Do you want to specify multiple copies for any images (e.g., lands or tokens)? (Y/N): Y

Enter the image file name (e.g., 'forest.png'): forest.png
How many copies of 'forest.png' do you want in total? (Enter a number >=1): 4
Added 3 extra copies of 'forest.png'.

Add multiples for another image? (Y/N): Y

Enter the image file name (e.g., 'forest.png'): soldier_token.png
How many copies of 'soldier_token.png' do you want in total? (Enter a number >=1): 2
Added 1 extra copies of 'soldier_token.png'.

Add multiples for another image? (Y/N): N

PDF generated: my_deck_proxies.pdf
```

- **Notes on Prompts**:
  - PDF Name: If you press Enter without typing, it defaults to `proxies_with_thin_gaps_and_cropmarks.pdf`.
  - Y/N for Multiples: Enter 'Y' to add duplicates; 'N' to skip. You can add multiples for as many images as needed.
  - File Names: Must match exactly (case-sensitive) from the loaded list. If not found, it will prompt to try again.
  - Quantity: Enter a number >=1; it adds extras beyond the original copy.

## Troubleshooting

- **No Images Loaded**: Ensure the `./images` folder exists and contains valid image files. Check console output for errors.
- **Invalid Inputs**: The script validates Y/N, file names, and quantities—follow the prompts.
- **PDF Issues**: If the PDF doesn't generate, check for library installation errors or image corruption.
- **Customization**: Edit the script code for changes like gap size (`gap_x`, `gap_y`), grid layout (`num_cols`, `num_rows`), or crop mark length (`crop_length`).

If you encounter issues or need enhancements, feel free to modify the script or ask for help!

Last Updated: August 15, 2025