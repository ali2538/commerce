from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, WatchList


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        if User.objects.filter(username=username).exists():
            return render(request, 'auctions/register.html', {
                "message": 'Username Already Taken'
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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        title = request.POST['name']
        description = request.POST['description']
        startingBid = request.POST['startingBid']
        category = request.POST['category']
        image_path = request.POST['item_image']
        listing = Listing(createdBy=request.user, item_title=title, description=description, startingBid=startingBid, highestBid=startingBid,
                          category=category, item_image=image_path)
        listing.save()
        return HttpResponseRedirect(reverse('auctions:index'))

    else:
        return render(request, 'auctions/newListing.html')


def listing(request, listing_id):
    if request.method == 'POST':
        pass
    else:
        listing_details = Listing.objects.get(pk=listing_id)
        in_watchlist = False
        if request.user.is_authenticated:
            if WatchList.objects.filter(user=request.user, listing_id=listing_id):
                in_watchlist = True
        return render(request, 'auctions/listing.html', {
            'listing': listing_details,
            'watched': in_watchlist
        })


def categories(request):
    categories = list(Listing.objects.values(
        'category').order_by().annotate(Count('category')))
    return render(request, 'auctions/categories.html', {
        'categories': categories
    })


def category(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, 'auctions/category.html', {
                  'listings': listings,
                  'category': category
                  }
                  )


def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watch_item = WatchList(listing=listing, user=request.user)
    watch_item.save()
    return HttpResponseRedirect(reverse('auctions:listing', kwargs={
        'listing_id': listing_id
    }))
