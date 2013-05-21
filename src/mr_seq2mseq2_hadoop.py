"""
MapReduce job to compute global variance of a series of simulation runs for all node space.

Example:

python mr_seq2mseq2_hadoop.py \
hdfs://icme-hadoop1.localdomain/user/yangyang/dbsmall/data.seq/random_media/random_media*.seq \
-r hadoop --no-output -o tsqr/exodus.bseq --variable TEMP --numParas 64

"""

__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os

from mrjob.job import MRJob
from numpy import *

class MRSeq2Mseq(MRJob):

    STREAMING_INTERFACE = MRJob.STREAMING_INTERFACE_TYPED_BYTES
    
    def configure_options(self):
        """Add command-line options specific to this script."""
        super(MRSeq2Mseq, self).configure_options()
        
        self.add_passthrough_option(
            '--variable', dest='variable',
            help='--variable VAR, the variable need to compute global variance'       
        )
        
        self.add_passthrough_option(
            '--numParas', dest='numParas',
            help='--numParas INT, the number of parameters'       
        )
       
    def load_options(self, args):
        super(MRSeq2Mseq, self).load_options(args)
            
        if self.options.variable is None:
            self.option_parser.error('You must specify the --variable VAR')
        else:
            self.variable = self.options.variable
            
        if self.options.variable is None:
            self.option_parser.error('You must specify the --numParas INT')
        else:
            self.numParas = self.options.numParas
    
    def mapper(self, key, value):
        """
        input: 
          key = -1 => xcoord data
          key = -2 => ycoord data
          key = -3 => zcoord data
          key = (fset, timestep) => value = array
        output: (r,timestep,node), (param,value)
        """
        # ignore coordinate (x,y,z) data
        if (key != -1) and (key != -2) and (key != -3) : 
            for i, var in enumerate(value):
                name = var[0]
                if name == self.variable:
                    fset = int(key[0])
                    p = fset%int(self.numParas)
                    if p == 0:
                        p = int(self.numParas)
                        r = fset/int(self.numParas)
                    else:
                        r = fset/int(self.numParas) + 1
                    t = key[1]
                    for j, val in enumerate(var[1]):
                        yield (r,t,j), (p,val)
     

    def reducer(self, key, values): 
        """ 
        Each key is a (r,timestep, node) pair.  Each value is (param,value) pair.
        We want to make an array of all the values over the parameters. 
        """
        valarray = [val for val in values] # realize the 
        array = [0. for _ in xrange(len(valarray))]
        print >>sys.stderr, "key, vals", key, valarray
        for val in valarray:
            pi = val[0]
            v = val[1]
            array[pi-1] = v
            
        yield key, array  
        
    def steps(self):
        return [self.mr(self.mapper, self.reducer),]

if __name__ == '__main__':
    MRSeq2Mseq.run()
