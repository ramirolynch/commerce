from django import forms
from django.forms import ModelForm
from .models import Listing, Bid, Watchlist, Comment 
from django.forms import BaseModelFormSet
from django.forms import modelformset_factory


class newListForm(ModelForm):

    class Meta:
        model = Listing
        fields = ('listing_name', 'description','start_price', 'comedy_category', 'url')
        widgets = {
            "description": forms.TextInput(
                attrs={
                "class":"form-control"
                }),
            "listing_name": forms.TextInput(
                attrs={
                "class":"form-control"
                }),

            "comedy_category":forms.Select(
                attrs={
                "class":"form-control"
                }),

            "url": forms.TextInput(
                attrs={
                "class":"form-control"
                }),

            "start_price": forms.NumberInput(
                attrs={
                "class":"form-control"
                }),
        }
        

class newBid(ModelForm):
    class Meta:
        model = Bid 
        fields = ('bid',)

        widgets = {
        
        "bid": forms.NumberInput(
            attrs={
            "class":"form-group",
            "Placeholder": "Enter Your New Bid",
            })

        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body':""
        }
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class":"form-group",
                    "placeholder":"Type Your Comment",
                }
            )
        }

class ChangeActiveForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['active']
        labels = {
            'active':"Change Status"
        }
        widgets = {
            'active': forms.CheckboxInput(
                attrs={
                    'class':'form-group',
                    'placeholder':'Change',
                    'input_type': 'checkbox'
                }
            )
        }

        


   



   