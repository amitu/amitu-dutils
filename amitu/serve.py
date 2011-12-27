import os, argparse
from amitu.wsgiserver import CherryPyWSGIServer

def runserver(ip, port, settings_module=None):
    if settings_module: os.environ["DJANGO_SETTINGS_MODULE"] = settings_module

    from django.core.handlers.wsgi import WSGIHandler
    server = CherryPyWSGIServer((ip, port), WSGIHandler())

    print "Started http server on %s:%s." % (ip, port)
    print "Hit ^C to exit."

    try:
        server.start()
    except KeyboardInterrupt:
        print "Shutting down gracefully."
        server.stop()

def main():
    parser = argparse.ArgumentParser(
        description="Serve a django project with cherrypy's wsgiserver"
    )
    parser.add_argument("--ip", default="127.0.0.1")
    parser.add_argument("--port", default=8001, type=int)
    parser.add_argument("--setting", default="settings")
    parser.add_argument("project", nargs="?")

    args = parser.parse_args()

    if args.project:
        runserver(args.ip, args.port, "%s.%s" % (args.project, args.setting))
    else:
        runserver(args.ip, args.port, args.setting)

if __name__ == "__main__":
    main()

