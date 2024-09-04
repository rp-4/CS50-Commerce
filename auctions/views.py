from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required


from .models import Users, Categories, Listings, Images, Comments, Bids, Winners, Watchlists
from .forms import NewListingForm, ModifyListingForm

def index(request):
    # if Users.is_authenticated:
        
    all_listings = Listings.objects.filter(status = "active")

    for l in all_listings:
        print(l.id, l.category_id, l.title, l.added_by_user_id)
    return render(request, "auctions/index.html", {
        "listings" : all_listings
        })
    # else:
    #     #return HttpResponseRedirect(reverse("index"))
    #     return render(request, "auctions/index.html")

# @csrf_exempt
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

        # Attempt to create new user
        try:
            user = Users.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def my_listings(request):
    # if Users.is_authenticated:
        
    all_listings = Listings.objects.filter(added_by_user_id = request.user.id)

    for l in all_listings:
        print(l.id, l.category_id, l.title, l.added_by_user_id)
    
    return render(request, "auctions/my_listings.html", {
        "listings" : all_listings
        })



# @login_required
def listing_view(request, listing_id):
    
    # if Users.is_authenticated:
    print(listing_id)

    try:
        listing = Listings.objects.get(id = listing_id)
        return render(request, "auctions/listing_view.html", {
            "listing": listing
            })
    except Listings.DoesNotExist:
        return render(request, "auctions/listing_view.html", {
                "message": "Listing not found!"
            })
  
  
@login_required      
def listing_edit(request, listing_id):
    print("here", listing_id)
    
    # get all categories
    categories = Categories.objects.all()

    try:
        old_listing_info = Listings.objects.get(id = listing_id)
        print(old_listing_info)
    except Listings.DoesNotExist:
        return render(request, "auctions/listing_view.html", {
                "message": "Listing not found!"
            })   

    if request.method == "POST":
        # print("listing_edit", listing_id)
        print("saving in editing mode", listing_id)

        print(request.POST["title"], 
              request.POST["category"],
              request.POST["description"],
              request.POST["price"],
              request.POST["status"],
              "user id", request.user.id)

        return HttpResponseRedirect(reverse("auctions:listing_view", kwargs={'listing_id': listing_id}))

        
    # return HttpResponseRedirect(reverse(listing_view))
    # return render(request, "auctions/listing_edit.html", {
    #     "listing" : old_listing_info,
    #     "categories": categories,
    # })
    else:
        return render(request, "auctions/listing_edit.html", {
        
        "form": ModifyListingForm(initial={'new_title': old_listing_info.title,
                                        'new_description': old_listing_info.description,
                                        'price': old_listing_info.listing_price,
                                        'status': (old_listing_info.status, old_listing_info.status.title()), 
            }),
        "listing_id" : old_listing_info.id,
        })


@login_required      
def listing_new(request):
    
    # get all categories
    categories = Categories.objects.all()

    if request.method == "POST":
        # print("listing_edit", listing_id)
        print("Entering new Listing")
        # print(request.POST["new_title"], 
        #       request.POST["category"],
        #       request.POST["new_description"],
        #       request.POST["price"],
        #       request.POST["status"],
        #       "user id", request.user.id)
        
        print(request.POST["new_title"], 
              request.POST["new_description"],
              request.POST["price"],
              "user id", request.user.id)
        
        # get listing id

        # title = request.POST["title"]
        # category = Categories.objects.get(id = request.POST["category"])
        # description = request.POST["description"]
        # price = request.POST["price"]
        # status = request.POST["status"]
        # user_id = Users.objects.get(id = request.user.id)

  
        # # Attempt to add new listing
        # try:
        #     listing = Listings.objects.get_or_create(title = title, 
        #                                       category_id = category, 
        #                                       description = description, 
        #                                       listing_price = price,
        #                                       added_by_user_id = user_id,
        #                                       status = status)[0]
        #     listing.save()
        # except IntegrityError as e:
        #     return render(request, "auctions/listing_new.html", {
        #         "message": f"Listing already exist: {e}"
        #     })

        # return HttpResponseRedirect(reverse("auctions:listing_view", kwargs={'listing_id': listing_id}))
        return HttpResponseRedirect(reverse("auctions:my_listings"))
    
    else:
        return render(request, "auctions/listing_new.html", {
        
        "form": NewListingForm(initial={'new_title': "testing title",
                                        'new_description': "testing description",
                                        'price': 30,
            })
        })