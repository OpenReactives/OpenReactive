from .pipeline import RenderPipeline
import numpy as np


class Renderer:
    def __init__(self, width=800, height=600):
        self.pipeline = RenderPipeline(width, height)
        self.width = width
        self.height = height
        self.auto_clear = True
        self.sort_objects = True

    def render(self, scene, camera):
        if self.auto_clear:
            self.pipeline.clear()

        self.pipeline.render(scene, camera)

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.pipeline.resize(width, height)

    def get_render_target(self):
        return self.pipeline.color_buffer

    def clear(self, color=True, depth=True):
        self.pipeline.clear(color, depth)

    def set_clear_color(self, r, g, b, a=1.0):
        self.pipeline.set_clear_color(r, g, b, a)

    def save_screenshot(self, filename):
        self.pipeline.save_to_file(filename)
