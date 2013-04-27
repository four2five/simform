simform: MapReduce based Simulation Informatics
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

Synopsis
--------

Here are some commands I ran to do a quick analysis on the EC2 cluster:

### Initialization

    $ make dir=hdfs://nebula/data/exodus-runs

    $ make setup_database name=runs variable=TEMP dir=hdfs://ec2-107-22-80-153.compute-1.amazonaws.com:8020/user/temp/simform/
    $ make -f runs preprocess
    $ make -f runs convert timestepfile=timesteps.txt

In this case, we had to normalize time-steps across the different files as the default step-length is variable.

### Compute the global variance
	$ make -f runs var
	$ make -f runs outputvar

### Simple interpolation

    $ make -f runs predict design=design_points.txt points=new_points.txt

and then dump out exodus files

    $ make -f runs seq2exodus  numExodusfiles=10 OutputName=output/thermal_maze

### SVD based Model Reduction

    $ make -f runs seq2mseq
    $ make -f runs model numExodusfiles=6
    $ make -f runs interpsvd design=design_points.txt points=new_points.txt

Setup
---------------

mrsimform requires quite a few libraries as it combines the
functionality of many different pieces of code.  Please see
INSTALL.md for help on setup.  The code does not actually 
require any pieces to be installed on the system.  But this 
makes it much easier.  We've provided a list of commands to
setup a demostration cluster on Amazon's EC2 system and process
a small collection of files.  See the demo directory.

Papers
------

These codes are based on a few active research projects from
the authors.  

* [Tall and Skinny QR Factorizations in MapReduce architectures](http://dx.doi.org/10.1145/1996092.1996103),
Constantine and Gleich.

* Direct Tall and Skinny QR Factorizations in MapReduce architectures,
Benson, Gleich, and Demmel. Submitted.

* [Distinguishing Signal from Noise in an SVD of simulation data](10.1109/ICASSP.2012.6289125),
Constantine and Gleich.


