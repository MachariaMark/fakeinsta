from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, views, forms
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from .forms import LikesForm, CommentsForm, UpdateProfileForm, UploadPicForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,Http404,HttpResponseRedirect