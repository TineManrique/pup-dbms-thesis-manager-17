import csv
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
import jinja2
import os
import logging
import json
import urllib
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class User(ndb.Model):
    created_by = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(indexed=True)
    first_name = ndb.StringProperty(indexed=True)
    last_name = ndb.StringProperty(indexed=True)
    user_type = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class Faculty(ndb.Model):
    faculty_name = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(indexed=True)
    phone_number = ndb.StringProperty(indexed=True)
    birthdate =ndb.StringProperty(indexed=True)
    department = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_by_name(cls, adviser_name):
    	try:
    		return ndb.Key(cls, adviser_name).get()
    	except Exception:
    		return None

class Student(ndb.Model):
    full_name = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(indexed=True)
    phone_number = ndb.StringProperty(indexed=True)
    student_number = ndb.StringProperty(indexed=True)
    birthdate =ndb.StringProperty(indexed=True)
    year_graduated = ndb.StringProperty(indexed=True)
    department = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
'''
@classmethod
def get_by_key(cls, keyname):
    try:
        return ndb.Key(cls, keyname).get()
    except Exception:
        return None
'''

class University(ndb.Model):
    university_name = ndb.StringProperty(indexed=True)
    address = ndb.StringProperty(indexed=True)
    initials =ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class College(ndb.Model):
    college_name = ndb.StringProperty(indexed=True)
    university_key = ndb.KeyProperty(indexed=True)
    department_list = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class Department(ndb.Model):
    department_name = ndb.StringProperty(indexed=True)
    college_key = ndb.KeyProperty(indexed=True)
    chairperson = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_department(cls, dept, college, uni):
    	university = University.query(University.university_name == uni).get()
    	college =College.query(College.university_key == university.key).get()
    	return cls.query(cls.college_key == college.key).get()


class Thesis(ndb.Model):
    
    created_by = ndb.KeyProperty(indexed=True)
    year = ndb.StringProperty(indexed=True)
    title = ndb.StringProperty(indexed=True)
    subtitle = ndb.StringProperty()
    abstract = ndb.TextProperty()
    #adviser = ndb.StringProperty(indexed=True)
    section = ndb.StringProperty()
    adviser_key = ndb.KeyProperty(indexed=True)
    proponent_keys = ndb.KeyProperty(repeated=True)
    department_key = ndb.KeyProperty(indexed=True)
    tags = ndb.StringProperty(repeated=True)
    # member1 = ndb.StringProperty(indexed=True)
    # member2 = ndb.StringProperty(indexed=True)
    # member3 = ndb.StringProperty(indexed=True)
    # member4 = ndb.StringProperty(indexed=True)
    # member5 = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

def Process_CSV(blob_info):
	blob_reader = blobstore.BlobReader(blob_info.key())
	reader = csv.DictReader(blob_reader, delimiter=',')
	uni = University(university_name='Polytechnic University of the Philippines', address='Sta. Mesa, Manila', initials='PUP')
	uni.put()
	
	college = College(college_name='Engineering', university_key=uni.key)
	college.put()
	
	dept = Department(department_name='Computer Engineering', chairperson= 'Pedrito Tenerife Jr.', college_key=college.key)
	dept.put()

	for row in reader:
		user = users.get_current_user()
		tag_list = []
		articles={'a','an', 'the','is', 'are', 'this', 'that', 'for', 'to', 'and','with', 'as', 'based'}
		title_list = row['Title'].lower().split(' ')
		thesis = Thesis(id=''.join(title_list))
		tag_list.extend(title_list)
		thesis.year = row['Year']
		thesis.title = row['Title']
		thesis.abstract = row['Abstract']
		thesis.section = row['Section']
		thesis.subtitle = ''
		faculty = Faculty.get_by_name(row['Adviser'].lower().replace(' ', ''))
		if faculty is None:
			if row['Adviser'] != '':
				faculty = Faculty(id=row['Adviser'].lower().replace(' ', ''), 
					#first_name=row['Adviser'].split(' ')[0].title(),  last_name=row['Adviser'].split(' ')[1].title())
					faculty_name=row['Adviser'].title())
				tag_list.extend(row['Adviser'].lower().split(' '))
			else:
				faculty = Faculty(id='Anonymous', faculty_name='Professor')
			faculty.put()
			thesis.adviser_key = faculty.key
		else:
			#tag_list.extend(row['Adviser'].lower().split(' '))
			thesis.adviser_key = faculty.key
		member_list = [
			row['Member 1'], 
			row['Member 2'], 
			row['Member 3'], 
			row['Member 4'], 
			row['Member 5']
			]
		member_keys = []
		for member in member_list:
			if member != '':
				tag_list.extend(member.lower().split(' '))
				student = Student(full_name=member)
				student.put()
				member_keys.append(student.key)
		for tag in tag_list:
			if tag not in articles:
				tag=tag.replace('.','').replace(',','').replace(':','').replace(';','')
		thesis.proponent_keys = member_keys
		thesis.tags = tag_list
		thesis.department_key = dept.key
		thesis.put()
	

class UploadPageHandler(blobstore_handlers.BlobstoreUploadHandler):
	def get(self):

		upload_url = blobstore.create_upload_url('/upload')
		template_data = {
			'upload_url': upload_url
		}
		template = JINJA_ENVIRONMENT.get_template('upload.html')
		self.response.write(template.render(template_data))
		
	def post(self):
		upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
		blob_info = upload_files[0]
		Process_CSV(blob_info)

		blobstore.delete(blob_info.key())  # optional: delete file after import
		self.redirect('/upload')

class LoginPageHandler(webapp2.RequestHandler):
    def get(self):
      
        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '

            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
  
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
            
        else:
            url = users.create_login_url('/register')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
           
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class RegisterPageHandler(webapp2.RequestHandler):

    def get(self):
        loggedin_user = users.get_current_user()
        if loggedin_user: 
            user_key = ndb.Key('User', loggedin_user.user_id())
            user = user_key.get()
            if user:
                url = users.create_logout_url('/home')
                url_linktext = 'LOG OUT'
                status = 'Hello, '
                template_values = {
                    'url': url,
                    'url_linktext': url_linktext,
                    'status' : status
                }
                self.redirect('/home')
            else:
                template = JINJA_ENVIRONMENT.get_template('register.html')
                self.response.write(template.render())
        else:
            self.redirect(users.create_login_url('/register'))

    def post(self):

        user = User(id=users.get_current_user().user_id(), email= users.get_current_user().email(), first_name = self.request.get('first_name'), last_name = self.request.get('last_name')) 
        user.put()
        self.redirect('/home')

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
       
        faculty = Faculty.query().order(-Faculty.date).fetch()
        logging.info(faculty)

        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'faculty_list':faculty

            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
            
    def post(self):
       
        thesis = Thesis()
        department=Department()
        faculty = Faculty()
        college = College()
        student = Student()

        department_name = self.request.get('department_name')
        adviser_name = self.request.get('adviser')
        department = Department.get_by_key(department_name)
        
        if department is None:
            department = Department(key=ndb.Key(Department, department_name), department_name=department_name)
            department.put()

        thesis.department_key = department.put()
       
       
        thesis.email = users.get_current_user().email()
        thesis.year = self.request.get('year')
        thesis.title = self.request.get('title')
        thesis.subtitle = self.request.get('subtitle')
        thesis.abstract = self.request.get('abstract')
        
        thesis.section = self.request.get('section')
        thesis.key = thesis.put()
        thesis.put()
        self.redirect('/home')


class Filter2011Page(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        thesis_query = Thesis.query(Thesis.year == "2011")

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'thesis_query': thesis_query
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('filter.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class Filter2012Page(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        thesis_query = Thesis.query(Thesis.year == "2012")

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'thesis_query': thesis_query
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('filter.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class Filter2013Page(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        thesis_query = Thesis.query(Thesis.year == "2013")

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'thesis_query': thesis_query
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('filter.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class Filter2014Page(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        thesis_query = Thesis.query(Thesis.year == "2014")

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'thesis_query': thesis_query
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('filter.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())


class Filter2015Page(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        thesis_query = Thesis.query(Thesis.year == "2015")

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'thesis_query': thesis_query
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('filter.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class ThesisListPage(webapp2.RequestHandler):
    def get(self):
        thesis_list = []
        thesiss = Thesis.query().order(-Thesis.date).fetch()
        logging.info(thesiss)
        #thesiss = Thesis.query().order(-Thesis.date).fetch()
        for thes in thesiss:
            thesis_list.append({
                    'thesis_url':thes.key.urlsafe(),
                    'thesis_title':thes.title,
                    'thesis_year':thes.year
                    });

        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'thesis_list': thesis_list
            }

            
            template = JINJA_ENVIRONMENT.get_template('thesis_list_page.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class APIThesisHandler(webapp2.RequestHandler):
    def get(self):
        thesiss = Thesis.query().order(-Thesis.date).fetch()
        users = User.query().order(-User.date).fetch()
        thesis_list = []
        user_list = []

        for thesis in thesiss:
            thesis_list.append({
                'id': thesis.key.urlsafe(),
                'department_key': thesis.department_key,
                'year' : thesis.year,
                'title' : thesis.title,
                'subtitle' : thesis.subtitle,
                'abstract' : thesis.abstract,
                'adviser_key' : thesis.adviser_key,
                'section' : thesis.section,
                'proponent_keys': thesis.proponent_keys,
                'tags': thesis.tags
                });

        response = {
             'result' : 'OK',
             'data' : thesis_list
        }

        for user in users:
            user_list.append({
                'id': user.key.urlsafe(),
                'created_by': user.created_by,
                'email' : user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                });
            
        response = {
             'result' : 'OK',
             'data' : user_list
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        thesis = Thesis()
        user = User()
       
        user.first_name = self.request.get('first_name')
        user.last_name = self.request.get('last_name')

        thesis.created_by = users.get_current_user().user_id()
        thesis.email = users.get_current_user().email()
        thesis.department = self.request.get('department')
        thesis.year = self.request.get('year')
        thesis.title = self.request.get('title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser_key = self.request.get('adviser_key')
        thesis.section = self.request.get('section')
        thesis.proponent_keys = self.request.get('proponent_keys')
        thesis.tags = self.request.get('tags')

        thesis.key = thesis.put()
        user.key = user.put()
        thesis.put()
        user.put()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
        'result' : 'OK',
        'data':{
                'created_by': thesis.created_by,
                'email' : thesis.email,              
                'id': thesis.key.urlsafe(),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.user_type,
                'department_key': thesis.department_key,
                'year' : thesis.year,
                'title' : thesis.title,
                'subtitle' : thesis.subtitle,
                'abstract' : thesis.abstract,
                'adviser' : thesis.adviser_key,
                'section' : thesis.section,
                'proponent_keys': thesis.proponent_keys,
                'tags' : thesis.tags
        }
        }
        self.response.out.write(json.dumps(response))


class DisplayThesisPage(webapp2.RequestHandler):
    def get(self, thesis_id):
        #thesis = Thesis.query().order(-Thesis.date).fetch()

        #t = Thesis.query().fetch()
        

        #for t in thesis:
        	#thesis_title= t.title

        #qry = Thesis.query(Thesis.tags.IN(thesis.tags))
        thesis_list = []
        thesiss = Thesis.query().order(-Thesis.date).fetch()
        logging.info(thesiss)
        #thesiss = Thesis.query().order(-Thesis.date).fetch()
        for thes in thesiss:
            thesis_list.append({
                    'thesis_url':thes.key.urlsafe(),
                    'thesis_title':thes.title,
                    'thesis_year':thes.year,
                    'thesis_abstract': thes.abstract
                    });
        user = users.get_current_user()

        if user:

            
            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'thesis_list': thesis_list
            #'title': title
            #'thesis_title': thesis_title,
            #'thesis_title': thesis_title,
            #'thesis_year': thesis_year,
            #'qry':qry

            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('view_thesis.html')
            self.response.write(template.render(template_values))
            

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class SearchPage(webapp2.RequestHandler):

    def get(self):
        thesis = Thesis.query().fetch()
        student = Student.query().fetch()
        
        user = users.get_current_user()

        #thesis_query = Thesis.query(Thesis.title.IN("Automated"))

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'thesis_list': thesis,
            'student_list': student

            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('search.html')
            self.response.write(template.render(template_values))
            #template = JINJA_ENVIRONMENT.get_template(thesis.key.urlsafe())
           

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class DeleteEntry(webapp2.RequestHandler):
    def get(self, thesis_id):
        thesis = Thesis.get_by_id(int(thesis_id))
        thesis.key.delete()
        self.redirect('/thesis/list/all')
        #self.response.out.write('<alert>Successfully Deleted</alert>')


class EditEntry(webapp2.RequestHandler):
    def get(self, thesis_id):
        thesis = Thesis.get_by_id(int(thesis_id))
        template_data = {
            'thesis': thesis
        }
        user = users.get_current_user()

        if user:

            url = users.create_logout_url(self.request.uri)
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            }
        
        template = JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render(template_values))
        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_data))

    def post(self, thesis_id):
        
        thesis = Thesis.get_by_id(int(thesis_id))
        thesis.created_by = users.get_current_user().user_id()
        thesis.email = users.get_current_user().email()
        
        thesis.department_key = self.request.get('department_key')
        thesis.year = self.request.get('year')
        thesis.title = self.request.get('title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = self.request.get('section')
        thesis.proponent_keys = self.request.get('proponent_keys')
        thesis.tags = self.request.get('tags')
       
        thesis.put()
        self.redirect('/')

class LoginPageHandler(webapp2.RequestHandler):
    def get(self):
      
        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '

            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
  
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
            
        else:
            url = users.create_login_url('/register')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
           
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
          
class StudentCreatePageHandler(webapp2.RequestHandler):
    def get(self):
        
        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,

            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('studentcreate.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
            
    def post(self):
       
        student = Student()
       
        student.email = self.request.get('email')
        student.full_name = self.request.get('full_name')
        student.phone_number = self.request.get('phone_number')
        student.student_number = self.request.get('student_number')
        student.birthdate = self.request.get('birthdate')
        student.year_graduated = self.request.get('year_graduated')
        student.department_key = self.request.get('department_key')

       
        student.key = student.put()
        student.put()
        self.redirect('/student/create')

class FacultyCreatePageHandler(webapp2.RequestHandler):

    def get(self):
       
        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('facultycreate.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
            
    def post(self):
       
        faculty = Faculty()
       
        faculty.email = self.request.get('email')
        faculty.faculty_name = self.request.get('faculty_name')
        faculty.phone_number = self.request.get('phone_number')
        faculty.birthdate = self.request.get('birthdate')
        faculty.department = self.request.get('department')


        faculty.key = faculty.put()
        faculty.put()
        self.redirect('/faculty/create')

class UniversityCreatePageHandler(webapp2.RequestHandler):
    
    def get(self):
       
        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('universitycreate.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
            
    def post(self):
       
        university = University()
       
        university.university_name = self.request.get('university_name')
        university.address = self.request.get('address')
        university.initial= self.request.get('initial')

        university.key = university.put()
        university.put()
        self.redirect('/university/create')

class CollegeCreatePageHandler(webapp2.RequestHandler):
    
    def get(self):

        #college = College(college_name=college_name, university_key=university.key)
        #college.put()

        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('collegecreate.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
            
    def post(self):
       
        college = College()
       
        college.college_name = self.request.get('college_name')
        college.university = self.request.get('university')
        college.department_list =self.request.get('department_list')
       
        college.key = college.put()
        college.put()
        self.redirect('/college/create')

class DepartmentCreatePageHandler(webapp2.RequestHandler):
    
    def get(self):
       
        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('departmentcreate.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
            
    def post(self):
       
        department = Department()
       
        department.department_name = self.request.get('department_name')
        department.college = self.request.get('college')
        department.chairperson = self.request.get('chairperson')
       
        department.key = department.put()
        department.put()
        self.redirect('/department/create')

class StudentListPage(webapp2.RequestHandler):
    def get(self):
        student = Student.query().order(-Student.date).fetch()
        logging.info(student)
        
        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'student_list': student
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('student_list_page.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class FacultyListPage(webapp2.RequestHandler):
    def get(self):
        faculty = Faculty.query().order(-Faculty.date).fetch()
        logging.info(faculty)
        
        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'faculty_list': faculty
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('faculty_list_page.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class UniversityListPage(webapp2.RequestHandler):
    def get(self):

        university = University.query().order(-University.date).fetch()
        logging.info(university)

        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'university_list': university
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('university_list_page.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class DepartmentListPage(webapp2.RequestHandler):
    def get(self):

        department = Department.query().order(-Department.date).fetch()
        logging.info(department)

        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'department_list': department
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('department_list_page.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class CollegeListPage(webapp2.RequestHandler):
    def get(self):

        college = College.query().order(-College.date).fetch()
        logging.info(college)

        user = users.get_current_user()

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'college_list': college
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('college_list_page.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_login_url('/home')
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 
            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())

class DeleteEntry(webapp2.RequestHandler):
    def get(self, thesis_id):
        thesis = Thesis.get_by_id(thesis_id)
        thesis.key.delete()
        self.redirect('/thesis/list/all')
        #self.response.out.write('<alert>Successfully Deleted</alert>')


class EditEntry(webapp2.RequestHandler):
    def get(self, thesis_id):
        #thesis = Thesis.get_by_id(thesis_id)
        key = ndb.Key('Thesis', thesis_id)
        thesis = key.get()
        template_data = {
            'thesis': thesis
        }
        user = users.get_current_user()

        if user:

            url = users.create_logout_url(self.request.uri)
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            }
        
        template = JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render(template_values))
        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_data))

    def post(self, thesis_id):
        
        thesis = Thesis.get_by_id(thesis_id)
        thesis.created_by = users.get_current_user().user_id()
        thesis.email = users.get_current_user().email()
        
        thesis.department_key = self.request.get('department_key')
        thesis.year = self.request.get('year')
        thesis.title = self.request.get('title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = self.request.get('section')
        thesis.proponent_keys = self.request.get('proponent_keys')
        thesis.tags = self.request.get('tags')
       
        thesis.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
	('/edit_thesis/(.*)', EditEntry),
    ('/delete_thesis/(.*)', DeleteEntry),
	('/student/create', StudentCreatePageHandler),
    ('/faculty/create', FacultyCreatePageHandler),
    ('/university/create', UniversityCreatePageHandler),
    ('/college/create', CollegeCreatePageHandler),
    ('/department/create', DepartmentCreatePageHandler),
    ('/student/list', StudentListPage),
    ('/faculty/list', FacultyListPage),
    ('/faculty/list', FacultyListPage),
    ('/university/list', UniversityListPage),
    ('/department/list', DepartmentListPage),
    ('/college/list', CollegeListPage),
    ('/thesis/list/2011',Filter2011Page),
    ('/thesis/list/2012',Filter2012Page),
    ('/thesis/list/2013',Filter2013Page),
    ('/thesis/list/2014',Filter2014Page),
    ('/thesis/list/2015',Filter2015Page),
    ('/thesis/list/all', ThesisListPage),
    ('/thesis/(.*)', DisplayThesisPage),
    ('/api/thesis',APIThesisHandler),
    ('/upload', UploadPageHandler),
    ('/search', SearchPage),
    ('/register', RegisterPageHandler),
    ('/login', LoginPageHandler),
    ('/home', MainPageHandler),
    ('/', MainPageHandler)
    

   
], debug=True)
