Common Problems
===============


1. The HDFS path should be as the following format: 
hdfs://namenodehost/user/username.  If it isn't like this,
we always run into problems.  You can _try_ and see if
hdfs:///user/username
will work (i.e. implicit host), but most often, this causes
other problems.

2. Check that the `HADOOP_HOME` environment variable is set correctly.

3. Make sure you install dumbo with `easy_install -z dumbo` otherwise,
it won't be able to find itself and you'll get errors on `import dumbo`

