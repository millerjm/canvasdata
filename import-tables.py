#!/usr/bin/python
import os
import time
import dateutil
import datetime
import requests
import json
import config
import sys
import mysql.connector
import pprint
import gzip
from mysql.connector import errorcode
from dateutil import parser
from datetime import datetime
from datetime import tzinfo
from os import listdir
from os.path import isfile, join
from os import walk
from config import *
from functions import *
from cd_functions import *

print(sys.argv)
try:
    load_interval = sys.argv[1].lower()
except:
    load_interval = None
    load_int_error = "No Date Interval argument given.  Must be FULL, WEEK, or DAY."
else:
    if load_interval == 'full':
        date_diff_string = all_time_string
        print(date_diff_string)
    elif load_interval == 'week':
        date_diff_string = last_week_string
        print(date_diff_string)
    elif load_interval == 'day':
        date_diff_string = yesterday_string
        print(date_diff_string)
    else:
        load_interval = None
        load_int_error = "Invalid Command Line Argument for  Date Interval given.  Must be FULL, WEEK, or DAY."
if load_interval is not None:  
    print("Date Interval for Data Load: " + load_interval)
else:
    print(load_int_error)
    exit()
    
def main():
    start_time = datetime.now()
    try_db(canvasdata_config)
    print(source_folder)
    dir_list = generate_dir_list(source_folder)
    print(dir_list)
    for d in dir_list:  
        for p in process_list:
            if p == d:  
                #print(d)
                directory_start_time = datetime.datetime.now()
                print("Start Time for Import of " + d + ": " + directory_start_time.strftime(dt_format))
                target_folder = source_folder + "/" + d
                print(target_folder)
                file_list=generate_file_list(target_folder, d)
                file_count = 0
                for f in file_list:
                    file_count += 1
                    print ("------------------------------File " + str(file_count) + ": " + f + "----------------------------------------------")
                    dir_path = source_folder + "/" + d
                    pathname = dir_path + "/" + f
                    print(pathname)
                    table_part = str(f.split("-")[1])
                    print(table_part)
                    gz_size = os.path.getsize(pathname)
                    if gz_size != 0:
                        split_temp_dir = dir_path + '/split-temp/'
                        print(split_temp_dir)
                        split_list = process_gz_file(gz_size, pathname, f, source_folder, split_temp_dir)
                        print("Loading Split Files")
                    if table_part == 'account_dim':  	
                        split_file_count = load_account_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'role_dim':  
                        split_file_count = load_role_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)    
                    elif table_part == 'course_dim':  	
                        split_file_count = load_course_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)	
                    elif table_part == 'course_section_dim':  	
                        split_file_count = load_course_section_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)                                                                  
                    elif table_part == 'enrollment_dim':  	
                        split_file_count = load_enrollment_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)	 
                    elif table_part == 'enrollment_fact':  	
                        split_file_count = load_enrollment_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'enrollment_rollup_dim':  	
                        split_file_count = load_enrollment_rollup_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'enrollment_term_dim':
                        split_file_count = load_enrollment_term_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'external_tool_activation_dim':
                        split_file_count = load_external_tool_activation_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'external_tool_activation_fact':
                        split_file_count = load_external_tool_activation_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'group_dim':
                        split_file_count = load_group_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(split_file_count)
                    elif table_part == 'group_fact':
                        split_file_count = load_group_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'group_membership_dim':
                        split_file_count = load_group_membership_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(split_file_count)
                    elif table_part == 'group_membership_fact':
                        split_file_count = load_group_membership_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'pseudonym_dim':  
                        split_file_count = load_pseudonym_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(split_file_count)
                    elif table_part == 'pseudonym_fact':
                        split_file_count = load_pseudonym_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'user_dim':
                        split_file_count = load_user_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)  
                    elif table_part == 'course_score_dim':  	
                        split_file_count = load_course_score_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)	  
                    elif table_part == 'course_score_fact':  	
                        split_file_count = load_course_score_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)	                          
                    elif table_part == 'assignment_dim':  	
                        split_file_count = load_assignment_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'assignment_fact':  	
                        split_file_count = load_assignment_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)    
                    elif table_part == 'submission_comment_dim':  
                        split_file_count = load_submission_comment_dim(split_list, split_temp_dir, canvasdata_config, table_part)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'submission_comment_fact':
                        split_file_count = load_submission_comment_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)                        
                    elif table_part == 'submission_dim':  
                        split_file_count = load_submission_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'submission_fact':
                        split_file_count = load_submission_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'quiz_dim':  
                        split_file_count = load_quiz_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(split_file_count)
                    elif table_part == 'quiz_fact':
                        split_file_count = load_quiz_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)                        
                    elif table_part == 'discussion_entry_fact':  	
                        split_file_count = load_discussion_entry_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)	  
                    elif table_part == 'discussion_topic_fact':  	
                        split_file_count = load_discussion_topic_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)	
                    elif table_part == 'discussion_entry_dim':
                        split_file_count = load_discussion_entry_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'discussion_topic_dim':
                        split_file_count = load_discussion_topic_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'conversation_dim':  	
                        split_file_count = load_conversation_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)	
                    elif table_part == 'conversation_message_dim':  	
                        split_file_count = load_conversation_message_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'conversation_message_participant_fact':  	
                        split_file_count = load_conversation_message_participant_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)	 
                    elif table_part == 'wiki_dim':  
                        split_file_count = load_wiki_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'wiki_fact':  
                        split_file_count = load_wiki_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'wiki_page_dim':  
                        split_file_count = load_wiki_page_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)
                    elif table_part == 'wiki_page_fact':  
                        split_file_count = load_wiki_page_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string)
                        print(table_part)
                        print(split_file_count)                        
                directory_end_time = datetime.now()
                print("Start Time for Import of " + d + ": " + directory_start_time.strftime(dt_format))
                print("End Time for Import of " + d + " : " + directory_end_time.strftime(dt_format))
                directory_elapsed_time = str(directory_end_time - directory_start_time)
                print("Total Time for Import of " + d + ": " + directory_elapsed_time)
    end_time = datetime.now()
    elapsed_time = str(end_time - start_time)
    print("Start Time for Import: " + start_time.strftime(dt_format))
    print("End Time for Import: " + end_time.strftime(dt_format))
    print("Total Time for Import: " + elapsed_time)

main()
