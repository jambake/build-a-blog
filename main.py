import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):

    title = db.StringProperty(required = True)
    new = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):

    def render_front(self, title="", new="", error=""):
        newposts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")

        self.render("base.html", title=title, new=new, error=error, newposts=newposts)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        new = self.request.get("new")

        if title and new:
            a = Post(title = title, new = new)
            a.put()

            self.redirect("/")

        else:
            error = "We need both a title and blog post!"
            self.render_front(title, new, error)


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
