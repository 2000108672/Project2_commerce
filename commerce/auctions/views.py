from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def listing(request, id):
    # Get listing data by id
    listingData = Listing.objects.get(pk=id)

    # Check if the user has added this listing to their watchlist
    isListingInWatchlist = request.user in listingData.watchlist.all()

    # Get all comments for this listing
    allComments = Comment.objects.filter(listing=listingData)

    # Check if the user is the owner of this listing
    isOwner = request.user.username == listingData.owner.username

    # Render the listing.html template with the necessary data
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner
    })


def closeAuction(request, id):
    # Get the listing data by id
    listingData = Listing.objects.get(pk=id)

    # Set the listing as inactive
    listingData.isActive = False

    # Save the listing data
    listingData.save()

    # Check if the user has added this listing to their watchlist
    isListingInWatchlist = request.user in listingData.watchlist.all()

    # Get all comments for this listing
    allComments = Comment.objects.filter(listing=listingData)

    # Check if the user is the owner of this listing
    isOwner = request.user.username == listingData.owner.username

    # Render the listing.html template with the necessary data, as well as a success message
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "Congratulations! Your auction has been closed successfully"
    })


def addBid(request, id):
    # Get the new bid amount from the form data
    newBid = request.POST['newBid']

    # Get the listing data by id
    listingData = Listing.objects.get(pk=id)

    # Check if the user has added this listing to their watchlist
    isListingInWatchlist = request.user in listingData.watchlist.all()

    # Get all comments for this listing
    allComments = Comment.objects.filter(listing=listingData)

    # Check if the user is the owner of this listing
    isOwner = request.user.username == listingData.owner.username

    # Check if the new bid is greater than the current bid
    if int(newBid) > listingData.price.bid:
        # Create a new bid with the user and new bid amount
        updateBid = Bid(user=request.user, bid=int(newBid))

        # Save the new bid
        updateBid.save()

        # Set the new bid as the price for this listing
        listingData.price = updateBid

        # Save the listing data
        listingData.save()

        # Render the listing.html template with the necessary data, as well as a success message
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid was updated successfully",
            "update": True,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,
        })
    else:
        # Render the listing.html template with the necessary data, as well as an error message
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid updated Failed",
            "update": False,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,

        })


# View for adding a comment to a listing
def addComment(request, id):
    # Get the current user and the listing from the URL parameter
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)

    # Get the comment message from the form data
    message = request.POST['newComment']

    # Create a new Comment object with the current user, listing, and message
    newComment = Comment(
        author=currentUser,
        listing=listingData,
        message=message
    )

    # Save the new comment to the database
    newComment.save()

    # Redirect back to the listing page
    return HttpResponseRedirect(reverse("listing", args=(id, )))

# View for displaying the user's watchlist
def watchlist(request):
    # Get the current user's watchlist of listings
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()

    # Render the watchlist template with the user's watchlist of listings
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

# View for removing a listing from the user's watchlist
def removeWatchlist(request, id):
    # Get the listing from the URL parameter and the current user
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user

    # Remove the listing from the user's watchlist
    listingData.watchlist.remove(currentUser)

    # Redirect back to the listing page
    return HttpResponseRedirect(reverse("listing", args=(id, )))

# View for adding a listing to the user's watchlist
def addWatchlist(request, id):
    # Get the listing from the URL parameter and the current user
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user

    # Add the listing to the user's watchlist
    listingData.watchlist.add(currentUser)

    # Redirect back to the listing page
    return HttpResponseRedirect(reverse("listing", args=(id, )))

# View for displaying all active listings or filtered by category
def index(request):
    # Get all active listings and all categories
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()

    # Render the index template with the active listings and all categories
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": allCategories,
    })

# View for displaying active listings filtered by category
def displayCategory(request):
    if request.method == "POST":
        # Get the selected category from the form data
        categoryFromForm = request.POST['category']

        # Get the category object with the selected name
        category = Category.objects.get(categoryName=categoryFromForm)

        # Get all active listings with the selected category
        activeListings = Listing.objects.filter(isActive=True, category=category)

        # Get all categories
        allCategories = Category.objects.all()

        # Render the index template with the active listings and all categories
        return render(request, "auctions/index.html", {
            "listings": activeListings,
            "categories": allCategories,
        })


def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        # Get data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        # Who is the user
        currentUser = request.user
        # Get all content about the category
        categoryData = Category.objects.get(categoryName=category)
        # create a bid object
        bid = Bid(bid=int(price), user=currentUser)
        bid.save()
        # Create a new lsiting object
        newListing = Listing(
            title=title, 
            description=description, 
            imageUrl=imageurl,
            price=bid,
            category=categoryData,
            owner=currentUser
        )
        # Insert the object in our database
        newListing.save()
        # Redirect to the newly created listing's page
        return HttpResponseRedirect(reverse("listing", args=(newListing.id,)))


def login_view(request):
    if request.method == "POST":
        # Authenticate user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {"message": "Invalid username and/or password."})
    else:
        # Show login page
        return render(request, "auctions/login.html")


def logout_view(request):
    # Log out user
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        # Get user details from registration form
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Check if password matches confirmation
        if password != confirmation:
            return render(request, "auctions/register.html", {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {"message": "Username already taken."})

        # Log in newly created user
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        # Show registration page
        return render(request, "auctions/register.html")
