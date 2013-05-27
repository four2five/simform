"""
Create a numpy typed bytes array with a prescribed
structure to test through SVD.

test-matrix-1.mseq2
test-matrix-2.mseq2
"""

import util

from hadoop.io import SequenceFile
from hadoop.io.SequenceFile import CompressionType
from hadoop.typedbytes import *

# writer = SequenceFile.createWriter(os.path.join(outdir,outputfilename),
#            TypedBytesWritable, TypedBytesWritable,compression_type=CompressionType.RECORD)
# key = TypedBytesWritable()
# value = TypedBytesWritable()
# key.set(-1)
#        value.set(xdata2)
#        writer.append(key,value)
# writer.close

from numpy import *

cm = util.CommandManager(verbose=True)

# create two files with the following config:

# file 1 has three numpy blocks
# file 2 has one numpy block, one row, and one numpy block

ncols = 4
# blocksize = -1 => single row
blocksizes = [[3,4,7],[5,-1,0,2]]
hdfsbase = 'mrmc-test/'
basename = 'test/test-matrix'

# ensure repeatability
random.seed(1)

fullmat = []

row = 1
for i, sizes in enumerate(blocksizes):
    fname = basename + '-%i.mseq2'%(i+1)
    
    writer = SequenceFile.createWriter(fname,
             TypedBytesWritable, TypedBytesWritable,compression_type=CompressionType.RECORD)
    for bsize in sizes:
        if bsize == -1:
            key = row
            row += 1
            val = random.randn(ncols).tolist()
            fullmat.append(val)
        elif bsize == 1:
            key = row
            val = random.randn(1,ncols)
            row += 1
            fullmat.append(val[0].tolist())
        else:
            key = (row, row+bsize)
            row += bsize
            val = random.randn(bsize,ncols)
            for eachrow in val:
                fullmat.append(eachrow.tolist())
                
        tbkey = TypedBytesWritable()
        tbkey.set(key)
        tbval = TypedBytesWritable()
        tbval.set(val)
        
        writer.append(tbkey,tbval)
    writer.close()
    
    cm.copy_to_hdfs(fname, hdfsbase)
    
fmat = array(fullmat)
savetxt('test/test-matrix.txt',fmat)    
