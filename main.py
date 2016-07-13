#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Guestbook

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("main.html")

class VnosHandler(BaseHandler):
    def post(self):
        ime = self.request.get("ime")
        priimek = self.request.get("priimek")
        email = self.request.get("email")
        message = self.request.get("sporocilo")
        date = self.request.get("datum")

        guestbook = Guestbook(name=ime, surname=priimek, email=email, message=message)
        guestbook.put()

        return self.write("You have written: " + "\n" + " name: " + ime + " surname: " + priimek + " email: " + email +
                          " message: " + message)

class SeznamVnosovHandler(BaseHandler):
    def get(self):
        guests = Guestbook.query().fetch()

        guestsbooks = { "guests": guests }

        return self.render_template("seznam_vnosov.html", params=guestsbooks)

class PosamezenVnosHandler(BaseHandler):
    def get(self, guestbook_id):
        guest = Guestbook.get_by_id(int(guestbook_id))
        params = { "guest": guest }
        return self.render_template("posamezen_vnos.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vnosi', VnosHandler),
    webapp2.Route('/seznam_vnosov', SeznamVnosovHandler),
    webapp2.Route('/posamezen_vnos/<guestbook_id:\\d+>', PosamezenVnosHandler),
], debug=True)

