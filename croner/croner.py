#!/usr/bin/python

import MySQLdb
from datetime import datetime, timedelta
import re

class croner:

    # params : release       : String
    #          instances      : String
    #          role          : Int
    def __init__(self, logger, cron_file, section_name, cron_hour, cron_minute, deadline, app_location, python_location):
        self.logger = logger
        self.cron_file = cron_file
        self.section_begin = "#"+section_name+"-begin\n"
        self.section_end = "#"+section_name+"-end"
        self.cron_hour=cron_hour
        self.cron_minute=cron_minute
        self.cron_file = cron_file
        self.deadline = deadline
        self.app_location = app_location
	self.python_location = python_location

    def refreshCrontab(self):
        # create regular expression pattern
        chop = re.compile(self.section_begin+'.*?'+self.section_end, re.DOTALL)
        # open file
        f = open(self.cron_file, 'r')
        data = f.read()
        f.close()
        # chop text between #chop-begin and #chop-end
        data_chopped = chop.sub('', data)
        # save result
        f = open(self.cron_file, 'w')
        f.write(data_chopped)
        f.close()

    def fillJobs(self, jobs):
        # save result (append to file)
        f = open(self.cron_file, 'a')
        f.write(self.section_begin)
        for i in range(0,len(jobs)):
            #every event will have 2 entries or jobs one with the role 5 and the other with the role 10
            f.write(jobs[i]+"\n")
        f.write(self.section_end)
        f.close()

    def bypass_weekend(self, date):
	day_name = date.strftime("%A")
	if day_name == "Saturday":
		date = date  - timedelta(days=1)
	elif day_name == "Sunday":
		date = date  - timedelta(days=2)
	return date

    def cronHourMinute(self, date):
        if str(date.hour) != "0":
		self.cron_hour = date.hour
		self.cron_minute = date.minute
	    

    def getJobs(self, cur):
        now = datetime.now()
        jobs_array = []
        cur.execute("SELECT id, title, instance, start, end, playbooks, rulebeforeevent, version_release, ruleinevent FROM evenement")
        # print all the first cell of all the rows
        for row in cur.fetchall():
	    #dt = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
	    dt= row[3]
	    dtbeforeevent = dt - timedelta(days=int(self.deadline))
	    dtbeforeevent = self.bypass_weekend(dtbeforeevent)
	    #print dtbeforeevent
	    #print dt
            if now <= dt:
                cron_date_before = str(self.cron_minute)+" "+str(self.cron_hour)+" "+str(dtbeforeevent.day)+" "+str(dtbeforeevent.month)
                #this section must be taken from the db
                params_before = "-r \""+row[7]+"\" -i \""+row[2]+"\" -p \""+row[5]+"\" -u "+row[6]+" -e "+str(row[0])
                cron_date_in = str(self.cron_minute)+" "+str(self.cron_hour)+" "+str(dt.day)+" "+str(dt.month)
                params_in = "-r \""+row[7]+"\" -i \""+row[2]+"\" -u "+row[8]+" -e "+str(row[0])
                script= self.app_location+" && "+self.python_location+" 2AU.py"

                jobs_array.append(cron_date_before+" * cd "+script+" "+params_before)
                jobs_array.append(cron_date_in+" * cd "+script+" "+params_in)
        return jobs_array

