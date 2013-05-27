#hadoop fs -mkdir mrmc-test
#mkdir test

#python generate_mseq2_test.py

python run_full_tsqr.py --input=mrmc-test/test-matrix-* --output=mrmc-test/ \
   --ncols=4 --svd=2 --hadoop=/usr/lib/hadoop --local_output=test 
