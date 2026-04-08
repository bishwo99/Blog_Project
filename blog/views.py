from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import Post,Comment,Tag,Categories

# Create your views here.



