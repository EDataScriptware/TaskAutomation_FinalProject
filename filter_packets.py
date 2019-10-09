import sys
import os
import shutil


def filter( in_filename, out_filename ) :
	infile = open(in_filename, 'r') # Open input file to read
	outfile = open(out_filename, 'w') #Open output file to write
	#firstLine = infile.readline()	
	f = open(in_filename)
	first = f.readline()	
	outfile.write(first)
	line = infile.readline() # Read the first line of the file
	# outfile.write(firstLine[0])

	# read the file until 
	while line:
	    #outfile.write(firstLine[0])
	    line = infile.readline() # this should be the summary line of the file
	    print line
	    
	    if ( line.count( 'Echo (ping) reply' ) > 0 or line.count( 'Echo (ping) request' ) > 0 ) :
		write_line = 1
		outfile.write( line + '\n' )
	    else :
		write_line = 0

	    line = infile.readline() # Read next line

            while( line.count( 'No.' ) == 0 ) :
		print line
		line = infile.readline() # read the line from the file
		# check to see if the line is empty, which indicates end of file   
		if not line :
		     break
		else :
		    line = line
		    if ( write_line == 1 ) :
			 outfile.write( line + '\n' )
	    print line
	 
	infile.close()
	outfile.close()


#Version defines as how many version are in the Node
version = 0 
#Making a new folder to insert filtered in
try:  
    os.mkdir("Filtered")
except:  
	print "File already exists"

	
#Keeps looping unless there is no other Node left (Node1, Node2, Node3, etc.)
while True:
	#Like count varialbe but "version"
	version = version + 1
	#Instantiates a new variable and overwritten each time a file is written
	packet_input_file = 'Node' + str(version) + '.txt'
	#Filtered for output
	packet_output_file = 'NodeFiltered' + str(version) + '.txt'

	#Will check to see whether the file exists or not. If it does not exist, it moves to the except. 
	try:
		
		#Reading the file
		fh = open(packet_input_file, 'r')
		#File exists and is inputted into the function where packet_output_file filtered and outputted
		filter(packet_input_file, packet_output_file )
		shutil.move(packet_output_file, 'Filtered')

	except:
	#File does not exist and will move out of the loop and program ends
		break

#END

