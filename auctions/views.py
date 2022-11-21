from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import AuctionForm
import datetime
from .models import User, Auction,Watchlist
from django.contrib.auth.decorators import login_required




@login_required
def addBid(request,id_auction):
    bid_value = request.POST['bid']
    bid_username = request.user
    bid_auction = id_auction
    print(bid_value)
    print(bid_username)
    print(bid_auction)

    return HttpResponse('bid')



@login_required
def showQtdWatchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user).first()
    auctions = watchlist.auction.all()
    qtdAuctions = len(auctions)
    response = {
        'qtdAuctions':qtdAuctions
    }
    return JsonResponse(response)


@login_required
def addWatchList(request,id_auction):
    print(f"{id_auction}{request.user}")
    watchlist = Watchlist.objects.get(user=request.user)
    auction = Auction.objects.get(id=id_auction)
    watchlist.auction.add(auction)
    
    
    return HttpResponseRedirect(reverse('watchlist'))


@login_required
def deleteWatchList(request,id_auction):
    print(f"{id_auction}{request.user}")
    watchlist = Watchlist.objects.get(user=request.user)
    auction = Auction.objects.get(id=id_auction)
    watchlist.auction.remove(auction)
    
    
    return HttpResponseRedirect(reverse('watchlist'))


@login_required
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user).first()
    if watchlist == None:
        watchlist = Watchlist.objects.create(user=request.user)
        watchlist.save()
        watchlist = Watchlist.objects.filter(user=request.user).first()
        auctions = watchlist.auction.all()
        qtdAuctions = len(auctions)
        context = {
        'auctions':auctions,
        'qtdAuctions':qtdAuctions
        }
        return render(request,"auctions/watchlist.html",context)


    else:
        auctions = watchlist.auction.all()
        qtdAuctions = len(auctions)
        context = {
        'auctions':auctions,
        'qtdAuctions':qtdAuctions
        }
        return render(request,"auctions/watchlist.html",context)




def list_details(request,id_auction):
    auction = Auction.objects.get(id=id_auction)
    watchlist_current_user = Watchlist.objects.get(user = request.user)
    watchlist_current_user = watchlist_current_user.auction.all()
    
    
    context = {
        'auction': auction,
        'myauctions':watchlist_current_user
       
    }
    return render(request,"auctions/list_details.html",context)

def index(request):
    auctions = Auction.objects.all()
    watchlist_current_user = 0
    if request.user.is_authenticated:
        watchlist_current_user = Watchlist.objects.get(user = request.user)
        watchlist_current_user = watchlist_current_user.auction.all()   


   
    return render(request, "auctions/index.html" ,{
        'auctions':auctions,
        'myauctions':watchlist_current_user
      
       
    
    })


def create_list(request):
    
    if request.method == 'POST':
        form = AuctionForm(request.POST,request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            initial_bid = form.cleaned_data["initial_bid"]
            auction_url_img = form.cleaned_data["auction_url_img"]
            category = form.cleaned_data["category"]
            created_by = request.user
            created_at = datetime.datetime.now() 

            auction = Auction.objects.create(auction_title = title, auction_desc = description, initial_bids =initial_bid,auction_url_img = auction_url_img, auction_category=category,created_at =created_at, created_by= created_by)
            auction.save()
            #print(title,description,initial_bid,auction_url_img,category,created_by,created_at)
            return HttpResponseRedirect(reverse('index'))

        else:
            print(form.errors)
            return HttpResponseRedirect(reverse('index'))

    return render(request,"auctions/create_list.html",{
        'form':AuctionForm()
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
            watchlist = Watchlist.objects.create(user=user)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
