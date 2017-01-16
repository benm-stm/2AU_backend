# myconfig.py:
#python 2AU.py 'codex 9.0' codex-test.cro.st.com,127.0.0.1 raf.yml,test.yml 8
#Needed modules
#pip install ansible
#pip install paramiko PyYAML Jinja2 httplib2 six (to be verified)

#ansible source http://stackoverflow.com/questions/35368044/how-to-use-ansible-2-0-python-api-to-run-a-playbook

#see https://serversforhackers.com/running-ansible-2-programmatically

#needed steps
# http://docs.ansible.com/ansible/intro_installation.html#running-from-source

app_location = "/root/2AU_python_script"
python_location = "/usr/local/bin/python"
#sendmail, download packages and create repo before the deadline in days
deadline = 3
opretionLaunchTime = "6:00h"
opretionFinishTime = "7:00h"

#email configuration
send_mail = 1
sender_email_address = "upgradeAutomation@st.com"
#In case you want to force the email address for only one type of mail you have to force it in the mail template under mailContent by specifying th email like it is shown below
#===TO
#mohamed-rafik.benmansour@st.com
#TO===

recipients_email_address = ["codex-team@lists.codex.cro.st.com"]

smtp_server= "smtpapp1.cro.st.com"

testPlatformLink = "crx19006.cro.st.com:8082"

# The conception of the input is a sum of squares (8 4 2 1) like the access rules in linux (which is 4 2 1)
# If we want to add a new entry in our defined_rules table the next digit will be 16 ...
#  8:"sendmail_to_team",
#  4:"sendmail_to_prodops",
#  2:"sendmail_to_run_tests",
#  1:"run_playbooks"
defined_rules = {
    "8":"sendmail_to_team",
    "4":"sendmail_to_prodops",
    "2":"sendmail_to_run_tests",
    "1":"run_playbooks"
    }

#to run related playbooks
hostingPlatform = ["codex-test.cro.st.com"]
#if set to 0, even when passed in the params the playbooks won't launch
run_playbooks = 1
playbooks_path = "/root/2AU_python_script/playbook/playbooks/"

#logging
log_file = "/root/2AU_python_script/2AU.log"
log_lvl = "logging.DEBUG"
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

#tasks chron
cron_file = "/var/spool/cron/root"
#if you change this var make sure to erase its content first
section_name = "2AU"
#cron behaviour
cron_hour = 9
cron_minute = 0

#DB informations
#DB creation query
#GRANT ALL PRIVILEGES ON dbTest.* To 'user'@'hostname' IDENTIFIED BY 'password';

#in order to launch the restful server you have to issue the following comma	nd as root
# cd /root/2AU_python_script/webservices & python webserver.py > /dev/null 2>&1 
db_host="localhost"
db_user="admin"
db_passwd="password"
db_name="2AU"
db_port="3306"

#Web server infos
server_port = "8080"
