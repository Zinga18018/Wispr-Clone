from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="wisprclone",
    version="1.0.0",
    author="WisprClone Team",
    author_email="contact@wisprclone.com",
    description="A powerful, real-time speech-to-text application using OpenAI Whisper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wisprclone",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "wisprclone=wisprclone.main:main",
            "wisprclone-gui=wisprclone.gui:main",
            "wisprclone-cli=wisprclone.cli:main",
        ],
    },
) 