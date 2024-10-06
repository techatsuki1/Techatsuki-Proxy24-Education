from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .models import CustomUser

from django.db.models.query_utils import Q

from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, SetPasswordForm, PasswordResetForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError




def get_user_context(request):
    context = {}
    if request.user.is_authenticated:
        current_user = request.user
        context.update({
            'current_user': current_user,
            'username': current_user.username,
            'email': current_user.email,
            'description': current_user.description,
            
            'image': current_user.image.url if current_user.image else None,
            'status': current_user.status,
            'website_url': current_user.website_url,
            'twitter_profile': current_user.twitter_profile,
            'facebook_profile': current_user.facebook_profile,
            'linkedin_profile': current_user.linkedin_profile,
            'youtube_profile': current_user.youtube_profile,
            
            
        })
    return context


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
                the received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('homepage')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="users/register.html",
        context={"form": form}
    )

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("homepage")

@user_not_authenticated
def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            status = form.cleaned_data["status"]

            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Check if the user's status matches the form status
                if user.status == status:
                    login(request, user)
                    messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                    # Set a flag in the session
                    request.session['show_celebration'] = True
                    return redirect("homepage")
                else:
                    messages.error(request, "The status does not match.")
            else:
                messages.error(request, "Invalid username or password.")

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                
                messages.error(request, error)

    form = UserLoginForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={"form": form}
    )


 
@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})

@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('homepage')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password_reset.html", 
        context={"form": form}
    )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('homepage')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("homepage")




@login_required
def accountsecurity(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if new_password and confirm_new_password:
            if new_password == confirm_new_password:
                try:
                    # Validate the password
                    validate_password(new_password, request.user)

                    # Update password and save user
                    request.user.set_password(new_password)
                    request.user.save()

                    # Important: keep the user logged in after password change
                    update_session_auth_hash(request, request.user)

                    messages.success(request, "Your password has been successfully updated.")
                    return redirect('accountsecurity')  # Redirect to avoid form re-submission

                except ValidationError as e:
                    # If password validation fails, pass errors to the template
                    messages.error(request, e)

            else:
                messages.error(request, "The new password and confirmation do not match.")
        else:
            messages.error(request, "Please fill out all fields.")
    
    context = get_user_context(request)
    return render(request, "profile/account-security.html", context)

def profilephoto(request):
    if request.method == "POST":
        image_file = request.FILES.get('image_file')  # Get the uploaded file
        
        if image_file:  # If the user has uploaded an image
            current_user = request.user
            current_user.image = image_file  # Assign the image to the user's image field
            current_user.save()  # Save the updated user object
            
            # Optionally: Add a success message if desired
            # messages.success(request, "Profile image updated successfully!")

        return redirect('profilephoto')  # Redirect to the same page to avoid re-submission
    
    context = get_user_context(request)  # Pass user context to the template
    return render(request, "profile/profile-photo.html", context)

def closeaccount(request):
    context = get_user_context(request)
    return render(request,"profile/Close-Account.html",context)
def editnotification(request):
    context = get_user_context(request)
    return render(request,"profile/Edit-notifications.html",context)
def privacy(request):
    context = get_user_context(request)
    return render(request,"profile/Privacy.html",context)




@login_required
def profile(request):
    if request.method == "POST":
        user = request.user  # Get the current logged-in user
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        last_name = request.POST.get('last_name')
        headline = request.POST.get('headline')
        description = request.POST.get('description')
        language = request.POST.get('locale')
        website_url = request.POST.get('website_url')
        twitter_profile = request.POST.get('twitter_profile')
        facebook_profile = request.POST.get('facebook_profile')
        linkedin_profile = request.POST.get('linkedin_profile')
        youtube_profile = request.POST.get('youtube_profile')
        

        # Update user and profile fields
        user.first_name = first_name
        user.last_name = last_name
        user.email=email
        user.headline = headline
        user.description = description
        user.language = language
        user.website_url = website_url
        user.twitter_profile = twitter_profile
        user.facebook_profile = facebook_profile
        user.linkedin_profile = linkedin_profile
        user.youtube_profile = youtube_profile
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    # Context for GET request
    context = {
        'user': request.user,
        
    }
    return render(request, 'profile/profile.html', context)
from django.shortcuts import render
from .models import CustomUser

def tutor_list(request):
    # Fetch all users with status 'tutor'
    tutors = CustomUser.objects.filter(status='tutor')
    
    return render(request, 'tutor_list.html', {'tutors': tutors})
