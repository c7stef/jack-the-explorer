import pygame
from PIL import Image

def scale_surface(surface, new_size):
    """
    Scale a Pygame surface to the specified width and height using Pillow for high-quality scaling.
    
    :param surface: pygame.Surface - The surface to scale.
    :param new_width: int - The desired width.
    :param new_height: int - The desired height.
    :return: pygame.Surface - The scaled surface.
    """
    new_width, new_height = new_size

    # Convert Pygame surface to a Pillow Image
    mode = "RGBA"  # Adjust if your surface uses a different mode
    size = surface.get_size()
    data = pygame.image.tostring(surface, mode)
    pil_image = Image.frombytes(mode, size, data)
    
    # Scale the image using Pillow with LANCZOS resampling
    scaled_pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
    
    # Convert back to a Pygame surface
    scaled_data = scaled_pil_image.tobytes()
    scaled_surface = pygame.image.fromstring(scaled_data, scaled_pil_image.size, mode)
    
    return scaled_surface