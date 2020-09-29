#!/usr/bin/python
###################################################################
#Script Name	: hmgdb_downloader.py                                                                                         
#Description	: This script takes as input a .csv table retrieved from the https://webapp.ufz.de/hmgdb/ and downloads metagenomic libraries from SRA and MGRAST                                                                                                                                          
#Author       	: Rodolfo Brizola Toscan  - https://www.ufz.de/index.php?en=43568                                            
#Email         	: rodolfo.toscan@ufz.de                                           
###################################################################
# modified by Alexander Bartholomäus
# abarth@gfz-potsdam.de
# 
### changes / improvements compared to Rodolfos script: 
#  - use Python3 (tested with 3.5.5)
#  - use Python libs instead of system commands to run on all OperatingSystems especially Windows
#  - some optimization and parameter checks
#
### building
# 1) install all used modules + pyinstaller module, e.g. via pip install modules1, ..., pyinstaller 
# 2) build: pyinstaller --onefile --workpath workingDir hmgdb_downloader_exe.py
### execution
# 1) by click on exe: place hmgdb_selected_dataset...csv to same folder as exe, output folder in same folder as exe
# 2) via command line: parameter option for input and output are possible
###################################################################

import signal
import os
import sys
import time
from urllib.request import urlopen
from urllib.request import urlretrieve
import re

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

# find file names among list of strings
def find_files(string):
	split = re.split(r"[\s ]",string)
	matches = [s for s in split if "fastq" in s]
	
	return matches

# download SRA/ENA
def download_ena(sra_list,output_path):

	# if output path does not exist, creates it
	if os.path.isdir(output_path) == False:
		os.mkdir(output_path)
	output_path_sra = os.path.join(output_path,'SRA')
	if os.path.isdir(output_path_sra) == False:
		os.mkdir(output_path_sra)

	# process each SRA entry
	for sra in sra_list:
		time.sleep(1)								 #  SLEEP
		signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
		sra=sra.replace("\"","").strip()
		# check if output folder exists
		if os.path.isdir(os.path.join(os.getcwd(),output_path_sra, sra)) == False:
			os.mkdir(os.path.join(os.getcwd(),output_path_sra, sra))
		# parse different ENA FTP structure for file download	
		if len(sra) ==12:
			signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
			down_path = 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/'+sra[:6]+sra[9:12]+"/"+sra+"/"
		elif len(sra) ==11:
			signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
			down_path = 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/'+sra[:6]+"/0"+sra[9:11]+"/"+sra+"/"
		elif len(sra) ==10:
			signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
			down_path =  'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/'+sra[:6]+"/00"+sra[9:10]+"/"+sra+"/"
		elif len(sra) ==9:
			signal.signal(signal.SIGINT, signal_handler) # CTRL C SIGNAL HANDLER
			down_path = 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/'+sra[:6]+"/"+sra[9:10]+"/"+sra+"/"
		# status print
		print('     processing folder '+down_path)			
		# find files	
		urlpath = urlopen(down_path)
		string = urlpath.read().decode('UTF8')
		down_files = find_files(string)
		# download
		for f in down_files:
			print('      file: '+f) 
			urlretrieve(down_path+'/'+f, os.path.join(output_path_sra, sra, f))

	# Status		
	print("ENA/SRA download done!")

# MGRast		
def download_mgrast(mgrast_list, output_path, mgfa):
	
	# if output path does not exist, creates it
	if os.path.isdir(output_path) == False:
		os.mkdir(output_path)
	output_path_mg = os.path.join(output_path,'MGRast')
	if os.path.isdir(output_path_mg) == False:
		os.mkdir(output_path_mg)

	# process each MGRast entry
	for mg in mgrast_list:
		mg = mg.replace("\"","").strip()
		print("      Downloading "+mg)
		
		# check if output folder exists
		mg_out = mg.replace('.','_')
		if os.path.isdir(os.path.join(output_path_mg, mg_out)) == False:
			os.mkdir(os.path.join(output_path_mg, mg_out))
		
		# try download raw or alternative (fna) file 
		try:
			urlretrieve("https://api.metagenomics.anl.gov/1/download/"+mg+"?file=050.2", os.path.join(output_path_mg, mg_out, mg+'.fq'))
		except:
			if mgfa == 'y':
				try:
					print('      Raw file not found. Trying alternative file fna.')
					urlretrieve("https://api.metagenomics.anl.gov/1/download/"+mg+"?file=299.1", os.path.join(output_path_mg, mg_out, mg+'.fa'))
				except:
					print('        No raw and no alternative file found!')
			else:
				print('        raw file not found.')
	# Status		
	print("MGRast download done!")
			
		
def help_message():
    print("\n\tHMgDB Downloader v.1")
    print("\tUsage: $ python hmgdb_downloader.py [OPTIONS]")
    print("\n\tOPTIONS:")
    print("\n\t-h        	 this help message")
    print("\n\t-o     		 < /path/to/output > 			Path to output folder. If not given, the data will be placed where the script is executed.")
    print("\n\t-i     		 < /path/to/input_csv_file > 			Path to input csv file. If not given, hmgdb_downloaded_metadata_dataset.csv is search in the location of the script.")
    print("\n\n")

def signal_handler(signal, frame):
  sys.exit(0)

def get_download_file(file_list):
	matches = [s for s in file_list if "hmgdb_selected_dataset" in s]
	if len(matches)>0:
		matches.sort()
		matches.reverse()
		return(matches[0])
	else:
		('\nNo input file found. Please put the file with name starting with hmgdb_selected_dataset... into the same directory as the hmgdb_downloader_exe and execute again.')
		input('\n\nPress Enter to exit...')	
		sys.exit()


def main():
	# status
	print("\n--> HMgDB Downloader - Windows exe - v.1")
	
	# check interupt
	signal.signal(signal.SIGINT, signal_handler)
	
	#1 ########## getting arguments
	arguments = sys.argv
	
	#2 ########## getting help
	if "-h" in arguments:								# if -h in arguments,
		help_message()									# prints help message
		sys.exit()

	#3 ########## set output
	if "-o" in arguments:						# if -o is in arguments			
		flag_index=arguments.index("-o")	
		output_path=arguments[flag_index+1]		# set output path
		#print('\nOutdir: '+output_path)
	else: output_path = os.path.join(os.getcwd(),'output') 						# if -o is not given, output in the current folder
	
	#4 ########## set if user wants fasta files in abscense of raw fastq files for MG-rast
	mgfa_in = input('\nFetching processed files from MGRast when raw data is not available? Please type Yes[default]/No:  ')
	if mgfa_in.lower() == 'y' or mgfa_in.lower() == 'yes' or mgfa_in == '':
		mgfa = 'y'
		print('\n -> Trying processed MGRast data if raw data is not available')
	else:
		mgfa = 'n'
		print('\n -> Fetching only raw data from MGRast')
	
	#5 ########## check if input file is given or in known format in same dir
	if "-i" in arguments:
		flag_index=arguments.index("-i")		
		infile=arguments[flag_index+1]
		if not os.path.exists(infile):
			print('\nNo input file: '+infile+' found!')
			input('\n\nPress Enter to exit...')	
	else:
		files = os.listdir(os.getcwd()) # get files in current folder in known format
		infile = get_download_file(files) # select newest
		if len(infile)==0:
			print('\nNo input file found! Please put the file with name starting with hmgdb_selected_dataset... into the same directory as the hmgdb_downloader_exe and execute again.')
			input('\n\nPress Enter to exit...')	
	print('\n -> Using input file: '+infile)	

	#6 ########## DOWNLOAD!	
	sra_list, mgrast_list = get_input_file(infile)
	#print(sra_list)
	

	if len(sra_list) == 0 and len(mgrast_list) == 0:
		print("\n ! No file to download, please check the content of the input file: "+infile)
		input('\nPress Enter to exit...')
	else:
		print(" -> Starting download of "+str(len(sra_list))+" libraries from ENA and "+str(len(mgrast_list))+" libraries from MG-RAST")
		print("\n ->  Writing to folder: "+output_path)	
		# DOWNLOAD SRA
		if len(sra_list) > 0:
			print("\n -> Starting with SRA:")
			download_ena(sra_list, output_path)
		# DOWNLOAD MGRAST
		if len(mgrast_list) > 0:
			print("\n -> Starting with MGRAST:")
			download_mgrast(mgrast_list, output_path, mgfa)
		
		# input to close
		input('\nDownload completed! Press Enter to exit...')

# main function
main()


