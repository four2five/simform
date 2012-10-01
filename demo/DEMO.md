Whirr-EC2 Demo
==============

This is a slightly terse guide to a quick check of our simform codes
on a Whirr-launched EC2 Hadoop cluster.

We begin where we left off in `README.md`

Configuring the cluster
-----------------------

1. ssh into one of the node

ssh -i $(HOME)/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no 50.16.61.230

2. once there, we want to create a place to put our exodus files

    hadoop fs -mkdir /user/temp
    hadoop fs -mkdir /user/temp/simform
    
3. After that's done, we need to get exodus files into the cluster.
The easiest wa to do this is to copy them into the temp directory,
and then move them:    

    # Only the temp directory has enough space for a few GB of data
    cd /mnt/tmp
    mkdir scratch
    cd scratch
    # copy them from your computer 
    rsync -avz mysource.computer.com:~/mydatadir/*.e scratch/

The final step is to load the files into HDFS

    cd scratch
    for f in `ls *.e`; do hadoop fs -put $f /user/temp/simform & ; done

Wait until these finish.  It can take a while.

4.  Meanwhile we need to install some software on all the nodes.  Using
the ip addresses in ~/.whirr/mrsimform-hadoop/instances, we can run the following
commands:

    for node in 107.22.80.153 50.17.5.207 50.16.113.97 107.20.113.124 23.21.6.71; do
      ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" \
        -o StrictHostKeyChecking=no $node \
        sudo apt-get install -y python-numpy python-scipy python-setuptools \
        python-netcdf python-dev libatlas3gf-base
      ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" \
        -o StrictHostKeyChecking=no $node \
        sudo easy_install -z typedbytes
      ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" \
        -o StrictHostKeyChecking=no $node \
        sudo easy_install ctypedbytes
    done  

This will install all the necessary software into all the nodes
**ASSUMING YOU UPDATE THE LIST OF IP ADDRESSES FOR YOUR EXAMPLE**

5. Now, ssh into the head node, and let's install some of the 
other software there.

**Basic setup**

    sudo apt-get install git-core

    cd ~
    mkdir devextern
    cd devextern

**Install dumbo**

    sudo easy_install -z dumbo
    
**Install mrjob**

    git clone https://github.com/dgleich/mrjob.git
    cd mrjob
    sudo python setup.py install
    cd ..

**Install hyy-hadoop**
Now we need to get hyy-hadoop everywhere.  
Check `~/.whirr/mrsimform-hadoop/instances`
for the private IPs of all the nodes:

    cd ~/devextern
    git clone https://github.com/hyysun/Hadoop.git
    cd Hadoop
    cd python-hadoop
    python setup.py sdist

    for node in 10.34.86.56 10.76.213.246 10.116.190.35 10.35.94.101 10.113.42.21; do
      scp -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no  dist/Hadoop-0.2.tar.gz $node:~
      ssh -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no $node sudo easy_install Hadoop-0.2.tar.gz
    done
    
6. Install simform! We've got all the prereqs installed now.  We can get the new codes!    

    cd ~
    mkdir dev
    cd dev
    git clone https://github.com/hyysun/simform.git

    cd simform/src

Except we need to install dumbo feathers    

**Install feathers**

    cd model
    git clone https://github.com/klbostee/feathers.git
    cd feathers
    sh build.sh
    cp feathers.jar ..
    
7. System setup.  Run    

    export HADOOP_HOME=/usr/lib/hadoop

and set the following as .mrjob.conf

    runners:
      hadoop:
        hadoop_home: /usr/lib/hadoop
        jobconf:
          mapreduce.task.timeout: 3600000
          mapred.task.timeout: 3600000
          mapred.reduce.tasks: 8
          mapred.child.java.opts: -Xmx2G
          
Running the codes
------------------          
          
For the next step, we need the actual HDFS path. For my demo, it is:

    hdfs://ec2-107-22-80-153.compute-1.amazonaws.com:8020      
    
1. Build the database    
    
    make setup_database name=runs variable=TEMP \
        dir=hdfs://ec2-107-22-80-153.compute-1.amazonaws.com:8020/user/temp/simform/

    make -f runs preprocess

At this point, we need to edit the output directory to enable the mapred user
to write to it

    hadoop fs -chmod 777 /user/temp/simform/output

    make -f runs convert timestepfile=timesteps.txt
        

2. Make some predictions and save exodus files

    make -f runs predict design=design_points.txt points=new_points.txt
    make -f runs seq2exodus  numExodusfiles=10 OutputName=output/thermal_maze

3. Compute the SVD

    make -f runs seq2mseq
    
    make -f runs model numExodusfiles=6
    
