import csv
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
import jinja2
import os
import logging
import json
import urllib


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
    def get_by_key(cls, keyname):
        try:
            return ndb.Key(cls, keyname).get()
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

    @classmethod
    def get_by_key(cls, keyname):
        try:
            return ndb.Key(cls, keyname).get()
        except Exception:
            return None

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
    
    @classmethod
    def get_by_key(cls, keyname):
        try:
            return ndb.Key(cls, keyname).get()
        except Exception:
            return None

    date = ndb.DateTimeProperty(auto_now_add=True)

class Thesis(ndb.Model):
    # username = ndb.StringProperty(indexed=True)
    # created_by = ndb.StringProperty(indexed=True)
    # email = ndb.StringProperty(indexed=True)
    # university = ndb.StringProperty(indexed=True)
    # college = ndb.StringProperty(indexed=True)
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

'''
thesiss = Thesis.query().order(-Thesis.date).fetch()
qry = Thesis.query(Thesis.year == '2011')

for qry in thesiss:
    thesis_list.append({
        'id': thesis.key.id(),
        'university':thesis.university,
        'title':thesis.title,
        'section':thesis.section
        });


f = csv.reader(open('PUPCOEThesisList.csv' , 'r'), skipinitialspace= True)
for row in f:
    thesis = Thesis()
    thesis.university = row[0]
    thesis.college = row[1]
    thesis.department = row[2]
    thesis.year = row[3]
    thesis.title = row[4]
    thesis.abstract = row[5]
    thesis.section =row[6]
    thesis.adviser = row[7]
    thesis.member1 = row[8]
    thesis.member2 = row[9]
    thesis.member3 = row[10]
    thesis.member4 = row[11]
    thesis.member5 = row[12]
    thesis.put()
'''

class ImportHandler(webapp2.RequestHandler):
    def get(self):
        file = open(os.path.join(os.path.dirname(__file__), 'PUPCOEThesisList.csv'))
        # logging.info(file)
        fileReader = csv.reader(file)

        department_key = ndb.Key(urlsafe='ah5kZXZ-cHVwLWRibXMtdGhlc2lzLW1hbmFnZXItMTdyFwsSCkRlcGFydG1lbnQYgICAgICAgAsM')
        department = department_key.get()
        college = department.college_key.get()
        university = college.university_key.get()
        logging.info(department.department_name + ' ' + college.college_name + ' ' + university.initials)

        #mem = []

        for row in fileReader:
            thesis = Thesis()
            thesis.year = row[3]
            thesis.title = row[4]
            subtitle = ''
            thesis.abstract = row[5]
            thesis.section = row[6]
            
            member1 = row[8]
            member2 = row[9]
            member3= row[10]
            member4 = row[11]
            member5= row[12]
            
            # thesis.department_key = department_key
            #thesis.tags = ['pupcoe', 'mcu']
            adviser_name = row[7] # 'Rodolfo Talan'
            adviser_keyname = adviser_name.strip().replace(' ', '').lower()
            adviser = Faculty.get_by_key(adviser_keyname)

            articles={'a','an', 'the','is', 'are', 'this', 'that', 'for', 'to', 'and'}
            tags = []
            title = thesis.title
            words = title.lower().split()

            for word in words:
                if word not in articles:
                    tags.append(word)
                    thesis.tags = tags

            '''
            for i in range(0, len(mem)):
                mem[0]_keyname =mem[0].strip().replace(' ', '').lower()
            '''

        
            proponent1_keyname = member1.strip().replace(' ', '').lower()
            proponent2_keyname = member2.strip().replace(' ', '').lower()
            proponent3_keyname = member3.strip().replace(' ', '').lower()
            proponent4_keyname = member4.strip().replace(' ', '').lower()
            proponent5_keyname = member5.strip().replace(' ', '').lower()
            proponent1 = Student.get_by_key(proponent1_keyname)
            proponent2 = Student.get_by_key(proponent2_keyname)
            proponent3 = Student.get_by_key(proponent3_keyname)
            proponent4 = Student.get_by_key(proponent4_keyname)
            proponent5 = Student.get_by_key(proponent5_keyname)
        

            if adviser is None:
                adviser = Faculty(key=ndb.Key(Faculty, adviser_keyname), faculty_name=adviser_name)
                adviser.put()
            thesis.department_key = department_key
            thesis.adviser_key = adviser.key
            thesis.put()

            
            if proponent1 is None:
                proponent1 = Student(key=ndb.Key(Student, proponent1_keyname), full_name=member1)
                proponent1.put()
            thesis.department_key = department_key
            thesis.proponent_keys = proponent1.key
            thesis.put()

            if proponent2 is None:
                proponent2 = Student(key=ndb.Key(Student, proponent2_keyname), full_name=member2)
                proponent2.put()
            thesis.department_key = department_key
            thesis.proponent_keys = proponent2.key
            thesis.put()

            if proponent3 is None:
                proponent3 = Student(key=ndb.Key(Student, proponent1_keyname), full_name=member3)
                proponent3.put()
            thesis.department_key = department_key
            thesis.proponent_keys = proponent3.key
            thesis.put()

            if proponent4 is None:
                proponent4 = Student(key=ndb.Key(Student, proponent1_keyname), full_name=member4)
                proponent4.put()
            thesis.department_key = department_key
            thesis.proponent_keys = proponent1.key
            thesis.put()

            if proponent5 is None:
                proponent5 = Student(key=ndb.Key(Student, proponent1_keyname), full_name=member5)
                proponent5.put()
            thesis.department_key = department_key
            thesis.proponent_keys = proponent5.key
            thesis.put()
        

        template = JINJA_ENVIRONMENT.get_template('main.html')
        #self.response.write()

class SetupDBHandler(webapp2.RequestHandler):
    def get(self):

        university = University(university_name='Polytechnic University of the Philippines', initials='PUP')
        university.put()

        #up = University(name='University of the Philippines', initials='UP')
        #up.put()

        college = College(college_name='Engineering', university_key=university.key)
        college.put()

        #college_up = College(name='Engineering', university_key=up.key)
        #college_up.put()

        #archi_college = College(name='Architecture', university_key=university.key)
        #archi_college.put()

        coe_department = Department(department_name='COE', college_key=college.key)
        coe_department.put()

        #coe_up_department = Department(name='COE', college_key=college_up.key)
        #coe_up_department.put()

        #ece_department = Department(name='ECE', college_key=college.key)
        #ece_department.put()

        self.response.write('Datastore setup completed')

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
        #mem = []

        department_name = self.request.get('department_name')
        adviser_name = self.request.get('adviser')
        '''
        mem[0] = self.request.get('mem1')
        mem[1] = self.request.get('mem2')
        mem[2] = self.request.get('mem3')
        mem[3] = self.request.get('mem4')
        mem[4] = self.request.get('mem5')

        for i in range(0, len(mem)):
            student.full_name = mem[i]
            thesis.proponent_keys.append(student.put())
        '''
        #department_keyname = department_name
        department = Department.get_by_key(department_name)
        '''
        faculty = Faculty.get_by_key(adviser_name)
        #adviser.put()

        if faculty is None:
            faculty = Faculty(key=ndb.Key(Faculty, faculty_name), faculty_name=adviser_name)
            faculty.put()

        thesis.adviser_key = faculty.put()
        '''

        if department is None:
            department = Department(key=ndb.Key(Department, department_name), department_name=department_name)
            department.put()

        thesis.department_key = department.put()
       
        #thesis.created_by = users.get_current_user().user_id()
        thesis.email = users.get_current_user().email()
        #thesis.department_key = self.request.get('department')
        thesis.year = self.request.get('year')
        thesis.title = self.request.get('title')
        thesis.subtitle = self.request.get('subtitle')
        thesis.abstract = self.request.get('abstract')
        
        thesis.section = self.request.get('section')
        #thesis.proponent_keys = self.request.get('proponent')
        #thesis.tags= self.request.get('tags')
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

class FilterAdviserPage(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        faculty = Faculty.query().fetch()
        adviser_name = self.request.get('adviser')
        thesis_query = Thesis.query(Thesis.adviser_key == adviser_name)

        if user:

            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'thesis_query': thesis_query,
            'faculty_list': faculty
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('filteradviser.html')
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
        thesis = Thesis.query().order(-Thesis.date).fetch()
        
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
            'thesis_list': thesis

            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('search.html')
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

class APIThesisHandler(webapp2.RequestHandler):
    def get(self):
        thesiss = Thesis.query().order(-Thesis.date).fetch()
        users = User.query().order(-User.date).fetch()
        thesis_list = []
        user_list = []

        for thesis in thesiss:
            thesis_list.append({
                'id': thesis.key.id(),
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
                'id': user.key.id(),
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
                'id': thesis.key.id(),
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

class APIStudentHandler(webapp2.RequestHandler):
    def get(self):
        students = Student.query().order(-Student.date).fetch()
        #users = User.query().order(-User.date).fetch()
        student_list = []
        #user_list = []

        for student in students:
            student_list.append({
                'id': student.key.id(),
                'full_name': student.full_name,
                'email': student.email,
                'student_number':student.student_number,
                'phone_number':student.phone_number,
                'birthdate':student.birthdate,
                'year_graduated':student.year_graduated
                });

        response = {
             'result' : 'OK',
             'data' : student_list
        }
        '''
        for user in users:
            user_list.append({
                'id': user.key.id(),
                'created_by': user.created_by,
                'email' : user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                });
            
        response = {
             'result' : 'OK',
             'data' : user_list
        }
        '''
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        student = Student()
    
        
        student.full_name = self.request.get('full_name')
        student.email = self.request.get('email')
        student.student_number = self.request.get('student_number')
        student.phone_number = self.request.get('phone_number')
        student.birthdate = self.request.get('birthdate')
        student.year_graduated= self.request.get('year_graduated')
       

        student.key = student.put()
        student.put()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
        'result' : 'OK',
        'data':{
                'id': student.key.id(),
                'full_name': student.full_name,
                'email': student.email,
                'phone_number':student.phone_number,
                'birthdate':student.birthdate,
                'year_graduated':student.year_graduated
        }
        }
        self.response.out.write(json.dumps(response))

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

class ThesisListPage(webapp2.RequestHandler):
    def get(self):

        thesiss = Thesis.query().order(-Thesis.date).fetch()
        logging.info(thesiss)

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
            'thesis_list': thesiss
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
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
                'url_linktext': url_linktext,
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

class DisplayStudentPage(webapp2.RequestHandler):
    def get(self, student_id):

        student = Student.get_by_id(int(student_id))

        #student = Student.query().order(-Student.date).fetch()
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
            template = JINJA_ENVIRONMENT.get_template('view_student.html')
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
'''
class DisplayUniversityPage(webapp2.RequestHandler):
    def get(self, student_id):
        universities = University.get_by_id(int(student_id))

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
            'university': universities
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('view_university.html')
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

class DisplayFacultyPage(webapp2.RequestHandler):
    def get(self, student_id):
        faculties = Thesis.get_by_id(int(student_id))

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
            'faculty': faculties
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('view_faculty.html')
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

class DisplayCollegePage(webapp2.RequestHandler):
    def get(self, student_id):
        colleges = Thesis.get_by_id(int(student_id))

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
            'college': colleges
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('view_college.html')
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
'''


class DisplayThesisPage(webapp2.RequestHandler):
    def get(self, student_id):
        thesis = Thesis.get_by_id(int(student_id))
        #students_fname = []
        #t = Thesis.query().fetch()
        #t =Thesis.query().order(+Thesis.adviser_key).fetch()
        #u =Thesis.query().order(+Thesis.department_key).fetch()
        

        

        '''
        thesis =Thesis()
        title =thesis.title
        thesis.title = title.lower()
        thesis = []

        exist = any([thesis.title(word) != -1 for word in thesis.tags])

        if exist:
            thesis_list = thesis.append(thesis.title)
            template_values = {
            'thesis_list': thesis_list
            }

        '''


        user = users.get_current_user()

        if user:
            '''
            for thesis in t:
                for i in range(len(thesis.proponent_keys)):
                    entity = thesis.proponent_keys.get()
                    students_fname[i] = entity.full_name

            logging.info(students_fname)

            for thesis in t:
                a = thesis.adviser_key.get()
                full_name = a.faculty_name
            
            for thesis in u:
                a = thesis.department_key.get()
                b = a.college_key.get()
                college_name = b.college_name
                department_name = a.department_name
            '''
            url = users.create_logout_url('/login')
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            'thesis': thesis,
            #'full_name': full_name,
            #'students_fname': students_fname,
            #'department_name': department_name,
            #'college_name':college_name

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

app = webapp2.WSGIApplication([
    
    ('/setup', SetupDBHandler),
    ('/csvimporter', ImportHandler),
    ('/register', RegisterPageHandler),
    ('/login', LoginPageHandler),
    ('/edit_thesis/(.*)', EditEntry),
    ('/delete_thesis/(.*)', DeleteEntry),
    ('/api/thesis', APIThesisHandler),
    ('/api/student', APIStudentHandler),
    ('/home', MainPageHandler),
    ('/', MainPageHandler),
    ('/student/create', StudentCreatePageHandler),
    ('/faculty/create', FacultyCreatePageHandler),
    ('/university/create', UniversityCreatePageHandler),
    ('/college/create', CollegeCreatePageHandler),
    ('/department/create', DepartmentCreatePageHandler),
    ('/thesis/list/2011',Filter2011Page),
    ('/thesis/list/2012',Filter2012Page),
    ('/thesis/list/2013',Filter2013Page),
    ('/thesis/list/2014',Filter2014Page),
    ('/thesis/list/2015',Filter2015Page),
    ('/search', SearchPage), 
    ('/student/list', StudentListPage),
    ('student/(.*)',DisplayStudentPage),
    ('/thesis/list/all', ThesisListPage),
    ('/thesis/list/adviser', FilterAdviserPage),
    ('/thesis/(.*)', DisplayThesisPage),
    ('/faculty/list', FacultyListPage),
    ('/university/list', UniversityListPage),
    ('/department/list', DepartmentListPage),
    ('/college/list', CollegeListPage)

    

], debug=True)
