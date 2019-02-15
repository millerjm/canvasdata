#!/usr/bin/python

import time
import dateutil
import datetime
from dateutil import parser
from datetime import tzinfo

#mysql db setup
canvasdata_config = {
    'user': 'USERNAME',
    'password': 'PASSWORD',
    'host': '127.0.0.1',
    'database': 'DATABASE_NAME',
}


apiKey = u'CANVAS_DATA_API_KEY'
apiSecret = u'CANVAS_DATA_API_SECRET'
apiHost = u'portal.inshosteddata.com'
apiContentType = u'application/json'
apiMethod = u'GET'
#apiPath = u'/api/account/self/file/latest'
apiTime = unicode(datetime.utcnow().strftime('%a, %d %b %y %H:%M:%S GMT'))
#setup for cli api

latest_api_path = u'/api/account/self/file/latest'
dumplist_api_path = u'/api/account/self/dump'
bydump_api_path = u'/api/account/self/file/byDump'
bytable_api_path = u'/api/account/self/file/byTable'
dumplog_file = '/usr/local/canvasdata/dumps'

#setup to configure date and diff options
today = datetime.datetime.today()
d_format = '%Y-%m-%d'
dt_format = ('%Y-%m-%d %H:%M:%S')
yesterday= today - datetime.timedelta(days=2)
last_week = today - datetime.timedelta(days=7)
today_string = today.strftime(d_format)
yesterday_string = yesterday.strftime(d_format)
last_week_string = last_week.strftime(d_format)
all_time_string = '2014-01-01 00:00:00'

#source folder for all of the gz files
source_folder ="/usr/local/mounts/gz"

#location of bash script command to update all data
update_script = "bash /usr/local/canvasdata/canvasdata.sh"

#another way to limit what's imported...
process_list = ['account_dim', 'assignment_dim', 'assignment_fact', 'conversation_dim', 'conversation_message_dim', 'conversation_message_participant_fact', 'course_dim', 'course_score_dim', 'course_score_fact', 'course_section_dim', 'discussion_entry_dim', 'discussion_entry_fact', 'discussion_topic_dim', 'discussion_topic_fact', 'enrollment_dim', 'enrollment_fact', 'enrollment_rollup_dim', 'enrollment_term_dim', 'external_tool_activation_dim', 'external_tool_activation_fact', 'group_dim', 'group_fact', 'group_membership_dim', 'group_membership_fact', 'pseudonym_dim', 'pseudonym_fact', 'quiz_dim', 'quiz_fact', 'role_dim', 'submission_comment_dim ', 'submission_comment_fact', 'submission_fact', 'submission_dim', 'user_dim', 'wiki_dim', 'wiki_fact', 'wiki_page_dim', 'wiki_page_fact']
