from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render
from .forms import AuctionListingForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist



def index(request):
    Active_AuctionListing = AuctionListing.objects.filter(status__in=['active', 'Active'])

    return render(request, "auctions/index.html",
                  {
                      "AuctionListing" : Active_AuctionListing
                  })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required(login_url='unauthorized')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
@login_required(login_url='unauthorized')
def add_auction_listing(request):
    if request.method == 'POST':
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            auction_listing = form.save(commit=False)
            auction_listing.owner = request.user
            auction_listing.save()
        return HttpResponseRedirect(reverse('listing_page', args=[auction_listing.id]))
    else:
        form = AuctionListingForm()
    return render(request, 'auctions/add.html', {'form': form})



def Listing_Page(request, Listing_id):
    try:
        try:
            auction_listing = AuctionListing.objects.get(pk=Listing_id)
        except (ObjectDoesNotExist, ValueError):
            return render(request, 'auctions/Error.html')

        highest_bid = Bid.objects.filter(auction_listing=auction_listing).aggregate(Max('bid_price'))
        highest_bid_price = highest_bid['bid_price__max']
        bid=Bid.objects.filter(auction_listing=auction_listing, bid_price=highest_bid_price).first()
        bids = Bid.objects.filter(auction_listing=auction_listing, bid_price=highest_bid_price)
        if bid is not None and bid.winning==True and bid.user.username ==request.user.username:
            return render(request, 'auctions/won.html')
        else:
            highest_bidder = None
            if auction_listing.owner == request.user:
                owner = True
            else:
                owner = False


            if bids.exists():
                if request.user == bids.first().user:
                    highest_bidder = "You are the highest bidder"
                else:
                    highest_bidder = f'The Highest Bidder is {bids.first().user}'
            if request.user.is_authenticated:
                try:
                    wishlist = Wishlist.objects.get(user=request.user, auction_listing=Listing_id)
                    wish = 'Remove from wishlist'
                except Wishlist.DoesNotExist:
                    wish = 'Add to wishlist'
            else:
                wish= None
                    

            comments= Comment.objects.filter(auction_listing=Listing_id)
            return render(request, 'auctions/Listing_Page.html',
                        {
                                'auction_listing': auction_listing,
                                'bids': bids, 
                                'highest_bid_price': highest_bid_price,
                                'highest_bidder': highest_bidder,
                                'wish': wish,
                                'owner': owner,
                                'comments':comments
                            })

    except Bid.DoesNotExist:
        pass
    
@login_required(login_url='unauthorized')
def place_bid(request, Listing_id):
    if request.method == 'POST':
        bid_price = float(request.POST['bid_price'])
        auction_listing = AuctionListing.objects.get(pk=Listing_id)

        
        highest_bid = Bid.objects.filter(auction_listing=auction_listing).aggregate(Max('bid_price'))
        highest_bid_price = highest_bid['bid_price__max']
        if bid_price <= 0:
            return render(request, 'auctions/Listing_Page.html',
                    {
                        'auction_listing': auction_listing,
                        'message': "Bid price must be Higher than 0.",
                        'highest_bid_price': highest_bid_price,
                    })
        if auction_listing.status.lower() == 'active':
            if highest_bid_price is None or bid_price > float(highest_bid_price):
                bid = Bid(user=request.user, auction_listing=auction_listing, bid_price=bid_price)
                bid.save()
            elif bid_price < float(highest_bid_price):
                return render(request, 'auctions/Listing_Page.html',
                   {
                        'auction_listing': auction_listing,
                        'highest_bid_price': highest_bid_price,
                        'message': f"Must be more than ${highest_bid_price}"
                    })
        elif auction_listing.status.lower() == 'closed':
            return render(request, 'auctions/closed.html')
    return redirect('listing_page', Listing_id=Listing_id)

@login_required(login_url='unauthorized')
def Add_Wishlist(request, Listing_id):
    auction_listing = get_object_or_404(AuctionListing, id=Listing_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, auction_listing=auction_listing)
    wishlist.save()
    
    return redirect('listing_page', Listing_id=Listing_id)
@login_required(login_url='unauthorized')
def rem_Wishlist(request, Listing_id):
    wishlist = get_object_or_404(Wishlist, user=request.user, auction_listing__id=Listing_id)
    wishlist.delete()
    
    return redirect('listing_page', Listing_id=Listing_id)



@login_required(login_url='unauthorized')
def close_bidding(request, Listing_id):
    auction_listing = get_object_or_404(AuctionListing, pk=Listing_id, owner=request.user)
    auction_listing.status = 'closed'
    auction_listing.save()

    auction_listing = AuctionListing.objects.get(pk=Listing_id)
    highest_bid = Bid.objects.filter(auction_listing=auction_listing).aggregate(Max('bid_price'))
    highest_bid_price = highest_bid['bid_price__max']
    bids = Bid.objects.filter(auction_listing=auction_listing, bid_price=highest_bid_price)
    
    winner_bid = None  # Initialize the winner_bid variable
    
    if bids.exists():
        winner_bid = bids.first()
        winner_bid.winning = True
        winner_bid.save()
    
    print(winner_bid)  # winner_bid will either contain the valid bid or None
    return redirect('listing_page', Listing_id=Listing_id)

@login_required(login_url='unauthorized')
def add_comment(request, Listing_id):
        listing = get_object_or_404(AuctionListing, pk=Listing_id)

        if request.method == 'POST':
            comment_text = request.POST.get('comment_text')
            comment = Comment(user=request.user, auction_listing=listing, content=comment_text)
            comment.save()
            return redirect('listing_page', Listing_id=Listing_id)
        

def wishlist_view(request):
    if request.method=="POST":
        pass
    wishlists = Wishlist.objects.filter(user_id=request.user.id)
    auction_listings = AuctionListing.objects.filter(pk__in=wishlists.values('auction_listing_id'))
    return render(request, 'auctions/wishlist.html',
                  {
                      'AuctionListings':auction_listings
                  })

def categories(request):
    if request.method=='POST':
        selected_category = request.POST.get('category')
        auction_listings = AuctionListing.objects.filter(category=selected_category)
        return render(request, 'auctions/category.html',
                      {
                          'auction_listings':auction_listings
                      })
    return render(request, 'auctions/category_intro.html',
                  {
                      'categories':AuctionListing.CATEGORY_CHOICES
                  })

def unauthorized_access(request):
    return render(request, 'auctions/unauthorized.html')


def invalid_listing_id(request, Listing_id):
    return render(request, 'auctions/Error.html')