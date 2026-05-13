from setuptools import setup, find_packages

setup(
    name="glitxh",
    version="0.5.5",

    package_dir={"": "src"},
    packages=find_packages(where="src"),

    zip_safe=False,
)
