from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from .models import *
from django.forms import modelformset_factory
from .forms import *
from django.utils import timezone
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from decimal import Decimal 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import Http404


def index(request):


    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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



@login_required
def newList(request):
    
    form = newListForm(request.POST, request.FILES)

    if request.method == 'POST':

        form = newListForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.seller = request.user
            instance.created = timezone.now()
            form = instance.save()
            return redirect('index')

    else:

        form = newListForm()
        return render(request, "auctions/newList.html", {"form": form})


@login_required
def listing_detail(request, listing_id):

    listing = Listing.objects.get(id=listing_id)
    bid = newBid(request.POST)

    try:
        lastbid1 = Bid.objects.latest('bid')
        lastbid = lastbid1.bid
    except Bid.DoesNotExist:
        lastbid = None
        lastbid1 = None

    comment = listing.relatedlisting.filter(active=True)
    comment_form = CommentForm()

    try:
        watchlist = Watchlist.objects.get(user=request.user)
    except Watchlist.DoesNotExist:
        watchlist = None

    try:
        listing1 = listing.auction_for_bid.all().last().bid
        bidder = listing.auction_for_bid.all().last().bidder

        context = {'listing':listing, 'bid':bid, 'lastbid1':lastbid1, 'lastbid':lastbid, 'listing1':listing1, 'bidder':bidder, 'watchlist':watchlist, 'comment':comment, 'comment_form':comment_form}
    except AttributeError:
        context = {'listing':listing, 'bid':bid, 'lastbid1':lastbid1, 'lastbid':lastbid, 'watchlist':watchlist, 'comment':comment, 'comment_form':comment_form}



    if request.method == "POST":

        placebid(request, listing_id)
        addwatchlist(request, listing_id)
        addcomment(request, listing_id)
        changestatus(request, listing_id)

    return render(request, "auctions/listing_detail.html", context)



def placebid(request,listing_id):

    listing1 = Listing.objects.get(id=listing_id)
    seller = listing1.seller
    bidder = request.user
    startprice = listing1.start_price


    if request.POST['action'] == "newbid":

        bidform = newBid(request.POST)

        if bidform.is_valid():

            userbid = Decimal(request.POST.get("bid", "")) 

            try:
                listing2 = listing1.auction_for_bid.all().last().bid

                if userbid > listing2:

                    newbid = Bid(bidder=bidder, bid=userbid, listing=listing1)
                    newbid.save()
                    listing1.allbids.add(newbid)
                    listing1.latestbid = newbid
                    listing1.save()

                    messages.success(request, "The bid was succesful")
                    id=listing_id
                    context = {'id':id, 'seller':seller, 'bidder':bidder, 'listing2':listing2 }
                    response = redirect("auctions/listing_detail", context)
                    return response
                else:
                     messages.error(request, "Your bid must be higher than the current bid")
                     response = redirect("auctions/listing_detail",id=listing_id)
                     return response

            except AttributeError:
                if userbid > startprice:

                    newbid = Bid(bidder=bidder, bid=userbid, listing=listing1)
                    newbid.save()
                    listing1.allbids.add(newbid)
                    listing1.latestbid = newbid
                    listing1.save()

                    messages.success(request, "The bid was succesful")
                    id=listing_id
                    context = {'id':id, 'seller':seller, 'bidder':bidder }
                    response = redirect("auctions/listing_detail", context)
                    return response
                else:
                    messages.error(request, "Your bid must be higher than the start price")
                    response = redirect("auctions/listing_detail",id=listing_id)
                    return response

    else:
        return redirect('index')


def watchlist(request):
    
    if request.user.id is None:
        return redirect('index')

    lastbid = Bid.objects.last()
    lastbid1 = lastbid.bid 
    highbidder = lastbid.bidder

    try:
        mywatchlist = Watchlist.objects.get(user=request.user)
        mywatchlist = mywatchlist.watch.all()
    except Watchlist.DoesNotExist:
        mywatchlist = None
        
    context = {
        'mywatchlist': mywatchlist,
        'lastbid1':lastbid1,
        'highbidder':highbidder
        }

    return render(request, "auctions/watchlist.html", context)


@login_required
def addwatchlist(request, listing_id):

    if request.POST['action'] == 'watchme':

        addauction = Listing.objects.get(id=listing_id)

        try:
            watchlist = Watchlist.objects.get(user=request.user)
        except Watchlist.DoesNotExist:
            watchlist = Watchlist(user=request.user, id=listing_id)
            watchlist.save()

        if addauction in watchlist.watch.all():
            watchlist.watch.remove(addauction)
            watchlist.save()
            messages.success(request, "This joke was removed from your watchlist")
        else:
            watchlist.watch.add(addauction)
            watchlist.save()
            messages.success(request, "This joke was added to your watchlist")

            response = redirect("auctions/listing_detail.html", id=listing_id)
            return response

@login_required
def addcomment(request, listing_id):

    #this grabs the current listing_id and its contents and saves it under a variable "listing"
    listing = Listing.objects.get(id=listing_id)
    #this grabs the user

    # lists active comments for this listing
    comment = listing.relatedlisting.filter(active=True)

    new_comment = None

    if request.POST['action'] == 'Add Comment':
        # a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current listing to the comment
            new_comment.listing = listing
            new_comment.user = request.user

            # save the comment to the database
            new_comment.save()
        else:
            comment_form = CommentForm()
            response = redirect("auctions/listing_detail.html", { 'listing': listing, 'comment': comment, 'new_comment': new_comment, 'comment_form': comment_form })
            return response

@login_required
def mylistings(request):


    listings= Listing.objects.filter(seller=request.user)
    activeForm = ChangeActiveForm()

    context = {'mylistings':listings, 'activeForm':activeForm }

    return render(request, "auctions/mylistings.html", context)


@login_required
def mylisting(request, listing_id):

    listing = Listing.objects.get(id=listing_id)
    activeForm = ChangeActiveForm()
    changeForm = ChangeActiveForm(request.POST)
    watchlist = Watchlist.objects.get(user=request.user)
    
    try:
        listing1 = listing.auction_for_bid.all().last().bid
        bidder = listing.auction_for_bid.all().last().bidder
    except AttributeError:
        listing1 = None
        bidder = None
    
    # lists active comments for this listing
    comment = listing.relatedlisting.filter(active=True)
    comment_form = CommentForm()

    if request.method == "POST":

        addwatchlist(request, listing_id)
        addcomment(request, listing_id)
        changestatus(request, listing_id)

    context = { "listing": listing, "watchlist": watchlist, "comment": comment,
                'comment_form': comment_form, 'changeForm':changeForm,
                'activeForm':activeForm, 'listing1':listing1, 'bidder':bidder
              }
    return render(request, "auctions/mylisting.html", context=context)


@login_required
def changestatus(request, listing_id):

    if request.POST['action'] == 'changestatus':
        
        listing_object=Listing.objects.get(id=listing_id)
        listing_object.active = False
        listing_object.save()

        messages.success(request, "Your listing has been closed")

        return render(request, "auctions/mylisting.html")

# @login_required
# def closedlisting(request):
#     try:  
#         winners = Bid.objects.all() 
#         return render(request, template_name="auctions/closelisting.html", context={"winners":winners})
#     except Bid.DoesNotExist:
#         raise Http404("The model does not have results")

@login_required
def closedlisting(request):
    return render(request, "auctions/closedlisting.html", {
        "listings": Listing.objects.all()
        })

@login_required
def categorieslisting(request):
    data = ['Clean', 'Blue', 'Absurd', 'Political', 'Dark']
    return render(request, template_name="auctions/categorylisting.html", context={"categories":data})

@login_required
def categoriesdetail(request, category):
    """ Return all filtered objects """
    data = Listing.objects.filter(comedy_category=category)
    return render(request, template_name="auctions/categorydetail.html", context={"items":data})



