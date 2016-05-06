from django.shortcuts import render, get_object_or_404
from django.template import loader, RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView
from django.utils import timezone
from django.db.models import Count

from .models import Page, File, Hashtag, Comment, User
from .forms import page_form, comment_form, tag_form
from .views_helper import views_helper as VH
from .views_helper import cookies
from .stats import stats
from wikiblog.models_helper import models_helper as MH
from wikiblog.utilities import names

import os

#-----------------------HOME PAGE-----------------------------------------
#Temporary index page
def index(request):

    #If the user has cookies enabled, Set the cookies
    #The function checks if they already have the cookie
    if cookies.enabled_cookies(request):   
        cookie = cookies.Cookie()
        cookie.set_initial_cookies(request)

    context={}
        
    return render(request, 'wikiblog/index.html', context)

#Lists all of the existing Pages - Currently just redirecting to the hashtag view
def homepage(request):
    hashtag_id = Hashtag.objects.get(tag="ALL").id
    
    return HttpResponseRedirect(reverse('wikiblog:hashtag_detail', args=(hashtag_id,))) 

#------------------------PAGE VIEWS--------------------------------------
#Create a new page with a forms.
def create_page(request): 
    new_page = VH.save_wiki_page(request)
    
    #If new_page succesfully saves, it will contain a Page object. If not it will be empty.
    if new_page:
        return HttpResponseRedirect(reverse('wikiblog:detail', args=(new_page.id,)))

    #If a GET (or any other method) we'll create a blank form
    else:
        form = page_form()
        form3 = tag_form()
        #bad form naming
        context = {
                'form': form,
                'form3': form3,
                   }
        return render(request, 'wikiblog/create_page.html', context)


#Displays the information pertaining to a specific page, like it's title, files, tags, bodytext etc.
def detail(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    form = comment_form()

    #Decide whether the user matches the page creator to show edit button
    valid_user=False
    try:
        if cookies.page_matches_user(request,page):
            valid_user=True
    except:
        pass
    
    context = {
        'page' : page,
        
        #process the body text and check for wikisyntax to insert a href links
        'bodytext' : VH.process_wiki_syntax(page.bodytext),
        'title' : page.title,
        'form' : form,
        'show_edit_btn': valid_user,
        }
    return render(request, 'wikiblog/details.html', context)


#Edit the page with forms
def edit_page(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    
    #prefill tag form with the existing tags
    tags = " ".join(["#"+hashtag.tag for hashtag in page.hashtag_set.all()])
    
    #prefill page_form with the page information.
    form = page_form(initial={'title': page.title, 'bodytext': page.bodytext})
    form3 = tag_form(initial={'tag': tags})
    
    #Terrible form naming, need to fix.
    context = {
        'page' : page,
        'form': form,
        'form3': form3,
        }
    return render(request, 'wikiblog/edit_page.html', context)

#Saves and updates the edited page
def submit_edit(request, page_id):
    page = get_object_or_404(Page, pk=page_id) 
    updated_page = VH.save_submit(request, page)
    
    context = {
    'page' : updated_page,
    }
    return HttpResponseRedirect(reverse('wikiblog:detail', args=(page_id,)))


#Deletes the given page
def delete_page(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    
    #Validate that it is the user who created the Page
    if cookies.page_matches_user(request, page):
        VH.update_hashtags([],page)
        page.delete()   
    return HttpResponseRedirect(reverse('wikiblog:homepage',))


#------------------------FILE VIEW-----------------------------------------
#Displays all files and their correlated pages
def file_view(request, hashtag_id, display_id=1):
    hashtag = get_object_or_404(Hashtag, id = hashtag_id)

    #Make display_id an int
    display_id = int(display_id) - 1

    #Get all pages assosiated with the hashtag
    ht_pages = hashtag.page.all()

    #Get all the files assosisated with the pages, in a list of lists
    all_files = [page.file_set.all() for page in ht_pages]

    #Start and end range for the Display_ID to get the correct interval of files
    begin = (display_id)*16
    end = begin + 16

    #Flatten the files list and get the correct files based on the display_id
    flatten_files = [file for file_list in all_files for file in file_list][begin:end]

    #Display next button if flatten_files contains 16 elements
    dnb = len(flatten_files)>=16
    
    #Display back button if display_id>1 (but we subtract 1 at the top of the function, because my method of getting next page is bad)
    dbb = display_id>=1
    
    context = {
        'all_files' : flatten_files,
        'hashtag': hashtag,
        'fileview_display_id': display_id,
        'display_next_button': dnb,
        'display_back_button': dbb,
        }

    return render(request, 'wikiblog/fileview.html', context)

#-----------------------COMMENT VIEWS------------------------------------------
#Adds comment to the page
def add_page_comment(request, page_id):
    page = get_object_or_404(Page, pk=page_id)

    VH.save_page_comment(request, page)        
    return HttpResponseRedirect(reverse('wikiblog:detail', args=(page_id,)))

#Add comment to a comment (subcomment/childcomment)
def add_subcomment(request, parent_comment_id, page_id):    
    parent_comment = get_object_or_404(Comment, pk=parent_comment_id)

    if request.method=="POST":
        form = comment_form(request.POST)

        #Get the comment name and content, and save the new comment object
        if form.is_valid():
            try:
                name = request.session['user_name']
            except:
                name = "anonymous"
            text_content = request.POST['content']
            new_comment = Comment(user_name=name, content=text_content, date=timezone.now(), page=None, parent=parent_comment) 
            new_comment.save()
            
    return HttpResponseRedirect(reverse('wikiblog:detail', args=(page_id,)))

#-------------------------HASHTAG VIEWS------------------------------------------
#Handles many hashtag_detail related views
##def display(request, hashtag, pages_to_display, display_num):
##    context={
##        "hashtag_pages": pages_to_display,
##        "hashtag": hashtag,
##        "display_num": display_num,
##        }
##    return render(request, "wikiblog/hashtag_detail.html", context)
    

#Displays the list of pages that are linked to the given Hashtag.
#Display_num = 0 because clicking on the tag takes you to the first display.
def hashtag_detail(request, hashtag_id, display_num=0):
    hashtag = get_object_or_404(Hashtag, id = hashtag_id)

    #So we only display 10 pages
    pages_to_display = hashtag.page.all()[:10]
    context={
            "hashtag_pages": pages_to_display,
            "hashtag": hashtag,
            "display_num": display_num,
        }
    return render(request, "wikiblog/hashtag_detail.html", context)

#Displays the next list of pages on the hashtag view or homepage
#defaults to prev display, passing in  display_num+2 turns the behavior into next page
#display type "next" or "previous"
def next_display(request, hashtag_id, display_num):
    hashtag = get_object_or_404(Hashtag, id = hashtag_id)

    #Get prev display
    display_num = int(display_num) - 1
    
    #Index start so we only display 10 pages
    index_start = 10*display_num
    pages_to_display = hashtag.page.all()[index_start : index_start + 10]
    context={
            "hashtag_pages": pages_to_display,
            "hashtag": hashtag,
            "display_num": display_num,
        }
    
    return render(request, "wikiblog/hashtag_detail.html", context)

#Order the pages by whatever sorting option was chosen.
def sort_pages(request, hashtag_id, sort_option):
    hashtag = get_object_or_404(Hashtag, id = hashtag_id)
    
    #Sort by new works
    if sort_option == "new":
        all_pages = hashtag.page.all().order_by('-date')
        
    #Working on comments, popular, files
    elif sort_option == "comments":
        all_pages = hashtag.page.all().annotate(num_comment=Count('comment')).order_by('-num_comment')
    elif sort_option == "files":
        all_pages = hashtag.page.all().annotate(num_file=Count('file')).order_by('-num_file')
    
    context={
        "hashtag_pages": all_pages,
        "hashtag": hashtag,
       }
    return render(request, "wikiblog/hashtag_detail.html", context)

#----------------------------------------------------------------------------------------

def about(request):
    return render(request, "wikiblog/about.html")
#---------------------------------------------------------------------------

#Sorts Files
def sort_files(request, hashtag_id, sort_option):
    pass


#Feature in development
def sort_tags(request):
    try:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        stats.write_user_stats(user)
        return HttpResponse("Stats written")
    except:
        return HttpResponse("couldn't write stats")

#Updates download_file tracking information
def download_file(request, file_id):
    return httpResponse("worked download_file!")

