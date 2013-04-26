"""
MapReduce job 

python mr_outputvar_hadoop.py \
hdfs://icme-hadoop1.localdomain/user/yangyang/simform/output/data.var/p* \
-r hadoop --no-output -o output --variable TEMP_VAR \
--outputname = global_var
--outdir = hdfs://icme-hadoop1.localdomain/user/yangyang/simform/output/var/
--indir = hdfs://icme-hadoop1.localdomain/user/yangyang/simform/

"""

__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from mrjob.job import MRJob
from mrjob.compat import get_jobconf_value

import exopy2 as ep
import numpy as np
from subprocess import call, check_call, Popen, PIPE, STDOUT

def insert_vars(source, destination, varNames, varVals):
    #Copy all dims for new exofile creation
	for d in source.cdf.dimensions.keys():
		if d == 'time_step':
			destination.cdf.createDimension('time_step', source.cdf.dimensions['time_step'])
		elif d == 'num_nod_var':
		    pass
			#destination.cdf.createDimension(d,0)
		else:
			length = source.cdf.dimensions[d]
			destination.cdf.createDimension(d,length)
	
	# put in new variable values
	for (index,value) in enumerate(varVals):
	    name = varNames[index]
        tmp = destination.cdf.createVariable(name,('d'),('num_nodes',))
        tmp.assignValue(value)
        #destination.cdf.variables[name].assignValue(value)
	
	# Copy all variables for new exofile creation
	for var in source.cdf.variables.keys():
		if 'vals_nod_var' in var:
			pass
		elif var == 'name_nod_var':
			pass
		elif var == 'time_whole':
			getvar= source.cdf.variables[var]
			vardata = getvar.getValue()
			var1 = destination.cdf.createVariable(var,(getvar.typecode()),(getvar.dimensions))
			var1.assignValue(vardata)
		elif source.cdf.variables[var].dimensions[0] == 'time_step': # NOTE assume all time dimensions are in first dimension
			continue
		else:
			getvars = source.cdf.variables[var]
			vardata = getvars.getValue()
			thisvar= source.cdf.variables[var]
			vartype  = thisvar.typecode()
			var1 = destination.cdf.createVariable(var,(vartype) ,(thisvar.dimensions))
			var1.assignValue(vardata)	
			attList = dir(thisvar)
			newattlist=[]
			for i in range(len(attList)):
				if attList[i] == 'assignValue':
					pass
				elif attList[i] == 'getValue':
					pass
				elif attList[i] == 'typecode':
					pass
				else:
					newattlist.append(attList[i])
			for a in newattlist:
				attData = getattr(thisvar,a)
				setattr(var1, a, attData)
				
	# copy remaining attributes
	newattlist=[]
	for attr in dir(source.cdf):
		if attr not in dir(destination.cdf):
			newattlist.append(attr)
	for attr in newattlist:
		attData = getattr(source.cdf,attr)
		setattr(destination.cdf, attr, attData)
		
	return 0

class MROutputExodus(MRJob):

    STREAMING_INTERFACE = MRJob.STREAMING_INTERFACE_TYPED_BYTES
    JOBCONF = {'mapred.child.java.opts':'-Xmx8GB'}
    
    def configure_options(self):
        """Add command-line options specific to this script."""
        super(MROutputExodus, self).configure_options()
        
        self.add_passthrough_option(
            '--variable', dest='variable',
            help='--variable VAR, the variable need to be inserted in the exodus file'       
        )
        self.add_passthrough_option(
            '--outputname', dest='outputname',
            help='--outputname NAME, the name of created new interpolation exodus file'       
        )
        self.add_passthrough_option(
            '--outdir', dest='outdir',
            help='--outdir DIR, Write the output to the directory DIR'       
        )
        self.add_passthrough_option(
            '--indir', dest='indir',
            help='--indir DIR, The HDFS directory you can get the template exodus file '       
        )
    
       
    def load_options(self, args):
        super(MROutputExodus, self).load_options(args)
            
        if self.options.variable is None:
            self.option_parser.error('You must specify the --variable VAR')
        else:
            self.variable = self.options.variable
        
        if self.options.outputname is None:
            self.option_parser.error('You must specify the --outputname NAME')
        else:
            self.outputname = self.options.outputname
            
        if self.options.outdir is None:
            self.option_parser.error('You must specify the --outdir DIR')
        else:
            self.outdir = self.options.outdir
            
        if self.options.indir is None:
            self.option_parser.error('You must specify the --indir DIR')
        else:
            self.indir = self.options.indir
    

    def mapper(self, key, value):     
        """
        input: index, valarray
        output: fnum, (index, valarray)
        """
        fnum = -1
        yield fnum, (key, value)
                
        
    def reducer(self, key, values):
        """
        input: -1, (index, valarray)
        output: global variance exodus file
        """
        
        val_order = {}
        
        for i, value in enumerate(values):
            val_order[value[0]]=value[1]
            
            
        val = [ ]  
        for k,value in sorted(val_order.iteritems()):
            val.extend(value)
        val2 = np.array(val)
        
        # grab template exodus file from HDFS
        
        tmpstr = self.indir[7:]
        index = tmpstr.find('/')
        prefix = 'hdfs://'+tmpstr[0:index]
        
        cmd = 'hadoop fs -ls '+ self.indir
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        content = p.stdout.read()
        files = content.split('\n')
        
        flag = True

        for file in files:
            file = file.split(' ')
            fname = file[len(file)-1]
            if fname.endswith('.e'):
                fname = prefix + fname
                if flag:
                    check_call(['hadoop', 'fs', '-copyToLocal', fname, 'template.e'])
                    flag = False
                    break
        
        template = 'template.e'
        
        # create new interpolation exodus file
        
        if call(['test', '-e', template]) != 0:
            print >>sys.stderr,  "The template file doesnot exist!"
            yield key,1
        else: 
        
            print >>sys.stderr,  "Reading templatefile %s"%(template)
            templatefile = ep.ExoFile(template,'r')
            
            outfile = self.outputname+'.e'
            print >>sys.stderr, "Writing outputfile %s"%(os.path.join(outfile))
            newfile = ep.ExoFile(os.path.join(outfile),'w')  
            
            result = insert_vars(templatefile, newfile, (self.variable,), (val2,))
            
            #templatefile.change_nodal_vars2(newfile, time, (self.variable, ), (val,), ('d',))
            
            newfile.cdf.sync() 
            newfile.cdf.close()
            
            print >>sys.stderr, "Finished writing data, copying to Hadoop"
            
            user = get_jobconf_value('mapreduce.job.user.name')
            call(['hadoop', 'fs', '-copyFromLocal', outfile, os.path.join(self.outdir,outfile)])
            call(['hadoop', 'fs', '-chown', '-R', user, os.path.join(self.outdir)])
            
            print >>sys.stderr, "Copied to Hadoop, removing ..."
            
            call(['rm', template])
            call(['rm', outfile])
            yield key,0
            
            print >>sys.stderr, "Done"
        
        

if __name__ == '__main__':
    MROutputExodus.run()
