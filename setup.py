from setuptools import setup, find_packages
from Cython.Build import cythonize
import glob

setup(
    name="glitxh",
    version="0.5.4",

    package_dir={"": "src"},
    packages=find_packages(where="src"),

    ext_modules=cythonize(
        glob.glob("src/glitxh/*.py"),
        compiler_directives={
            "language_level": "3"
        }
    ),

    zip_safe=False,
)
