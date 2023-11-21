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
from .forms import SignUpForm
from .models import CustomUser
from spliterapp.models import Group
from django.contrib.auth.models import User


# from spliterapp.views import main
# from django.contrib.auth.models import User
def index(request):
    return render(request, "index.html")


def Main(
    request,
):
    # group = Group.objects.get(id=group_id)
    user = request.user  # Get the current user
    user_groups = Group.objects.filter(members=user)

    return render(request, "group/base.html", {"user_groups": user_groups})


################ login forms###################################################
def Login(request):
    if request.method == "POST":
        # AuthenticationForm_can_also_be_used__

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f" welcome {username} !!")
            return redirect("Main")
        else:
            messages.info(request, f"account do not exit plz sign in")
    form = AuthenticationForm()
    return render(request, "register/login.html", {"form": form, "title": "log in"})


# otp verification

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import random

from django.contrib import messages


def VerifyOTP(request):
    # import pdb; pdb.set_trace()
    username1 = request.session.get("username1")
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("signup_otp")
        user_id = request.session.get("signup_user_id")

        if stored_otp and entered_otp == str(stored_otp):
            del request.session["signup_otp"]
            del request.session["signup_user_id"]

            user = CustomUser.objects.get(pk=user_id)
            user.is_active = True
            user.save()

            messages.success(
                request,
                f"Your email has been verified, and your account is now active. You can log in.",
            )
            return redirect("Login")
        # return render(request,"re")
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    return render(request, "register/verify_otp.html", {"username": username1})


from django.contrib import messages


def Signup(request):
    if request.method == "POST":
        # import pdb; pdb.set_trace()
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")

            if CustomUser.objects.filter(email=email).exists():
                messages.error(
                    request,
                    f"This email is already registered. You can directly login.",
                )
                return render(
                    request,
                    "register/login.html",
                    {"form": form, "title": "Register Here"},
                )
            user = form.save()
            username = form.cleaned_data.get("username")
            # Generate a random OTP

            otp = random.randint(100000, 999999)

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

            # request.session['username1'] = user
            request.session['signup_submitted'] = True
            request.session["signup_otp"] = otp
            request.session["signup_user_id"] = user.id
            request.session["username1"] = username

            messages.success(
                request,
                f"An OTP has been sent to your email. Please verify your email.",
            )
            return redirect(
                "VerifyOTP",
            )
            # return render(request, 'register/verify_otp.html', {'username' : username})

        else:
            request.session.pop('signup_submitted', None)   
            email = form.cleaned_data.get("email")
            if not CustomUser.objects.filter(email=email).exists():
                messages.error(
                    request,
                    f"This email is not registered. please try again .",
                )
                return render(
                    request,
                    "register/login.html",
                    {"form": form, "title": "Register Here"},
                )
            # messages.success(request, f'Your Email Id is Alerady register . You can direct Login.')
            return render(
                request,
                "register/signup.html",
                {"form": form, "title": "Register Here"},
            )
    else:
        form = SignUpForm()
    return render(
        request, "register/signup.html", {"form": form, "title": "Register Here"}
    )
