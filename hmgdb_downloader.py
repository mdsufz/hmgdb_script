#!/usr/bin/python
###################################################################
#Script Name	: hmgdb_downloader.py                                                                                         
#Description	: This script takes as input a .csv table retrieved from the https://webapp.ufz.de/hmgdb/ and downloads metagenomic libraries from SRA and MGRAST                                                                                                                                          
#Author       	: Rodolfo Brizola Toscan  - https://www.ufz.de/index.php?en=43568                                            
#Email         	: rodolfo.toscan@ufz.de                                           
###################################################################
import signal
import os
import sys
import commands
import time
 
def get_input_file(hmgdb_csv_file):
	l="a"
	f=open(hmgdb_csv_file,"r")
	mgrast_list=[]
	sra_list=[]
	header=f.readline()
	while True:
		l=f.readline()
		if not l: break
		else:
			#~ print l
			id=l.split(",")[0]
			#~ print id
			if "mg" in id:
				mgrast_list.append(id)
			else:
				sra_list.append(id)
	f.close()
	#~ print sra_list
	#~ print mgrast_list
	
	return sra_list, mgrast_list

def download_ena(sra_list,output_path,dl,aspera_exec,aspera_ssh):
	#print "#\tDOWNLOADING..."#,sra_list
	log_file="wget_log_file"
	
	# if output path does not exist, creates it
	if os.path.isdir(output_path) == False:
		os.system("mkdir -p "+output_path)
	
	
	# if download is with wget, do
	if dl == "wget":
		for sra in sra_list:
			time.sleep(1)								 #  SLEEP
			signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
			if os.path.isdir(output_path+"/"+sra) == False:
				os.system("mkdir -p "+output_path+"/"+sra)
			sra=sra.replace("\"","").strip()
			if len(sra) ==12:
				time.sleep(1)								 #  SLEEP
				signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
				cmd="wget --retry-connrefused -w "+output_path+"/"+sra+"/"+"   --show-progress 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/"+sra[:6]+sra[9:12]+"/"+sra+"/*'"
				#~ cmd="wget --retry-connrefused  -a  "+log_file+"   --show-progress 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/"+sra[:6]+sra[9:12]+"/"+sra+"/*'"
				os.system(cmd)
			elif len(sra) ==11:
				time.sleep(1)								 #  SLEEP
				signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
				cmd="wget --retry-connrefused -P "+output_path+"/"+sra+"/"+"    --show-progress 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/"+sra[:6]+"/0"+sra[9:11]+"/"+sra+"/*'"
				#~ cmd="wget --retry-connrefused -a  "+log_file+" --show-progress 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/"+sra[:6]+"/0"+sra[9:11]+"/"+sra+"/*'"
				os.system(cmd)
			elif len(sra) ==10:
				time.sleep(1)								 #  SLEEP
				signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
				cmd="wget --retry-connrefused -P "+output_path+"/"+sra+"/"+"  --show-progress 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/"+sra[:6]+"/00"+sra[9:10]+"/"+sra+"/*'"
				#~ cmd="wget --retry-connrefused  -a  "+log_file+" --show-progress 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/"+sra[:6]+"/00"+sra[9:10]+"/"+sra+"/*'"
				os.system(cmd)
			elif len(sra) ==9:
				time.sleep(1)								 #  SLEEP
				signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
				cmd="wget --retry-connrefused -P "+output_path+"/"+sra+"/"+"   --show-progress 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/"+sra[:6]+"/"+sra[9:10]+"/"+sra+"/*'"
				#~ cmd="wget --retry-connrefused  -a  "+log_file+"  --show-progress 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/"+sra[:6]+"/"+sra[9:10]+"/"+sra+"/*'"
				os.system(cmd)
	
	else: # if download is with aspera, do
		for sra in sra_list:
			sra=sra.replace("\"","").strip()
			if len(sra) ==12:
				time.sleep(1)								 #  SLEEP
				signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
				cmd=aspera_exec+"  -QT -l 1000m -P33001 -i "+aspera_ssh+" era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/"+sra[:6]+sra[9:12]+"/"+sra+"/. "+output_path
				os.system(cmd)
				print cmd
			elif len(sra) ==11:
				time.sleep(1)								 #  SLEEP
				signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
				cmd=aspera_exec+"  -QT -l 1000m -P33001 -i "+aspera_ssh+" era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/"+sra[:6]+"/0"+sra[9:11]+"/"+sra+"/. "+output_path
				os.system(cmd)
				print cmd
			elif len(sra) ==10:
				time.sleep(1)								 #  SLEEP
				signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
				cmd=aspera_exec+" -QT -l 1000m -P33001 -i "+aspera_ssh+" era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/"+sra[:6]+"/00"+sra[9:10]+"/"+sra+"/. "+output_path
				os.system(cmd)
				print cmd
			elif len(sra) ==9:
				time.sleep(1)								 #  SLEEP
				signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
				cmd=aspera_exec+"  -QT -l 1000m -P33001 -i "+aspera_ssh+" era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/"+sra[:6]+"/"+sra[9:10]+"/"+sra+"/. "+output_path
				os.system(cmd)
				print cmd

	pass
				
def download_mgrast_wget(mgrast_list,mgfa,output_path):
	
	# if output path does not exist, creates it
	if os.path.isdir(output_path) == False:
		os.system("mkdir -p "+output_path)


	for mg in mgrast_list:
		print "\n\tDownloading",mg
			
		temp_out_file=output_path+"/"+mg+"/"+mg+"-temp.fq"
		final_out_file=output_path+"/"+mg+"/"+mg+".fq"
		
		if os.path.isdir(output_path+"/"+mg) == False:
			os.system("mkdir -p "+output_path+"/"+mg)
		
		cmd="curl  http://api.metagenomics.anl.gov/1/download/"+mg+"?file=050.2 -o "+temp_out_file
		status,aux=commands.getstatusoutput(cmd)
		
		check="head -n 10 "+temp_out_file+" | grep @ | wc -l " 
		status,aux=commands.getstatusoutput(check)

		if aux.strip() == '0':

			os.system("rm -rf "+temp_out_file)

			if mgfa == 'y' or mgfa == 'Y':
				next_file=aux.split("=")[-1].replace("\"}","")
				time.sleep(1)								 #  SLEEP
				signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
				cmd="curl  http://api.metagenomics.anl.gov/1/download/"+mg+"?file=299.1 -o "+output_path+"/"+mg+"/"+mg+".fa"
				os.system(cmd)
				os.system("gzip "+output_path+"/"+mg+"/"+mg+".fa")
				#~ print "Done!"
			else:
				print "     -> Raw data for "+mg+" not available. If you are interested in processed data, add the -mgfa argument as 'y'"
		else:
			os.system("mv "+temp_out_file+" "+final_out_file)
			os.system("gzip "+final_out_file)
			print "Done!"
		
def help_message():
	print "\n\tHMgDB Downloader v.1"
	print "\tUsage: $ python hmgdb_downloader.py [OPTIONS] hmgdb_downloaded_metadata_dataset.csv"
	print "\n\tOPTIONS:"
	print "\n\t-h        	 this help message"
	print "\n\t-aspera_exec 	 < /path/to/ascp >			Provide the path to the aspera key file if you would like to download it with aspera."
	print "								If not given, data will be downloaded using wget." 
	print "\n\t-aspera_ssh 	 < /path/to/asperaweb_id_dsa.openssh >	Provide the path to the aspera key file if you would like to download it with aspera."
	print "\n\t-mgfa   	 < y/n >    				Not all libraries hosted in MG-RAST's database have their raw (non QC'ed) available. "
	print "                        					Set this option to y in case you desire to have processed reads anyway. Default=n      "
	print "\n\t-o     		 < /path/to/output > 			Path to output folder. If not given, the data will be placed where the script is executed."
	print "\n\n"

def main():
	#os.system("trap \"echo Exited!; exit;\" SIGINT SIGTERM")
	

	signal.signal(signal.SIGINT, signal_handler)
	#1 ########## getting arguments
	arguments = sys.argv
	
	#2 ########## getting help
	if "-h" in arguments:								# if -h in arguments,
		help_message()									# prints help message
		sys.exit()
	
	#3 ########## set type of download
	if "-aspera_exec" in arguments:						# if -aspera_exec in arguemtns
		flag_index=arguments.index("-aspera_exec")  
		try:
			aspera_exec=arguments[flag_index+1]	
		except IndexError:
			help_message()								# if executable is given but not the key, close program and exhibit help message
			print "\n #### Please provide the path to the aspera ascp file in -aspera_exect (usually $HOME/.aspera/connect/bin/ascp). ###"		
			sys.exit()
			
		#aspera_exec=arguments[flag_index+1]				# get aspera executable path
		if "-aspera_ssh" in arguments:			   		# check for aspera ssh input
			flag_index=arguments.index("-aspera_ssh")	# get aspera ssh input
			aspera_ssh=arguments[flag_index+1]
			dl="aspera"									# if executable and key are given, set download with aspera
		else:
			help_message()								# if executable is given but not the key, close program and exhibit help message
			print "\n #### Please provide the path to the aspera SSH file in -aspera_ssh (usually $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh). ###"		
			sys.exit()
	else:					# if no aspera input is given
		dl="wget"			# set download as wget
		aspera_exec=""						
		aspera_ssh=""

	#4 ########## set output
	if "-o" in arguments:						# if -o is in arguments			
		flag_index=arguments.index("-o")	
		output_path=arguments[flag_index+1]		# set output path
	else: output_path ="." 						# if -o is not given, output in the current folder
	

	#5 ########## set if user wants fasta files in abscense of raw fastq files for MG-rast
	if "-mgfa" in arguments:					# if  -mgfa flag is in arguments
		flag_index=arguments.index("-mgfa")		
		mgfa=arguments[flag_index+1]	# y=download subsequent files 
	else:mgfa="n"						# n=nope
	
	#6 ########## check if input file is csv or tsv. if not, abort
	if "csv" not in arguments[-1] and "tsv" not in arguments[-1]:
		help_message()
		sys.exit()
		
	#7 ########## DOWNLOAD!
	else:	
		csv_file=sys.argv[-1]
		sra_list, mgrast_list = get_input_file(csv_file)
		
		
		print "\n--> HMgDB Downloader v.1"
		print " -> Starting download of",str(len(sra_list)),"libraries from ENA and",str(len(mgrast_list)),"libraries from MG-RAST"
		#~ if output_path==".": print " -> Dumping files to "
		print " -> Downloading with",dl
		#~ print "\n -> output folder
		
		if len(sra_list) > 0:
			print "\n -> Starting with SRA:"
			# DOWNLOAD SRA
			#print sra_list
			download_ena(sra_list,output_path,dl,aspera_exec,aspera_ssh)
		
		if len(mgrast_list) > 0:
			print "\n -> starting with MGRAST:"
				#~ # DOWNLOAD MGRAST
			download_mgrast_wget(mgrast_list,mgfa,output_path)
			
#os.system("trap \"echo Exited!; exit;\" SIGINT SIGTERM")

#def signal_handler(sig, frame):
#        print('You pressed Ctrl+C!')
#        sys.exit(0)

#signal.signal(signal.SIGINT, signal_handler)
#print('Press Ctrl+C')
#signal.pause()
#exit_gracefully()	
def signal_handler(signal, frame):
  sys.exit(0)

#signal.signal(signal.SIGINT, signal_handler)



main()


