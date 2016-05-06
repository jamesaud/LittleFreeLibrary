from wikiblog.models import User, Page, User_page_accessed, User, Random_name
from django.utils import timezone
import random

#Invoke at index page
class Cookie():
    def set_initial_cookies(self, request):
        
        #See if user_name and cookies exists already
        try:
            request.session['user_name']
            request.session['date_accessed']
            request.session['user_id']
            print("------@@@@-----You already have a cookie------@@@@-------")
            print("Your user name is:  " + request.session['user_name'])
            
        #If it doesn't exist, generate a user_name and more cookie info
        except:
            #Create new user object, then use the data to populate the cookies
            #.. so that the cookie correctly matches the database
            new_user = self.create_new_user()

            request.session['user_name'] = new_user.user_name
            request.session['date_accessed'] = str(new_user.date_accessed)
            request.session['user_id'] = new_user.id
            print("------@@@@-----Generating new cookie------@@@@-------")
            print("Your user name is:  " + request.session['user_name'])
            
    #Helper function creates user with random name       
    def create_new_user(self):
            username = generate_random_name()
            dateaccessed = timezone.now()
            
            new_user = User(user_name = username, date_accessed = dateaccessed)
            new_user.save()
            
            return new_user

#-----------------------------------------------------------------------------
        
#Gets a user object from the cookie if it exists        
def get_user_obj(request):
    try:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
    except:
        user = None
    return user

#-------------------------------------------------------
#Random user_name generator
def generate_random_name():
    try:
        #Grab the random name object
        random_name_obj = Random_name.objects.all()[:1].get()

        #Get the name from it in text form
        name = random_name_obj.user_name

        #Delete from the database so it will not be repeated
        random_name_obj.delete()

        return name
    except:

        #Default to something else
        return "random_name" + str(random.randint(0, 1000000))

#-------------------------------------------------------

#Tests if client has cookies enabled, returns boolean
def enabled_cookies(request):
    request.session.set_test_cookie()
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        return True
    else:
        return False

#Check if user is the creator of a page
def page_matches_user(request,page):
    try:
        if page.user == get_user_obj(request) and page.user!=None:
            return True
    except:
        return False
