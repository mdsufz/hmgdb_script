### Repository of script tools for the HumanMetagenomeDB

Repository of scripts for the HumanMetagenomeDB
The Python script can be used on all Operating Systems.
Windows executable file with Aspera Download support is also provided for easy use on Windows.

#### INSTALLATION

- git clone https://github.com/mdsufz/hmgdb_script
- cd hmgdb_script

#### HMgDB DOWNLOADER USAGE
Downloads the sequencing data and outputs to the "output" directory
- python3 hmgdb_downloader.py -o output -i hmgdb_downloaded_metadata_dataset.csv

#### HMgDB DOWNLOADER USAGE USING ASPERA
Aspera Support is currently available for Linux and Windows.

- python3 hmgdb_downloader.py -o output -i hmgdb_downloaded_metadata_dataset.csv -aspera_exec /path/to/ascp -aspera_ssh /path/to/asperaweb_id_dsa.openssh

#### OPTIONS:

Usage: $ python hmgdb_downloader.py [OPTIONS]

-h        	 this help message

-o     		 < /path/to/output > 			Path to output folder. If not given, the data will be placed where the script is executed.

-i     		 < /path/to/input_csv_file > 		Path to input csv file. If not given, hmgdb_downloaded_metadata_dataset.csv is search in the location of the script.

-aspera_exec 	 < /path/to/ascp >			Provide the path to the aspera key file if you would like to download it with aspera.

-aspera_ssh 	 < /path/to/asperaweb_id_dsa.openssh >	Provide the path to the aspera key file if you would like to download it with aspera.
