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
from config import *
from cd_functions import *

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
