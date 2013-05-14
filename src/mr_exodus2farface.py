"""
MapReduce job to extract the far-face of the random media simulations
and output it to a simple text file for further processing.

History
-------
:2013-05-11: Initial version

Example(on ICME Hadoop):

python mr_exodus2farface.py hdfs://icme-hadoop1.localdomain/user/yangyang/simform/input.txt \
-r hadoop  --variables TEMP \
--timestepfile timesteps.txt  --python-archive simform-deploy.tar.gz 

"""

__author__ = 'David F. Gleich <dgleich@purdue.edu> and Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from subprocess import call, check_call

from mrjob.compat import get_jobconf_value
from mrjob.job import MRJob

import exopy2 as ep

from hadoop.io import SequenceFile
from hadoop.io.SequenceFile import CompressionType
from hadoop.typedbytes import *

def extract_farface(inputfile, fset, variables):
    
    print >>sys.stderr, "Converting %s"%(inputfile)
    f = ep.ExoFile(inputfile,'r')
        
    Vars = variables.split(',')
    
    # Get time data and coordinate (x,y,z) data
    time = f.cdf.variables["time_whole"]
    timedata = list(time.getValue())
    coordz = f.cdf.variables["coordz"]
    zdata = list(coordz.getValue())
    coordy = f.cdf.variables["coordy"]
    ydata = list(coordy.getValue())
    coordx = f.cdf.variables["coordx"]
    xdata = list(coordx.getValue())
    
    normalized_timesteps = timedata
    total_time_steps = len(normalized_timesteps)
    
    # Get variable data
    varnames = f.node_variable_names()
    vardata = []
    for i, var in enumerate(Vars):
        vdata = None
        vindex = None
        for vi,n in enumerate(varnames):
            if n == var.strip():
                #vtemp = vi
                vindex = vi
                break
        if vindex == None:
            print  >> sys.stderr, 'The variable ', var.strip(), 'does not exist!'
            sys.exit(-1)
        tmp = f.vars['vals_nod_var'+str(vindex+1)]
        tmpdata = tmp.getValue()
        vardata.append((var.strip(), tmpdata))
        
    
    #for ti in xrange(total_time_steps):    
    ti = total_time_steps-1 # las time step only
    print >>sys.stderr, "Converting %s timestep %i"%(inputfile, ti)
    for m, var in enumerate(vardata):
        name = var[0]
        data = var[1]
        
        for vj, x in enumerate(xdata):
            if x < -0.09993:
                # fset posind posy posz timeind time varind var
                yield fset, "%i\t%.18e\t%.18e\t%i\t%.18e\t%i\t%.18e"%(
                    vj, ydata[vj], zdata[vj], ti, normalized_timesteps[ti],
                    m, data[ti][vj])
    
class MRExodus2Farface(MRJob):

    MRJob.HADOOP_INPUT_FORMAT = 'org.apache.hadoop.mapred.lib.NLineInputFormat'
    
    def configure_options(self):
        """Add command-line options specific to this script."""
        super(MRExodus2Farface, self).configure_options()
        
        self.add_passthrough_option(
            '--variables', dest='variables',
            help='--variables VARS, Only output the variables in the comma delimited list'       
        )
        
    def load_options(self, args):
        super(MRExodus2Farface, self).load_options(args)
        
        if self.options.variables is None:
            self.option_parser.error('You must specify the --variables VARS')
        else:
            self.variables = self.options.variables
       
            
    def filename2fset(self, path):
        """ Convert a filename into a file-set number by finding the first 
        number in the path starting from the filename. 

        If we cannot find a path in the filename, return -1
        Any non-negative number returned indicates we found a file-set number
        """
        fdir,fname = os.path.split(path)
        if len(fname) == 0 and len(fdir) == 0:
            return -1
        fsetnum=''
        for i,c in enumerate(fname):
            if c.isdigit():
                fsetnum+=c
        if len(fsetnum) > 0:
            return int(fsetnum)
        else:
            return self.filename2fset(fdir)
    
    def mapper(self, _, line):
        print >>sys.stderr, "processing file %s"%(line) 
        # step 0: strip off unexpected characters
        line = line.split('\t')[1]
        # step 1: fetch the exodus file from Hadoop cluster
        file = os.path.basename(line)
        localfile = os.path.join('./', file)
        if os.path.isfile(localfile):
            call(['rm', localfile])
        
        print >>sys.stderr, "copying %s to %s"%(line, localfile) 
        check_call(['hadoop', 'fs', '-copyToLocal', line, localfile])

        # step 1a: determine its fset num
        fsetno = self.filename2fset(line)
        print >>sys.stderr, "fsetno = %i"%(fsetno)
                
        for key,val in extract_farface(localfile, 
                        fsetno, self.variables):
            yield key, val

        print >>sys.stderr, "removing localfile %s"%(localfile)
        check_call(['rm',localfile])

def test(inputfile,variable):
    for key,val in extract_farface(inputfile, -1,  variable):
        print "%i\t%s"%(key, val)
 
        
if __name__ == '__main__':
    MRExodus2Farface.run()
