import os, argparse
from werkzeug import run_simple, DebuggedApplication

def runserver(ip, port, settings_module=None, debug=False):
    if settings_module: os.environ["DJANGO_SETTINGS_MODULE"] = settings_module
    from django.core.handlers.wsgi import WSGIHandler

    app = WSGIHandler()

    if debug: app = DebuggedApplication(app, True)

    print "Started http server on %s:%s." % (ip, port)
    if debug: print "This is DEBUG server, HIGHLY INSECURE!"
    print "Hit ^C to exit."

    try:
        run_simple(ip, port, app)
    except KeyboardInterrupt:
        print "Shutting down gracefully."

def main():
    parser = argparse.ArgumentParser(
        description="Serve a django project with cherrypy's wsgiserver"
    )
    parser.add_argument("--ip", default="127.0.0.1")
    parser.add_argument("--port", default=8001, type=int)
    parser.add_argument("--setting", default="settings")
    parser.add_argument("--debug", default=False, action="store_true")
    parser.add_argument("project", nargs="?")

    args = parser.parse_args()

    if args.project:
        runserver(args.ip, args.port, "%s.%s" % (args.project, args.setting))
    else:
        runserver(args.ip, args.port, args.setting)

if __name__ == "__main__":
    main()




