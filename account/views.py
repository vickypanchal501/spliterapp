from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import random
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from .forms import SignUpForm, OTPVerificationForm
from .models import CustomUser
from spliterapp.models import Group


from django.contrib.auth.hashers import make_password

def index(request):
    return render(request, "index.html")


def Main(
    request,
):
    # group = Group.objects.get(id=group_id)
    user = request.user  # Get the current user
    user_groups = Group.objects.filter(members=user)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    
    return render(request, "group/base.html",{'user_groups': user_groups})
=======
    return render(request, "group/main.html",{'user_groups': user_groups})
>>>>>>> vikas
=======
    
    return render(request, "group/base.html",{'user_groups': user_groups})
>>>>>>> vikcy
################ login forms################################################### 
=======

    return render(request, "group/base.html", {"user_groups": user_groups})

>>>>>>> vicky
def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user with the provided email exists
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            authenticated_user = authenticate(request, email=email, password=password)

            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, f"Welcome {authenticated_user.username}!")
                return redirect("Main")
            else:
                messages.error(request, "Invalid password. Please try again.")
        else:
            messages.error(request, "Invalid email or user does not exist.")
    
    return render(request, "register/login.html", {"title": "Log in"})

def Signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            # Generate a random OTP
            otp = random.randint(1000, 9999)

            # Create the email content
            htmly = get_template("register/gmail.html")
            context = {"username": username, "otp": otp}
            subject, from_email, to = "Welcome", "panchalvikas472@gmail.com", email
            html_content = htmly.render(context)

            msg = EmailMultiAlternatives(
                subject, "Your OTP is: {}".format(otp), from_email, [to]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # Store necessary information in the session for OTP verification
            request.session["signup_otp"] = otp
            request.session["signup_username"] = username
            request.session["signup_email"] = email
            request.session["signup_password"] = password

            messages.success(
                request, "An OTP has been sent to your email. Please verify your email."
            )
            return redirect("VerifyOTP")

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = SignUpForm()

    return render(
        request, "register/signup.html", {"form": form, "title": "Register Here"}
    )




def VerifyOTP(request):
    username = request.session.get("signup_username")
    email = request.session.get("signup_email")
    form = OTPVerificationForm(request.POST or None)

    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("signup_otp")

        if stored_otp and entered_otp == str(stored_otp):
            # Check if the user is already registered
            existing_user = CustomUser.objects.filter(email=email).first()

            if existing_user:
                messages.warning(request, "User already registered. Please log in.")
            else:
                # Complete the registration process and save the user
                user = CustomUser(username=username, email=email)
                
                # Set the user's password using the password stored in the session
                user.password = make_password(request.session.get("signup_password"))
                
                user.save()
                
                # Authenticate and log in the user
                authenticated_user = authenticate(username=username, password=request.session.get("signup_password"))
                login(request, authenticated_user)
                
                messages.success(request, "Registration successful. You are now logged in.")
            
            if "signup_otp" in request.session:
                del request.session["signup_otp"]
            if "signup_username" in request.session:
                del request.session["signup_username"]
            if "signup_email" in request.session:
                del request.session["signup_email"]
            if "signup_password" in request.session:
                del request.session["signup_password"]

            return redirect("Main")  # Redirect to your home page

        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "register/verify_otp.html", {"username": username, "form": form})