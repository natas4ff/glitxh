from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "yourpackage.main",
        ["yourpackage/main.py"]
    ),
    Extension(
        "yourpackage.api",
        ["yourpackage/api.py"]
    )
]

setup(
    name="yourpackage",
    version="1.0.0",
    packages=["yourpackage"],

    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3"
        }
    ),

    zip_safe=False,
)
