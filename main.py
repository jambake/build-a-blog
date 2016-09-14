import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

#def get_posts(limit, offset):


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Posts(db.Model):

    title = db.StringProperty(required = True)
    newpost = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):

    def render_front(self, title="", newpost="", error=""):
        newposts = db.GqlQuery("SELECT * FROM Posts ORDER BY created DESC LIMIT 5")

        self.render("frontpage.html", title=title, newpost=newpost, error=error, newposts=newposts)

    def get(self):
        self.render_front()


class Blog(Handler):

    def render_front(self, title="", newpost="", error=""):
        newposts = db.GqlQuery("SELECT * FROM Posts ORDER BY created DESC")

        self.render("blog.html", title=title, newpost=newpost, error=error, newposts=newposts)

    def get(self):
        self.render_front()

class NewPost(Handler):

    def render_front(self, title="", newpost="", error=""):
        newposts = db.GqlQuery("SELECT * FROM Posts")

        self.render("newpost.html", title=title, newpost=newpost, error=error, newposts=newposts)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        newpost = self.request.get("newpost")

        if title and newpost:
            a = Posts(title = title, newpost = newpost)
            a.put()

            self.redirect("/blog/%s" % a.key().id())

        else:
            error = "We need both a title and blog post!"
            self.render_front(title, newpost, error)

class ViewPostHandler(webapp2.RequestHandler):

    def get(self, id):

        post_data = Posts.get_by_id(int(id))
        newpost = post_data.newpost
        self.response.write(newpost)

class About(Handler):

    def get(self):
        self.render("about.html")



app = webapp2.WSGIApplication([
    ('/', MainPage), ('/blog', Blog), ('/newpost', NewPost), ('/about', About), webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
