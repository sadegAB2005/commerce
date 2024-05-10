# forms.py
from django import forms
from .models import AuctionListing,Bid

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['name', 'price', 'description', 'category', 'image']


from django import forms
from .models import Bid

