#!/usr/bin/env Python
# -*- coding:utf-8 -*-

import os,time
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
from tornado.options import define, options

define("port", default = 5566, help = "run on the given port", type = int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''<html><head><title>Linux Http File Server</title></head><body>''')
        upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files') 
        if not os.path.exists(upload_path):
                os.mkdir(upload_path)
        filelist = os.listdir('files')
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'files')
        self.write('''<table width = "50%" border = "1"><tr><th>filename</th><th>filesize</th><th>last modified time</th></tr>''')
        for f in filelist:
            filename = ('''<tr align = "center"><td><a href="./download/%s">%s</td>''') % (f,f)
            self.write(filename)
            filesize = ('''<td>%s byte</td>''') % os.path.getsize(os.path.join(filepath,f))
            self.write(filesize)
            updated = ('''<td>%s</td>''') % time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getmtime(os.path.join(filepath,f))))
            self.write(updated)
        self.write('''</tr>''')
        self.write('''<form action = 'upload' enctype = "multipart/form-data" method = 'post'><input
    type = 'file' name = 'file'/><input type = 'submit'value = 'upload' /></form>''')
        self.write('''</body></html>''')

    def post(self):
        pass

class UploadHandler(tornado.web.RequestHandler):
    def get(self):
       pass

    def post(self):
        if self.request.files:
            upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files') 
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            file_metas = self.request.files['file']  
            for meta in file_metas:
                filename = meta['filename']
                filepath = os.path.join(upload_path, filename)
                with open(filepath, 'wb') as f:
                    f.write(meta['body'])
                self.redirect('../')

settings = dict(
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
    static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "statics"),
    )

url = [
	(r'/',IndexHandler),
	(r'/upload',UploadHandler),
    (r'/download/(.*)', tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(os.path.abspath(__file__)),"files")}),
]

application = tornado.web.Application(
	handlers = url,
	**settings
    )


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    print "Development server is running at http://127.0.0.1:%s" % options.port
    print "Quit the server with Control-C"

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

