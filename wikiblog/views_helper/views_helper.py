from wikiblog.models import Page, File, Comment, Hashtag, User
from wikiblog.forms import page_form, choices_form, comment_form, tag_form
from .wiki_syntax import page_linker
from django.http import HttpResponse, Http404
from django.utils import timezone

from wikiblog.views_helper import cookies
import wikiblog.GlobalVariables as Global

import re, os

#In MB as an Integer
maxFileSize = Global.getMaxFileSize()


#Saves the created Page from the page model form.
def save_wiki_page(request):
    
    #If this is a POST request we need to process the form data
    if request.method == 'POST':

        #Create a form instance and populate it with data from the request:
        pageForm = page_form(
            {'title': request.POST['title'], 'bodytext': request.POST['bodytext'],})
        tagForm = tag_form(
            {'tag': request.POST['tag']})
        
        if pageForm.is_valid():
            #process the data in form.cleaned_data as required
            # ...
	    # ...
	    # ...
	    
	    #Get the relevant fields for a Page
            new_title = request.POST['title']
            new_bodytext = request.POST['bodytext']

            #Try to get user from cookies
            try:
                    user_id=request.session['user_id']
                    user_obj=User.objects.get(id=user_id)
            except:
                    user_obj=None

            #Save the new Page object
            new_page = Page(title = pgt(new_title), bodytext = pgt(new_bodytext), date=timezone.now(), user=user_obj)  
            new_page.save()

            #Get File Post data and save the object.
            if request.FILES.getlist("files"):
                uploaded_files = request.FILES.getlist("files")
                for uploaded_file in uploaded_files:
                    testFile(uploaded_file)
                    file_model = File(name = uploaded_file.name, file_obj = uploaded_file, page = new_page)
                    file_model.save()
                
            #Create an empty tags list to pass to save_hashtags if tagForm.is_valid() is false
            tags=[]
            if tagForm.is_valid():
                tag_field = request.POST['tag']

                #Get the tag string, and extract the list of tags
                tags = extract_hashtags(tag_field)  
            
            #Save our list of tags, each tag is saved as an object.
            save_hashtags(tags, new_page)

            #Return new_page if successfully saves Post fields.    
            return new_page
            
    #Return nothing otherwise, so our view knows to redirect to an error page
    return 

#Saves an edited page
def save_submit(request, page):
    
    #If method is POST, populate the forms.
    #User must match the PAGE USER to be able to make any edits.
    #Must make sure they are not both none
    if request.method == 'POST' and cookies.page_matches_user(request, page):
        pageForm = page_form(
            {'title': request.POST['title'],'bodytext': request.POST['bodytext'],})
        #uploadFileForm = upload_file_form(request.POST, request.FILES)
        choices = request.POST.getlist('choices')
        tagForm = tag_form({'tag': request.POST['tag']})
        
        #Update the existing page from the updated content in the Page model form
        if pageForm.is_valid():
            new_title = request.POST['title']
            new_bodytext = request.POST['bodytext']  
            #need to clean data
            #...
            #...
            
            #Save the page object
            page.title = pgt(new_title)
            page.bodytext = pgt(new_bodytext)
            page.save()

            #Get File Post data and save the object.
            if request.FILES.getlist("files"):
                uploaded_files = request.FILES.getlist("files")
                for uploaded_file in uploaded_files:
                    testFile(uploaded_file)
                    file_model = File(name = uploaded_file.name, file_obj = uploaded_file, page = page)
                    file_model.save()
                
            #If the user selected any files to delete (check boxes), delete the assosciated File object
            if choices:
                file_ids_list = request.POST.getlist('choices')
                for file_id in file_ids_list:
                    try:
                        file = File.objects.get(pk = file_id) 
                        file.delete()
                    except:
                        pass
                    
            #Pass empty Tag list to update_hashtags, because it means the user deleted all the hashtags.             
            tags=[]
            if tagForm.is_valid():
                tag_field = request.POST['tag']
                tags = extract_hashtags(tag_field)

            #Update the new hashtags and delete the missing ones.       
            update_hashtags(tags, page)

        #Return page if success    
        return page
    
    #Else our view knows this failed by returning nothing.    
    return

#Save a page comment from a Page model form. 
def save_page_comment(request, page_obj):
    if request.method=="POST":
        form = comment_form(request.POST)
        
        if form.is_valid():
            try:
                name = request.session['user_name']
            except:
                name = "anonymous"
            text_content = request.POST['content']
            new_comment = Comment(user_name=name, content=text_content, date=timezone.now(), page=page_obj, parent=None)
            new_comment.save()

#Adds the a href links to text.
def process_wiki_syntax(bodytext):
    bodytext = page_linker(bodytext)
    return bodytext

#Process generic text
def pgt(text):
    return text.strip()

#Extract hashtags from hashtag charfield, "#tag1 #tag2 #tag3 #tag4"
def extract_hashtags(string):
    tags = re.findall("#[\w]+", string)
    return [tag[1:] for tag in tags]

#Create new hashtag or get existing one, then add page to the hashtag
def save_hashtags(hashtag_list, page):
    
    #Always associate page with hashtag object #all
    hashtag_list.append("ALL")
    for tag_text in hashtag_list:

        #Check if hashtag already exists
        try:
            hashtag = Hashtag.objects.get(tag=tag_text)
            
        #If not, create it.
        except:
            hashtag = Hashtag(tag=tag_text)
            hashtag.save()
            
        #Assosiate the page with the Hashtag.
        hashtag.page.add(page)
        hashtag.save()

#Takes in a list of tags and updates an already existing page with those tags
def update_hashtags(current_hashtags, page):
    #Names of the page's existing tags
    existing_tags = [hashtag.tag for hashtag in page.hashtag_set.all()]
    
    #Cross references the existing tags to check which ones are new
    new_tags = [tag for tag in current_hashtags if tag not in existing_tags]
    
    #Cross references the existing tags to see which were removed
    removed_tags = [tag for tag in existing_tags if tag not in current_hashtags]
    
    #Disassosiate the page from the hashtags that were removed. 
    for tag_text in removed_tags:
        hashtag = Hashtag.objects.get(tag=tag_text)
        
        #Remove the page assosiation  from the hashtag
        page.hashtag_set.remove(hashtag)

        #removed hashtag if it has no pages
        if not hashtag.page.all():
            hashtag.delete()
            
    #Save the removed hashtags.
    page.save()
    
    #Save the new hashtags
    save_hashtags(new_tags, page)

#Validates file size:
def testFile(file):
    #Converts os.path.getsize to megabytes from bytes by multiplying by 1 million
    if file.size * .000001 > maxFileSize:
        raise Http404("File " + file.name + " must be under size: " + str(maxFileSize) + " MB.")
    
