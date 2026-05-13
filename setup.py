from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

extensions = [
    Extension(
        "glitxh.glitxh",
        ["src/glitxh/glitxh.py"]
    ),
]

setup(
    name="glitxh",
    version="0.5.1",

    package_dir={"": "src"},
    packages=find_packages(where="src"),

    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3"
        }
    ),

    zip_safe=False,
)
