ssh into one of the node

ssh -i $(HOME)/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no 50.16.61.230

once there...

hadoop fs -mkdir /user/temp
hadoop fs -mkdir /user/temp/simform

# Only the temp directory has enough space
cd /mnt/tmp

mkdir scratch

cd scratch

rsync -avz mysource.computer.com:~/mydatadir/*.e scratch/

for f in `ls *.e`; do hadoop fs -put $f /user/temp/simform & ; done

Wait until these finish

Now, we need to install numpy, scipy on all nodes

'ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no dgleich@107.22.80.153'
'ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no dgleich@107.20.113.124'
'ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no dgleich@50.16.113.97'
'ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no dgleich@23.21.6.71'
'ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no dgleich@50.17.5.207'

for node in 107.22.80.153 50.17.5.207 50.16.113.97 107.20.113.124 23.21.6.71; do
  ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no dgleich@$node sudo apt-get install -y python-numpy python-scipy python-setuptools  python-netcdf python-dev libatlas3gf-base
  ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no dgleich@$node sudo easy_install typedbytes ctypedbytes 
done  

for node in 107.22.80.153 50.17.5.207 50.16.113.97 107.20.113.124 23.21.6.71; do
  ssh -i /home/dgleich/.ssh/id_rsa_whirr -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no dgleich@$node sudo apt-get install -y libatlas3gf-base
done  


Now, ssh into the head node

sudo apt-get install git-core

mkdir devextern
cd devextern

Install dumbo

    sudo easy_install -z dumbo
    
# install mrjob
git clone https://github.com/dgleich/mrjob.git
cd mrjob
sudo python setup.py install
cd ..

Now we need to get hyy-hadoop everywhere.  Check ~/.whirr/mrsimform-hadoop/instances
for the private IPs of all the nodes:

    git clone https://github.com/hyysun/Hadoop.git
    cd Hadoop
    cd python-hadoop
    python setup.py sdist

    for node in 10.34.86.56 10.76.213.246 10.116.190.35 10.35.94.101 10.113.42.21; do
      scp -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no  dist/Hadoop-0.2.tar.gz $node:~
      ssh -o "UserKnownHostsFile /dev/null" -o StrictHostKeyChecking=no $node sudo easy_install Hadoop-0.2.tar.gz
    done
    
We've got all the prereqs installed now.  We can get the new codes!    

cd ~
mkdir dev
cd dev
git clone https://github.com/hyysun/simform.git

cd simform/src

cd model

# install feathers
git clone https://github.com/klbostee/feathers.git
cd feathers
sh build.sh
cp feathers.jar ..

export HADOOP_HOME=/usr/lib/hadoop

set the following as .mrjob.conf

runners:
  hadoop:
    hadoop_home: /usr/lib/hadoop
    jobconf:
      mapreduce.task.timeout: 3600000
      mapred.task.timeout: 3600000
      mapred.reduce.tasks: 8
      mapred.child.java.opts: -Xmx2G
      
For the next step, we need the actual HDFS path. For my demo, it is:

    hdfs://ec2-107-22-80-153.compute-1.amazonaws.com:8020      
    
make setup_database name=runs variable=TEMP dir=hdfs://ec2-107-22-80-153.compute-1.amazonaws.com:8020/user/temp/simform/

make -f runs preprocess

At this point, we need to edit the output directory to enable the mapred user
to write to it

hadoop fs -chmod 777 /user/temp/simform/output

make -f runs convert timestepfile=timesteps.txt
    using normalized timesteps  20min36s

make -f runs convert
exodus2seq_output=hdfs://icme-hadoop1.localdomain/user/yangyang/simform/output/data.seq2/
    without using normalized timesteps  20min24s

make -f runs predict design=design_points.txt points=new_points.txt
    16min2s

make -f runs seq2exodus  numExodusfiles=10 OutputName=output/thermal_maze
    locally, 9min

SVD:
make -f runs seq2mseq
    map: 40min
    reduce:55min
    total:1hr35min

make -f runs model numExodusfiles=6
    full1 22min51s
    full2 1min
    full3 3min57s
    TSMatMul 3min29s
    total: 32min

