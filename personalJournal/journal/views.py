from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Entry
import re
import bcrypt

# Create your views here.
def loginPage(request):
    #Render login page
    return render(request, 'login.html')

def registration(request):
    #Render register page
    return render(request, 'register.html')

def login(request):
    #Login Validator
    print("*"*70)
    print("SUCCESSFULLY MADE IT TO THE login METHOD")
    print("*"*70)
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['loginEmail']) # filter returns a list with the object instance
        if user: # empty list returns false, only proceeds if there is an instance with the email provided
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['loginPW'].encode(), logged_user.password.encode()):
                request.session['userID'] = logged_user.id
                return redirect('/dashboard')
            else:
                messages.error(request, "Invalid login credentials, please try again.")
                return redirect('/')
        else:
            messages.error(request, "That Email doesn't exist, please register!")
            return redirect('/')

def register(request):
    #Registraion Validator
    print("*"*70)
    print("SUCCESSFULLY MADE IT TO THE register METHOD")
    print("*"*70)
    errors = User.objects.registrationValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/registration')
    else:
        password = request.POST['regPW']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() # creates a hash PW of the password given
        new_user = User.objects.create(
            first_name=request.POST['regFN'],
            last_name=request.POST['regLN'],
            email=request.POST['regEmail'],
            password=pw_hash,
        )
        
        request.session['userID'] = new_user.id
        return redirect('/dashboard')

def dashboard(request):
    #Render Dashboard/Home page
    if 'userID' in request.session:
        user = User.objects.get(id=request.session['userID'])
        context = {
            'user': user,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

def createEntry(request):
    #Add journay entry to the database
    user = User.objects.get(id=request.session['userID'])
    errors = Entry.objects.entryValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    else:
        Entry.objects.create(
            title=request.POST['entryTitle'],
            desc=request.POST['entryDesc'],
            journal_entry=request.POST['entry'],
            author=user,
            )
        return redirect('/dashboard')

def editPage(request, num):
    #Render edit page
    entryToEdit = Entry.objects.get(id=num)
    user = User.objects.get(id=request.session['userID'])
    context = {
        'user': user,
        'entry': entryToEdit,
    }
    return render(request, "editPage.html", context)

def edit(request, num):
    #edit a journal entry
    errors = Entry.objects.entryValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/editPage/{num}')
    else:
        entryToEdit = Entry.objects.get(id=num)
        entryToEdit.title = request.POST['entryTitle']
        entryToEdit.desc = request.POST['entryDesc']
        entryToEdit.journal_entry = request.POST['entry']
        entryToEdit.save()
        return redirect('/dashboard')


def delete(request, num):
    #Delete Journal Entry
    entryToDelete = Entry.objects.get(id=num)
    entryToDelete.delete()
    return redirect('/dashboard')

def logout(request):
    #Clears session and logs user out
    request.session.clear()
    return redirect('/')