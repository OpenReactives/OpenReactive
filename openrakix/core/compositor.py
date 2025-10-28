import numpy as np
from PIL import Image, ImageFilter, ImageEnhance


class Compositor:
    def __init__(self):
        self.effects = []
        self.blend_mode = 'normal'

    def add_effect(self, effect_name, **params):
        self.effects.append({
            'name': effect_name,
            'params': params
        })
        return self

    def clear_effects(self):
        self.effects = []
        return self

    def process(self, frame_data):
        if len(self.effects) == 0:
            return frame_data

        image_data = (frame_data * 255).astype(np.uint8)
        img = Image.fromarray(image_data, mode='RGBA')

        for effect in self.effects:
            img = self._apply_effect(img, effect['name'], effect['params'])

        processed_data = np.array(img).astype(np.float32) / 255.0
        return processed_data

    def _apply_effect(self, img, effect_name, params):
        if effect_name == 'blur':
            radius = params.get('radius', 5)
            return img.filter(ImageFilter.GaussianBlur(radius))

        elif effect_name == 'sharpen':
            return img.filter(ImageFilter.SHARPEN)

        elif effect_name == 'edge_enhance':
            return img.filter(ImageFilter.EDGE_ENHANCE)

        elif effect_name == 'emboss':
            return img.filter(ImageFilter.EMBOSS)

        elif effect_name == 'brightness':
            factor = params.get('factor', 1.2)
            enhancer = ImageEnhance.Brightness(img)
            return enhancer.enhance(factor)

        elif effect_name == 'contrast':
            factor = params.get('factor', 1.2)
            enhancer = ImageEnhance.Contrast(img)
            return enhancer.enhance(factor)

        elif effect_name == 'saturation':
            factor = params.get('factor', 1.2)
            enhancer = ImageEnhance.Color(img)
            return enhancer.enhance(factor)

        elif effect_name == 'grayscale':
            return img.convert('L').convert('RGBA')

        elif effect_name == 'sepia':
            return self._apply_sepia(img)

        elif effect_name == 'vignette':
            strength = params.get('strength', 0.5)
            return self._apply_vignette(img, strength)

        elif effect_name == 'chromatic_aberration':
            offset = params.get('offset', 5)
            return self._apply_chromatic_aberration(img, offset)

        elif effect_name == 'pixelate':
            pixel_size = params.get('pixel_size', 10)
            return self._apply_pixelate(img, pixel_size)

        elif effect_name == 'wave':
            amplitude = params.get('amplitude', 10)
            frequency = params.get('frequency', 0.01)
            return self._apply_wave(img, amplitude, frequency)

        return img

    def _apply_sepia(self, img):
        data = np.array(img)
        r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]

        tr = 0.393 * r + 0.769 * g + 0.189 * b
        tg = 0.349 * r + 0.686 * g + 0.168 * b
        tb = 0.272 * r + 0.534 * g + 0.131 * b

        data[:, :, 0] = np.clip(tr, 0, 255)
        data[:, :, 1] = np.clip(tg, 0, 255)
        data[:, :, 2] = np.clip(tb, 0, 255)

        return Image.fromarray(data.astype(np.uint8))

    def _apply_vignette(self, img, strength):
        width, height = img.size
        data = np.array(img).astype(np.float32)

        center_x, center_y = width / 2, height / 2
        max_dist = np.sqrt(center_x**2 + center_y**2)

        for y in range(height):
            for x in range(width):
                dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                vignette_factor = 1 - (dist / max_dist) * strength
                vignette_factor = max(0, vignette_factor)

                data[y, x, :3] *= vignette_factor

        return Image.fromarray(data.astype(np.uint8))

    def _apply_chromatic_aberration(self, img, offset):
        data = np.array(img)
        height, width = data.shape[:2]

        result = data.copy()

        if offset > 0:
            result[:, offset:, 0] = data[:, :-offset, 0]

        if offset > 0:
            result[:, :-offset, 2] = data[:, offset:, 2]

        return Image.fromarray(result)

    def _apply_pixelate(self, img, pixel_size):
        width, height = img.size

        small = img.resize(
            (width // pixel_size, height // pixel_size),
            Image.NEAREST
        )

        return small.resize((width, height), Image.NEAREST)

    def _apply_wave(self, img, amplitude, frequency):
        data = np.array(img)
        height, width = data.shape[:2]
        result = np.zeros_like(data)

        for y in range(height):
            offset = int(amplitude * np.sin(2 * np.pi * frequency * y))
            for x in range(width):
                src_x = (x + offset) % width
                result[y, x] = data[y, src_x]

        return Image.fromarray(result)

    def blend(self, img1, img2, alpha=0.5):
        return Image.blend(img1, img2, alpha)

    def composite(self, foreground, background, mask=None):
        if mask:
            return Image.composite(foreground, background, mask)
        else:
            return Image.alpha_composite(background, foreground)
