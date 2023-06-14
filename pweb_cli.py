from pf_flask_web.pweb_engine import PWebEngine

pweb_engine = PWebEngine.start("PWebEngine", __file__)
pweb_engine.version = "0.0.1"

cli = pweb_engine.cli
wsgi = pweb_engine.get_app()

if __name__ == '__main__':
    pweb_engine.run()

