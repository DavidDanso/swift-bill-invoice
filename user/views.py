from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

################################ welcome_email view
def welcomeEmail(request):
    return render(request, 'welcome_email.html')


################################ welcome_email view
def welcomeUser(request):
    return render(request, 'welcome_msg.html')


########################################## home page views
def homePage(request):
    context = {}
    return render(request, 'user/index.html', context)


########################################## profile page views
@login_required(login_url='login')
def profilePage(request):
    # user profile
    profile = Profile.objects.get(user=request.user)

    # Invoices
    invoices = profile.acc_user.all()
    invoice_count = invoices.count()


    # user profile form INSTANCE
    form = UserProfileForm(instance=profile)

    if request.method == 'POST':
        # user profile form
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,  'Profile updated Successful✅')
            return redirect('dashboard')
    
        elif 'delete_account' in request.POST:
                profile.delete()
                messages.success(request, 'Account delete Successful')
                return redirect('signup')

    context = {'form': form, 'invoice_count': invoice_count}
    return render(request, 'user/profile.html', context)


########################################## login page views
def loginPage(request):
     # 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,  'User not found❌')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            # user login success message
            messages.success(request,  'User login Successful')
            return redirect('dashboard')
        else:
            messages.error(request,  'Username or Password is incorrect❌')

    return render(request, 'user/login.html')


################################ logout views
def logoutPage(request):
    logout(request)
    return redirect('login')


########################################## signup page views
def signupPage(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('welcome')
        else:
            messages.error(request,  'Error: Please check your information and try again')

    context = {'form': form}
    return render(request, 'user/signup.html', context)
