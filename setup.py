from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="metabase-python",
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": "src/metabase/_version.py",
        "fallback_version": "0.0.0",
    },
    description="A Python wrapper for interacting with Metabase's API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Charles Lariviere",
    author_email="charleslariviere1@gmail.com  ",
    url="https://github.com/chasleslr/metabase-python",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "pandas",
    ],
    extras_require={},
    setup_requires=[
        "setuptools_scm>=3.3.1",
    ],
)
