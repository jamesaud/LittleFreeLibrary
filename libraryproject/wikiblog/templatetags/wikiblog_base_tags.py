from django import template
from wikiblog.models import Hashtag, User, User_page_accessed, Page
from django.utils import timezone
from django.db.models import Count

from wikiblog.views_helper import cookies
from wikiblog.models_helper import models_helper as MH

register = template.Library()

#Get's all the existing hashtags to load as a sidebar
#Sorts according to the field
@register.inclusion_tag('wikiblog/tags/hashtags_nav.html')
def get_hashtags():
    hashtags = Hashtag.objects.all().annotate(num_page=Count('page')).order_by('-num_page')[:25]  
    return {"hashtags": hashtags}

#To be done on all pages (through base.html)
@register.inclusion_tag('wikiblog/tags/base_tags.html')
def update_user_cookies(request):
    #If the user has cookies working properly:
    try:
        #Get current user from cookies
        user_id = request.session['user_id']
        curr_user = User.objects.get(id=user_id)

        #Set to the referring URL
        prev_url = request.META.get('HTTP_REFERER')
        
        #get current URL
        curr_url = request.build_absolute_uri()

        #datetime
        dt = timezone.now()

        #Create the User_page_accessed object and add to the databas
        upa = User_page_accessed(user = curr_user,
                             url = curr_url,
                             referring_url = prev_url,
                             date_accessed = dt)
        upa.save()

    except:
        pass
    
        
@register.inclusion_tag('wikiblog/tags/comment_total.html')
def total_page_comments(page_id):
    try:
        page = Page.objects.get(id=page_id)
        comment_calculator = MH.PageCalc()
        total_comments = comment_calculator.total_page_comments(page)
    except:
        total_comments = 0
    return {"total_comments": total_comments}

@register.simple_tag(takes_context=True)
def sub1(num1):
    return int(num1) - 1
