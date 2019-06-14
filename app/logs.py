"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

import os
import logging

def logger(filename ='logs.log',message='hhh',flag='info'):
    try:
        logging.basicConfig(filename='logs/'+str(filename),level=logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logging.info('Message is : {}  | | Flag  : {}'.format(str(message), str(flag)))
    except Exception as e :
        logging.error('Failed to log erros to files : '+ str(e))
        pass
