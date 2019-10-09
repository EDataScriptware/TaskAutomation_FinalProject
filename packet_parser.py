import sys
import os
import shutil

# Store list of filtered text files into an array for memory
L = []

#Type "python packet_parser.py NodeFiltered*.txt parse_output*.txt"

def parse(filtered, out_parse) :

	#StreamReader
	filteredRead = open(filtered, 'r') # open all filtered texts to read
	parse_filtered = open(out_parse, 'w') # Write to each 4 parse file 
	
	line = filteredRead.readline().strip() # read the first line of the filtered text

	# read the file until
	while line :
		
		if not ( line ):
			break
		if ( line.count( 'Echo (ping) request' ) > 0 or line.count( 'Echo (ping) reply') > 0 ):
			
			tokens = line.split()
			time = tokens[1]
		
			#DO NOT DELETE THE COMMENTS TOKENS. IT HELPS US TO UNDERSTAND THE ORDER OF THE SUMMARY LINE
			# Time, Source IP, Destination IP
				#print ('1: ', tokens[1])
				#print ('2: ', tokens[2])
				#print ('3: ', tokens[3])

			# Echo (ping) Request and Reply
				#print ('6: ', tokens[6])
				#print ('7: ', tokens[7])
				#print ('8: ', tokens[8])
	
			# Sequence, Frame Length, and TTL
				#print ('10: ', tokens[10])
				#print ('5: ', tokens[5])
				#print ('11: ', tokens[11])

			# remove 'seq=' from tokens[10]
			seqString = tokens[10]
			seq2 = seqString[4:]
			seq3tokens = seq2.split('/')
			find_seq = seq3tokens[0]

			# remove 'ttl=' string from tokens[11]
			ttlString = tokens[11]
			ttl2 = ttlString[4:]
			find_ttl = ttl2
			
			# remove 'Echo(ping)' from tokens[6]
			echo_ping_string = tokens[6] + tokens[7] + tokens[8]
			echo_ping = echo_ping_string[10:]
			find_echo_ping = echo_ping
			#print "Test here : " + find_echo_ping
			parse_filtered.write( tokens[1] + ',' + tokens[2] + ',' + tokens[3] + ',' + find_echo_ping + ',' + find_seq + ',' + tokens[5] + ',' + find_ttl )
	
			parse_filtered.write( '\n' )

		line = filteredRead.readline() # .strip() # Read the next line

	print line


	filteredRead.close()
	parse_filtered.close()

parse_version = 0	

while True: 

	parse_version = parse_version + 1

	in_filename = 'NodeFiltered' + str(parse_version) + '.txt'

	out_filename = 'Parse' + str(parse_version) + '.csv'
		
	try: 
			
		fh = open(in_filename, 'r')

		parse(in_filename, out_filename)

	except: 
		break
