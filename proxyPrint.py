# This script generates a PDF with Magic: The Gathering card images arranged on A4 pages.
# Each page holds up to 9 cards (3x3 grid) with exact dimensions and gridlines for cutting.
# Requirements: pip install reportlab pillow requests

import argparse
import requests
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def get_card_image(card_name):
    """
    Fetch the PNG image of an MTG card from Scryfall API.
    """
    api_url = f"https://api.scryfall.com/cards/named?fuzzy={card_name.replace(' ', '+')}"
    resp = requests.get(api_url)
    if resp.status_code != 200:
        raise ValueError(f"Failed to fetch card data for '{card_name}'")
    data = resp.json()
    if 'image_uris' in data:
        img_url = data['image_uris']['png']
    else:
        # For double-faced cards, use the front face
        img_url = data['card_faces'][0]['image_uris']['png']
    img_resp = requests.get(img_url)
    if img_resp.status_code != 200:
        raise ValueError(f"Failed to fetch image for '{card_name}'")
    return Image.open(BytesIO(img_resp.content))

def main():
    parser = argparse.ArgumentParser(description="Generate PDF with MTG card images for printing on A4 paper.")
    parser.add_argument('card_names', nargs='+', help="List of MTG card names (e.g., 'Black Lotus' 'Ancestral Recall')")
    parser.add_argument('--output', default='mtg_cards.pdf', help="Output PDF file name (default: mtg_cards.pdf)")
    args = parser.parse_args()

    # Fetch images
    images = []
    for name in args.card_names:
        try:
            img = get_card_image(name)
            images.append(img)
        except ValueError as e:
            print(e)
            continue

    if not images:
        print("No valid cards found. Exiting.")
        return

    # PDF setup
    card_width = 63 * mm
    card_height = 88 * mm
    a4_width = 210 * mm
    a4_height = 297 * mm
    num_cols = 3
    num_rows = 3
    margin_x = (a4_width - num_cols * card_width) / 2
    margin_y = (a4_height - num_rows * card_height) / 2

    c = canvas.Canvas(args.output, pagesize=(a4_width, a4_height))

    for idx, img in enumerate(images):
        if idx > 0 and idx % (num_cols * num_rows) == 0:
            c.showPage()

        pos = idx % (num_cols * num_rows)
        col = pos % num_cols
        row = pos // num_cols

        x = margin_x + col * card_width
        y = a4_height - margin_y - (row + 1) * card_height  # y from bottom

        # Draw gridline (cutting guide)
        c.setLineWidth(0.2)  # Thin line for guidance
        c.setDash(1, 2)  # Dashed line
        c.rect(x, y, card_width, card_height)
        c.setDash()  # Reset to solid

        # Draw image
        c.drawInlineImage(img, x, y, width=card_width, height=card_height)

    c.save()
    print(f"PDF generated: {args.output}")

if __name__ == "__main__":
    main()