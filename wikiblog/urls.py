from django.conf.urls import url

from . import views

app_name = 'wikiblog'

#Index Page
urlpatterns = [
    url(r'^$', views.index, name='index'),
]

#base url
urlpatterns += [
    #displays given page
    url(r'^(?P<page_id>[0-9]+)/detail$', views.detail, name='detail'),
    
    #homepage
    url('homepage/$', views.homepage, name='homepage'),

    #file view
    url(r'^(?P<hashtag_id>[0-9]+)/fileview/page(?P<display_id>[0-9]+)/$', views.file_view, name='file_view'),

    #add page comment
    url(r'^(?P<page_id>[0-9]+)/comment/$', views.add_page_comment, name='add_page_comment'),
    
    #create page
    url('create_page/$', views.create_page, name='create_page'),

    #edit page
    url(r'^(?P<page_id>[0-9]+)/edit/$', views.edit_page, name='edit_page'),
    
    #submit edited page
    url(r'^(?P<page_id>[0-9]+)/submit-edit/$', views.submit_edit, name='submit_edit'),

    #to delete page
    url(r'^(?P<page_id>[0-9]+)/delete/$', views.delete_page, name='delete_page'),

    #add subcomment
    url(r'^(?P<parent_comment_id>[0-9]+)/(?P<page_id>[0-9]+)/sub-comment/$', views.add_subcomment, name='add_subcomment'),

    #hashtag detail
    url(r'^(?P<hashtag_id>[0-9]+)/$', views.hashtag_detail, name='hashtag_detail'),

    #sort tags
    url('hashtag/sort$', views.sort_tags, name='sort_tags'),

    #sort pages
    url(r'^(?P<hashtag_id>[0-9]+)/sort(?P<sort_option>[\w]+)/$', views.sort_pages, name='sort_pages'),

    #next_display(request, hashtag_id, display_num)
    url(r'^(?P<hashtag_id>[0-9]+)/page(?P<display_num>[0-9]+)/$', views.next_display, name='next_display'),

    #About page
    url('about/$', views.about, name='about'),
    ]

