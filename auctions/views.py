from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


from .models import Users, Categories, Listings, Images, Comments, Bids, Winners, Watchlists
from .forms import NewListingForm, ModifyListingForm
import os

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
        image = Images.objects.get(listing_id = listing)

        return render(request, "auctions/listing_view.html", {
            "listing": listing,
            "image": image.image
            })
    except Listings.DoesNotExist:
        return render(request, "auctions/listing_view.html", {
                "message": "Listing not found!"
            })
  
  
@login_required      
def listing_edit(request, listing_id):

    print("here", listing_id)
    
    try:
        old_listing_info = Listings.objects.get(id = listing_id)
        old_image = Images.objects.get(listing_id = old_listing_info)
        print(old_listing_info)
    except Listings.DoesNotExist:
        return render(request, "auctions/listing_view.html", {
                "message": "Listing not found!"
            })   

    if request.method == "POST":
        # print("listing_edit", listing_id)
        print("saving in editing mode", listing_id)

        print(request.POST["new_title"], 
              request.POST["categories"],
              request.POST["new_description"],
              request.POST["price"],
              request.POST["status"],
              "user id", request.user.id)

            
        title = request.POST["new_title"]
        category = Categories.objects.get(category = request.POST["categories"])
        description = request.POST["new_description"]
        price = request.POST["price"]
        status = request.POST["status"]
        user_id = Users.objects.get(id = request.user.id)
        new_image = request.FILES["image"]

        # Attempt to add new listing
        try:
            Listings.objects.filter(id = listing_id).update(
                                                title = title, 
                                                category_id = category, 
                                                description = description, 
                                                listing_price = price,
                                                added_by_user_id = user_id,
                                                status = status)

        except IntegrityError as e:
            return render(request, "auctions/listing_edit.html", {
                "form": ModifyListingForm(initial={'new_title': old_listing_info.title,
                                                    'new_description': old_listing_info.description,
                                                    'price': old_listing_info.listing_price,
                                                    'status': (old_listing_info.status, old_listing_info.status.title()), 
                                                    }),
                "listing_id" : old_listing_info.id,
                "image": old_image.image,
                "message": f"Error while uploading image: {e}",
                })
        
        try:
            img_instance = get_object_or_404(Images, listing_id = old_listing_info)
            old_img_to_delete = img_instance.image.path
            img_instance.image = new_image
            img_instance.save()
            # Images.objects.filter(listing_id = old_listing_info).update(image = request.FILES["image"])
        except IntegrityError as e:
            return render(request, "auctions/listing_edit.html", {
                "form": ModifyListingForm(initial={'new_title': old_listing_info.title,
                                                    'new_description': old_listing_info.description,
                                                    'price': old_listing_info.listing_price,
                                                    'status': (old_listing_info.status, old_listing_info.status.title()), 
                                                    }),
                "listing_id" : old_listing_info.id,
                "image": old_image.image,
                "message": f"Error while uploading image: {e}",
                })
        
        # delete old image
        if os.path.exists(old_img_to_delete):
            os.remove(old_img_to_delete)

        return HttpResponseRedirect(reverse("auctions:listing_view", kwargs={'listing_id': listing_id}))

    else:
        return render(request, "auctions/listing_edit.html", {
        
        "form": ModifyListingForm(initial={'new_title': old_listing_info.title,
                                        'new_description': old_listing_info.description,
                                        'price': old_listing_info.listing_price,
                                        'status': (old_listing_info.status, old_listing_info.status.title()), 
            }),
        "listing_id" : old_listing_info.id,
        "image": old_image.image
        })


@login_required      
def listing_new(request):
    
    if request.method == "POST":

        print("Entering new Listing")
        
        print(request.POST["new_title"], 
              request.POST["new_description"],
              request.POST["price"],
              "user id", request.user.id)
        
        # get listing id

        title = request.POST["new_title"]
        category = Categories.objects.get(category = request.POST["categories"])
        description = request.POST["new_description"]
        price = request.POST["price"]
        # status = request.POST["status"]
        user_id = Users.objects.get(id = request.user.id)
        image = request.FILES["image"]

        # Attempt to add new listing
        try:
            listing = Listings.objects.create(title = title, 
                                              category_id = category, 
                                              description = description, 
                                              listing_price = price,
                                              added_by_user_id = user_id,
                                              status = 'active')
            # dont use .save() with get_or_create()
            # listing.save()
            print("here in try", listing)
        except IntegrityError as e:
            return render(request, "auctions/listing_new.html", {
                "message": f"Listing already exist: {e}"
            })
        
        # get the listing to upload image
        listing_pk = Listings.objects.get(title = title)
        
        try:
            Images.objects.create(listing_id = listing_pk, image = image)
        except IntegrityError as e:
            return render(request, "auctions/listing_new.html", {
                "message": f"Error while uploading image: {e}"
            })


        # return HttpResponseRedirect(reverse("auctions:listing_view", kwargs={'listing_id': listing_id}))
        return HttpResponseRedirect(reverse("auctions:my_listings"))
    
    else:
        return render(request, "auctions/listing_new.html", {
        
        "form_new": NewListingForm(initial={'new_title': "testing title ",
                                        'new_description': "testing description",
                                        'price': 30,
            })
         
        })