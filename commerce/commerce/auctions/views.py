from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import connection
from datetime import datetime
from django.template import RequestContext

from .models import User, listings, Bids, Comments,closed_listings,WatchList


def index(request):
    L = listings.objects.all()

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

    # grabbing data
    cursor = connection.cursor()
    cursor.execute('select count(*) from auctions_bids')
    cursor.fetchall()

    count = Listings.bids.all().count()

    # logic
    # if request.method == "POST" and 
    if request.method == "POST" and offer:
        if float(offer) < Listings.price or float(offer) <= prices[-1]:
            float(offer)
            error = "bid unsuccessful offer at higher price"
            count -= 1

            prices = list(auction_bid.values_list('amount', flat=True))
            prices.sort()

            return render(request, "auctions/listing.html", {
                "item": Listings,
                "users": Listings.owner.all(),
                "error": error,
                "count_of_bids": count,
                "highest_bid": prices[-1]
            })
        


        else:
            prices = list(auction_bid.values_list('amount', flat=True))
            prices.sort()

            bid = Listings.bids.create(amount=float(offer))

            bid.save()

            return HttpResponseRedirect(Listings)
    if request.method == "POST" and close:
        Listings = listings.objects.get(pk=close)   
        highest_bid_obj = Bids.objects.filter(auction = Listings, amount=prices[-1]).order_by('-amount').first()
        Closed_Listings = closed_listings.objects.all()
        Closed_Listings.create(title= Listings.title, description=Listings.description, image = Listings.image, price=Listings.price, category=Listings.category,date=Listings.date, winner=highest_bid_obj.user.username)
        Listings.delete()
        
        return HttpResponseRedirect(reverse('closed'))
    
    # if request.method == "POST" and request.GET.get('comment'):
    #     return render(request. "auctions/")

    # If the request method is not POST, or if the count is less than 2
    prices = list(auction_bid.values_list('amount', flat=True))

    prices.sort()
    try: 
        global highest_bid1
        highest_bid1 = prices[-1]
    except IndexError:
        return render(request, "auctions/listing.html", {
        "item": Listings,
        "users": Listings.owner.all(),
        "count_of_bids": count
    })

    
    return render(request, "auctions/listing.html", {
        "item": Listings,
        "users": Listings.owner.all(),
        "count_of_bids": count,
        "highest_bid": highest_bid1
    })


def closed(request):
    closed_items = closed_listings.objects.all()
    return render(request, "auctions/closed.html",
                  {
                      "auction":closed_items
                  })
def old_auction(request, title):

    closed_items = closed_listings.objects.get(pk=title)
    if request.GET.get('comment'):
        comment = Comments(content=request.GET.get('comment'), closed_auction=closed_items)
        comment.save()

        return render(request, "auctions/closed_listing.html",
                      {
                          "item": closed_items,
                          "comment": comments
                      })
    comments = Comments.objects.filter(closed_auction=closed_items)
    return render(request, "auctions/closed_listing.html",
                  { 
                      "item": closed_items
                      ,"comment": comments
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
   added = False
   if request.user:
        item = listings.objects.get(pk = title)
        watchlist = WatchList.objects.create(listing = item, user = request.user)
        watchlist.save()
        added = True
        context = {
        'added': added
        }
        print('syuf')

        request_context = RequestContext(request, context)
        return HttpResponseRedirect(reverse("auction_listings", args = title), context) 
   return HttpResponseRedirect(reverse("auction_listings", args = title), context) 

    