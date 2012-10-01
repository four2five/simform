Installing simform
====================

Getting simform running the first time can be très-annoying!  On ubuntu, with
CDH3 on EC2, it's actually pretty painless -- see the demo directory.  
But no one who puts up real clusters seems to use Ubuntu.  

### Requirements

**All nodes**

* A recent branch of python2, say 2.6
* numpy
* pynetcdf or python-netcdf (Scientific.IO.NetCDF)
* Hadoop -- tested with CDH3, earlier prototypes tested with Hadoop 0.21
* [python-hadoop](https://github.com/hyysun/Hadoop.git) package

**Only the head node, or job submission node**

* make -- nothing special here, any version should do
* [dumbo](https://github.com/klbostee/dumbo)
* [dumbo-feathers](https://github.com/klbostee/feathers) -- this requires compiling some Java against the
  current version of Hadoop  
* A version of the JDK to compile dumbo-feathers  
* [mrjob](https://github.com/Yelp/mrjob)

**Recommended for all nodes**

* [ctypedbytes](https://github.com/klbostee/ctypedbytes) -- this makes
all the IO go faster

**Recommended for the head node**

* git

Required environment variables
-----------

One of the most common problems is forgetting to set the `HADOOP_HOME`
environment variable.  This should be set to whereever your hadoop
installation lives, e.g. /usr/lib/hadoop

Ubuntu install with CDH3
-------------

See the demo directory.

### Ubuntu 10.04 (Lucid)

**All nodes**

    sudo apt-get install python-dev python-numpy \
        python-setuptools python-netcdf \
        libatlast3gf-base
        
    sudo easy_install -z typedbytes 
    sudo easy_install ctypedbytes
    
**Head node**

*Install the easy stuff*

    sudo apt-get install git-core
    sudo easy_install -z dumbo
    
*Install MRJob*

    mkdir ~/devextern
    cd ~/devextern
    git clone https://github.com/dgleich/mrjob.git
    cd mrjob
    sudo python setup.py install
    
*Install python-hadoop locally*

    cd ~/devextern
    git clone https://github.com/hyysun/Hadoop.git
    cd Hadoop/python-hadoop
    python setup.py sdist
    sudo easy_install dist/Hadoop-0.20.tar.gz
    
You must install the same `Hadoop-0.20.tar.gz` file via
`easy_install` on all nodes -- see below.  We may be able to turn
this into an egg distribution in the future.

*Install feathers*

You must install feathers into a subdirectory of the 
current simform distribution.  Here's an example:

    cd simform/src # THIS ONLY WORKS AFTER YOU INSTALL SIMFORM!
    cd model
    git clone https://github.com/klbostee/feathers.git
    cd feathers
    sh build.sh
    cp feathers.jar ..
    
**All nodes again**

    <copy Hadoop-0.20.tar.gz from head>
    sudo easy_install Hadoop-0.20.tar.gz
    
> For these last steps, here is what I did on a test cluster for EC2:
> 
>     for node in 10.34.86.56 10.76.213.246 10.116.190.35 10.35.94.101 10.113.42.21; do
>       scp -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no  dist/Hadoop-0.2.tar.gz $node:~
>       ssh -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no $node sudo easy_install Hadoop-0.2.tar.gz
>     done
    

Redhat install with CDH3
--------------

**These were written for a different purpose, but do contain all
of the install instructions.  If you think it's easier to follow
the ubuntu instructions, you can follow them for any of the install
except for the apt-get pieces, which, obviously, don't work on Redhat.**

Here are some install instructions you can reference to meet the requirements:

On all nodes (hadoop namenode and datanodes), we should install the following packages:

    # install numpy
    wget "http://sourceforge.net/projects/numpy/files/NumPy/1.6.1/numpy-1.6.1.tar.gz/download"
    tar xfz numpy-1.6.1.tar.gz
    cd numpy-1.6.1
    python setup.py install
    cd ..

    # install ctypedbytes
    git clone https://github.com/klbostee/ctypedbytes.git
    cd ctypedbytes
    python setup.py install
    cd ..

    # install netcdf
    wget "http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-4.1.3.tar.gz" 
    tar xfz netcdf-4.1.3.tar.gz 
    cd netcdf-4.1.3 
    ./configure --with-pic --disable-dap --disable-netcdf-4 
    make 
    make install 
    make check
    cd ..

    # install pynetcdf
    wget "http://downloads.sourceforge.net/project/pylab/PyNetCDF/0.7/pynetcdf-0.7.tar.gz"
    tar xfz pynetcdf-0.7.tar.gz 
    cd pynetcdf-0.7 
    python setup.py install 
    cd ..

    # install hyy-python-hadoop
    git clone https://github.com/hyysun/Hadoop.git
    cd Hadoop
    cd pyhton-hadoop
    python setup.py install
    cd ..
    cd ..

If you have some problems about netcdf, try:
1. Place usr-local.conf in /etc/ld.so.conf.d on all nodes.
(see icme-hadoop1 /etc/ld.so.conf.d/ for the template)
2. Run ldconfig -v as root on all nodes.

We need to install the following packages on the Hadoop namenode:

    # install mrjob
    git clone https://github.com/dgleich/mrjob.git
    cd mrjob
    python setup.py install
    cd ..

    # install dumbo
    git clone https://github.com/klbostee/dumbo
    cd dumbo
    python setup.py install
    cd ..
    
2. To get dumbo feathers, run following:
git clone https://github.com/klbostee/feathers.git
cd feathers
bash build.sh

After that, move feathers.jar into your java classpath or just copy feathers.jar to src/model.
    
