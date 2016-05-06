import re
from wikiblog.models import Page, File
from django.utils import timezone

#Finds all linked page syntax "[[linkedpage]]" reformats it by calling create_page_link on the linked page syntax
def page_linker(text):
    #Find all "[[linkedpage]]" strings
    collected_links = re.findall("\[\[[^\[&^\]]+\]\]", text)
    
    #If there are any linked pages, replace them with a hrefs to the page   
    if collected_links:     
        for phrase in collected_links:
            bracket_syntax_phrase = "\[\["+phrase[2:-2]+"\]\]"
            
            #Sub the old phrase with an ahref link by calling create_page_link(phrase)
            text = re.sub(bracket_syntax_phrase, create_page_link(phrase), text)
    return text

#Return an ahref html link that links to a created Page object 
def create_page_link(phrase):
    page = Page(title = phrase, bodytext=" ", date=timezone.now())
    page.save()
    return '<a href = \"' + page.getlink() + '\">' + phrase + '</a>' 
   
