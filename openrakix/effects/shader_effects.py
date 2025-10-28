import numpy as np


class ShaderEffect:
    def __init__(self, name="ShaderEffect"):
        self.name = name
        self.uniforms = {}
        self.enabled = True

    def set_uniform(self, name, value):
        self.uniforms[name] = value

    def apply(self, pixel_data, uniforms=None):
        if not self.enabled:
            return pixel_data

        if uniforms:
            self.uniforms.update(uniforms)

        return self._process(pixel_data)

    def _process(self, pixel_data):
        return pixel_data


class WaveEffect(ShaderEffect):
    def __init__(self):
        super().__init__("WaveEffect")
        self.uniforms = {
            "amplitude": 10.0,
            "frequency": 0.01,
            "time": 0.0,
            "direction": "horizontal"
        }

    def _process(self, pixel_data):
        height, width = pixel_data.shape[:2]
        result = np.zeros_like(pixel_data)

        amplitude = self.uniforms.get("amplitude", 10.0)
        frequency = self.uniforms.get("frequency", 0.01)
        time = self.uniforms.get("time", 0.0)
        direction = self.uniforms.get("direction", "horizontal")

        if direction == "horizontal":
            for y in range(height):
                offset = int(amplitude * np.sin(2 * np.pi * frequency * y + time))
                for x in range(width):
                    src_x = (x + offset) % width
                    result[y, x] = pixel_data[y, src_x]
        else:
            for x in range(width):
                offset = int(amplitude * np.sin(2 * np.pi * frequency * x + time))
                for y in range(height):
                    src_y = (y + offset) % height
                    result[y, x] = pixel_data[src_y, x]

        return result


class RippleEffect(ShaderEffect):
    def __init__(self):
        super().__init__("RippleEffect")
        self.uniforms = {
            "center": (0.5, 0.5),
            "amplitude": 20.0,
            "frequency": 0.05,
            "time": 0.0
        }

    def _process(self, pixel_data):
        height, width = pixel_data.shape[:2]
        result = np.zeros_like(pixel_data)

        center = self.uniforms.get("center", (0.5, 0.5))
        amplitude = self.uniforms.get("amplitude", 20.0)
        frequency = self.uniforms.get("frequency", 0.05)
        time = self.uniforms.get("time", 0.0)

        center_x = int(center[0] * width)
        center_y = int(center[1] * height)

        for y in range(height):
            for x in range(width):
                dx = x - center_x
                dy = y - center_y
                distance = np.sqrt(dx * dx + dy * dy)

                offset = amplitude * np.sin(2 * np.pi * frequency * distance - time)

                if distance > 0:
                    src_x = int(x + (dx / distance) * offset)
                    src_y = int(y + (dy / distance) * offset)

                    src_x = max(0, min(width - 1, src_x))
                    src_y = max(0, min(height - 1, src_y))

                    result[y, x] = pixel_data[src_y, src_x]
                else:
                    result[y, x] = pixel_data[y, x]

        return result


class ChromaticAberrationEffect(ShaderEffect):
    def __init__(self):
        super().__init__("ChromaticAberrationEffect")
        self.uniforms = {
            "offset": 5.0
        }

    def _process(self, pixel_data):
        offset = int(self.uniforms.get("offset", 5.0))
        result = pixel_data.copy()

        if offset > 0:
            result[:, offset:, 0] = pixel_data[:, :-offset, 0]
            result[:, :-offset, 2] = pixel_data[:, offset:, 2]

        return result


class BloomEffect(ShaderEffect):
    def __init__(self):
        super().__init__("BloomEffect")
        self.uniforms = {
            "threshold": 0.7,
            "intensity": 1.5
        }

    def _process(self, pixel_data):
        threshold = self.uniforms.get("threshold", 0.7)
        intensity = self.uniforms.get("intensity", 1.5)

        brightness = np.mean(pixel_data[:, :, :3], axis=2)
        bright_mask = brightness > threshold

        bloom = pixel_data.copy()
        bloom[:, :, :3] *= bright_mask[:, :, np.newaxis] * intensity

        from scipy.ndimage import gaussian_filter
        bloom[:, :, 0] = gaussian_filter(bloom[:, :, 0], sigma=10)
        bloom[:, :, 1] = gaussian_filter(bloom[:, :, 1], sigma=10)
        bloom[:, :, 2] = gaussian_filter(bloom[:, :, 2], sigma=10)

        result = np.clip(pixel_data + bloom * 0.5, 0, 1)
        return result


class VignetteEffect(ShaderEffect):
    def __init__(self):
        super().__init__("VignetteEffect")
        self.uniforms = {
            "strength": 0.5,
            "radius": 0.8
        }

    def _process(self, pixel_data):
        height, width = pixel_data.shape[:2]
        strength = self.uniforms.get("strength", 0.5)
        radius = self.uniforms.get("radius", 0.8)

        center_x, center_y = width / 2, height / 2
        max_dist = np.sqrt(center_x**2 + center_y**2)

        result = pixel_data.copy()

        for y in range(height):
            for x in range(width):
                dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                normalized_dist = (dist / max_dist) / radius
                vignette_factor = 1 - np.clip(normalized_dist, 0, 1) * strength

                result[y, x, :3] *= vignette_factor

        return result


class ColorGradeEffect(ShaderEffect):
    def __init__(self):
        super().__init__("ColorGradeEffect")
        self.uniforms = {
            "temperature": 0.0,
            "tint": 0.0,
            "saturation": 1.0,
            "contrast": 1.0,
            "brightness": 0.0
        }

    def _process(self, pixel_data):
        result = pixel_data.copy()

        temperature = self.uniforms.get("temperature", 0.0)
        if temperature != 0:
            result[:, :, 0] += temperature * 0.1
            result[:, :, 2] -= temperature * 0.1

        tint = self.uniforms.get("tint", 0.0)
        if tint != 0:
            result[:, :, 1] += tint * 0.1

        saturation = self.uniforms.get("saturation", 1.0)
        if saturation != 1.0:
            gray = np.mean(result[:, :, :3], axis=2, keepdims=True)
            result[:, :, :3] = gray + (result[:, :, :3] - gray) * saturation

        contrast = self.uniforms.get("contrast", 1.0)
        if contrast != 1.0:
            result[:, :, :3] = (result[:, :, :3] - 0.5) * contrast + 0.5

        brightness = self.uniforms.get("brightness", 0.0)
        if brightness != 0:
            result[:, :, :3] += brightness

        result = np.clip(result, 0, 1)
        return result
