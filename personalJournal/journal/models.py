from django.db import models
import re

# Create your models here.

EMAIL_REGEX =  re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class webManager(models.Manager):
    def registrationValidator(self, postData):
        errors = {}
        if len(postData['regFN']) < 2:
            errors['fnLength'] = "First Name must be at least 2 characters!"
        if len(postData['regLN']) < 3:
            errors['lnLength'] = "Last Name must be at least 3 characters!"
        if not EMAIL_REGEX.match(postData['regEmail']): # test whether a field matches the pattern
        # method .match will return None if no match can be found
        # if argument matches the regular expression, a match object instance is returned
            errors['email'] = "Invalid Email Address!"
        elif User.objects.filter(email=postData['regEmail']):
            errors['exists'] = "Email already exists, please try another Email or login!"
        if len(postData['regPW']) < 8:
            errors['pwLength'] = "Password must be at least 8 characters!"
        if postData['regPW'] != postData['regCon']:
            errors['noMatch'] = "The Password and Cofirm Password do no match, please make sure they match!"
        return errors
    
    def loginValidator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['loginEmail']):
            errors['invalid'] = "Not a valid Email Address!"
        if not postData['loginEmail']:
            errors['emailRequierd'] = "Login Email Required!"
        if not postData['loginPW']:
            errors['pwRequired'] = "Login Password Required!"
        return errors
    
    def entryValidator(self, postData):
        errors = {}
        if len(postData['entryTitle']) < 3:
            errors['titleLength'] = "Entry Title must be at least 3 characters!"
        elif len(postData['entryTitle']) > 80:
            errors['titleTooLong'] = "Entry Title is too long! Max is 80 characters!"
        if len(postData['entryDesc']) < 4:
            errors['descLength'] = "Entry Description must be at least 4 characters!"
        elif len(postData['entryDesc']) > 100:
            errors['descLong'] = "Entry Description is too long! Max is 100 characters!"
        if not postData['entry']:
            errors['entryempty'] = "Journal Entry is required!"
        return errors
        
class User(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=60)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #entries
    objects = webManager()

class Entry(models.Model):
    title = models.CharField(max_length=80)
    desc = models.CharField(max_length=100)
    journal_entry = models.TextField()
    author = models.ForeignKey(User, related_name="entries", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = webManager()