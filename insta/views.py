from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, views, forms
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from .forms import LikesForm, CommentsForm, UpdateProfileForm, UploadPicForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,Http404,HttpResponseRedirect

#landing page
def landing(request):
    form = forms.AuthenticationForm
    return render(request, 'landing_page.html', locals())

#home page
@login_required(login_url='/accounts/login')
def home(request):
  likesForm = LikesForm
  commentForm = CommentsForm
  images = Image.objects.all()
  user = request.user.get_username()
  profile = Profile.objects.all()
  likes = Like.objects.all()
  
  return render(request,'insta_pages/home.html', locals())

def likes(request,image_id):
  likesForm = LikesForm()
  #  CRUD     
  obj1=Like.objects.create(user=request.user,image=get_object_or_404(Image,pk=image_id),likes=1)
  obj1.save()
  print(obj1)
  return redirect('instaHome')

def comments(request,image_id):
  commentsForm = CommentsForm()
  if request.method == 'POST':
    commentsForm = CommentsForm(request.POST)
    if commentsForm.is_valid():
      form = commentsForm.save(commit=False)
      form.user=request.user
      form.image = get_object_or_404(Image,pk=image_id)
      form.save()
  
  return redirect('instaHome')

#search feature
@login_required(login_url='/accounts/login')
def search_results(request):
  likesForm = LikesForm
  commentForm = CommentsForm
  images = Image.objects.all()
  user = request.user.get_username()
  current_user = request.user
  photos = Image.objects.filter(profile=current_user.id)
  profile = Profile.objects.all()
  likes = Like.objects.all()
        
  try:
    user = User.objects.get(id =request.user.id)
  except ObjectDoesNotExist:
    raise Http404()
  message = 'based on your search term'
  return render(request, 'insta_pages/search.html',locals())
      
  if 'username' in request.GET and request.GET["username"]:
    form = forms.AuthenticationForm
    images = Image.objects.all()
    user = request.user.get_username()
    profile = Profile.objects.all()
    search_term = request.GET.get("username")
    searched_users = Image.search_by_username(search_term)
    message = f"{search_term}"
    # print(User.objects.get(username=search_term))
    photos = Image.objects.filter(profile=User.objects.get(username=search_term))

    return render(request, 'insta_pages/search.html',locals())

  else:
    message = "You haven't searched for any term"
    return render(request, 'insta_pages/search.html',locals())

#profile page
@login_required(login_url='/accounts/login')
def profilePage(request):
  likesForm = LikesForm
  commentForm = CommentsForm
  images = Image.objects.all()
  user = request.user.get_username()
  current_user = request.user
  photos = Image.objects.filter(profile=current_user.id)
  profile = Profile.objects.all()
  likes = Like.objects.all()
    
  return render(request,'insta_pages/profile.html', locals())

#update current user profile
@login_required(login_url='/accounts/login')
def updateProfile(request):
  current_user = request.user
  my_prof = Profile.objects.get(user=current_user.id)
  updateForm = UpdateProfileForm(instance=request.user)
 
  if request.method == 'POST':
    updateForm = UpdateProfileForm(request.POST,request.FILES,instance=request.user.profile)

    if updateForm.is_valid():
      updateForm.save()      
            
    return redirect('instaProfile')
  else:
    updateForm = UpdateProfileForm(instance=request.user.profile)

  return render(request,'insta_pages/update_profile.html', locals())

#upload feed/pic/video page
@login_required(login_url='/accounts/login')
def uploadPic(request):
  current_user = request.user
  # my_prof = Profile.objects.get(id=current_user.id)
  uploadForm = UploadPicForm()
  print(uploadForm)
  # uploadForm = UploadPicForm(request.POST or None,request.FILES or None)

  if request.method == 'POST':
    uploadForm = UploadPicForm(request.POST,request.FILES)
    # profile = request.user.username
    # uploadForm = UploadPicForm(request.POST or None,request.FILES or None)
    user = request.user.id

    if uploadForm.is_valid():
      upload = uploadForm.save(commit=False)
      upload.user = request.user.profile
      upload.profile = current_user
      upload.save()    
            
    return redirect('instaProfile')
  else:
    # uploadForm = UploadPicForm(request.POST or None,request.FILES or None)
    uploadForm = UploadPicForm()

  return render(request,'klooni_pages/upload_pic.html', locals()) 