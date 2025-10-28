import sys
import os
import subprocess
from PIL import Image
import numpy as np


class WallpaperEngine:
    def __init__(self):
        self.platform_manager = None
        self.current_scene = None
        self.renderer = None
        self.compositor = None
        self.running = False
        self.frame_rate = 30
        self.resolution = (1920, 1080)

    def initialize(self, platform=None):
        from ..platforms.platform_manager import PlatformManager

        if platform is None:
            platform = self._detect_platform()

        self.platform_manager = PlatformManager(platform)
        self.platform_manager.initialize()

        print(f"OpenRakix initialized for {platform}")
        return self

    def _detect_platform(self):
        if sys.platform.startswith('linux'):
            return 'linux'
        elif sys.platform == 'darwin':
            return 'macos'
        elif sys.platform == 'win32':
            return 'windows'
        else:
            return 'generic'

    def set_scene(self, scene):
        self.current_scene = scene
        return self

    def set_renderer(self, renderer):
        self.renderer = renderer
        return self

    def set_compositor(self, compositor):
        self.compositor = compositor
        return self

    def set_resolution(self, width, height):
        self.resolution = (width, height)
        if self.renderer:
            self.renderer.set_size(width, height)
        return self

    def set_frame_rate(self, fps):
        self.frame_rate = fps
        return self

    def render_frame(self, camera=None):
        if not self.renderer or not self.current_scene:
            return None

        if camera is None:
            camera = self.current_scene.get_main_camera()

        self.renderer.render(self.current_scene, camera)
        frame_data = self.renderer.get_render_target()

        if self.compositor:
            frame_data = self.compositor.process(frame_data)

        return frame_data

    def set_wallpaper(self, image_path_or_data):
        if not self.platform_manager:
            raise RuntimeError("WallpaperEngine not initialized. Call initialize() first.")

        if isinstance(image_path_or_data, str):
            self.platform_manager.set_wallpaper(image_path_or_data)
        elif isinstance(image_path_or_data, np.ndarray):
            temp_path = "/tmp/openrx_wallpaper.png"
            image_data = (image_path_or_data * 255).astype(np.uint8)
            img = Image.fromarray(image_data, mode='RGBA')
            img.save(temp_path)
            self.platform_manager.set_wallpaper(temp_path)
        else:
            raise ValueError("Invalid image data type")

        return self

    def start_live_wallpaper(self, update_callback=None):
        if not self.platform_manager:
            raise RuntimeError("WallpaperEngine not initialized. Call initialize() first.")

        self.running = True
        import time

        frame_time = 1.0 / self.frame_rate

        try:
            while self.running:
                start_time = time.time()

                if update_callback:
                    update_callback(self.current_scene)

                frame_data = self.render_frame()

                if frame_data is not None:
                    self.set_wallpaper(frame_data)

                elapsed = time.time() - start_time
                sleep_time = max(0, frame_time - elapsed)
                time.sleep(sleep_time)

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        if self.platform_manager:
            self.platform_manager.cleanup()
        print("OpenRakix wallpaper engine stopped")

    def render_to_wallpaper(self, scene, camera=None):
        self.set_scene(scene)
        frame_data = self.render_frame(camera)

        if frame_data is not None:
            self.set_wallpaper(frame_data)

        return self

    def apply_effect(self, effect_name, **params):
        if not self.compositor:
            from .compositor import Compositor
            self.compositor = Compositor()

        self.compositor.add_effect(effect_name, **params)
        return self

    def clear_effects(self):
        if self.compositor:
            self.compositor.clear_effects()
        return self
