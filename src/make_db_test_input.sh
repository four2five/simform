rm -f inputtest.txt
touch inputtest.txt
# in tiny, we do p =
# realization r = 1, 2, 3

for p in $(seq 1 4 64); do
  for r in $(seq 1 3); do
     i=$(($p + ($r-1)*64))
     echo hdfs://icme-hadoop1.localdomain/user/jatempl/random_media/run$i/random_media.e >> inputtest.txt
  done
done

