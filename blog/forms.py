from django import forms
from . models import Categories,Post,Comment,Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','category','tag']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields= ['content']