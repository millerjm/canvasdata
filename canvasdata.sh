#!/bin/bash
today=`date +"%Y-%m-%d"`
echo $today
now=`date +"%Y-%m-%d_%H%M"`
echo $now
log_dir="/usr/local/github-millerjm/canvasdata_downloaded_2/canvasdata/logs/"
log_ext=".txt"
filename="$log_dir$today$log_ext"
echo $filename
#runs the files needed for starfish first, and then any other tables we want to load
#copy of data-fetch with just starfish-related files enabled
bash /usr/local/github-millerjm/canvasdata_downloaded_2/canvasdata/data-fetch_sf.sh | tee -a $filename
python /usr/local/github-millerjm/canvasdata_downloaded_2/canvasdata/import-tables.py full  | tee -a $filename
python /usr/local/github-millerjm/canvasdata_downloaded_2/canvasdata/run-starfish-queries_login.py | tee -a $filename

#updates Peoplesoft with our last_login date for starfish
#python /usr/local/canvasdata/ps/ps_lda_all_local_login.py 2191 saprd full | tee -a $filename


#gets the other files that we didn't get for starfish.  
bash /usr/local/github-millerjm/canvasdata_downloaded_2/canvasdata/data-fetch.sh | tee -a $filename
python /usr/local/github-millerjm/canvasdata_downloaded_2/canvasdata/import-tables.py week  | tee -a $filename
python /usr/local/github-millerjm/canvasdata_downloaded_2/canvasdata/run-queries.py | tee -a $filename
