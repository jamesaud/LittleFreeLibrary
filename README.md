# LittleFreeLibrary

Description and tutorial:
https://jamesaudretsch.wordpress.com/little-free-library-project-part-0/

Quick add to Django Project:

Add to settings.py:
  To INSTALLED_APPS:
      'wikiblog.apps.WikiblogConfig'
  On its own line:
      SESSION_EXPIRE_AT_BROWSER_CLOSE = True
      
Add to urls.py:
  To url_patterns:
      url('wikiblog/', include('wikiblog.urls'))
      
