from distutils.command.upload import upload
from django import forms
from .models import Auction


class AuctionForm(forms.Form):

    title = forms.CharField(label='Title',max_length=30)
    description = forms.CharField(label='Description',max_length=255)
    initial_bid = forms.FloatField(label='Initial Bid')
    auction_url_img = forms.ImageField(label="Image")
    category = forms.CharField(label='Category',max_length=30)

    title.widget.attrs.update({'class': 'form-control'})
    description.widget.attrs.update({'class': 'form-control'})
    initial_bid.widget.attrs.update({'class': 'form-control'})
    auction_url_img.widget.attrs.update({'class': 'form-control'})
    category.widget.attrs.update({'class': 'form-control'})

    
