"""
Script untuk membuat logo placeholder
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    """Create simple logo placeholder"""
    # Create image
    size = (300, 300)
    img = Image.new('RGB', size, color='#2c3e50')
    draw = ImageDraw.Draw(img)

    # Draw circle
    circle_bbox = [50, 50, 250, 250]
    draw.ellipse(circle_bbox, fill='#3498db', outline='white', width=5)

    # Draw text
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()

    text = "PA"

    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2 - 10)
    draw.text(position, text, fill='white', font=font)

    # Save
    logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
    img.save(logo_path)
    print(f"Logo created: {logo_path}")

if __name__ == "__main__":
    create_logo()
