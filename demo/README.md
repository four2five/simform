In this demo, we are going to use the mrsimform codes to manipulate
a small set of Exodus files on Amazon's EC2 system.

To do so, we'll use Apache Whirr to create the Hadoop cluster on EC2.
[Here is a good intro to Whirr on Ubuntu.](http://www.evanconkle.com/2011/11/run-hadoop-cluster-ec2-easy-apache-whirr/)

1. Install whirr.  I used the version 0.7.1 after running into
problems with the default version, and 0.8

    wget http://archive.apache.org/dist/whirr/whirr-0.7.1/whirr-0.7.1.tar.gz
    tar xzvf whirr-0.7.1.tar.gz
    cd whirr-0.7.1/bin
    export PATH=`pwd`:$PATH
    
These commands only setup whirr for the current session.  So if you 
need to launch multiple command prompts, you'll need to repeat the path
addition each time.    

2. Generate a new keypair 

    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa_whirr

2. Edit mrsimform-hadoop.properties to add your EC2 credentials.  Save
this as "my-mrsimform-hadoop.properties"

3. Launch the nodes

    whirr launch-cluster --config my-mrsimform-hadoop.properties
    
4. Login to the nodes.  whirr should spit out a list of nodes when
it launches.  I just pick the first one.

    ssh -i $(HOME)/.ssh/id_rsa_whirr -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ec2-50-16-181-181.compute-1.amazonaws.com
    
5. Now see DEMO.md for how to configure the cluster and run a few commands.    
    
15. Destroy the cluster

    whirr destroy-cluster --config my-mrsimform-hadoop.properties 
    
Referenes
---------    

* <http://www.evanconkle.com/2011/11/run-hadoop-cluster-ec2-easy-apache-whirr/>
* <http://archive.cloudera.com/cdh/3/whirr/contrib/python/running-mapreduce-jobs.html>
