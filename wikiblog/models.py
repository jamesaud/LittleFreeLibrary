from django.db import models

import os
# Create your models here.

#---------------------------------USER AND STATS-----------------------------
class User(models.Model):
    user_name = models.CharField(max_length=60, unique=True)
    date_accessed = models.DateTimeField(auto_now = True,)
    
    def __str__(self):
        return self.user_name

class User_page_accessed(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,)

    #URL currently on
    url = models.CharField(max_length = 500)

    #URL coming from
    referring_url = models.CharField(max_length = 500, blank=True, null=True)
    
    #Datetime clicking URL
    date_accessed = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.url + " : " + self.user.user_name

    class Meta:
        ordering = ['-date_accessed']
#----------------------------------------------------------------------------
       
class Page(models.Model):
    title = models.CharField(max_length = 255,)
    bodytext = models.CharField(max_length = 40000,blank=True, null=True)
    date = models.DateTimeField(auto_now = True,)

    #User who created the page
    user = models.ForeignKey(User, blank=True, null=True)
    
    def getlink(self):
        return "/wikiblog/" + str(self.id)

    def __str__(self):
            return self.title
        
    class Meta:
            ordering = ['-date']

class Hashtag(models.Model):
    tag = models.CharField(max_length = 30, unique = True)
    page = models.ManyToManyField(Page,)

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['tag']
    
class File(models.Model):
    name = models.URLField(max_length = 255,)
    file_obj = models.FileField(upload_to='uploaded_files/%Y/%m/%d')
    page = models.ForeignKey(Page,
                             on_delete=models.CASCADE,
                             null = False,
                        )
    date = models.DateTimeField(auto_now = True,)
    
    #Return relative link to its location
    def getlink(self):
        return "/media/" + str(self.file_obj)
    
    def __str__(self):
        return self.name


class Comment(models.Model):
    user_name = models.CharField(max_length=50)
    content = models.CharField(max_length = 500)
    date = models.DateTimeField(auto_now = True,)

    #ONLY comments at the top level should have a relationship with Page. a subcomment will have this set to null.
    page = models.ForeignKey(Page,
                             blank = True,
                             null = True,
                             )
    
    #One comment can have multiple subcomments(responses)
    parent = models.ForeignKey('self',
                             on_delete=models.CASCADE,
                             blank = True,
                             null = True,
                        )
    
    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-date']

#Just a model to hold the thousands of unique random names.
#When one is assigned to a user, it is deleted from the database
class Random_name(models.Model):
    user_name = models.CharField(max_length=50, unique=True,)

    def __str__(self):
        return self.user_name
