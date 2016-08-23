#!/usr/bin/env python
import os 
import webapp2
import jinja2

template_dir=os.path.join(os.path.dirname(__file__), 'templates')#creates a path
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))#assigns path to

def hasSpace(name):
    for i in name:
        if i == " ":
            return True
    return False

def validEmail(email):
    """
        @ must exist, and before dot(.)
        length of at least 3??
    """
    atExist = False
    dotExist = False
    if len(email) < 3:
        return False
    for i in range(len(email)):
        if email[i] == "@":
            for j in range(i,len(email)):
                if email[j] == ".":
                    return True
            return False
    return False 

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
    def get(self):
        username = self.request.get('username')
        password = self.request.get('password')
        confirm = self.request.get('confirm')
        email = self.request.get('email')
        errors = False
        errorName = ""
        errorPass = ""
        errorEmail = ""
        if username == '':
            errorName += "We can't steal your identity without a Username. <br> Please enter a Username now."
            errors = True
        if hasSpace(username):
            errorName += "<br>Your Username cannot have a space."
            errors = True
        if (len(username) < 3 or len(username) > 15) and username != '':
            errorName += "<br>Your Username is too long, too short, or stupid"
            errors = True
        if password == '':
            errors = True
            errorPass += "You did not enter a password.  <br>Please do that now."
        if len(password) < 5 and password != '':
            errors = True
            errorPass += "Your password doesn't seem secure enough.<br> We're stealing it anyway, but we would like you to enter a longer password"
        if len(password) > 20:
            errors = True
            errorPass += "<br>Whoa!  That's too long.  We can't write all that down when you're not looking!!"
        if password != confirm:
            errors = True
            errorPass += "<br>Your password does not match the confirmation. <br>We're not sure which one to steal!!"
        if validEmail(email) == False and email != '':
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
