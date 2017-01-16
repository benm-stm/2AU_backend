import web
import sys
sys.path.append('/root/2AU_python_script/dao')
from dao import DAO
import json

class GetEvents:
    def GET(self):
        try:
            web.header('Access-Control-Allow-Origin',      '*')
            web.header('Access-Control-Allow-Credentials', 'true')
            db = DAO()
            query = "SELECT id, title, instance, version_release, start, end, playbooks, rulebeforeevent, ruleinevent FROM evenement"
            query_result = [dict(id=int(row[0]), title=row[1], instance=row[2], release=row[3], start=str(row[4]), end=str(row[5]), playbooks=row[6], ruleb=str(row[7]), rulei=str(row[8])) for row in db.get_rows(query)]
            print "aquisition done"
            return json.dumps(query_result)
        except Exception, e:
            print "Error [%r]" % (e)
            #sys.exit(1)


#CREATE TABLE IF NOT EXISTS `evenement` (
#  `id` int(11) NOT NULL AUTO_INCREMENT,
#  `title` varchar(255) NOT NULL,
#  `instance` varchar(255) NOT NULL,
#  `release` varchar(10) NOT NULL,
#  `start`  datetime NOT NULL,
#  `end` datetime NOT NULL,
#  `playbooks` varchar(255) NOT NULL,
#  `rule` varchar(6) NOT NULL,
#  PRIMARY KEY (`id`),
#  UNIQUE KEY `id` (`id`)
#) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
