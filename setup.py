
#!/usr/bin/env python
import setuptools
import glob

setuptools.setup(
    name="tokamak_radiation_environment",
    version="0.0.1",
    include_package_data=True,
    description="",
    packages=setuptools.find_packages(),
    install_requires=[
            "numpy",
            "pandas",
            "matplotlib",
            "openmc"
    ],
)
