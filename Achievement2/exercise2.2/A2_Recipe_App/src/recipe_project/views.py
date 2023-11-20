from django.shortcuts import render, redirect

# django authentication libraries
from django.contrib.auth import authenticate, login, logout

from django.conf import settings

from .forms import LoginForm, SignUpForm


def success(request):
    logout(request)  # the use pre-defined Django function to logout
    context = {
        "MEDIA_URL": settings.MEDIA_URL,
    }
    return render(request, "auth/success.html", context)


# define function that takes request from user
def login_view(request):
    # initialize error message to none
    error_message = None
    # form object with username and password fields
    form = LoginForm()

    # POST request generated when user hits login button
    if request.method == "POST":
        # read data sent by form via POST request
        form = LoginForm(data=request.POST)

        # check if form is valid
        if form.is_valid():
            # read form
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # use Django authenticate to validate user
            user = authenticate(username=username, password=password)
            # if authenticated
            if user is not None:
                # use Django login function to login
                login(request, user)
                return redirect("recipes:home")
        # error handling
        else:
            error_message = "Oops, something went wrong"

    context = {
        # send form
        "form": form,
        # send error message
        "error_message": error_message,
        "MEDIA_URL": settings.MEDIA_URL,
    }

    # load the login page using "context" information
    return render(request, "auth/login.html", context)


# define function that takes request from user
def logout_view(request):
    # use predefined Django logout function
    logout(request)
    # navigate user to login form after logging out
    return render(request, "auth/success.html")


def signup(request):
    error_message = None
    success_message = None
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(data=request.POST)

        if form.is_valid():
            # Create the user and log them in
            user = form.create_user()

            login(request, user)
            success_message = "You have successfully signed up!"
            return redirect("recipes:home")

        else:
            error_message = "Oops, something went wrong during signup."

    context = {
        "form": form,
        "error_message": error_message,
        "success_message": success_message,
        "MEDIA_URL": settings.MEDIA_URL,
    }

    return render(request, "auth/signup.html", context)
