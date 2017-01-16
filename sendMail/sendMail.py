import smtplib
from email.MIMEText import MIMEText
import re
import os
import datetime


class sendMail:

    def __init__(self, instances, release, logger, opretionLaunchTime, opretionFinishTime, testPlatformLink, eventID, cursor):
        self.release=release
        self.instances=instances
        self.logger= logger
        self.opretionLaunchTime = opretionLaunchTime
        self.opretionFinishTime = opretionFinishTime
        self.testPlatformLink = testPlatformLink
	self.eventID = eventID
	self.cursor = cursor
    
    def getSection( self, data, section_name):
        try:
            first = '==='+section_name
            last = section_name+'==='
            start = data.rindex( first ) + len( first )
            end = data.rindex( last, start )
            return data[start:end]
        except ValueError:
            self.logger.error("section name "+section_name+" does not exist")
            return ""

    def getEventStartDate(self, cur, eventID):
        cur.execute("SELECT start FROM evenement WHERE id="+eventID)
        for row in cur.fetchall():
            return  row[0]

    def getEventEndDate(self, cur, eventID):
        cur.execute("SELECT end FROM evenement WHERE id="+eventID)
        for row in cur.fetchall():
            return  row[0]

    def getEventTime(self, startDate, endDate):
	if str(startDate.hour) != '0' or str(startDate.minute) != '0' or  str(startDate.hour) != '0' or str(startDate.minute) != '0':
	    startTime = str(startDate.hour)+":"+str(startDate.minute)
	    endTime = str(endDate.hour)+":"+str(endDate.minute)
	    return startTime, endTime
	else:
	    return self.opretionLaunchTime, self.opretionFinishTime

    def send(self, fromaddr,toaddr,server, content):
        start_date_raw = self.getEventStartDate(self.cursor, self.eventID)
	end_date_raw = self.getEventEndDate(self.cursor, self.eventID)
	startTime,endTime = self.getEventTime(start_date_raw, end_date_raw)
	
        end_date = start_date_raw.strftime("%A %d %B %Y")
        short_current_date = start_date_raw.strftime("%d-%m-%Y")

        server = smtplib.SMTP(server)
        for i in range(0,len(self.instances)):
            fp = open(os.path.dirname(os.path.abspath(__file__))+'/mailContent/'+content, 'rb')
            #remove line breaks
            data=fp.read().replace("\n", "")
            fp.close()
            #replacing values withdynamic ones
            data = data.replace("=upgradeDate=", end_date)
            data = data.replace("=upgradeInstance=", self.instances[i])
            data = data.replace("=shortUpgradeDate=", short_current_date)
            data = data.replace("=opretionLaunchTime=", startTime)
            data = data.replace("=opretionFinishTime=", endTime)
            data = data.replace("=release=", self.release)
            data = data.replace("=testPlatformLink=", self.testPlatformLink)

            #construct mail
            msg = MIMEText(self.getSection(data, "BODY"))
            msg['From'] = fromaddr
            #Insert dynamic mail in case we want to change recipient
            if self.getSection(data, "TO") == "default":
                msg['To'] = ", ".join(toaddr)
            else:
                msg['To'] = self.getSection(data, "TO")
		msg['Cc'] = self.getSection(data, "CC")
                toaddr = [self.getSection(data, "TO")]
                self.logger.info("recipients are specified in the template : "+str(toaddr))
            msg['Subject'] = self.getSection(data, "SUBJECT")
            msg['Content-Type'] = "text/html; charset=utf-8"

            #server.starttls()
            #server.login(fromaddr, "YOUR PASSWORD")
            server.sendmail(fromaddr, toaddr, msg.as_string())
            self.logger.info("mail sent from %s to %s" %(fromaddr, toaddr));
        server.quit()

