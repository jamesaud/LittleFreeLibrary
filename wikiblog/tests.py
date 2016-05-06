from django.test import TestCase
from wikiblog.models import Page, File
from .views_helper import wiki_syntax as WS
import unittest

def printout(material):
    print("-------------------------")
    print(material)
    print("--------------------------")

class WikiSyntax(TestCase):
    def test_syntax_creation(self):
        text1 = "EXISTING"
        text2 = "here is a [[wikisyntax_test_link]]"
        
        self.assertEqual(WS.page_linker(text2), 'here is a <a href = "/wikiblog/1">wikisyntax_test_link</a>')
        self.assertEqual(WS.page_linker(text1), 'EXISTING')

