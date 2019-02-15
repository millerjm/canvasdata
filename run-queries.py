#!/usr/bin/python
import os
import time
import dateutil
import datetime
import requests
import json
from config import *
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

#populates a bunch of rollup fields

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
        
def execute_sql_file(filename, db_config):
    # Open and read the file as a single buffer
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    f = open(filename, 'r')
    sql_file = f.read()
    f.close()
    # all SQL commands (split on ';')
    sql_commands = sql_file.split(';')
    print(sql_commands)
    # Execute every command from the input file
    for query in sql_commands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        #print(query)
        try:  
            cursor.execute(query)
        except Exception as e:  
            print(e)
        finally:  
            cnx.commit()
    cursor.close()    
    cnx.close()

def main():  
    #query_test = '/usr/local/canvasdata/scripts/query.sql'

    #execute_sql_file(query_test, canvasdata_config)
    print("ssc_canvas_enrollment_role_counts.sql")
    execute_sql_file(install_location + '/sql/ssc_canvas_enrollment_role_counts.sql', canvasdata_config)
    print("/usr/local/canvasdata/sql/ssc_course_info_dl_inst.sql")
    execute_sql_file(install_location + '/sql/ssc_course_info_dl_inst.sql', canvasdata_config)
    print("/usr/local/canvasdata/sql/ssc_discussion_inst_counts.sql")
    execute_sql_file(install_location + '/sql/ssc_discussion_inst_counts.sql', canvasdata_config)
    print("/usr/local/canvasdata/sql/ssc_assignment_counts.sql")
    execute_sql_file(install_location + '/sql/ssc_assignment_counts.sql', canvasdata_config)
    print("/usr/local/canvasdata/sql/ssc_conversation_course_counts.sql")
    execute_sql_file(install_location + 'sql/ssc_conversation_course_counts.sql', canvasdata_config)
    print("/usr/local/canvasdata/sql/ssc_discussion_counts.sql")
    execute_sql_file(install_location + '/sql/ssc_discussion_counts.sql', canvasdata_config)

main()
