from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt

def root(request):
    return render(request,'login_reg.html')

# Login/Register Functionality
def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == "first_name":
                messages.error(request, value, extra_tags="first_name")
            if key == "last_name":
                messages.error(request, value, extra_tags="last_name")
            if key == "reg_email":
                messages.error(request, value, extra_tags="reg_email")
            if key == "reg_password":
                messages.error(request, value, extra_tags="reg_password")
            if key == "confirm_pw":
                messages.error(request, value, extra_tags="confirm_pw")
        return redirect("/")
    else:
        hashed_password = bcrypt.hashpw(
            request.POST["reg_password"].encode(), bcrypt.gensalt()
        ).decode()
        user = User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["reg_email"],
            password=hashed_password,
        )
        request.session["user_id"] = user.id
        return redirect("/wall")


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == "log_email":
                messages.error(request, value, extra_tags="log_email")
            if key == "log_password":
                messages.error(request, value, extra_tags="log_password")
        return redirect("/")
    else:
        user_list = User.objects.filter(email=request.POST["log_email"])
        if len(user_list) == 0:
            messages.error(request, "Email address not found.", extra_tags="log_email")
            return redirect("/")
        else:
            user = user_list[0]
            if bcrypt.checkpw(
                request.POST["log_password"].encode(), user.password.encode()
            ):
                request.session["user_id"] = user.id
                return redirect("/wall")
            else:
                messages.error(
                    request, "Incorrect password.", extra_tags="log_password"
                )
                return redirect("/")

# Wall Functionality

def wall(request):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        context = {
            "user": User.objects.get(id=request.session["user_id"]),
            "all_messages" : Message.objects.all()
        }
    return render(request, "wall.html", context)


def post_message(request, user_id):
    errors = Message.objects.message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == "content":
                messages.error(request, value, extra_tags="content")
        return redirect("/wall")
    else:
        message = Message.objects.create(
            content= request.POST["content"],
            posted_by= User.objects.get(id=request.session['user_id'])
        )
    return redirect('/wall')

def post_comment(request, user_id):
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == "content":
                messages.error(request, value, extra_tags="content")
        return redirect("/wall")
    else:
        comment = Comment.objects.create(
            content = request.POST["content"],
            posted_by = User.objects.get(id=request.session['user_id']),
            message_parent = Message.objects.get(id=int(request.POST['message_parent']))
        )
    return redirect ('/wall')

def logoff(request):
    request.session.flush()
    return redirect("/")