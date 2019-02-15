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
from datetime import tzinfo
from os import listdir
from os.path import isfile, join
from os import walk
import pytz
from config import *

def get_timestamp_string():
    data_timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    return data_timestamp

def try_db(config):
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("Connection Test Successful")
        cnx.close()

def utcnow_tz():  
    return datetime.now(tz=pytz.utc)

def generate_dir_list(source_folder):
    dir_list = os.listdir(source_folder)
    dir_list.sort()
    return dir_list

def generate_file_list(table_folder, dir_name):
    print("starting generate_file_list")
    file_list = []
    for f in os.listdir(source_folder + "/" + dir_name):
        if f != "schema.json":
            file_ext =  f[-3:]
            if file_ext  == ".gz":
                if os.path.getsize(source_folder + "/" + dir_name + "/" + f) > 0:
                    lower_f = f.lower()
                    file_list.append(lower_f)
    file_list.sort()
    return file_list

def sort_temp_table(db_config, table_part, primary_key):
    cnx = mysql.connector.connect(**db_config)
    query = "ALTER TABLE temp_" + table_part + " ORDER BY " + str(primary_key) + " ASC"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def truncate_temp_table(db_config, table_part):
    #print("truncate temp table function")
    cnx = mysql.connector.connect(**db_config)
    query = "TRUNCATE TABLE temp_" + table_part
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def generate_split_file_list(source_folder):
    file_list = []
    for f in os.listdir(source_folder):
        if os.path.getsize(source_folder + "/" + f) > 0:
            lower_f = f.lower()
            file_list.append(lower_f)
    file_list.sort()
    print(file_list)
    return file_list

def process_gz_file(gz_size, pathname, unzipped_file_name, source_folder, split_temp_dir):
        print(gz_size)
        unzipped_file_path = ungzip_file(pathname)
        print(unzipped_file_path)
        unzipped_file_name = str(unzipped_file_name[:-3])
        print(unzipped_file_name)
        large_csv_file = split_temp_dir + unzipped_file_name
        #print("Moving unzipped file to split_temp: " + large_csv_file)
        os.rename(unzipped_file_path, large_csv_file)
        #print("Deleting original gz file")
        os.remove(pathname)
        #print("Splitting into rows of 50K with numeric suffix: " + large_csv_file)
        split_csv_file(large_csv_file)
        #print("Deleting:" + large_csv_file)
        os.remove(large_csv_file)
        split_list = generate_split_file_list(split_temp_dir)
        return split_list

def ungzip_file(pathname):
    in_file = gzip.open(pathname, 'rb')
    out_pathname = pathname[:-3]
    #print(out_pathname)
    out_file = open(out_pathname, 'wb')
    out_file.write( in_file.read() )
    in_file.close()
    out_file.close()
    return out_pathname

def split_csv_file(csv_file):
    #print(csv_file)
    split_command = 'split -l 10000 -d -a4 ' + csv_file + ' ' + csv_file + '-'
    #print(split_command)
    os.system(split_command)

#============================TABLE FUNCTIONS=================================#

def load_account_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_account_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_account_dim(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_account_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_account_dim (id, canvas_id, name, depth, workflow_state, parent_account, parent_account_id, grandparent_account, grandparent_account_id, root_account, root_account_id, subaccount1, subaccount1_id, subaccount2, subaccount2_id, subaccount3, subaccount3_id, subaccount4, subaccount4_id, subaccount5, subaccount5_id, subaccount6, subaccount6_id, subaccount7, subaccount7_id, subaccount8, subaccount8_id, subaccount9, subaccount9_id, subaccount10, subaccount10_id, subaccount11, subaccount11_id, subaccount12, subaccount12_id, subaccount13, subaccount13_id, subaccount14, subaccount14_id, subaccount15, subaccount15_id, sis_source_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_account_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, name, depth, workflow_state, parent_account, parent_account_id, grandparent_account, grandparent_account_id, root_account, root_account_id, subaccount1, subaccount1_id, subaccount2, subaccount2_id, subaccount3, subaccount3_id, subaccount4, subaccount4_id, subaccount5, subaccount5_id, subaccount6, subaccount6_id, subaccount7, subaccount7_id, subaccount8, subaccount8_id, subaccount9, subaccount9_id, subaccount10, subaccount10_id, subaccount11, subaccount11_id, subaccount12, subaccount12_id, subaccount13, subaccount13_id, subaccount14, subaccount14_id, subaccount15, subaccount15_id, sis_source_id, '" + str(data_timestamp) + "' from temp_account_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE name=t.name, depth=t.depth, workflow_state=t.workflow_state, parent_account=t.parent_account, parent_account_id=t.parent_account_id, grandparent_account=t.grandparent_account, grandparent_account_id=t.grandparent_account_id, root_account=t.root_account, root_account_id=t.root_account_id, subaccount1=t.subaccount1, subaccount1_id=t.subaccount1_id, subaccount2=t.subaccount2, subaccount2_id=t.subaccount2_id, subaccount3=t.subaccount3, subaccount3_id=t.subaccount3_id, subaccount4=t.subaccount4, subaccount4_id=t.subaccount4_id, subaccount5=t.subaccount5, subaccount5_id=t.subaccount5_id, subaccount6=t.subaccount6, subaccount6_id=t.subaccount6_id, subaccount7=t.subaccount7, subaccount7_id=t.subaccount7_id, subaccount8=t.subaccount8, subaccount8_id=t.subaccount8_id, subaccount9=t.subaccount9, subaccount9_id=t.subaccount9_id, subaccount10=t.subaccount10, subaccount10_id=t.subaccount10_id, subaccount11=t.subaccount11, subaccount11_id=t.subaccount11_id, subaccount12=t.subaccount12, subaccount12_id=t.subaccount12_id, subaccount13=t.subaccount13, subaccount13_id=t.subaccount13_id, subaccount14=t.subaccount14, subaccount14_id=t.subaccount14_id, subaccount15=t.subaccount15, subaccount15_id=t.subaccount15_id, sis_source_id=t.sis_source_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_assignment_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_assignment_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_assignment_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_assignment_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_dim (id, canvas_id, course_id, title, description, due_at, unlock_at, lock_at, points_possible, grading_type, submission_types, workflow_state, created_at, updated_at, peer_review_count, peer_reviews_due_at, peer_reviews_assigned, peer_reviews, automatic_peer_reviews, all_day, all_day_date, could_be_locked, grade_group_students_individually, anonymous_peer_reviews, muted, assignment_group_id, position, visibility, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_assignment_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, course_id, title, @dummy, due_at, unlock_at, lock_at, points_possible, grading_type, submission_types, workflow_state, created_at, updated_at, peer_review_count, peer_reviews_due_at, peer_reviews_assigned, peer_reviews, automatic_peer_reviews, all_day, all_day_date, could_be_locked, grade_group_students_individually, anonymous_peer_reviews, muted, assignment_group_id, position, visibility, '" + str(data_timestamp) + "' from temp_assignment_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "

    query3 = "ON DUPLICATE KEY UPDATE course_id=t.course_id, title=t.title, due_at=t.due_at, unlock_at=t.unlock_at, lock_at=t.lock_at, points_possible=t.points_possible, grading_type=t.grading_type, submission_types=t.submission_types, workflow_state=t.workflow_state, created_at=t.created_at, updated_at=t.updated_at, peer_review_count=t.peer_review_count, peer_reviews_due_at=t.peer_reviews_due_at, peer_reviews_assigned=t.peer_reviews_assigned, peer_reviews=t.peer_reviews, automatic_peer_reviews=t.automatic_peer_reviews, all_day=t.all_day, all_day_date=t.all_day_date, could_be_locked=t.could_be_locked, grade_group_students_individually=t.grade_group_students_individually, anonymous_peer_reviews=t.anonymous_peer_reviews, muted=t.muted, assignment_group_id=t.assignment_group_id, position=t.position, visibility=t.visibility, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_assignment_dim_body(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "_body(SELECT "
    query2 = "id, description, '" + str(data_timestamp) + "' from temp_assignment_dim t where description is not null) "
    query3 = "ON DUPLICATE KEY UPDATE description=t.description, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_assignment_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_assignment_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'assignment_id')
        insert_assignment_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_assignment_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_fact (assignment_id, course_id, course_account_id, enrollment_term_id, points_possible, peer_review_count, assignment_group_id, external_tool_id, @dummy)"
    print(query)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_assignment_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "assignment_id, course_id, course_account_id, enrollment_term_id, points_possible, peer_review_count, assignment_group_id, external_tool_id,'" + str(data_timestamp) + "' from temp_assignment_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE course_id=t.course_id, course_account_id=t.course_account_id, enrollment_term_id=t.enrollment_term_id, points_possible=t.points_possible, peer_review_count=t.peer_review_count, assignment_group_id=t.assignment_group_id, external_tool_id=t.external_tool_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    print(query)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_assignment_group_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
	sf_path = split_temp_dir + sf
	insert_assignment_group_dim_temp(canvasdata_config, sf_path, table_part)
	sort_temp_table(canvasdata_config, table_part, 'id')
	insert_assignment_group_dim(canvasdata_config, table_part, date_diff_string)
	truncate_temp_table(canvasdata_config, table_part)
	os.remove(sf_path)
    return split_file_count

def insert_assignment_group_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_group_dim (id, canvas_id, course_id, name, default_assignment_name, workflow_state, position, created_at, updated_at, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	
	
def insert_assignment_group_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, course_id, name, default_assignment_name, workflow_state, position, created_at, updated_at, '" + str(data_timestamp) + "' from temp_assignment_group_dim t  where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE course_id=t.course_id, name=t.name, default_assignment_name=t.default_assignment_name, workflow_state=t.workflow_state, position=t.position, created_at=t.created_at, updated_at=t.updated_at, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()
    
def load_assignment_group_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
	sf_path = split_temp_dir + sf
	insert_assignment_group_fact_temp(canvasdata_config, sf_path, table_part)
	sort_temp_table(canvasdata_config, table_part, 'id')
	insert_assignment_group_fact(canvasdata_config, table_part)
	truncate_temp_table(canvasdata_config, table_part)
	os.remove(sf_path)
    return split_file_count

def insert_assignment_group_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_group_fact (assignment_group_id, course_id, group_weight, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	
	
def insert_assignment_group_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "assignment_group_id, course_id, group_weight, '" + str(data_timestamp) + "' from temp_assignment_group_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE course_id=t.course_id, group_weight=t.group_weight, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    
    
def load_assignment_group_rule_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_assignment_group_rule_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_assignment_group_rule_dim(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_assignment_group_rule_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_group_rule_dim (assignment_group_id, drop_lowest, drop_highest, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	
	
def insert_assignment_group_rule_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "assignment_group_id, drop_lowest, drop_highest, '" + str(data_timestamp) + "' from temp_assignment_group_rule_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE drop_lowest=t.drop_lowest, drop_highest=t.drop_highest, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    
    
def load_assignment_group_score_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_assignment_group_score_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_assignment_group_score_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_assignment_group_score_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_group_score_dim (score_id, canvas_id, assignment_group_id, enrollment_id, created_at, updated_at, workflow_state, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	
	
def insert_assignment_group_score_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "score_id, canvas_id, assignment_group_id, enrollment_id, created_at, updated_at, workflow_state, '" + str(data_timestamp) + "' from temp_assignment_group_score_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE assignment_group_id=t.assignment_group_id, enrollment_id=t.enrollment_id, created_at=t.created_at, updated_at=t.updated_at, workflow_state=t.workflow_state, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    
    
def load_assignment_group_score_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_assignment_group_score_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_assignment_group_score_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_assignment_group_score_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_group_score_fact (score_id, canvas_id, account_id, course_id, assignment_group_id, enrollment_id, current_score, final_score, muted_current_score, muted_final_score, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	
	
def insert_assignment_group_score_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "score_id, canvas_id, account_id, course_id, assignment_group_id, enrollment_id, current_score, final_score, muted_current_score, muted_final_score, '" + str(data_timestamp) + "' from temp_assignment_group_score_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE account_id=t.account_id, course_id=t.course_id, assignment_group_id=t.assignment_group_id, enrollment_id=t.enrollment_id, current_score=t.current_score, final_score=t.final_score, muted_current_score=t.muted_current_score, muted_final_score=t.muted_final_score, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    
    
def load_assignment_override_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_assignment_override_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_assignment_override_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_assignment_override_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_override_dim (id, canvas_id, assignment_id, course_section_id, group_id, quiz_id, all_day, all_day_date, assignment_version, created_at, due_at, due_at_overridden, lock_at, lock_at_overridden, set_type, title, unlock_at, unlock_at_overridden, updated_at, quiz_version, workflow_state, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	
	
def insert_assignment_override_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, has_attachments, has_media_objects, subject, course_id, group_id, account_id, '" + str(data_timestamp) + "' from temp_assignment_override_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE assignment_id=t.assignment_id, course_section_id=t.course_section_id, group_id=t.group_id, quiz_id=t.quiz_id, all_day=t.all_day, all_day_date=t.all_day_date, assignment_version=t.assignment_version, created_at=t.created_at, due_at=t.due_at, due_at_overridden=t.due_at_overridden, lock_at=t.lock_at, lock_at_overridden=t.lock_at_overridden, set_type=t.set_type, title=t.title, unlock_at=t.unlock_at, unlock_at_overridden=t.unlock_at_overridden, updated_at=t.updated_at, quiz_version=t.quiz_version, workflow_state=t.workflow_state, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    
    
def load_assignment_override_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_assignment_override_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_assignment_override_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_assignment_override_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_override_fact (assignment_override_id, account_id, assignment_id, assignment_group_id, course_id, course_section_id, enrollment_term_id, group_id, group_category_id, group_parent_account_id, nonxlist_course_id, quiz_id, group_wiki_id, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	

def insert_assignment_override_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "assignment_override_id, account_id, assignment_id, assignment_group_id, course_id, course_section_id, enrollment_term_id, group_id, group_category_id, group_parent_account_id, nonxlist_course_id, quiz_id, group_wiki_id, '" + str(data_timestamp) + "' from temp_assignment_override_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE account_id=t.account_id, assignment_id=t.assignment_id, assignment_group_id=t.assignment_group_id, course_id=t.course_id, course_section_id=t.course_section_id, enrollment_term_id=t.enrollment_term_id, group_id=t.group_id, group_category_id=t.group_category_id, group_parent_account_id=t.group_parent_account_id, nonxlist_course_id=t.nonxlist_course_id, quiz_id=t.quiz_id, group_wiki_id=t.group_wiki_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_assignment_override_user_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_assignment_override_user_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_assignment_override_user_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_assignment_override_user_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_override_user_dim (id, canvas_id, assignment_id, assignment_override_id, quiz_id, user_id, created_at, updated_at, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	

def insert_assignment_override_user_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, assignment_id, assignment_override_id, quiz_id, user_id, created_at, updated_at, '" + str(data_timestamp) + "' from temp_assignment_override_user_dim t  where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE assignment_id=t.assignment_id, assignment_override_id=t.assignment_override_id, quiz_id=t.quiz_id, user_id=t.user_id, created_at=t.created_at, updated_at=t.updated_at, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_assignment_override_user_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_assignment_override_user_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_assignment_override_user_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_assignment_override_user_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_override_user_fact (assignment_override_user_id, account_id, assignment_group_id, assignment_id, assignment_override_id, course_id, enrollment_term_id, quiz_id, user_id, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	

def insert_assignment_override_user_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "assignment_override_user_id, account_id, assignment_group_id, assignment_id, assignment_override_id, course_id, enrollment_term_id, quiz_id, user_id, '" + str(data_timestamp) + "' from temp_assignment_override_user_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE account_id=t.account_id, assignment_group_id=t.assignment_group_id, assignment_id=t.assignment_id, assignment_override_id=t.assignment_override_id, course_id=t.course_id, enrollment_term_id=t.enrollment_term_id, quiz_id=t.quiz_id, user_id=t.user_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()   

def load_assignment_override_user_rollup_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_assignment_override_user_rollup_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_assignment_override_user_rollup_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_assignment_override_user_rollup_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_override_user_rollup_fact (assignment_id, assignment_override_id, assignment_override_user_adhoc_id, assignment_group_id, course_id, course_account_id, course_section_id, enrollment_id, enrollment_term_id, group_category_id, group_id, group_parent_account_id, group_wiki_id, nonxlist_course_id, quiz_id, user_id, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	

def insert_assignment_override_user_rollup_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "assignment_id, assignment_override_id, assignment_override_user_adhoc_id, assignment_group_id, course_id, course_account_id, course_section_id, enrollment_id, enrollment_term_id, group_category_id, group_id, group_parent_account_id, group_wiki_id, nonxlist_course_id, quiz_id, user_id, '" + str(data_timestamp) + "' from temp_assignment_override_user_rollup_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE assignment_id=t.assignment_id, assignment_override_user_adhoc_id=t.assignment_override_user_adhoc_id, assignment_group_id=t.assignment_group_id, course_id=t.course_id, course_account_id=t.course_account_id, course_section_id=t.course_section_id, enrollment_id=t.enrollment_id, enrollment_term_id=t.enrollment_term_id, group_category_id=t.group_category_id, group_id=t.group_id, group_parent_account_id=t.group_parent_account_id, group_wiki_id=t.group_wiki_id, nonxlist_course_id=t.nonxlist_course_id, quiz_id=t.quiz_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_assignment_rule_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_assignment_rule_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_assignment_rule_dim(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_assignment_rule_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_assignment_rule_dim (assignment_id, drop_rule, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	

def insert_assignment_rule_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "assignment_id, drop_rule, '" + str(data_timestamp) + "' from temp_assignment_rule_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE drop_rule=t.drop_rule, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_conversation_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_conversation_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_conversation_dim(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_conversation_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_conversation_dim (id, canvas_id, has_attachments, has_media_objects, subject, course_id, group_id, account_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_conversation_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, has_attachments, has_media_objects, subject, course_id, group_id, account_id, '" + str(data_timestamp) + "' from temp_conversation_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE has_attachments=t.has_attachments, has_media_objects=t.has_media_objects, subject=t.subject, course_id=t.course_id, group_id=t.group_id, account_id=t.account_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_conversation_message_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        #print(sf_path)
        insert_conversation_message_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_conversation_message_dim(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_conversation_message_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_conversation_message_dim (id, canvas_id, conversation_id, author_id, created_at, generated, has_attachments, has_media_objects, @dummy, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	
	
def insert_conversation_message_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, conversation_id, author_id, created_at, generated, has_attachments, has_media_objects, body, '" + str(data_timestamp) + "' from temp_conversation_message_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE conversation_id=t.conversation_id, author_id=t.author_id, created_at=t.created_at, generated=t.generated, has_attachments=t.has_attachments, has_media_objects=t.has_media_objects, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()  

def insert_conversation_message_dim_body(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "_body(SELECT "
    query2 = "id, body, '" + str(data_timestamp) + "' from temp_conversation_message_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE body=t.body, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()      
    
def load_conversation_message_participant_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_conversation_message_participant_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'conversation_message_id, user_id')
        insert_conversation_message_participant_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_conversation_message_participant_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_conversation_message_participant_fact (conversation_message_id, conversation_id, user_id, course_id, @dummy, @dummy, group_id, @dummy, enrollment_rollup_id, message_size_bytes, message_character_count, message_word_count, message_line_count, data_timestamp, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	
	
def insert_conversation_message_participant_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT IGNORE INTO " + table_part + "(SELECT "
    query2 = "conversation_message_id, conversation_id, user_id, course_id, enrollment_term_id, course_account_id, group_id, account_id, enrollment_rollup_id, message_size_bytes, message_character_count, message_word_count, message_line_count, '" + str(data_timestamp) + "' from temp_conversation_message_participant_fact t ) "
    query = query1 + query2
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    
    
def load_course_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_course_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_course_dim(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count
	
def insert_course_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    #not loading syllabus at all
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_course_dim (id, canvas_id, root_account_id, account_id, enrollment_term_id, name, code, type, created_at, start_at, conclude_at, publicly_visible, sis_source_id, workflow_state, @dummy, wiki_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	
    
def insert_course_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, root_account_id, account_id, enrollment_term_id, name, code, type, created_at, start_at, conclude_at, publicly_visible, sis_source_id, workflow_state, @dummy, wiki_id, '" + str(data_timestamp) + "' from temp_course_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE root_account_id=t.root_account_id, account_id=t.account_id, enrollment_term_id=t.enrollment_term_id, name=t.name, code=t.code, type=t.type, created_at=t.created_at, start_at=t.start_at, conclude_at=t.conclude_at, publicly_visible=t.publicly_visible, sis_source_id=t.sis_source_id, workflow_state=t.workflow_state, wiki_id=t.wiki_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()
    
def insert_course_dim_body(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "_body(SELECT "
    query2 = "id, syllabus_body, '" + str(data_timestamp) + "' from temp_course_dim t where syllabus_body is not null) "
    query3 = "ON DUPLICATE KEY UPDATE syllabus_body=t.syllabus_body, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    
       
def load_course_score_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_course_score_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'score_id')
        insert_course_score_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_course_score_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_course_score_dim (score_id, canvas_id, enrollment_id, created_at, updated_at, workflow_state, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	
	
def insert_course_score_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "score_id, canvas_id, enrollment_id, created_at, updated_at, workflow_state, '" + str(data_timestamp) + "' from temp_course_score_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE enrollment_id=t.enrollment_id, created_at=t.created_at, updated_at=t.updated_at, workflow_state=t.workflow_state, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_course_score_fact (split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_course_score_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'score_id')
        insert_course_score_fact (canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_course_score_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_course_score_fact  (score_id, canvas_id, account_id, course_id, enrollment_id, current_score, final_score, muted_current_score, muted_final_score, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_course_score_fact (db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "score_id, canvas_id, account_id, course_id, enrollment_id, current_score, final_score, muted_current_score, muted_final_score, '" + str(data_timestamp) + "' from temp_course_score_fact  t ) "
    query3 = "ON DUPLICATE KEY UPDATE account_id=t.account_id, course_id=t.course_id, enrollment_id=t.enrollment_id, current_score=t.current_score, final_score=t.final_score, muted_current_score=t.muted_current_score, muted_final_score=t.muted_final_score, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_course_section_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_course_section_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_course_section_dim(canvasdata_config, table_part, date_diff_string)
        insert_course_section_term_tbl(canvasdata_config, 'course_section_term_tbl', date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_course_section_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_course_section_dim (id, canvas_id, name, course_id, enrollment_term_id, default_section, accepting_enrollments, can_manually_enroll, start_at, end_at, created_at, updated_at, workflow_state, restrict_enrollments_to_section_dates, nonxlist_course_id, sis_source_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_course_section_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, name, course_id, enrollment_term_id, default_section, accepting_enrollments, can_manually_enroll, start_at, end_at, created_at, updated_at, workflow_state, restrict_enrollments_to_section_dates, nonxlist_course_id, sis_source_id, '" + str(data_timestamp) + "' from temp_course_section_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE name=t.name, course_id=t.course_id, enrollment_term_id=t.enrollment_term_id, default_section=t.default_section, accepting_enrollments=t.accepting_enrollments, can_manually_enroll=t.can_manually_enroll, start_at=t.start_at, end_at=t.end_at, created_at=t.created_at, updated_at=t.updated_at, workflow_state=t.workflow_state, restrict_enrollments_to_section_dates=t.restrict_enrollments_to_section_dates, nonxlist_course_id=t.nonxlist_course_id, sis_source_id=t.sis_source_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def insert_course_section_term_tbl(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "t.id as section_id,  t.canvas_id as canvas_section_id, t.sis_source_id as sis_section_id, t.name as section_name, t.default_section, t.accepting_enrollments, t.start_at as section_start_at, t.end_at as section_end_at, t.workflow_state as section_workflow_state, t.restrict_enrollments_to_section_dates, t.nonxlist_course_id, c.id as course_id, c.canvas_id as canvas_course_id, c.sis_source_id as sis_course_id, c.account_id as course_account_id, c.name as course_name, c.code as course_code, c.created_at as course_created_at, c.start_at as course_start_at, c.conclude_at as course_conclude_at, c.publicly_visible as course_publicly_visible, c.workflow_state as course_workflow_state, etd.id as enrollment_term_id, etd.canvas_id as canvas_term_id, etd.sis_source_id as sis_term_id, etd.name as term_name, etd.date_start as term_date_start, etd.date_end as term_date_end, '" + str(data_timestamp) + "' from temp_course_section_dim t LEFT JOIN `course_dim` `c` ON `t`.`course_id` = `c`.`id`    left join enrollment_term_dim etd on c.enrollment_term_id = etd.id where DATEDIFF(updated_at, '" + date_diff_string + "') > 0  and (`t`.`workflow_state` <> 'deleted')  and t.sis_source_id IS NOT NULL and t.sis_source_id like '2%-%'  and etd.sis_source_id  like '2%-%' )"
    query3 = "ON DUPLICATE KEY UPDATE canvas_section_id=t.canvas_id, sis_section_id=t.sis_source_id, section_name=t.name, default_section=t.default_section, accepting_enrollments=t.accepting_enrollments, section_start_at=t.start_at, section_end_at=t.end_at, section_workflow_state=t.workflow_state, restrict_enrollments_to_section_dates=t.restrict_enrollments_to_section_dates, nonxlist_course_id=t.nonxlist_course_id, course_id=c.id, canvas_course_id=c.canvas_id, sis_course_id=c.sis_source_id, course_account_id=c.account_id, course_name=c.name, course_code=c.code,course_created_at=c.created_at, course_start_at=c.start_at, course_conclude_at=c.conclude_at, course_publicly_visible=c.publicly_visible, course_workflow_state=c.workflow_state, enrollment_term_id=etd.id, canvas_term_id=etd.canvas_id, sis_term_id=etd.sis_source_id, term_name=etd.name, term_date_start=etd.date_start, term_date_end=etd.date_end, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()      

def load_discussion_entry_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_discussion_entry_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_discussion_entry_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_discussion_entry_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    #message text not being loaded
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_discussion_entry_dim (id, canvas_id, @dummy, workflow_state, created_at, updated_at, deleted_at, depth, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_discussion_entry_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, message, workflow_state, created_at, updated_at, deleted_at, depth, '" + str(data_timestamp) + "' from temp_discussion_entry_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE message=t.message, workflow_state=t.workflow_state, created_at=t.created_at, updated_at=t.updated_at, deleted_at=t.deleted_at, depth=t.depth, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_discussion_entry_dim_body(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "_body(SELECT "
    query2 = "id, message, '" + str(data_timestamp) + "' from temp_discussion_entry_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE message=t.message, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_discussion_entry_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_discussion_entry_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'discussion_entry_id')
        insert_discussion_entry_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_discussion_entry_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_discussion_entry_fact (discussion_entry_id, parent_discussion_entry_id, user_id, topic_id, course_id, enrollment_term_id, course_account_id, topic_user_id, topic_assignment_id, topic_editor_id, enrollment_rollup_id, message_length, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_discussion_entry_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "discussion_entry_id, parent_discussion_entry_id, user_id, topic_id, course_id, enrollment_term_id, course_account_id, topic_user_id, topic_assignment_id, topic_editor_id, enrollment_rollup_id, message_length, '" + str(data_timestamp) + "' from temp_discussion_entry_fact t) "
    query3 = "ON DUPLICATE KEY UPDATE discussion_entry_id=t.discussion_entry_id, parent_discussion_entry_id=t.parent_discussion_entry_id, user_id=t.user_id, topic_id=t.topic_id, course_id=t.course_id, enrollment_term_id=t.enrollment_term_id, course_account_id=t.course_account_id, topic_user_id=t.topic_user_id, topic_assignment_id=t.topic_assignment_id, topic_editor_id=t.topic_editor_id, enrollment_rollup_id=t.enrollment_rollup_id, message_length=t.message_length, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_discussion_topic_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_discussion_topic_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_discussion_topic_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_discussion_topic_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    #message text not being loaded
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_discussion_topic_dim (id, canvas_id, title, @dummy, type, workflow_state, last_reply_at, created_at, updated_at, delayed_post_at, posted_at, deleted_at, discussion_type, pinned, locked, course_id, group_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_discussion_topic_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, title, @dummy, type, workflow_state, last_reply_at, created_at, updated_at, delayed_post_at, posted_at, deleted_at, discussion_type, pinned, locked, course_id, group_id, '" + str(data_timestamp) + "' from temp_discussion_topic_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE title=t.title, type=t.type, workflow_state=t.workflow_state, last_reply_at=t.last_reply_at, created_at=t.created_at, updated_at=t.updated_at, delayed_post_at=t.delayed_post_at, posted_at=t.posted_at, deleted_at=t.deleted_at, discussion_type=t.discussion_type, pinned=t.pinned, locked=t.locked, course_id=t.course_id, group_id=t.group_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_discussion_topic_dim_body(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "_body(SELECT "
    query2 = "id, message, '" + str(data_timestamp) + "' from temp_discussion_topic_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE message=t.message, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_discussion_topic_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_discussion_topic_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'discussion_topic_id')
        insert_discussion_topic_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_discussion_topic_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_discussion_topic_fact (discussion_topic_id, course_id, enrollment_term_id, course_account_id, user_id, assignment_id, editor_id, enrollment_rollup_id, message_length, group_id, group_parent_course_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_discussion_topic_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "discussion_topic_id, course_id, enrollment_term_id, course_account_id, user_id, assignment_id, editor_id, enrollment_rollup_id, message_length, group_id, group_parent_course_id, '" + str(data_timestamp) + "' from temp_discussion_topic_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE course_id=t.course_id, enrollment_term_id=t.enrollment_term_id, course_account_id=t.course_account_id, user_id=t.user_id, assignment_id=t.assignment_id, editor_id=t.editor_id, enrollment_rollup_id=t.enrollment_rollup_id, message_length=t.message_length, group_id=t.group_id, group_parent_course_id=t.group_parent_course_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_enrollment_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_enrollment_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_enrollment_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_enrollment_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_enrollment_dim (id, canvas_id, root_account_id, course_section_id, role_id, type, workflow_state, created_at, updated_at, start_at, end_at, completed_at, self_enrolled, sis_source_id, course_id, user_id, last_activity_at, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_enrollment_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, root_account_id, course_section_id, role_id, type, workflow_state, created_at, updated_at, start_at, end_at, completed_at, self_enrolled, sis_source_id, course_id, user_id, last_activity_at, '" + str(data_timestamp) + "' from temp_enrollment_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE root_account_id=t.root_account_id, course_section_id=t.course_section_id, role_id=t.role_id, type=t.type, workflow_state=t.workflow_state, created_at=t.created_at, updated_at=t.updated_at, start_at=t.start_at, end_at=t.end_at, completed_at=t.completed_at, self_enrolled=t.self_enrolled, sis_source_id=t.sis_source_id, course_id=t.course_id, user_id=t.user_id, last_activity_at=t.last_activity_at, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_enrollment_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_enrollment_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'enrollment_id')
        insert_enrollment_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_enrollment_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_enrollment_fact (enrollment_id, user_id, course_id, enrollment_term_id, course_account_id, course_section_id, computed_final_score, computed_current_score, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_enrollment_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "enrollment_id, user_id, course_id, enrollment_term_id, course_account_id, course_section_id, computed_final_score, computed_current_score, '" + str(data_timestamp) + "' from temp_enrollment_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE user_id=t.user_id, course_id=t.course_id, enrollment_term_id=t.enrollment_term_id, course_account_id=t.course_account_id, course_section_id=t.course_section_id, computed_final_score=t.computed_final_score, computed_current_score=t.computed_current_score, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_enrollment_rollup_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_enrollment_rollup_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_enrollment_rollup_dim(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_enrollment_rollup_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_enrollment_rollup_dim (id, user_id, course_id, enrollment_count, role_count, base_role_count, account_admin_role_count, teacher_enrollment_role_count, designer_enrollment_role_count, ta_enrollment_role_count, student_enrollment_role_count, observer_enrollment_role_count, account_membership_role_count, no_permissions_role_count, account_admin_enrollment_id, teacher_enrollment_enrollment_id, designer_enrollment_enrollment_id, ta_enrollment_enrollment_id, student_enrollment_enrollment_id, observer_enrollment_enrollment_id, account_membership_enrollment_id, no_permissions_enrollment_id, most_privileged_role, least_privileged_role, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_enrollment_rollup_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, user_id, course_id, enrollment_count, role_count, base_role_count, account_admin_role_count, teacher_enrollment_role_count, designer_enrollment_role_count, ta_enrollment_role_count, student_enrollment_role_count, observer_enrollment_role_count, account_membership_role_count, no_permissions_role_count, account_admin_enrollment_id, teacher_enrollment_enrollment_id, designer_enrollment_enrollment_id, ta_enrollment_enrollment_id, student_enrollment_enrollment_id, observer_enrollment_enrollment_id, account_membership_enrollment_id, no_permissions_enrollment_id, most_privileged_role, least_privileged_role, '" + str(data_timestamp) + "' from temp_enrollment_rollup_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE user_id=t.user_id, course_id=t.course_id, enrollment_count=t.enrollment_count, role_count=t.role_count, base_role_count=t.base_role_count, account_admin_role_count=t.account_admin_role_count, teacher_enrollment_role_count=t.teacher_enrollment_role_count, designer_enrollment_role_count=t.designer_enrollment_role_count, ta_enrollment_role_count=t.ta_enrollment_role_count, student_enrollment_role_count=t.student_enrollment_role_count, observer_enrollment_role_count=t.observer_enrollment_role_count, account_membership_role_count=t.account_membership_role_count, no_permissions_role_count=t.no_permissions_role_count, account_admin_enrollment_id=t.account_admin_enrollment_id, teacher_enrollment_enrollment_id=t.teacher_enrollment_enrollment_id, designer_enrollment_enrollment_id=t.designer_enrollment_enrollment_id, ta_enrollment_enrollment_id=t.ta_enrollment_enrollment_id, student_enrollment_enrollment_id=t.student_enrollment_enrollment_id, observer_enrollment_enrollment_id=t.observer_enrollment_enrollment_id, account_membership_enrollment_id=t.account_membership_enrollment_id, no_permissions_enrollment_id=t.no_permissions_enrollment_id, most_privileged_role=t.most_privileged_role, least_privileged_role=t.least_privileged_role, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_enrollment_term_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_enrollment_term_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_enrollment_term_dim(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_enrollment_term_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_enrollment_term_dim (id, canvas_id, root_account_id, name, date_start, date_end, sis_source_id, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	

def insert_enrollment_term_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, root_account_id, name, date_start, date_end, sis_source_id, '" + str(data_timestamp) + "' from temp_enrollment_term_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE root_account_id=t.root_account_id, name=t.name, date_start=t.date_start, date_end=t.date_end, sis_source_id=t.sis_source_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_external_tool_activation_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_external_tool_activation_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_external_tool_activation_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_external_tool_activation_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_external_tool_activation_dim (id, canvas_id, course_id, account_id, activation_target_type, url, name, description, workflow_state, privacy_level, created_at, updated_at, tool_id, selectable_all, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()

def insert_external_tool_activation_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, course_id, account_id, activation_target_type, url, name, description, workflow_state, privacy_level, created_at, updated_at, tool_id, selectable_all,  '" + str(data_timestamp) + "' from temp_external_tool_activation_dim t  where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE course_id=t.course_id, account_id=t.account_id, activation_target_type=t.activation_target_type, url=t.url, name=t.name, description=t.description, workflow_state=t.workflow_state, privacy_level=t.privacy_level, created_at=t.created_at, updated_at=t.updated_at, tool_id=t.tool_id, selectable_all=t.selectable_all, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    print(query)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_external_tool_activation_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_external_tool_activation_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'external_tool_activation_id')
        insert_external_tool_activation_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_external_tool_activation_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_external_tool_activation_fact (external_tool_activation_id, course_id, account_id, root_account_id, enrollment_term_id, course_account_id, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()

def insert_external_tool_activation_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = " external_tool_activation_id, course_id, account_id, root_account_id, enrollment_term_id, course_account_id, '" + str(data_timestamp) + "' from temp_external_tool_activation_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE course_id=t.course_id, account_id=t.account_id, root_account_id=t.root_account_id, enrollment_term_id=t.enrollment_term_id, course_account_id=t.course_account_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


def load_group_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_group_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_group_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_group_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_group_dim (id, canvas_id, name, description, created_at, updated_at, deleted_at, is_public, workflow_state, context_type, category, join_level, default_view, sis_source_id, group_category_id, account_id, wiki_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_group_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, name, description, created_at, updated_at, deleted_at, is_public, workflow_state, context_type, category, join_level, default_view, sis_source_id, group_category_id, account_id, wiki_id, '" + str(data_timestamp) + "' from temp_group_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE name=t.name, description=t.description, created_at=t.created_at, updated_at=t.updated_at, deleted_at=t.deleted_at, is_public=t.is_public, workflow_state=t.workflow_state, context_type=t.context_type, category=t.category, join_level=t.join_level, default_view=t.default_view, sis_source_id=t.sis_source_id, group_category_id=t.group_category_id, account_id=t.account_id, wiki_id=t.wiki_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_group_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_group_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'group_id')
        insert_group_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_group_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_group_fact (group_id, parent_course_id, parent_account_id, parent_course_account_id, enrollment_term_id, max_membership, storage_quota, group_category_id, account_id, wiki_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_group_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "group_id, parent_course_id, parent_account_id, parent_course_account_id, enrollment_term_id, max_membership, storage_quota, group_category_id, account_id, wiki_id, '" + str(data_timestamp) + "' from temp_group_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE group_id=t.group_id, parent_course_id=t.parent_course_id, parent_account_id=t.parent_account_id, parent_course_account_id=t.parent_course_account_id, enrollment_term_id=t.enrollment_term_id, max_membership=t.max_membership, storage_quota=t.storage_quota, group_category_id=t.group_category_id, account_id=t.account_id, wiki_id=t.wiki_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()




def load_group_membership_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_group_membership_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_group_membership_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_group_membership_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_group_membership_dim (id, canvas_id, group_id, moderator, workflow_state, created_at, updated_at, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_group_membership_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, group_id, moderator, workflow_state, created_at, updated_at,  '" + str(data_timestamp) + "' from temp_group_membership_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE group_id=t.group_id, moderator=t.moderator, workflow_state=t.workflow_state, created_at=t.created_at, updated_at=t.updated_at, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_group_membership_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_group_membership_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'group_id')
        insert_group_membership_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_group_membership_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_group_membership_fact (group_id, parent_course_id, parent_account_id, parent_course_account_id, enrollment_term_id, user_id, group_membership_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_group_membership_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "group_id, parent_course_id, parent_account_id, parent_course_account_id, enrollment_term_id, user_id, group_membership_id, '" + str(data_timestamp) + "' from temp_group_membership_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE group_id=t.group_id, parent_course_id=t.parent_course_id, parent_account_id=t.parent_account_id, parent_course_account_id=t.parent_course_account_id, enrollment_term_id=t.enrollment_term_id, user_id=t.user_id, group_membership_id=t.group_membership_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


















def load_pseudonym_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_pseudonym_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_pseudonym_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_pseudonym_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_pseudonym_dim (id, canvas_id, user_id, account_id, workflow_state, last_request_at, last_login_at, current_login_at, last_login_ip, current_login_ip, position, created_at, updated_at, password_auto_generated, deleted_at, sis_user_id, unique_name, integration_id, authentication_provider_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_pseudonym_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, user_id, account_id, workflow_state, last_request_at, last_login_at, current_login_at, last_login_ip, current_login_ip, position, created_at, updated_at, password_auto_generated, deleted_at, sis_user_id, unique_name, integration_id, authentication_provider_id, '" + str(data_timestamp) + "' from temp_pseudonym_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE user_id=t.user_id, account_id=t.account_id, workflow_state=t.workflow_state, last_request_at=t.last_request_at, last_login_at=t.last_login_at, current_login_at=t.current_login_at, last_login_ip=t.last_login_ip, current_login_ip=t.current_login_ip, position=t.position, created_at=t.created_at, updated_at=t.updated_at, password_auto_generated=t.password_auto_generated, deleted_at=t.deleted_at, sis_user_id=t.sis_user_id, unique_name=t.unique_name, integration_id=t.integration_id, authentication_provider_id=t.authentication_provider_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_pseudonym_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_pseudonym_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'pseudonym_id')
        insert_pseudonym_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_pseudonym_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_pseudonym_fact (pseudonym_id, user_id, account_id, login_count, failed_login_count, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_pseudonym_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "pseudonym_id, user_id, account_id, login_count, failed_login_count, '" + str(data_timestamp) + "' from temp_pseudonym_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE pseudonym_id=t.pseudonym_id, user_id=t.user_id, account_id=t.account_id, login_count=t.login_count, failed_login_count=t.failed_login_count, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    
 
def load_quiz_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_quiz_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_quiz_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_quiz_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    #quiz instructions not being loaded at all
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_quiz_dim (id, canvas_id, root_account_id, name, points_possible, description, quiz_type, course_id, assignment_id, workflow_state, scoring_policy, anonymous_submissions, display_questions, answer_display_order, go_back_to_previous_question, could_be_locked, browser_lockdown, browser_lockdown_for_displaying_results, browser_lockdown_monitor, ip_filter, show_results, show_correct_answers, show_correct_answers_at, hide_correct_answers_at, created_at, updated_at, published_at, unlock_at, lock_at, due_at, deleted_at, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_quiz_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, root_account_id, name, points_possible, @dummy, quiz_type, course_id, assignment_id, workflow_state, scoring_policy, anonymous_submissions, display_questions, answer_display_order, go_back_to_previous_question, could_be_locked, browser_lockdown, browser_lockdown_for_displaying_results, browser_lockdown_monitor, ip_filter, show_results, show_correct_answers, show_correct_answers_at, hide_correct_answers_at, created_at, updated_at, published_at, unlock_at, lock_at, due_at, deleted_at, '" + str(data_timestamp) + "' from temp_quiz_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE root_account_id=t.root_account_id, name=t.name, points_possible=t.points_possible, quiz_type=t.quiz_type, course_id=t.course_id, assignment_id=t.assignment_id, workflow_state=t.workflow_state, scoring_policy=t.scoring_policy, anonymous_submissions=t.anonymous_submissions, display_questions=t.display_questions, answer_display_order=t.answer_display_order, go_back_to_previous_question=t.go_back_to_previous_question, could_be_locked=t.could_be_locked, browser_lockdown=t.browser_lockdown, browser_lockdown_for_displaying_results=t.browser_lockdown_for_displaying_results, browser_lockdown_monitor=t.browser_lockdown_monitor, ip_filter=t.ip_filter, show_results=t.show_results, show_correct_answers=t.show_correct_answers, show_correct_answers_at=t.show_correct_answers_at, hide_correct_answers_at=t.hide_correct_answers_at, created_at=t.created_at, updated_at=t.updated_at, published_at=t.published_at, unlock_at=t.unlock_at, lock_at=t.lock_at, due_at=t.due_at, deleted_at=t.deleted_at, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_quiz_dim_body(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "_body(SELECT "
    query2 = "id, description, '" + str(data_timestamp) + "' from temp_quiz_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE description=t.description, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_quiz_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_quiz_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'quiz_id')
        insert_quiz_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_quiz_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_quiz_fact (quiz_id, points_possible, time_limit, allowed_attempts, unpublished_question_count, question_count, course_id, assignment_id, course_account_id, enrollment_term_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_quiz_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "quiz_id, points_possible, time_limit, allowed_attempts, unpublished_question_count, question_count, course_id, assignment_id, course_account_id, enrollment_term_id, '" + str(data_timestamp) + "' from temp_quiz_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE points_possible=t.points_possible, time_limit=t.time_limit, allowed_attempts=t.allowed_attempts, unpublished_question_count=t.unpublished_question_count, question_count=t.question_count, course_id=t.course_id, assignment_id=t.assignment_id, course_account_id=t.course_account_id, enrollment_term_id=t.enrollment_term_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_role_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_role_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_role_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_role_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_role_dim (id, canvas_id, root_account_id, account_id, name, base_role_type, workflow_state, created_at, updated_at, deleted_at, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_role_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, root_account_id, account_id, name, base_role_type, workflow_state, created_at, updated_at, deleted_at, '" + str(data_timestamp) + "' from temp_role_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE root_account_id=t.root_account_id, account_id=t.account_id, name=t.name, base_role_type=t.base_role_type, workflow_state=t.workflow_state, created_at=t.created_at, updated_at=t.updated_at, deleted_at=t.deleted_at, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_submission_comment_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_submission_comment_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_submission_comment_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_submission_comment_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_submission_comment_dim (id, canvas_id, submission_id, recipient_id, author_id, assessment_request_id, group_comment_id, @dummy, author_name, created_at, updated_at, anonymous, teacher_only_comment, hidden, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_submission_comment_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, submission_id, recipient_id, author_id, assessment_request_id, group_comment_id, @dummy, author_name, created_at, updated_at, anonymous, teacher_only_comment, hidden, '" + str(data_timestamp) + "' from temp_submission_comment_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE submission_id=t.submission_id, recipient_id=t.recipient_id, author_id=t.author_id, assessment_request_id=t.assessment_request_id, group_comment_id=t.group_comment_id, comment=t.comment, author_name=t.author_name, created_at=t.created_at, updated_at=t.updated_at, anonymous=t.anonymous, teacher_only_comment=t.teacher_only_comment, hidden=t.hidden, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_submission_comment_dim_body(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "_body(SELECT "
    query2 = "id, comment, '" + str(data_timestamp) + "' from temp_submission_comment_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE comment=t.comment, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_submission_comment_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_submission_comment_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'submission_comment_id')
        insert_submission_comment_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_submission_comment_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_submission_comment_fact (submission_comment_id, submission_id, recipient_id, author_id, assignment_id, course_id, enrollment_term_id, course_account_id, message_size_bytes, message_character_count, message_word_count, message_line_count, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_submission_comment_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "submission_comment_id, submission_id, recipient_id, author_id, assignment_id, course_id, enrollment_term_id, course_account_id, message_size_bytes, message_character_count, message_word_count, message_line_count, '" + str(data_timestamp) + "' from temp_submission_comment_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE submission_comment_id=t.submission_comment_id, submission_id=t.submission_id, recipient_id=t.recipient_id, author_id=t.author_id, assignment_id=t.assignment_id, course_id=t.course_id, enrollment_term_id=t.enrollment_term_id, course_account_id=t.course_account_id, message_size_bytes=t.message_size_bytes, message_character_count=t.message_character_count, message_word_count=t.message_word_count, message_line_count=t.message_line_count, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    

def load_submission_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_submission_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_submission_dim(canvasdata_config, 'submission_dim', date_diff_string)
        #insert_submission_dim_body(canvasdata_config, 'submission_body', date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_submission_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_submission_dim (id, canvas_id, @dummy, url, grade, submitted_at, submission_type, workflow_state, created_at, updated_at, processed, process_attempts, grade_matches_current_submission, published_grade, graded_at, has_rubric_assessment, attempt, has_admin_comment, assignment_id, excused, graded_anonymously, grader_id, group_id, quiz_submission_id, user_id, grade_state, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_submission_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, @dummy, url, grade, submitted_at, submission_type, workflow_state, created_at, updated_at, processed, grade_matches_current_submission, published_grade, graded_at, has_rubric_assessment, attempt, has_admin_comment, assignment_id, excused, graded_anonymously, grader_id, group_id, quiz_submission_id, user_id, grade_state, '" + str(data_timestamp) +"' from temp_submission_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) " 
    query3 = "ON DUPLICATE KEY UPDATE url=t.url, grade=t.grade, submitted_at=t.submitted_at, submission_type=t.submission_type, workflow_state=t.workflow_state, created_at=t.created_at, updated_at=t.updated_at, processed=t.processed, grade_matches_current_submission=t.grade_matches_current_submission, published_grade=t.published_grade, graded_at=t.graded_at, has_rubric_assessment=t.has_rubric_assessment, attempt=t.attempt, has_admin_comment=t.has_admin_comment, assignment_id=t.assignment_id, excused=t.excused, graded_anonymously=t.graded_anonymously, grader_id=t.grader_id, group_id=t.group_id, quiz_submission_id=t.quiz_submission_id, user_id=t.user_id, grade_state=t.grade_state, data_timestamp='" + str(data_timestamp) + "'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_submission_dim_body(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, body, '" + str(data_timestamp) + "' from temp_submission_dim t where body is not null) "
    query3 = "ON DUPLICATE KEY UPDATE body=t.body, data_timestamp='" + str(data_timestamp) + "'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    
    
def insert_submission_dim_info(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, NULL, NULL, user_id, NULL, quiz_submission_id, url, submitted_at, submission_type, workflow_state, created_at, updated_at, processed, attempt, grade_state, NULL,  '" + str(data_timestamp) + "' from temp_submission_dim t where submitted_at is not null and workflow_state <> 'deleted') "
    query3 = "ON DUPLICATE KEY UPDATE canvas_id=t.canvas_id, user_id=t.user_id, quiz_submission_id=t.quiz_submission_id, url=t.url, submitted_at=t.submitted_at, submission_type=t.submission_type, workflow_state=t.workflow_state, created_at=t.created_at, updated_at=t.updated_at, processed=t.processed, attempt=t.attempt, grade_state=t.grade_state, data_import_id='3', data_timestamp=t.data_timestamp"
    query = query1 + query2 + query3
    #print(query)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()           
  

def load_submission_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_submission_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'submission_id')
        insert_submission_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_submission_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_submission_fact (submission_id, assignment_id, course_id, @enrollment_term_id, user_id, grader_id, @course_account_id, enrollment_rollup_id, score, published_score, what_if_score, submission_comments_count, @account_id, @assignment_group_id, group_id, quiz_id, quiz_submission_id, wiki_id, @dummy)"
#    print(query)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_submission_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "submission_id, assignment_id, course_id, enrollment_term_id, user_id, grader_id, course_account_id, enrollment_rollup_id, score, published_score, what_if_score, submission_comments_count, account_id, assignment_group_id, group_id, quiz_id, quiz_submission_id, wiki_id, '" + str(data_timestamp) + "' from temp_submission_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE assignment_id=t.assignment_id, course_id=t.course_id, enrollment_term_id=t.enrollment_term_id, user_id=t.user_id, grader_id=t.grader_id, course_account_id=t.course_account_id, enrollment_rollup_id=t.enrollment_rollup_id, score=t.score, published_score=t.published_score, what_if_score=t.what_if_score, submission_comments_count=t.submission_comments_count, account_id=t.account_id, assignment_group_id=t.assignment_group_id, group_id=t.group_id, quiz_id=t.quiz_id, quiz_submission_id=t.quiz_submission_id, wiki_id=t.wiki_id, data_timestamp=t.data_timestamp"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()		
    
def insert_submission_fact_info(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "UPDATE " + table_part + " s INNER JOIN temp_submission_fact t on t.submission_id = s.submission_id "
    query3 = "SET s.assignment_id=t.assignment_id, s.course_id=t.course_id, s.user_id=t.user_id, s.enrollment_rollup_id=t.enrollment_rollup_id, s.quiz_submission_id=t.quiz_submission_id, s.data_import_id='3', s.data_timestamp=t.data_timestamp WHERE t.submission_id = s.submission_id"
    query = query1 + query3
    #print(query)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	  
    

def load_user_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_user_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_user_dim(canvasdata_config, table_part)
        insert_user_tbl(canvasdata_config, 'user_tbl')
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_user_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_user_dim (id, canvas_id, root_account_id, name, time_zone, created_at, visibility, school_name, school_position, gender, locale, public, birthdate, country_code, workflow_state, sortable_name, global_canvas_id, @dummy)"
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()	

def insert_user_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, root_account_id, name, time_zone, created_at, visibility, school_name, school_position, gender, locale, public, birthdate, country_code, workflow_state, sortable_name, global_canvas_id, '" + str(data_timestamp) + "' from temp_user_dim t ) "
    query3 = "ON DUPLICATE KEY UPDATE root_account_id=t.root_account_id, name=t.name, time_zone=t.time_zone, created_at=t.created_at, visibility=t.visibility, school_name=t.school_name, school_position=t.school_position, gender=t.gender, locale=t.locale, public=t.public, birthdate=t.birthdate, country_code=t.country_code, workflow_state=t.workflow_state, sortable_name=t.sortable_name, global_canvas_id=t.global_canvas_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    
    
def insert_user_tbl(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "t.id, t.canvas_id, p.sis_user_id, p.unique_name, t.name, t.sortable_name, t.created_at, t.workflow_state,  '" + str(data_timestamp) + "' from temp_user_dim t  LEFT JOIN `pseudonym_dim` `p` ON `t`.`id` = `p`.`user_id` WHERE (`p`.`workflow_state` = 'active') and (`p`.`sis_user_id` is not null)) "
    query3 = "ON DUPLICATE KEY UPDATE canvas_id = t.canvas_id, EMPLID=p.sis_user_id, OPRID=p.unique_name, name=t.name, sortable_name=t.sortable_name, created_at=t.created_at,workflow_state=t.workflow_state, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()        

def load_wiki_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        print("Split file")
        sf_path = split_temp_dir + sf
        print(sf_path)
        print("Inserting into Temp Table")
        insert_wiki_dim_temp(canvasdata_config, sf_path, table_part)
        print("Sorting Temp Table")
        sort_temp_table(canvasdata_config, table_part, 'id')
        print("Inserting into Table")
        insert_wiki_dim(canvasdata_config, table_part, date_diff_string)
        print("Truncating Table")
#        truncate_temp_table(canvasdata_config, table_part)
#        os.remove(sf_path)
    return split_file_count

def insert_wiki_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_wiki_dim (id, canvas_id, parent_type, title, created_at, updated_at, front_page_url, has_no_front_page, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	
	
def insert_wiki_dim(db_config, table_part, date_diff_string):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, parent_type, title, created_at, updated_at, front_page_url, has_no_front_page, '" + str(data_timestamp) + "' from temp_wiki_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE canvas_id=t.canvas_id, parent_type=t.parent_type, title=t.title, created_at=t.created_at, updated_at=t.updated_at, front_page_url=t.front_page_url, has_no_front_page=t.has_no_front_page, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    print(query)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close() 

def load_wiki_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_wiki_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'wiki_id')
        insert_wiki_fact(canvasdata_config, table_part)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_wiki_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_wiki_fact (wiki_id, parent_course_id, parent_group_id, parent_course_account_id, parent_group_account_id, account_id, root_account_id, enrollment_term_id, group_category_id, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	
	
def insert_wiki_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "wiki_id, parent_course_id, parent_group_id, parent_course_account_id, parent_group_account_id, account_id, root_account_id, enrollment_term_id, group_category_id, '" + str(data_timestamp) + "' from temp_wiki_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE parent_course_id=t.parent_course_id, parent_group_id=t.parent_group_id, parent_course_account_id=t.parent_course_account_id, parent_group_account_id=t.parent_group_account_id, account_id=t.account_id, root_account_id=t.root_account_id, enrollment_term_id=t.enrollment_term_id, group_category_id=t.group_category_id, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    print(query)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()  

def load_wiki_page_dim(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_w_dim_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_wiki_page_dim(canvasdata_config, table_part, date_diff_string)
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_wiki_page_dim_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_wiki_page_dim (id, canvas_id, title, body, workflow_state, created_at, updated_at, url, protected_editing, editing_roles, revised_at, could_be_locked, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	
	
def insert_wiki_page_dim(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, canvas_id, title, body, workflow_state, created_at, updated_at, url, protected_editing, editing_roles, revised_at, could_be_locked, '" + str(data_timestamp) + "' from temp_wiki_page_dim t where DATEDIFF(updated_at, '" + date_diff_string + "') > 0 ) "
    query3 = "ON DUPLICATE KEY UPDATE canvas_id=t.canvas_id, title=t.title, body=t.body, workflow_state=t.workflow_state, created_at=t.created_at, updated_at=t.updated_at, url=t.url, protected_editing=t.protected_editing, editing_roles=t.editing_roles, revised_at=t.revised_at, could_be_locked=t.could_be_locked, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()    
    
def insert_wiki_page_dim_body(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "id, body, '" + str(data_timestamp) + "' from temp_wiki_page_dim t where body is not null) "
    query3 = "ON DUPLICATE KEY UPDATE body=t.body, data_timestamp='" + str(data_timestamp) + "'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()     

def load_wiki_page_fact(split_list, split_temp_dir, canvasdata_config, table_part, date_diff_string):  
    split_file_count = 0
    for sf in split_list:
        split_file_count += 1
        sf_path = split_temp_dir + sf
        insert_wiki_page_fact_temp(canvasdata_config, sf_path, table_part)
        sort_temp_table(canvasdata_config, table_part, 'id')
        insert_wiki_page_fact(canvasdata_config, table_part)
        insert_wiki_page_dim_body(canvasdata_config, 'wiki_page_dim_body')
        truncate_temp_table(canvasdata_config, table_part)
        os.remove(sf_path)
    return split_file_count

def insert_wiki_page_fact_temp(db_config, csv_path_name, table_part):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = utcnow_tz()
    query = "LOAD DATA LOCAL INFILE '" + csv_path_name + "' INTO TABLE temp_wiki_page_fact (wiki_page_id, wiki_id, parent_course_id, parent_group_id, parent_course_account_id, parent_group_account_id, user_id, account_id, root_account_id, enrollment_term_id, group_category_id, wiki_page_comments_count, view_count, @dummy)"
    cursor = cnx.cursor()
    cnx.commit()
    cursor.execute(query)
    cursor.close()
    cnx.close()	
	
def insert_wiki_page_fact(db_config, table_part):
    data_timestamp = utcnow_tz()
    cnx = mysql.connector.connect(**db_config)
    query1 = "INSERT INTO " + table_part + "(SELECT "
    query2 = "wiki_page_id, wiki_id, parent_course_id, parent_group_id, parent_course_account_id, parent_group_account_id, user_id, account_id, root_account_id, enrollment_term_id, group_category_id, wiki_page_comments_count, view_count, '" + str(data_timestamp) + "' from temp_wiki_page_fact t ) "
    query3 = "ON DUPLICATE KEY UPDATE wiki_id=t.wiki_id, parent_course_id=t.parent_course_id, parent_group_id=t.parent_group_id, parent_course_account_id=t.parent_course_account_id, parent_group_account_id=t.parent_group_account_id, user_id=t.user_id, account_id=t.account_id, root_account_id=t.root_account_id, enrollment_term_id=t.enrollment_term_id, group_category_id=t.group_category_id, wiki_page_comments_count=t.wiki_page_comments_count, view_count=t.view_count, data_timestamp='" + str(data_timestamp) +"'"
    query = query1 + query2 + query3
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close() 
