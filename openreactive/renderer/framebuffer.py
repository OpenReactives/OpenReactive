import numpy as np


class Framebuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color_buffer = np.zeros((height, width, 4), dtype=np.float32)
        self.depth_buffer = np.ones((height, width), dtype=np.float32) * float('inf')
        self.stencil_buffer = np.zeros((height, width), dtype=np.uint8)

    def clear_color(self, r=0, g=0, b=0, a=1):
        self.color_buffer[:] = [r, g, b, a]

    def clear_depth(self, value=float('inf')):
        self.depth_buffer[:] = value

    def clear_stencil(self, value=0):
        self.stencil_buffer[:] = value

    def clear_all(self):
        self.clear_color()
        self.clear_depth()
        self.clear_stencil()

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.color_buffer = np.zeros((height, width, 4), dtype=np.float32)
        self.depth_buffer = np.ones((height, width), dtype=np.float32) * float('inf')
        self.stencil_buffer = np.zeros((height, width), dtype=np.uint8)

    def get_pixel(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.color_buffer[y, x]
        return None

    def set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.color_buffer[y, x] = color

    def to_image(self):
        from PIL import Image
        image_data = (self.color_buffer * 255).astype(np.uint8)
        return Image.fromarray(image_data, mode='RGBA')

    def save(self, filename):
        img = self.to_image()
        img.save(filename)
