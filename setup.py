from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "glitxh.main",
        ["glitxh/main.py"]
    ),
]

setup(
    name="glitxh",
    version="0.5.0",
    packages=["glitxh"],

    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3"
        }
    ),

    zip_safe=False,
)
