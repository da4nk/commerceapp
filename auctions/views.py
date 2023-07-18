from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db import connection
from datetime import datetime
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .models import User, listings, Bids, Comments,closed_listings,WatchList


def index(request):
    L = listings.objects.all()
    if request.user.is_authenticated:
        try:
            watchlist = WatchList.objects.get(user = request.user)
            count = WatchList.objects.count()
            return render(request, "auctions/index.html",
                        {
                            "auction": L,
                            "watched_items": count
                        })

        except WatchList.DoesNotExist:
            pass
    
    return render(request, "auctions/index.html",
                  {
                      "auction": L
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

# auction creat section

def create(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    price = request.POST.get('price')
    url = request.POST.get('url')
    category = request.POST.get('category')
    if request.method == "POST":
        Listing = listings.objects.create(title=title, description=description,image=url, price=price, category=category)
        Listing.save()            
        auction_listings = listings.objects.get(title=title)
        auction_listings.owner.add(request.user)
        return HttpResponseRedirect(reverse('index'))
    
    
    return render(request, "auctions/create.html")





#  listings section


def auction_listings(request, title):
    

 # variables
    Listings = listings.objects.get(pk=title)
    users = User.objects.all()
    offer = request.POST.get('bid')
    auction_bid = Listings.bids.all()
    prices = list(auction_bid.values_list('amount', flat=True))
    prices.sort()
    close = request.POST.get('close')
    comments = Comments.objects.all()

    highest_bid = max(prices, default=prices)
    # grabbing data


    count = Listings.bids.all().count()
    global added
    if request.user.is_authenticated:
        try: 
            created = WatchList.objects.get(listing = Listings, user = request.user)
            added = True
        except WatchList.DoesNotExist:
            added = False
    else:
        added = False
    # logic
    # if request.method == "POST" and 

    if request.method == "POST" and offer:
        if prices:
            if float(offer) < Listings.price or float(offer) <= highest_bid:
                float(offer)
                error = "bid unsuccessful offer at higher price"


                prices = list(auction_bid.values_list('amount', flat=True))
                prices.sort()

                return render(request, "auctions/listing.html", {
                    "item": Listings,
                    "users": Listings.owner.all(),
                    "error": error,
                    "count_of_bids": count,
                    "highest_bid": highest_bid,
                    'added': added,
                    "comments": comments
                })


            else:
                prices = list(auction_bid.values_list('amount', flat=True))
                prices.sort()

                bid = Listings.bids.create(amount=float(offer))

                bid.save()

                return HttpResponseRedirect(title)
        else:
            prices = list(auction_bid.values_list('amount', flat=True))
            prices.sort()

            bid = Listings.bids.create(amount=float(offer))

            bid.save()

            return HttpResponseRedirect(title)
    if request.method == "POST" and close:
        Listings = listings.objects.get(pk=close)   
        try:
            highest_bid_amount = max(prices, default = 0)

            highest_bid_obj = Bids.objects.filter(amount=highest_bid_amount).first()
            print(highest_bid_obj)
            Closed_Listings = closed_listings.objects.all()
            Closed_Listings.create(title= Listings.title, description=Listings.description,
                                    image = Listings.image, price=Listings.price, 
                                    category=Listings.category,date=Listings.date, 
                                    winner=highest_bid_obj.user.username)
        except AttributeError:
               Closed_Listings = closed_listings.objects.all()
               Closed_Listings.create(title= Listings.title, description=Listings.description,
                                    image = Listings.image, price=Listings.price, 
                                    category=Listings.category,date=Listings.date, 
                                    winner="no winner")

        Listings.delete()
        
        return HttpResponseRedirect(reverse('closed'))
    highest_bid = max(prices, default=0)


    return render(request, "auctions/listing.html", {
        "item": Listings,
        "users": Listings.owner.all(),
        "count_of_bids": count,
        "highest_bid": highest_bid,
                        'added': added,
                                        "comments": comments


    })


def closed(request):
    closed_items = closed_listings.objects.all()
    return render(request, "auctions/closed.html",
                  {
                      "auction":closed_items
                  })
def old_auction(request, title):

    closed_items = closed_listings.objects.get(pk=title)

       
    return render(request, "auctions/closed_listing.html",
                  { 
                      "item": closed_items
                  })





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



#  categories section
def categories(request):
    category = request.GET.get('category')
    listing_category = listings.objects.values_list('category')
    if not category:
        return render(request, 'auctions/categories.html',
                  {
                      "category": listing_category
                  })
    else:
        return HttpResponseRedirect('cdirect')

def cdirect(request, title):
    
    # try selecting auctions based on category
    selected_listings = listings.objects.filter(category=title).values()

    if not selected_listings:
        return render(request, "auctions/categories_error.html")        

    # if there is no category present error
                      
    return render(request, "auctions/category_list.html",
                      {
                          'listings': selected_listings
                      })
        


def watchlist(request, title):     
    item = listings.objects.get(pk = title)
    add = request.POST.get('add')
   
   

        
        
    if request.method == "POST" and add: 

        try:
            WatchList.objects.get(user = request.user, listing  = item)
            if WatchList.objects.get(user = request.user, listing= item):
                        WatchList.objects.filter(user=request.user, listing=item).delete()
                        return redirect(reverse('auction_listings', args=[title]))
        except WatchList.DoesNotExist:
            WatchList.objects.create(user = request.user, listing = item, added = True)
            return redirect(reverse('auction_listings', args=[title]))


     
        

    return redirect(reverse('auction_listings', args=[title]))


#  make page of watched items
@login_required
def watched_items(request):

    try:
        WatchList_id = WatchList.objects.get(user = request.user)
        listed_item = listings.objects.get(pk = WatchList_id.listing_id)
    except WatchList.DoesNotExist:
        return render(request, "auctions/noitems.html")

    return render(request, "auctions/watchlist.html",
                  {
                      "auctions": listed_item
                  })

@login_required
def comment(request, id):
    Listing = listings.objects.get(pk=id)
    content = request.POST.get('comment')
    if request.method == "POST":
        if content:
            Comments.objects.create(content = content, auction =Listing)   
        return redirect(reverse('auction_listings', args=[id]))
    return redirect(reverse('auction_listings', args=[id]))
