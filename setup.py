from setuptools import setup, find_packages

setup(
    name="openreactive",
    version="1.0.0",
    description="OpenGL-esque 3D processing system with web and OS projection capabilities",
    author="OpenReactive Team",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pillow>=9.0.0",
        "click>=8.0.0",
        "pyyaml>=6.0",
        "jinja2>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "openreactive=openreactive.cli:main",
            "openrx=openrakix.cli:main",
        ],
    },
    python_requires=">=3.8",
)
