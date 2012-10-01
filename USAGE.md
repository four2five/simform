Using mrsimform
===============

Overview and Ideas
------------------

Please see the associated report for a more mathematical perspective
on the ideas that the mrsimform codes implement.

The ideas discussed here relate to the basics of the code.  

Files
-----

There are three types of files we need:

* a directory exodus files
* `design_points.txt`
* `new_points.txt`

Let us describe each one.

### Exodus Files

The code is designed to work with a set of exodus files from
the ARIA package in the Sierra Mechanics toolkit.  Each file 
should have a name like:

    thermal_maze####.e
    
where #### is a number that starts from 0 or 1. (Note, this is
a technical limitation we are currently working to address.)  
The prefix on each name is entirely arbitrary, so

    myawsomesim####.e
    
is fine as well.    
These files should reside on a directory in the Hadoop Filesystem
(hereafter, HDFS).  

For instance, when we were developing the codes from yangyang's
user directory, we had all the files in `/user/yangyang/simform`
as the following listing shows:

    [dgleich@icme-hadoop1 ~]$ hadoop fs -ls /user/yangyang/simform
    Found 99 items
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 17:54 /user/yangyang/simform/thermal_maze0001.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 17:59 /user/yangyang/simform/thermal_maze0002.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 18:06 /user/yangyang/simform/thermal_maze0003.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 18:08 /user/yangyang/simform/thermal_maze0004.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 18:11 /user/yangyang/simform/thermal_maze0005.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 18:13 /user/yangyang/simform/thermal_maze0006.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 18:16 /user/yangyang/simform/thermal_maze0007.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 18:18 /user/yangyang/simform/thermal_maze0008.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 18:22 /user/yangyang/simform/thermal_maze0009.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 18:47 /user/yangyang/simform/thermal_maze0010.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 18:54 /user/yangyang/simform/thermal_maze0011.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 18:57 /user/yangyang/simform/thermal_maze0012.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:01 /user/yangyang/simform/thermal_maze0013.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:04 /user/yangyang/simform/thermal_maze0014.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:07 /user/yangyang/simform/thermal_maze0015.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:10 /user/yangyang/simform/thermal_maze0016.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:13 /user/yangyang/simform/thermal_maze0017.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:17 /user/yangyang/simform/thermal_maze0018.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:20 /user/yangyang/simform/thermal_maze0019.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:23 /user/yangyang/simform/thermal_maze0020.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:25 /user/yangyang/simform/thermal_maze0021.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:28 /user/yangyang/simform/thermal_maze0022.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:31 /user/yangyang/simform/thermal_maze0023.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:34 /user/yangyang/simform/thermal_maze0024.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:37 /user/yangyang/simform/thermal_maze0025.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:40 /user/yangyang/simform/thermal_maze0026.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:44 /user/yangyang/simform/thermal_maze0027.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:47 /user/yangyang/simform/thermal_maze0028.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:51 /user/yangyang/simform/thermal_maze0029.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:54 /user/yangyang/simform/thermal_maze0030.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 19:57 /user/yangyang/simform/thermal_maze0031.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:00 /user/yangyang/simform/thermal_maze0032.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:03 /user/yangyang/simform/thermal_maze0033.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:06 /user/yangyang/simform/thermal_maze0034.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:09 /user/yangyang/simform/thermal_maze0035.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:12 /user/yangyang/simform/thermal_maze0036.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:15 /user/yangyang/simform/thermal_maze0037.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:18 /user/yangyang/simform/thermal_maze0038.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:21 /user/yangyang/simform/thermal_maze0039.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:25 /user/yangyang/simform/thermal_maze0040.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:28 /user/yangyang/simform/thermal_maze0041.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:32 /user/yangyang/simform/thermal_maze0042.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:36 /user/yangyang/simform/thermal_maze0043.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:41 /user/yangyang/simform/thermal_maze0044.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:44 /user/yangyang/simform/thermal_maze0045.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:47 /user/yangyang/simform/thermal_maze0046.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:50 /user/yangyang/simform/thermal_maze0047.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:54 /user/yangyang/simform/thermal_maze0048.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 20:57 /user/yangyang/simform/thermal_maze0049.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:00 /user/yangyang/simform/thermal_maze0050.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:03 /user/yangyang/simform/thermal_maze0051.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:06 /user/yangyang/simform/thermal_maze0052.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:09 /user/yangyang/simform/thermal_maze0053.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:16 /user/yangyang/simform/thermal_maze0054.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:19 /user/yangyang/simform/thermal_maze0055.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:22 /user/yangyang/simform/thermal_maze0056.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:26 /user/yangyang/simform/thermal_maze0057.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:28 /user/yangyang/simform/thermal_maze0058.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:30 /user/yangyang/simform/thermal_maze0059.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:33 /user/yangyang/simform/thermal_maze0060.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:35 /user/yangyang/simform/thermal_maze0061.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:37 /user/yangyang/simform/thermal_maze0062.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:40 /user/yangyang/simform/thermal_maze0063.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:43 /user/yangyang/simform/thermal_maze0064.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:45 /user/yangyang/simform/thermal_maze0065.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:48 /user/yangyang/simform/thermal_maze0066.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:51 /user/yangyang/simform/thermal_maze0067.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:53 /user/yangyang/simform/thermal_maze0068.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:56 /user/yangyang/simform/thermal_maze0069.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 21:58 /user/yangyang/simform/thermal_maze0070.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:01 /user/yangyang/simform/thermal_maze0071.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:03 /user/yangyang/simform/thermal_maze0072.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:06 /user/yangyang/simform/thermal_maze0073.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:10 /user/yangyang/simform/thermal_maze0074.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:12 /user/yangyang/simform/thermal_maze0075.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:15 /user/yangyang/simform/thermal_maze0076.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:18 /user/yangyang/simform/thermal_maze0077.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:21 /user/yangyang/simform/thermal_maze0078.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:23 /user/yangyang/simform/thermal_maze0079.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:26 /user/yangyang/simform/thermal_maze0080.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:28 /user/yangyang/simform/thermal_maze0081.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:31 /user/yangyang/simform/thermal_maze0082.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:33 /user/yangyang/simform/thermal_maze0083.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:36 /user/yangyang/simform/thermal_maze0084.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:38 /user/yangyang/simform/thermal_maze0085.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:41 /user/yangyang/simform/thermal_maze0086.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:44 /user/yangyang/simform/thermal_maze0087.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:46 /user/yangyang/simform/thermal_maze0088.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:48 /user/yangyang/simform/thermal_maze0089.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:51 /user/yangyang/simform/thermal_maze0090.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:53 /user/yangyang/simform/thermal_maze0091.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:56 /user/yangyang/simform/thermal_maze0092.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 22:58 /user/yangyang/simform/thermal_maze0093.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 23:01 /user/yangyang/simform/thermal_maze0094.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 23:04 /user/yangyang/simform/thermal_maze0095.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 23:07 /user/yangyang/simform/thermal_maze0096.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 23:10 /user/yangyang/simform/thermal_maze0097.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 23:13 /user/yangyang/simform/thermal_maze0098.e
    -rw-r--r--   3 yangyang hadoop 3630756152 2012-05-13 18:50 /user/yangyang/simform/thermal_maze0099.e

### Design points

For each of these files, we need to know which points in the parameter
space generated the file.  These are stored in a file in the local
filesystem (not in HDFS!) called `design_points.txt`.  For these 99
exodus files, the `design_points.txt` file is provided in the `sample`
directory of this package.

Each line of the file `design_points.txt` indicates the parameters
that produced one simulation.  Hence the file:

    0.5 0.5
    -0.5 0.5
    0.5 -0.5
    -0.5 -0.5
    
indicates that we should have 4 exodus files, and that 

* file 0000 used parameters (0.5,0.5)
* file 0001 used parameters (-0.5,0.5)
* file 0002 used parameters (0.5,-0.5)
* file 0003 used parameters (-0.5,-0.5)

To reiterate, each line contains white-space seperated numbers, and each
number is a single parameter used to generate the simulation.  They should
always be in the same order.

There can be more entries in the design_points.txt file than there
are exodus files, but they must all be formatted.

If you need to check for a valid `design_points.txt` file the following 
Python code must be able to read it:

    file = open('design_points.txt')
    design = []
    for line in file:
        design.append([float(s) for s in line.split()])
        
Then, `design[#]` are the parameters used to generate the # simulation file.

### New points

The `new_points.txt` file has exactly the same format as `design_points.txt`
but the interpretation is completely different.  The function of
`new_points.txt` is to specify where we should evaluate the model
in the future.  Because of the way MapReduce works, it's usually
better to specify _many_ points in new_points.  So for our simple example:

     0.4   0.4
     0.2   0.4
     0.0   0.4
    -0.2   0.4
    -0.4   0.4
     0.4   0.2
     0.2   0.2
     0.0   0.2
    -0.2   0.2
    -0.4   0.4
     0.4   0.0
     0.2   0.0
     0.0   0.0
    -0.2   0.0
    -0.4   0.0
     0.4  -0.2
     0.2  -0.2
     0.0  -0.2
    -0.2  -0.2
    -0.4  -0.2
     0.4  -0.4
     0.2  -0.4
     0.0  -0.4
    -0.2  -0.4
    -0.4  -0.4

would interpolate everything at many points inside the region
bounded by the initial exodus files.

Building a database
-------------------

The idea behind 
