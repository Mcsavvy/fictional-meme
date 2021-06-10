from globals import (
    render,
)
from shop.models import Order
from globals.models import (
    AddressAndInfo,
    Profile, Theme,
    Themes, Node, User, nodify
)
from .decorators import (
    address_exists, allowed_user,
    authenticated_user, profile_exists,
    bind_request
)
from django.shortcuts import redirect
from .forms import CreateUserForm, UserProfileForm, AddressForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import JsonResponse
from .templatetags.theme import which, get
# Create your views here.


# LOGIN/REGISTER USER
@authenticated_user
def auth(request):
    if(request.method == "POST"):
        if request.POST['type'] == "login":
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                Node.objects.get(user=User.objects.get(username=username))
            except Exception:
                messages.error(request, 'No user with that username.')
                return redirect("auth")
            user = authenticate(request, username=username, password=password)
            if(user is not None):
                login(request, user)
                return redirect('dash')
            else:
                messages.error(request, 'Check password and try again.')
                return redirect("auth")
        else:
            required = ["email", "password", "username"]
            user_dict = {}
            for field in required:
                value = request.POST.get(field, "")
                if not value:
                    print(f"{field} is required.")
                    return redirect("auth")
                user_dict[field] = value
            password = user_dict.pop("password")
            new_user = User.objects.create(**user_dict)
            new_user.set_password(password)
            new_user.save()
            try:
                group = Group.objects.get(name='customer')
            except Group.DoesNotExist:
                group = Group.objects.create(name='customer')
            new_user.groups.add(group)
            node = nodify(new_user)
            if node == "OK":
                messages.success(
                    request,
                    "Account created! Log in to get started."
                )
            else:
                messages.warning(request, "Something went wrong.")
                print(node)
            return redirect('auth')
    return render(request, 'user/auth_form.html')


# USER DASHBOARD
@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
def user_dashboard(request):
    node = Node.objects.get(user=request.user)
    profile = node.get_profile
    address = node.get_info
    is_there = bool(profile)
    address_there = bool(address)
    context = {
        'profile': profile,
        'have_profile': is_there,
        'address_there': address_there,
        'address': address,
    }
    return render(request, 'user/user_dash.html', context)


# UPDATE USER PROFILE
@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
def profile_update(request):
    node = Node.objects.get(user=request.user)
    profile_form = UserProfileForm()
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            profile_form.save(node)
            messages.success(request, 'Profile Info Saved.')
            return redirect('dash')
    context = {
        'profile_form': profile_form
    }
    return render(request, 'user/profile_update.html', context)


# ADD ADDRESS
@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
def address_update(request):
    node = Node.objects.get(user=request.user)
    address_form = AddressForm()
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address_form.save(node)
            messages.success(request, 'Address Info Saved.')
            return redirect('dash')
    context = {
        'address_form': address_form
    }
    return render(request, 'user/address_update.html', context)


# LOGOUT USER
def logout_user(request):
    logout(request)
    return redirect('auth')


@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
def profile_edit(request):
    node = Node.objects.get(user=request.user)
    profile_form = UserProfileForm()
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            profile = Profile.objects.get(node=node)
            profile.first_name = request.POST['first_name']
            profile.last_name = request.POST['last_name']
            profile.email = request.POST['email']
            profile.save()
            messages.success(request, 'Profile Updated.')
            return redirect('dash')
    context = {
        'profile_form': profile_form,
        'profile': Profile.objects.get(node=node)
    }
    return render(request, 'user/profile_update.html', context)


# ADD ADDRESS
@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
def address_edit(request):
    node = Node.objects.get(user=request.user)
    address_form = AddressForm()
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            info = AddressAndInfo.objects.get(node=node)
            info.country = request.POST['country']
            info.city = request.POST['city']
            info.home_street = request.POST['home_street']
            info.phone = request.POST['phone']
            info.save()
            messages.success(request, 'Address Updated.')
            return redirect('dash')
    context = {
        'address_form': address_form,
        'info': AddressAndInfo.objects.get(node=node)
    }
    return render(request, 'user/address_update.html', context)


@bind_request('POST')
def theme(request):
    fields = "dm dk lt bg gb pm sc ab ba".split()
    user = request.user
    if request.method == "POST":
        theme_name = which(user.username)
        if theme_name == "NON-EXISTING-NODE":
            data = {
                "message": "You don't have permission to change theme.",
                "level": "error"
            }
            return JsonResponse(data)
        target = Theme.objects.get(name=theme_name)
        for i in target._meta.local_fields:
            try:
                setattr(target, i.name, request.POST[i.name])
            except Exception:
                pass
        target.save()
    data = {
        key: get(
            user.username,
            key
        ) for key in fields
    }
    return JsonResponse(data)