import web
import sys
sys.path.append('/root/2AU_python_script')
from myconfig import *

urls = (
    '/getEvents', 'getEvents.GetEvents',
    '/updateEvent', 'updateEvent.UpdateEvent',
    '/deleteEvent', 'deleteEvent.DeleteEvent',
    '/insertEvent', 'insertEvent.InsertEvent'
)

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

if __name__ == "__main__":
    app = MyApplication(urls, globals())
    app.run(port=int(server_port))
