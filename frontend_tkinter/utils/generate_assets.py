"""
Logo Generator Script

This script generates a simple logo for the Campus Event System application.
Run this script to create logo.png in the assets/images folder.
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_logo(output_path: str, size: tuple = (400, 200)):
    """
    Create Campus Event System logo.
    
    Args:
        output_path: Path to save the logo
        size: Logo dimensions (width, height)
    """
    # Create image with gradient-like background
    image = Image.new('RGB', size, color='#FFFFFF')
    draw = ImageDraw.Draw(image)
    
    # Draw gradient background (simplified - solid colors)
    # Top section - primary blue
    draw.rectangle([0, 0, size[0], size[1] // 3], fill='#3498DB')
    
    # Middle section - lighter blue
    draw.rectangle([0, size[1] // 3, size[0], 2 * size[1] // 3], fill='#5DADE2')
    
    # Bottom section - lightest blue
    draw.rectangle([0, 2 * size[1] // 3, size[0], size[1]], fill='#85C1E9')
    
    # Draw logo elements
    center_x = size[0] // 2
    center_y = size[1] // 2
    
    # Draw building icon (representing campus)
    building_width = 60
    building_height = 80
    building_x = center_x - 100
    building_y = center_y - building_height // 2
    
    # Building body
    draw.rectangle(
        [building_x, building_y, building_x + building_width, building_y + building_height],
        fill='white',
        outline='#2C3E50',
        width=2
    )
    
    # Windows
    window_size = 10
    for row in range(4):
        for col in range(2):
            wx = building_x + 15 + col * 25
            wy = building_y + 15 + row * 18
            draw.rectangle(
                [wx, wy, wx + window_size, wy + window_size],
                fill='#3498DB'
            )
    
    # Draw calendar icon
    cal_size = 70
    cal_x = center_x + 40
    cal_y = center_y - cal_size // 2
    
    # Calendar body
    draw.rectangle(
        [cal_x, cal_y, cal_x + cal_size, cal_y + cal_size],
        fill='white',
        outline='#2C3E50',
        width=2
    )
    
    # Calendar header
    draw.rectangle(
        [cal_x, cal_y, cal_x + cal_size, cal_y + 15],
        fill='#E74C3C'
    )
    
    # Calendar rings
    for i in range(3):
        ring_x = cal_x + 15 + i * 20
        draw.rectangle(
            [ring_x, cal_y - 5, ring_x + 8, cal_y + 5],
            fill='#E74C3C'
        )
    
    # Calendar date
    try:
        date_font = ImageFont.truetype("Arial.ttf", 28)
    except:
        date_font = ImageFont.load_default()
    
    draw.text(
        (cal_x + cal_size // 2 - 10, cal_y + 30),
        "15",
        fill='#2C3E50',
        font=date_font
    )
    
    # Draw text
    try:
        title_font = ImageFont.truetype("Arial.ttf", 36)
        subtitle_font = ImageFont.truetype("Arial.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Title
    title = "Campus Event"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(
        ((size[0] - title_width) // 2, 15),
        title,
        fill='white',
        font=title_font
    )
    
    # Subtitle
    subtitle = "Management System"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    draw.text(
        ((size[0] - subtitle_width) // 2, size[1] - 35),
        subtitle,
        fill='white',
        font=subtitle_font
    )
    
    # Save image
    image.save(output_path, 'PNG')
    print(f"Logo created: {output_path}")


def create_icon_placeholders(icons_path: str):
    """
    Create simple placeholder icons for the application.
    
    Args:
        icons_path: Path to icons directory
    """
    icons = {
        'dashboard': '#3498DB',
        'events': '#E74C3C',
        'resources': '#27AE60',
        'bookings': '#F39C12',
        'profile': '#9B59B6',
        'settings': '#95A5A6',
        'notifications': '#E91E63',
        'search': '#2ECC71',
        'add': '#16A085',
        'edit': '#2980B9',
        'delete': '#C0392B',
        'approve': '#27AE60',
        'reject': '#E74C3C',
        'logout': '#7F8C8D'
    }
    
    for icon_name, color in icons.items():
        icon_path = os.path.join(icons_path, f"{icon_name}.png")
        
        # Create 48x48 icon
        size = (48, 48)
        image = Image.new('RGBA', size, color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw colored circle
        margin = 4
        draw.ellipse(
            [margin, margin, size[0] - margin, size[1] - margin],
            fill=color,
            outline=None
        )
        
        # Add icon letter in center
        try:
            font = ImageFont.truetype("Arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        letter = icon_name[0].upper()
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        draw.text(
            ((size[0] - text_width) // 2, (size[1] - text_height) // 2 - 2),
            letter,
            fill='white',
            font=font
        )
        
        # Save icon
        image.save(icon_path, 'PNG')
    
    print(f"Created {len(icons)} placeholder icons in {icons_path}")


def create_placeholder_images(images_path: str):
    """
    Create placeholder images for events and resources.
    
    Args:
        images_path: Path to images directory
    """
    # Event placeholder
    event_img = Image.new('RGB', (600, 400), color='#3498DB')
    draw = ImageDraw.Draw(event_img)
    
    try:
        font = ImageFont.truetype("Arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    text = "EVENT"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text(
        ((600 - text_width) // 2, 176),
        text,
        fill='white',
        font=font
    )
    
    event_img.save(os.path.join(images_path, 'event_placeholder.png'), 'PNG')
    
    # Resource placeholder
    resource_img = Image.new('RGB', (600, 400), color='#27AE60')
    draw = ImageDraw.Draw(resource_img)
    
    text = "RESOURCE"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text(
        ((600 - text_width) // 2, 176),
        text,
        fill='white',
        font=font
    )
    
    resource_img.save(os.path.join(images_path, 'resource_placeholder.png'), 'PNG')
    
    # User avatar placeholder
    avatar_img = Image.new('RGB', (200, 200), color='#9B59B6')
    draw = ImageDraw.Draw(avatar_img)
    
    # Draw simple person icon
    # Head
    draw.ellipse([70, 40, 130, 100], fill='white')
    # Body
    draw.ellipse([50, 100, 150, 180], fill='white')
    
    avatar_img.save(os.path.join(images_path, 'avatar_placeholder.png'), 'PNG')
    
    print(f"Created placeholder images in {images_path}")


if __name__ == "__main__":
    # Get base path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(current_dir)
    
    # Create paths
    images_path = os.path.join(base_path, "assets", "images")
    icons_path = os.path.join(base_path, "assets", "icons")
    
    # Ensure directories exist
    os.makedirs(images_path, exist_ok=True)
    os.makedirs(icons_path, exist_ok=True)
    
    # Create logo
    logo_path = os.path.join(images_path, "logo.png")
    create_logo(logo_path)
    
    # Create icons
    create_icon_placeholders(icons_path)
    
    # Create placeholder images
    create_placeholder_images(images_path)
    
    print("\n✅ All assets created successfully!")
    print(f"   Logo: {logo_path}")
    print(f"   Icons: {icons_path}")
    print(f"   Images: {images_path}")
