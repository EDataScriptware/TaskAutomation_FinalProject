import sys

def compute(in_filename, out_filename) :
	#Declare a list object
	L = []
	TTL_sum = 0
	echo_requests_sent = 0
	echo_requests_received = 0
	echo_replies_sent = 0
	echo_replies_received = 0
	
	# Counting Bytes 
	echo_request_bytes_sent = 0
	echo_request_bytes_received = 0
	
	echo_request_data_sent = 0
	echo_request_data_receieved = 0
	
	# Average RTT in millisecond
	average_RTT = 0	
	# Echo Request Throughput (kB/sec) 	
	echo_req_throughput = 0.0 
	# Echo Request Goodput (kB/sec)
	echo_req_goodput = 0.0	
	# Average Reply Delay (us)
	avg_reply_delay = 0.0	
	# Average Echo Request Hop Count
	avg_echo_req_hop_count = 0.0
	avg_echo_req_hop_countTotal = 0

	request_timestamp = 0
	request_ts = 0.0
	step = 129
	avgRTT = 0
	math = 0
	counterTTL = 0
	
	reqTTL = 0
	rplTTL = 0

	total_TTL = 0
	counter = 0
	
	total_start_time = 0
	total_end_time = 0
	

	# Takes in parsed text OR csv file to read 
	infile = open(in_filename, 'r') # Open input file to read
	outfile = open(out_filename, 'w') # Write the info to an output file
	
	with open(in_filename) as f:
		for line in f:

			# UPDATE APRIL 24: Parsed file uses .CSV so split() includes a comma to split all fields
			# Append all rows in Parsed text file into the List L 		
			L.append(line.split(','))

		# For loop into the list iterating through elements, line by line
		# Loop starts at the rangerequest_timestamp between 0 and ends at 354,
		# len(L) returns the number of items in the list L, which is 354
		for i in range(0, len(L)):
			counter = counter + 1
			#print L[i]
			#print str(i+1)+":"+str(L[i-1])+ " \n" 

			# 1
			# Checks if Source IP Address equals to Node 1 IP (2nd column) & is equal to request (4th column) 
			# Counts all requests sent that match those criteria			
			if( L[i][1] == "192.168.100.1" ) and ( L[i][3] == "request" ) : 
				echo_requests_sent += 1 
			# 2
			# Checks if Source IP Address == Node 1 IP  and ICMP Type is == "reply"  
			# Counts all replies received that match those criteria		
			if L[i][1] == "192.168.100.1" and L[i][3] == "reply"  : 
				echo_requests_received += 1
			# 3
			# Checks if Dest IP Address == Node 1 IP and ICMP Type is == "request" 
			if L[i][2] == "192.168.100.1" and L[i][3] == "request":
				echo_replies_sent += 1
			# 4
			# Checks if Dest IP == Node 1 IP  and ICMP Type == "reply"
			# Then count all replies that match this criteria
			if L[i][2] == "192.168.100.1" and L[i][3] == "reply":
				echo_replies_received += 1
			# 5
			# Echo Request Bytes Sent Calculation
			# Checks if ICMP Type == "request" & Destination IP not == Node 1 IP	
			# Then adds all the bytes from the Frame Length column
			if L[i][3] == "request" and L[i][2] != "192.168.100.1":
				echo_request_bytes_sent += int(L[i][5])				
				
			# 6
			# Echo Request Bytes Received Calculation
			# Checks if Source IP == Node 1 IP Address and ICMP type == "reply"
			# Then add all the bytes from the Frame Length column
			if L[i][1] == "192.168.100.1"  and L[i][3] == "reply": 
				echo_request_bytes_received += int(L[i][5])			

			#7
			if L[i][3] == "request" and L[i][1] == "192.168.100.1" :
				echo_request_data_sent += (int(L[i][5]) -42) 
					
			#8
			if L[i][3] == "reply" and L[i][1] == "192.168.100.1" :
				echo_request_data_receieved += (int(L[i][5]) -42) 
			#9 -- 
			if L[i][3] == "request":
				request_timestamp = float(L[i][0])
			else:
				average_RTT += (float(L[i][0]) - request_timestamp)
		
			#12
			if L[i][3] == "request" and L[i][1] == "192.168.100.1":
				total_start_time += float(L[i][0])

			if L[i][3] == "reply" and L[i][2] == "192.168.100.1":
				total_end_time += float(L[i][0])

			if L[i][3] == "reply" and (L[i][2] == "192.168.100.1" or L[i][2] == "192.168.100.2"):
				# Average Reply Delay (us)	
				total_TTL += float(L[i][6])


			#13 -- User "TTL (Time to Live") field to accomplish this task.	
			

			if L[i][3] == "request" and L[i][2] == "192.168.100.1":
				avg_echo_req_hop_countTotal += int(L[i][6])				
				avg_echo_req_hop_count += int(L[i][6]) # Number of packets in output file to find an average.
				counterTTL = counterTTL + 1

				avg_echo_req_hop_count = float(((avg_echo_req_hop_count/counterTTL) /1.375))
				
		# avgRTT variable applies to #9, which is shown above			
		avgRTT = float(str(average_RTT/echo_requests_sent*1000)[:-9])

		#testing alternate way
		total_delay = total_end_time - total_start_time  
		average_RTT2 = float(total_delay / 128 * 1000)

		
		#10	
		#echo_req_throughput = round(float(echo_request_bytes_sent / average_RTT) / 1000)
		echo_req_throughput = round((float(echo_request_bytes_sent / total_delay) / 1000),1)
		#11
		#echo_req_goodput = round(float(echo_request_data_sent / average_RTT) /1000)
		echo_req_goodput = round((float(echo_request_data_sent / total_delay) /1000),1)


		print ''
		print "Echo Requests Sent \t\t", echo_requests_sent 		#1
		print "Echo Requests Received \t\t", echo_requests_received 	#2	
		print "Echo Replies Sent  \t\t", echo_replies_sent 		#3	
		print "Echo Replies Received \t\t", echo_replies_received 	#4	
		print "Echo Request Bytes Sent \t", echo_request_bytes_sent 	#5	
		print "Echo Request Bytes Received\t", echo_request_bytes_received #6	
		print "Echo Request Data Sent \t\t", echo_request_data_sent 	#7
		print "Echo Request Data Received \t" , echo_request_data_receieved #8
		print ""	
		print "Average RTT (ms)	\t", float(str(total_delay / 128 * 1000)[:-9])			#9
		print "Echo Request Throughput(kB/sec)", echo_req_throughput    #10	
		print "Echo Request Goodput (kB/sec) \t", echo_req_goodput 	#11
		print "Average Reply Delay (us) \t", round((total_TTL / counter), 2)	#12
		print ''
		print "Average Echo Request Hop Count \t", round(float(avg_echo_req_hop_count), 2) #13	
		print ''
	

	

		# Write into new CSV file

		
		linew = ("Node_Computed " + "\n\n" 
		+ "Echo Requests Sent \t" + "Echo Requests Received \t" + "Echo Replies Sent  \t" + "Echo Replies Received \t" 
		+ "\n" +str(echo_requests_sent) + "," + str(echo_requests_received) + "," + str(echo_replies_sent) + "," + str(echo_replies_received) + ","
		+ "\n Echo Request Bytes Sent \t" + "Echo Request Data Sent \t" +"\n" 
		+ str(echo_request_bytes_sent)  + "," + str(echo_request_data_sent) + ","
		+ "\n Echo Request Bytes Received\t" + "Echo Request Data Received \t" +"\n" 
		+ str(echo_request_bytes_received) + "," + str(echo_request_data_receieved)  + ","
		+ "\n"  
		+ "\n Average RTT (ms) \t" + str(avgRTT)
		+ "\n Echo Request Throughput(kB/sec) \t" + str(echo_req_throughput) 
		+ "\n Echo Request Goodput (kB/sec) \t" + str(echo_req_goodput) 
		+ "\n Average Reply Delay (microseconds) \t" + str(round((total_TTL / counter), 2))
		+ "\n Average Echo Request Hop Count \t" + str(round(float(avg_echo_req_hop_count), 2)))

	outfile.write(linew)
	
	f.close()
	
	outfile.close() # Close the file for writing
	
comp_version = 0	

while True: 

	comp_version = comp_version + 1

	in_filename = 'Parse' + str(comp_version) + '.csv'

	out_filename = 'compute_output.csv'
		
	try: 
			
		fh = open(in_filename, 'r')

		compute(in_filename, out_filename)

	except: 
		break
	


# Takes in the file name as an argument on the console
#in_filename = sys.argv[1]
# Passes the fileName
#compute(in_filename, out_filename)
