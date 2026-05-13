from setuptools import setup
from Cython.Build import cythonize
import os

files = []

for file in os.listdir():
    if file.endswith(".py") and file != "setup.py":
        files.append(file)

setup(
    ext_modules=cythonize(
        files,
        compiler_directives={
            'language_level': "3"
        }
    )
)