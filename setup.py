from setuptools import setup

setup(
   name='vicon_projector_server',
   version='0.2.0',
   packages=['vicon_projector_server'],
   license='LICENSE',
   maintainer="Akash Ratheesh",
   maintainer_email="akash.ratheeshbabu@colorado.edu",
   description='Vicon Projector Server',
   long_description=open('DESCRIPTION').read(),
   install_requires=[
       "pyqt6",
       "pyqtgraph",
       "numpy",
       "Werkzeug",
       "json-rpc",
       "tabulate",
   ],
)