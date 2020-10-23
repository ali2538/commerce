from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, WatchList, Bid, Comment
from auctions.forms import NewComment


def watchlist_count(username):
    user = User.objects.get(username=username)
    return WatchList.objects.filter(user=user).count()


def index(request):
    listings = Listing.objects.all()
    if request.user.is_authenticated:
        watched_count = watchlist_count(request.user.username)
        if watched_count > 0:
            return render(request, "auctions/index.html", {
                'listings': listings,
                'watched_count': watched_count
            })
        else:
            return render(request, "auctions/index.html", {
                'listings': listings
            })
    else:
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
        watched_count = watchlist_count(request.user.username)
        if watched_count > 0:
            return render(request, "auctions/newListing.html", {
                'watched_count': watched_count
            })
        else:
            return render(request, 'auctions/newListing.html')


def listing(request, listing_id):
    listing_details = Listing.objects.get(pk=listing_id)
    in_watchlist = False
    watched_count = 0
    comments = Comment.objects.filter(
        listing=listing_details).order_by('-commentDate')
    if request.user.is_authenticated:
        if WatchList.objects.filter(user=request.user, listing_id=listing_id):
            in_watchlist = True
        watched_count = watchlist_count(request.user.username)
    if request.method == 'POST':
        bid_amount = float(request.POST['newBid'])
        if bid_amount <= listing_details.highestBid:
            return render(request, 'auctions/listing.html', {
                'message': f"New Bid Has to Be Higher than the Current Highest Bid '${listing_details.highestBid}'",
                'listing': listing_details,
                'watched_count': watched_count,
                'comments': comments,
                'watched': in_watchlist
            })
        else:
            bidder = User.objects.get(username=request.user.username)
            new_bid = Bid(listing=listing_details,
                          bidder=bidder, amount=bid_amount)
            listing_details.highestBid = bid_amount
            new_bid.save()
            listing_details.save()
            return render(request, 'auctions/listing.html', {
                'message': f"New Bid Was Added Successfully and You Are Now the Highest Bidder",
                'listing': listing_details,
                'watched_count': watched_count,
                'comments': comments,
                'watched': in_watchlist
            })

    else:
        if watched_count > 0:
            return render(request, 'auctions/listing.html', {
                'listing': listing_details,
                'watched': in_watchlist,
                'comments': comments,
                'watched_count': watched_count
            })
        return render(request, 'auctions/listing.html', {
            'listing': listing_details,
            'comments': comments,
            'watched': in_watchlist
        })


def categories(request):
    categories = list(Listing.objects.values(
        'category').order_by().annotate(Count('category')))
    if request.user.is_authenticated:
        watched_count = watchlist_count(request.user.username)
        if watched_count > 0:
            return render(request, 'auctions/categories.html', {
                'categories': categories,
                'watched_count': watched_count
            })
    return render(request, 'auctions/categories.html', {
        'categories': categories
    })


def category(request, category):
    listings = Listing.objects.filter(category=category)
    if request.user.is_authenticated:
        watched_count = watchlist_count(request.user.username)
        if watched_count > 0:
            return render(request, 'auctions/category.html', {
                'listings': listings,
                'category': category,
                'watched_count': watched_count
            })
    return render(request, 'auctions/category.html', {
                  'listings': listings,
                  'category': category
                  })


def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user.username)
    watch_item = WatchList(listing=listing, user=user)
    watch_item.save()
    return HttpResponseRedirect(reverse('auctions:listing', kwargs={
        'listing_id': listing_id
    }))


def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user.username)
    watchlist = WatchList.objects.filter(listing=listing, user=user)
    watchlist.delete()
    return HttpResponseRedirect(reverse('auctions:listing', kwargs={
        'listing_id': listing_id
    }))


def load_watchlist(request):
    user = User.objects.get(username=request.user.username)
    user_watchlist = list(WatchList.objects.filter(user=user))
    return render(request, 'auctions/watchlist.html', {
        'watchlist': user_watchlist
    })


def add_comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        comment_form = NewComment(request.POST)
        if comment_form.is_valid():
            comment_title = comment_form.cleaned_data['new_comment_title']
            comment_body = comment_form.cleaned_data['new_comment_body']
            comment = Comment(listing=listing, commentBy=user,
                              comment=comment_body, comment_title=comment_title)
            comment.save()
            return HttpResponseRedirect(reverse('auctions:listing', kwargs={
                'listing_id': listing_id
            }))

    else:
        new_comment_form = NewComment()
        return render(request, 'auctions/new_comment.html', {
            'comment_form': new_comment_form,
            'listing': listing
        })


def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.auctionOpen = False
    highestBid = Bid.objects.filter(listing=listing).order_by('-amount')[0]
    listing.winner = highestBid.bidder
    listing.save()
    return HttpResponseRedirect(reverse('auctions:listing', kwargs={
        'listing_id': listing_id
    }))
