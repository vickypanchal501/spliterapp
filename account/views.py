from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import random
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from .forms import SignUpForm
from .models import CustomUser
# from django.contrib.auth.models import User
#################### index####################################### 
def index(request):
	return render(request, 'index.html', {'title':'index'})

########### register here ##################################### 
# def Signup(request):
# 	if request.method == 'POST':
# 		form = SignUpForm(request.POST)
# 		# import pdb;pdb.set_trace()
# 		if form.is_valid():
# 			form.save()
# 			username = form.cleaned_data.get('username')
# 			email = form.cleaned_data.get('email')
			
# 			htmly = get_template('register/gmail.html')
# 			otp = random.randrange(100000,9999999)
# 			d = { 'username': username ,"otp":otp}
# 			subject, from_email, to = 'welcome', 'panchalvikas472@gmail.com', email
# 			html_content = htmly.render(d)
# 			msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
# 			msg.attach_alternative(html_content, "text/html")
# 			msg.send()
# 			################################################################## 
# 			messages.success(request, f'Your account has been created ! You are now able to log in')
# 			return redirect('Login')
# 	else:
# 		form = SignUpForm()
# 	return render(request, 'register/signup.html', {'form': form, 'title':'register here'})

################ login forms################################################### 
def Login(request):
	if request.method == 'POST':

		# AuthenticationForm_can_also_be_used__

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {username} !!')
			return redirect('index')
		else:
			messages.info(request, f'account done not exit plz sign in')
	form = AuthenticationForm()
	return render(request, 'register/login.html', {'form':form, 'title':'log in'})



from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import random








from django.contrib import messages

def VerifyOTP(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('signup_otp')
        user_id = request.session.get('signup_user_id')

        if stored_otp and entered_otp == str(stored_otp):
            del request.session['signup_otp']
            del request.session['signup_user_id']
            
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True  
            user.save()
            
            messages.success(request, f'Your email has been verified, and your account is now active. You can log in.')
            return redirect('Login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'register/verify_otp.html')






from django.contrib import messages

def Signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            # Generate a random OTP
            otp = random.randint(100000, 999999)
            
            # Create the email content
            htmly = get_template('register/gmail.html')
            context = {'username': username, 'otp': otp}
            subject, from_email, to = 'Welcome', 'panchalvikas472@gmail.com', email
            html_content = htmly.render(context)
            
            
            msg = EmailMultiAlternatives(subject, 'Your OTP is: {}'.format(otp), from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            
            request.session['signup_otp'] = otp
            request.session['signup_user_id'] = user.id

            messages.success(request, f'An OTP has been sent to your email. Please verify your email.')
            return redirect('VerifyOTP')
    else:
        form = SignUpForm()
    return render(request, 'register/signup.html', {'form': form, 'title': 'Register Here'})
