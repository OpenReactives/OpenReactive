import sys
import os
import subprocess


class PlatformManager:
    def __init__(self, platform=None):
        self.platform = platform or self._detect_platform()
        self.backend = None

    def _detect_platform(self):
        if sys.platform.startswith('linux'):
            return 'linux'
        elif sys.platform == 'darwin':
            return 'macos'
        elif sys.platform == 'win32':
            return 'windows'
        else:
            return 'generic'

    def initialize(self):
        if self.platform == 'linux':
            self.backend = LinuxWallpaperBackend()
        elif self.platform == 'macos':
            self.backend = MacOSWallpaperBackend()
        elif self.platform == 'windows':
            self.backend = WindowsWallpaperBackend()
        else:
            self.backend = GenericWallpaperBackend()

        self.backend.initialize()

    def set_wallpaper(self, image_path):
        if not self.backend:
            raise RuntimeError("Platform backend not initialized")

        self.backend.set_wallpaper(image_path)

    def cleanup(self):
        if self.backend:
            self.backend.cleanup()


class LinuxWallpaperBackend:
    def __init__(self):
        self.desktop_environment = None
        self.method = None

    def initialize(self):
        self.desktop_environment = self._detect_desktop_environment()
        print(f"Detected desktop environment: {self.desktop_environment}")

    def _detect_desktop_environment(self):
        if os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            return 'gnome'
        elif os.environ.get('KDE_FULL_SESSION'):
            return 'kde'
        elif os.environ.get('DESKTOP_SESSION') == 'xfce':
            return 'xfce'
        elif os.environ.get('DESKTOP_SESSION') == 'mate':
            return 'mate'
        elif 'LXDE' in os.environ.get('DESKTOP_SESSION', ''):
            return 'lxde'
        else:
            return 'generic'

    def set_wallpaper(self, image_path):
        image_path = os.path.abspath(image_path)

        if self.desktop_environment == 'gnome':
            self._set_gnome_wallpaper(image_path)
        elif self.desktop_environment == 'kde':
            self._set_kde_wallpaper(image_path)
        elif self.desktop_environment == 'xfce':
            self._set_xfce_wallpaper(image_path)
        elif self.desktop_environment == 'mate':
            self._set_mate_wallpaper(image_path)
        else:
            self._set_generic_wallpaper(image_path)

    def _set_gnome_wallpaper(self, image_path):
        try:
            subprocess.run([
                'gsettings', 'set', 'org.gnome.desktop.background',
                'picture-uri', f'file://{image_path}'
            ], check=True)
            subprocess.run([
                'gsettings', 'set', 'org.gnome.desktop.background',
                'picture-uri-dark', f'file://{image_path}'
            ], check=False)
        except Exception as e:
            print(f"Failed to set GNOME wallpaper: {e}")

    def _set_kde_wallpaper(self, image_path):
        try:
            script = f'''
const desktops = desktops();
for (var i = 0; i < desktops.length; i++) {{
    desktops[i].wallpaperPlugin = "org.kde.image";
    desktops[i].currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
    desktops[i].writeConfig("Image", "file://{image_path}");
}}
'''
            subprocess.run(['qdbus', 'org.kde.plasmashell', '/PlasmaShell',
                          'org.kde.PlasmaShell.evaluateScript', script], check=True)
        except Exception as e:
            print(f"Failed to set KDE wallpaper: {e}")

    def _set_xfce_wallpaper(self, image_path):
        try:
            subprocess.run([
                'xfconf-query', '-c', 'xfce4-desktop',
                '-p', '/backdrop/screen0/monitor0/workspace0/last-image',
                '-s', image_path
            ], check=True)
        except Exception as e:
            print(f"Failed to set XFCE wallpaper: {e}")

    def _set_mate_wallpaper(self, image_path):
        try:
            subprocess.run([
                'gsettings', 'set', 'org.mate.background',
                'picture-filename', image_path
            ], check=True)
        except Exception as e:
            print(f"Failed to set MATE wallpaper: {e}")

    def _set_generic_wallpaper(self, image_path):
        try:
            subprocess.run(['feh', '--bg-scale', image_path], check=True)
        except FileNotFoundError:
            try:
                subprocess.run(['nitrogen', '--set-scaled', image_path], check=True)
            except Exception as e:
                print(f"Failed to set wallpaper with generic methods: {e}")

    def cleanup(self):
        pass


class MacOSWallpaperBackend:
    def initialize(self):
        pass

    def set_wallpaper(self, image_path):
        image_path = os.path.abspath(image_path)

        script = f'''
tell application "System Events"
    tell every desktop
        set picture to POSIX file "{image_path}"
    end tell
end tell
'''

        try:
            subprocess.run(['osascript', '-e', script], check=True)
        except Exception as e:
            print(f"Failed to set macOS wallpaper: {e}")

    def cleanup(self):
        pass


class WindowsWallpaperBackend:
    def initialize(self):
        pass

    def set_wallpaper(self, image_path):
        import ctypes

        image_path = os.path.abspath(image_path)

        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDCHANGE = 0x02

        try:
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER,
                0,
                image_path,
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )
        except Exception as e:
            print(f"Failed to set Windows wallpaper: {e}")

    def cleanup(self):
        pass


class GenericWallpaperBackend:
    def initialize(self):
        print("Using generic wallpaper backend (limited functionality)")

    def set_wallpaper(self, image_path):
        print(f"Would set wallpaper to: {image_path}")
        print("Generic backend does not support automatic wallpaper setting.")
        print("Please manually set the wallpaper using your system settings.")

    def cleanup(self):
        pass
