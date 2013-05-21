rm -f input.txt
touch input.txt
for i in $(seq 1 256)
do 
   echo hdfs://icme-hadoop1.localdomain/user/jatempl/random_media/run$i/random_media.e >> input.txt
done

