from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="placemark_linker",
    version="0.0.1",
    description="Link placemark to other areas represented with KML files",
    author="spameier",
    author_email="spameier@protonmail.ch",
    license="MIT",
    install_requires=requirements,
    packages=["placemark_linker"],
    entry_points={
        "console_scripts": ["placemark_linker=placemark_linker.placemark_linker:main"]
    },
)
