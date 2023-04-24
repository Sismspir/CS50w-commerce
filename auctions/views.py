from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Watchlist, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "Listing": Listing.objects.all()
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

@login_required(login_url="login")
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["text"]
        starting_price = request.POST["starting_price"]
        url = request.POST["url"]
        category = request.POST["category"]
        owner = request.user
        listing = Listing(title=title, text=text, starting_price=starting_price, img=url, owner=owner, category=category)
        listing.save()

    return render(request, "auctions/create.html")


def display(request, title):
    #find the clicked item using its title
    active_listings = Listing.objects.all()
    bids = Bid.objects.all()
    comments = Comment.objects.all()
    id = ""
    my_item = ""
    owner = ""
    text = ""
    starting_price = ""
    url = ""
    bid_maker = ""
    new_bid = 0
    for item in active_listings:
        if item.title == title:
            comment_list = []
            my_item = item
            is_active = my_item.is_active
            id = item.id
            owner = item.owner
            title = item.title
            text = item.text
            starting_price = item.starting_price
            url = item.img
            my_item = item
            for bid in bids:
                if item.title == bid.item.title:
                    new_bid = float(bid.value)
                    bid_maker = bid.bid_maker      

    if request.method == "POST":
        #checks if the user is logged in
        if not request.user.is_authenticated:
            message = "Error: You have to log in first.."
            return render(request, "auctions/error.html", {"message": message})
        #checks if the user made a bid    
        if request.POST.get("bid"):
            latest_bid = request.POST["bid"]
            if float(latest_bid) <= starting_price:
                return render(request, "auctions/error.html", {"message": "Your bid should be at least 0.01$ greater than the starting price."})
            current_bid = Bid(item=my_item, value=latest_bid, bid_maker=request.user)
            if float(latest_bid) > new_bid: 
                current_bid.save()
            else:
                return render(request, "auctions/error.html", {"message": "Your bid should be at least 0.01$ greater than the current bid."})

            message = "Your bid added successfully"
            return render(request, "auctions/error.html", {"message": message})
        #checks if the user commented the item
        elif request.POST.get("new_comment"):
            new_comment = request.POST.get("new_comment")
            comment = Comment(item=my_item, author=request.user, content=new_comment)
            comment.save()
        #checks if the user closed the Listing
        elif request.POST.get:
            if request.POST.get("bid") == None and request.POST.get("new_comment") == None:
                is_active = not my_item.is_active
                my_item.is_active = is_active
                my_item.save()
                # deletes comments when the item is sold
                comment_list = [] 
                for comment in comments:
                    if comment.item == my_item:
                        comment_list.append({ "author": comment.author, "content": comment.content})         
                return render(request, "auctions/display.html", { "id":id, "owner": owner, "title": title, "text": text, "starting_price": starting_price, "url": url,
                "comment_list": comment_list, "new_bid": new_bid, "is_active": is_active, "winner": bid_maker})

            
    # returns the comments made for the item
    for comment in comments:
        if comment.item == my_item:
            comment_list.append({ "author": comment.author, 
            "content": comment.content})                  
    return render(request, "auctions/display.html", { "id":id, "owner": owner, "title": title, "text": text, "starting_price": starting_price, "url": url, "comment_list": comment_list, "new_bid": new_bid, "is_active": is_active, "winner": bid_maker })

def watchlist(request):
    if not request.user.is_authenticated:
            message = "Error: You have to log in first.."
            return render(request, "auctions/error.html", {"message": message})
    my_list = Watchlist.objects.all()
    items = []
    for item in my_list:
        if request.user == item.owner:
            items.append(item)
    return render(request, "auctions/watchlist.html", {"list": items})

def delete(request):
    id=request.GET.get("id")
    message = "Your item deleted successfully!"
    try:
        object = Watchlist.objects.get(id=id)
        object.delete()
        return render(request, "auctions/error.html", {"message": message})
    except Watchlist.DoesNotExist:
        message = f"The item with id = {id} you're trying to delete doesn't exist."
        return render(request, "auctions/error.html", {"message": message})

def add(request):
    message = "Your item added successfully!"
    # try to add the item with the id given from display.html
    try:
        current_watchlist = Watchlist.objects.filter(owner=request.user)
        id=request.GET.get("id")
        object = Listing.objects.get(id=id)
        new_object = Watchlist(item=object, owner=request.user)
        print(object, "already exists in", current_watchlist)
        if not current_watchlist.filter(item=object).exists():
            new_object.save()
            return render(request, "auctions/error.html", {"message": message})
        else:
            message = "The item already exists in your watchlist."
            return render(request, "auctions/error.html", {"message": message})
    except TypeError:
        message = "You have to log in first!"
        return render(request, "auctions/error.html", {"message": message})

def category(request):
    items = Listing.objects.all()
    categories = []
    for item in items:
        if item.category not in categories:
            categories.append(item.category)
    return render(request, "auctions/category.html", {
        "categories": categories,
    })

def categories(request, category):
    items = Listing.objects.all()
    results = []
    for item in items:
        if item.category == category and item.is_active == True:
            results.append(item.title)
            category = item.category
    return render(request, "auctions/categories.html", {
        "results": results, "category": category,
    })
