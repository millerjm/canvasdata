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

#this file gets the last course login date from the enrollment table as the LDA for starfish.  


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
        print(query)
        try:  
            cursor.execute(query)
        except Exception as e:  
            print(e)
        finally:  
            cnx.commit()
    cursor.close()    
    cnx.close()

def execute_sql_file_strm(filename, db_config, strm):
    # Open and read the file as a single buffer
    cnx = mysql.connector.connect(**db_config)
    strm_criteria_string = strm + "-%'"
    strm_criteria_query = "set @strm_criteria = '" + strm_criteria_string
    print(strm_criteria_query)
    cursor = cnx.cursor(buffered=True)
    f = open(filename, 'r')
    sql_file = f.read()
    f.close()
    # all SQL commands (split on ';')
    sql_commands = sql_file.split(';')
    cursor.execute(strm_criteria_query)
    row = cursor.fetchone()
    while row is not None:  
        print(row)
        row = cursor.fetchone()
#    sql_commands.insert(0, "set @strm_criteria = '" + strm + "-%'")
    print(sql_commands)
    # Execute every command from the input file
    for query in sql_commands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        print(query)
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
        finally:
            cnx.commit()
    cursor.close()
    cnx.close()


#====================Queries===========================

def execute_query(db_config, query, data_tuple):
    # Open and read the file as a single buffer
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    try:
        if len(data_tuple) > 0 and data_tuple is not None:
            cursor.execute(query, data_tuple)
        elif len(data_tuple) == 0:
            cursor.execute(query)
    except mysql.connector.Error as err:
        print("Error Inserting Records" + str(err))
        print(cursor.statement)
    except Exception as e:
        print("Exception Error" + str(e))
        print(cursor.statement)
    else:  
        cnx.commit()
        print(cursor.statement)
        warnings = cursor.fetchwarnings()
        if warnings:
            print("Warnings: " + str(warnings))
            print(cursor.statement)
            print("Success Inserting Records")
        print("affected rows = {}".format(cursor.rowcount))
    finally:
        cursor.close()
        cnx.close()

def main():  
    data_timestamp=datetime.datetime.utcnow()
    #all of our sis section id's start with the PeopleSoft Term ID (STRM).  
    strm_list = ['2191', '2187']
    for strm in strm_list:  
        strm = strm + '-%'
        print(strm)
        #inserts utc time into table for consistency with rest of canvas data.  based on last course login
        insert_query_lda_utc = """insert into canvas_login_student (emplid, sis_section_id, course_last_login, data_timestamp) select emplid, sis_section_id, course_last_login, %s from canvas_login_student_vw v where v.sis_section_id <> '' and sis_section_id like %s on duplicate key update course_last_login=v.course_last_login, data_timestamp=%s"""
        print(insert_query_lda_utc)
        lda_utc_data = (unicode(data_timestamp), unicode(strm), unicode(data_timestamp))
        execute_query(canvasdata_config, insert_query_lda_utc, lda_utc_data)
        #inserts as local time to separate for faster and easier inserts to peoplesoft and starfish.  
        insert_query_lda_local = """insert into canvas_login_student_local (emplid, sis_section_id, course_last_login, data_timestamp) select emplid, sis_section_id, CONVERT_TZ(course_last_login,'UTC','America/New_York'), CONVERT_TZ(data_timestamp, 'UTC', 'America/New_York') from canvas_login_student c where c.sis_section_id <> '' and c.sis_section_id like '""" + strm + """' on duplicate key update course_last_login=CONVERT_TZ(c.course_last_login,'UTC','America/New_York'), data_timestamp=CONVERT_TZ(c.data_timestamp, 'UTC', 'America/New_York') """
        lda_local_data = []
        print(insert_query_lda_local)
        execute_query(canvasdata_config, insert_query_lda_local, lda_local_data)

main()
