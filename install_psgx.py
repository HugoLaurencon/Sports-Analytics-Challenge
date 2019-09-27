import os

packages = ["tensorflow", "keras", "numpy", "simplejson", "lxml", "h5py", "pandas"]

for package in packages:
    os.system("pip install " + package)
