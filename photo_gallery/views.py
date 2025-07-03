from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import RegisterForm, ProfileForm, PhotoUploadForm
from .models import Profile, Photo

# Home Page - Shows all uploaded photos
def index(request):
    photos = Photo.objects.all().order_by('-uploaded_at')
    return render(request, 'photo_gallery/index.html', {'photos': photos})


# Upload or Edit a Photo
@login_required
def photo_upload(request, photo_id=None):
    photo = None
    if photo_id:
        photo = get_object_or_404(Photo, id=photo_id, user=request.user)
        form = PhotoUploadForm(request.POST or None, request.FILES or None, instance=photo)
    else:
        form = PhotoUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        new_photo = form.save(commit=False)
        new_photo.user = request.user
        new_photo.save()
        return redirect('profile')

    return render(request, 'photo_gallery/photo_upload.html', {
        'form': form,
        'editing': bool(photo_id),
        'photo': photo
    })


# View Photo Details
def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'photo_gallery/photo_detail.html', {'photo': photo})


# Like or Unlike a Photo
@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('index')))


# Search Results View
def search_results(request):
    query = request.GET.get('q', '').lstrip('#')
    results = []
    if query:
        results = Photo.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()
    return render(request, 'photo_gallery/searchresults.html', {
        'query': query,
        'results': results
    })


# Register a New User
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Profile auto-created by signal
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {
                'form': form,
                'error': 'Invalid username or password'
            })
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# Logout View
@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return redirect('index')


# Profile View (edit and view others)
@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        # Update user fields from POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username:
            request.user.username = username
        if email:
            request.user.email = email
        request.user.save()

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
        form.fields['username'].initial = request.user.username
        form.fields['email'].initial = request.user.email

    all_users = User.objects.all()

    return render(request, 'accounts/profile.html', {
        'form': form,
        'all_users': all_users
    })


# Dashboard - Shows stats and recent uploads
@login_required
def dashboard_view(request):
    user_photos = Photo.objects.filter(user=request.user).order_by('-uploaded_at')[:6]
    photos_uploaded = user_photos.count()
    total_likes = sum(photo.likes.count() for photo in user_photos)

    return render(request, 'accounts/dashboard.html', {
        'photos_uploaded': photos_uploaded,
        'total_likes': total_likes,
        'recent_photos': user_photos
    })

@login_required
def photo_delete(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    if request.method == 'POST':
        photo.delete()
        return redirect('profile')
    return redirect('profile')
