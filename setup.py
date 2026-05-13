from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

extensions = [
    Extension(
        "glitxh.__main__",
        ["src/glitxh/__main__.py"]
    ),
]

setup(
    name="glitxh",
    version="0.5.0",

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
