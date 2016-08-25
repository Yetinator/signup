#!/usr/bin/env python
import os 
import webapp2
import jinja2
import re

template_dir=os.path.join(os.path.dirname(__file__), 'templates')#creates a path
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))#assigns path to

def userfunction(username):
    """
        This function returns false if there is a problem with the name.
    """
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)  

def passwordfunction(password, verify):
    PASS_RE = re.compile(r"^.{3,20}$")
    if password == verify:
        return PASS_RE.match(password)
    else:
        return False
    
def emailfunction(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    if email == '':
        return True
    return EMAIL_RE.match(email)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        """
        Writes whatever I tell it.  I'm the boss.  
        """
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        """
            creates a jinja template object out of thin air and pukes it into 
            the calling function. (in this case render() so it can later be 
            written)
        """
        t = jinja_env.get_template(template)
        return t.render(params)
       
    def render(self, template, **kw):
        """
            calls the write method and the render_str function
        """
        self.write(self.render_str(template, **kw))

class InputForm(Handler):
    def get(self):
        """
            Get original form
        """     
        self.render("signup.html")
    
class Submit(Handler):
    """
        Handles the submission
    """
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        errors = False
        errorName = ""
        errorPass = ""
        errorEmail = ""
        if not (userfunction(username)):
            errorName += "There is an error with the name somehow. "
            errors = True
        
        if not (passwordfunction(password, verify)):
            errors = True
            errorPass += "There is an error with your password somehow"
        
        if not (emailfunction(email)):
            errors = True
            errorEmail = "Your email is just wrong"
      
        if errors == True:
            self.render("signup.html", username=username, email=email, errorName = errorName, errorPass=errorPass, errorEmail=errorEmail)
        else:
            self.redirect('/success?username='+username)
        
        
class successForm(Handler):
    def get(self):
        username = self.request.get('username')
        self.render("success.html", username=username)

app = webapp2.WSGIApplication([
    ('/', InputForm),
    ('/submit', Submit),
    ('/success', successForm)
], debug=True)
