import sys
import os
import web
sys.path.append('/root/2AU_python_script/dao')
from dao import DAO
sys.path.append('/root/2AU_python_script')
from myconfig import *

class InsertEvent:
    def POST(self):
        try:
            web.header('Access-Control-Allow-Origin',      '*')
            web.header('Access-Control-Allow-Credentials', 'true')
            data = web.input()
            db = DAO()
            db.execute("INSERT INTO evenement (title, start, end, instance, version_release, playbooks, rulebeforeevent, ruleinevent) VALUES ('"+data.title+"','"+data.start+"','"+data.end+"','"+data.instance+"','"+data.release+"','"+data.playbooks+"','"+data.ruleb+"','"+data.rulei+"')")
            print "insertion done"
        except Exception, e:
            print "Error [%r]" % (e)
            #sys.exit(1)  
	os.system('python /root/2AU_python_script/2AU.py -c')
