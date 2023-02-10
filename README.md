# Requirements
    - vrpn (https://github.com/vrpn/vrpn)
    # Following will be installed when you install vicon_projector_server package
    - Pyqt6
    - pyqtgraph
    - Werkzeug
    - json-rpc
    - tabulate


# Installing VRPN
```sh
# Clone the repo
git clone https://github.com/vrpn/vrpn


cd vrpn
# Build VRPN
mkdir build
cd build
cmake ..
make vrpn-python

# This install vrpn python package in the default python
sudo make install vrpn-python
```
To change python version or install in a virtual env change appropriate paths in 
```
vrpn/python_vrpn/Makefile.python
```

# To install this package

```sh
pip3 install .
```

or for active development (editable),
```sh
pip3 install -e .
```

# Docs

To make documentation

```sh
cd docs/
make html
```

If you have issues building sphinx or if sphinx wasnt correctly installed with the python package. Use the following commands to install sphinx and rtd theme

```sh

sudo apt-get install python3-sphinx
#or
pip3 install sphinx

# To install sphinx theme
pip3 install sphinx_rtd_theme

```


If you add a new file, use the following command to add the file to Sphinx documentation. Run this once (from inside docs folder) when there are new python files.

```sh
sphinx-apidoc -o ../docs ../vicon_projector_server
```

# Work in progress
