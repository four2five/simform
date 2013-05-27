#hadoop fs -mkdir mrmc-test
#mkdir test

#python generate_mseq2_test.py

python run_full_tsqr.py --input=mrmc-test/test-matrix-?.mseq2 --output=mrmc-test/test-matrix-svd \
   --ncols=4 --svd=3 --hadoop=/usr/lib/hadoop --local_output=test-mrmc \
   --schedule=2,2,2
   
hadoop fs -get mrmc-test/test-matrix-svd_3/part-* test/

python hyy-python-hadoop/examples/SequenceFileReader.py test/part-00000
python hyy-python-hadoop/examples/SequenceFileReader.py test/part-00001

# compare to SVD of test/test-matrix.txt 
