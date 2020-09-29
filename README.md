### Repository of script tools for the HumanMetagenomeDB

Repository of scripts for the HumanMetagenomeDB

#### INSTALLATION

- git clone https://github.com/mdsufz/hmgdb_script
- cd hmgdb_script

#### HMgDB DOWNLOADER USAGE
Downloads the sequencing data and outputs to the "output" directory
- python hmgdb_downloader.py -o output -i hmgdb_downloaded_metadata_dataset.csv

#### OPTIONS:

-h               this help message
-o               < /path/to/output >                    Path to output folder. If not given, the data will be placed where the script is executed.
-i               < /path/to/input_csv_file >            Path to input csv file. If not given, hmgdb_downloaded_metadata_dataset.csv is search in the location of the script.
