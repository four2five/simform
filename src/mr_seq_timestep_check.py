"""
MapReduce job to output the set of all time-steps and the number of 
simulations for each timestep

Example:

python mr_seq_timestep_check.py \
hdfs://icme-hadoop1.localdomain/user/yangyang/simform/output2/data/thermal_maze00*/thermal_*.seq \
-r hadoop --no-output 

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
       
    def load_options(self, args):
        super(MRSeq2Mseq, self).load_options(args)
            
        if self.options.variable is None:
            self.option_parser.error('You must specify the --variable VAR')
        else:
            self.variable = self.options.variable
    
    def mapper(self, key, value):
        """
        input: 
          key = -1 => xcoord data
          key = -2 => ycoord data
          key = -3 => zcoord data
          key = (fset, timestep) => value = array
        output: key = timestep, value = simulation number
        """
        # ignore coordinate (x,y,z) data
        if (key != -1) and (key != -2) and (key != -3) : 
            for i, var in enumerate(value):
                name = var[0]
                if name == self.variable:
                    p = int(key[0])
                    t = key[1]
                    yield t, p
     

    def reducer(self, key, values): 
        """ 
        Each key is a timestep pair.  Each value is sim-number pair.
        We want to make an array of all sim-numbers for each timestep
        """
        valarray = [val for val in values] # realize the 
        valarray.sort()
        yield key, valarray
        
        
        
    def steps(self):
        return [self.mr(self.mapper, self.reducer),]

if __name__ == '__main__':
    MRSeq2Mseq.run()

