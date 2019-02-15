import requests
from datetime import datetime
import base64
import hashlib
import hmac
from json import loads
import pprint
import mysql.connector
import subprocess
import os
from config import *

#this file is the one you will run.  
#it uses the canvas data API instead of the CLI tool and will check for a new data dump and if it hasn't been imported, it will import.  It ignores historical files.  

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
        
def get_auth(api_path):
    apiTime = unicode(datetime.utcnow().strftime('%a, %d %b %y %H:%M:%S GMT'))
    msgList = []
    msgList.append(apiMethod)
    msgList.append(apiHost)
    msgList.append(apiContentType)
    msgList.append('')
    msgList.append(api_path)
    msgList.append('')
    msgList.append(apiTime)
    msgList.append(apiSecret)
    msgStr = bytes(unicode("".join("%s\n" % k for k in msgList).strip()))
    print(msgList)
    print(msgStr)
    sig = base64.b64encode(hmac.new(key=bytes(apiSecret),msg=msgStr,digestmod=hashlib.sha256).digest())
    sig = sig.decode('utf-8')
    return sig        
  
def get_headers(api_path):
    sig = get_auth(api_path)
    headers = {}
    headers['Authorization'] = 'HMACAuth {}:{}'.format(apiKey,sig)
    headers['Date'] = apiTime
    headers['Content-type'] = apiContentType
    return headers

def get_request(url, headers):
    r = requests.get(url, headers=headers)
   # print(r.json())
    return r

def parse_dump_list(dump_list):
    dump_id_list = []
    for d in dump_list:
        dump_id = d['dumpId']
        dump_id_list.append(dump_id)
    return dump_id_list
  
def parse_dump_info(response):
    daily = False
    historical = False
    partial = False
    resp = loads(response.text)
    dump_id = resp['dumpId']
    print("Dump ID: " + dump_id)
    sequence = resp['sequence']
    print("Sequence Number: " + str(sequence))
    num_files = resp['numFiles']
    print("Number of Files: " + str(num_files))
    created_at = resp['createdAt']
    print("Created At: " + created_at)
    account_id = resp['accountId']
    print("Account ID: " + account_id)
    created_at = resp['createdAt']
    print("Created At: " + created_at)
    finished =  resp['finished']
    print("Finished: " + str(finished))
    num_files = resp['numFiles']
    print("Number of Files: " + str(num_files))
    sequence = resp['sequence']
    print("Sequence Number: " + str(sequence))
    updated_at = resp['updatedAt']
    print("Updated At: " + updated_at)
    finished =  resp['finished']
    print("Finished: " + str(finished))
    expires_at = None
    #    dump_info.append(resp['expiresAt'])
    artifacts = resp['artifactsByTable']
     #   print(artifacts)
    try:
        user_dim = artifacts['user_dim']
    except:
        daily is False
    finally:
        daily is True
        print("Daily: " + str(daily))
            #print(user_dim)
        files = user_dim['files']
            #for f in files:
            #    print(f)
        print(user_dim['partial'])
        print(user_dim['tableName'])
        file_counter = 0
        for i in artifacts:
            #print(i)
            #print(i['account_dim'])
            file_counter += 1
        print(file_counter)
    try:
        requests = artifacts['requests']
    except:
        historical is False
    finally:
            #print(requests)
        files = requests['files']
            #for f in files:
            #    print(f)
        print(requests['partial'])
        print(requests['tableName'])
    dump_info = [dump_id, sequence, num_files, created_at, updated_at, expires_at, historical, finished, partial]
    return dump_info  
  
def insert_dump_info(db_config, dump_info):
    cnx = mysql.connector.connect(**db_config)
    data_timestamp = datetime.utcnow().strftime(dt_format)
    dump_id = str(dump_info[0])
    sequence = str(dump_info[1])
    file_count = str(dump_info[2])
    created_at = dump_info[3]
    updated_at = dump_info[4]
    expires_at = ''
    historical = str(int(dump_info[6]))
    finished = str(int(dump_info[7]))
    partial = str(int(dump_info[8]))
    query = "INSERT INTO import_dumps (dump_id, sequence, file_count, created_at, updated_at, expires_at, historical, finished, partial, data_timestamp) VALUES ('" + dump_id + "'," + str(sequence) + "," + str(file_count) + ",'" + created_at + "','" + updated_at + "','" + expires_at + "'," + str(historical) + "," + str(finished) + "," + str(partial) + ",'" + data_timestamp +  "') ON DUPLICATE KEY UPDATE sequence=" + sequence + ", file_count=" + file_count + ", created_at='" + created_at + "', updated_at='"+ updated_at + "', expires_at='" + expires_at + "', historical=" + historical + ", finished=" + finished + ", partial=" + partial + ", data_timestamp='" + data_timestamp + "'"
    print(query)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()
    return sequence, historical  
  
def get_dump_list(headers):
    dump_list = []
    dump_id_list = []
    api_path = dumplist_api_path
    #print(api_path)
    # headers = get_headers(api_path)
    #print(headers)
    url = 'https://' + apiHost + api_path
    print(url)
    r = get_request(url,headers)
    if r.status_code == 200:
        print(r.status_code)
        dump_list = r.json()
        dump_id_list = parse_dump_list(dump_list)
    else:
        print(r.status_code)
    return dump_id_list

def get_latest_dump_info(headers):
    api_path = latest_api_path
    print(headers)
    url = 'https://' + apiHost + api_path
    print(url)
    r = get_request(url,headers)
    if r.status_code == 200:
        print(r.status_code)
        dump_info = parse_dump_info(r)
        print(dump_info)
        dump_id, historical = insert_dump_info(canvasdata_config, dump_info)
    else:
        print(r.status_code)
        dump_id = ''
        historical = ''
    return dump_id, historical

def get_dump_info(headers, dump_id):
    api_path = bydump_api_path
    print(headers)
    url = 'https://' + apiHost + api_path + '/' + dump_id
    print(url)
    r = get_request(url,headers)
    if r.status_code == 200:
        print(r.status_code)
        #dump_info = parse_dump_info(r)
        #insert_dump_info(canvasdata_config, dump_info)
    else:
        print(r.status_code)

def write_dumplog_file(dump_sequence):
    cmd = 'touch ' +  dumplog_file + '/' + str(dump_sequence)
    print(cmd)
    p = subprocess.Popen(cmd, shell=True)
    os.waitpid(p.pid, 0)

def checkfor_dumplog_file(dump_sequence):
    path = dumplog_file + '/' + str(dump_sequence)
    print(path)
    exists = os.path.exists(path)
    return exists

def update_data(needs_imported, command):
    print("This file needs Imported: " + str(needs_imported))
    subprocess.call(command, shell=True) 

def new_data_checker():
    try_db(canvasdata_config)
    latest_headers = get_headers(latest_api_path)
    dump_sequence, historical = get_latest_dump_info(latest_headers)
    if dump_sequence is not None:
        exists = checkfor_dumplog_file(dump_sequence)
        print(dump_sequence)
        if exists is False:
            write_dumplog_file(dump_sequence)
            print("New file.  Time to update the database!")
            needs_imported = True
        else:
            print("Not a new file.  Try again later.")
            needs_imported = False
    return needs_imported

def main():
    needs_imported = new_data_checker()
    print("Needs Imported: " + str(needs_imported))
    if needs_imported:  
        update_data(needs_imported, update_script)

        
main()        
