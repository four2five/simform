mrsimform: MapReduce based Simulation Informatics
=========

### Written by Austin Benson, Paul Constantine, David F. Gleich, and Yangyang Hou

Functionality
-------------

This code is designed to work with a database of exodus files produced
by the ARIA thermal code in the Sierra Mechanics toolbox.  For such
a database, it will:
* convert the data into a format to make it easier to process in Hadoop
* compute the SVD of the database
* interpolate the solution at any set of new points using a linear
  interpolation routine
* interpolate the solution at any set of new points using a non-linear
  model reduction based interpolation routine that includes a estimate
  of the error
* convert all the MapReduce based predictions to exodus files.  

Setup
---------------

mrsimform requires quite a few libraries as it combines the
functionality of many different pieces of code.  Please see
INSTALL.md for help on setup.  The code does not actually 
require any pieces to be installed on the system.  But this 
makes it much easier.


Papers
------

* Tall and Skinny QR Factorizations in MapReduce architectures,
Constantine and Gleich.

* Direct Tall and Skinny QR Factorizations in MapReduce architectures,
Benson, Gleich, and Demmel.

* Distinguishing Signal from Noise in an SVD of simulation data,
Constantine and Gleich.


