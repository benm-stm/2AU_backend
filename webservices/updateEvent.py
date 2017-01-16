import sys
import os
import web
sys.path.append('/root/2AU_python_script/dao')
from dao import DAO
sys.path.append('/root/2AU_python_script')
from myconfig import *

class UpdateEvent:
    def POST(self):
        try:
            web.header('Access-Control-Allow-Origin',      '*')
            web.header('Access-Control-Allow-Credentials', 'true')
            data = web.input()
            db = DAO()
            db.execute("UPDATE evenement SET title='"+data.title+"', start='"+data.start+"', end='"+data.end+"', instance='"+data.instance+"', version_release='"+data.release+"',playbooks='"+data.playbooks+"', rulebeforeevent='"+data.ruleb+"', ruleinevent='"+data.rulei+"' WHERE id="+data.id)
            print "update done"
        except Exception, e:
            print "Error [%r]" % (e)
            #sys.exit(1)
	os.system('python /root/2AU_python_script/2AU.py -c')
