import random
from datetime import date

from django.shortcuts import redirect, render

from .forms import PlaceForm

from .data import DEFAULT_PLACES


def get_places(request):
    if "places" not in request.session:
        request.session["places"] = [
            place.copy() for place in DEFAULT_PLACES
        ]

    return request.session["places"]

def home(request):
    places = get_places(request)
    selected_place = None

    if request.method == "POST" and places:
        selected_place = random.choices(
            places,
            weights=[place["rating"] for place in places],
            k=1,
        )[0]

    return render(
        request,
        "places/home.html",
        {"selected_place": selected_place},
    )

def places_list(request):
    places = get_places(request)

    return render(
        request,
        "places/places_list.html",
        {"places": places},
    )


def place_detail(request, place_id):
    places = get_places(request)

    for place in places:
        if place["id"] == place_id:
            return render(
                request,
                "places/place_detail.html",
                {"place": place},
            )

    return redirect("home")

def add_place(request):
    if request.method == "POST":
        form = PlaceForm(request.POST)

        if form.is_valid():
            places = get_places(request)

            new_id = max(
                [place["id"] for place in places],
                default=0,
            ) + 1

            new_place = {
                "id": new_id,
                "name": form.cleaned_data["name"],
                "description": form.cleaned_data["description"],
                "place_type": form.cleaned_data["place_type"],
                "location": form.cleaned_data["location"],
                "rating": form.cleaned_data["rating"],
                "created_at": date.today().strftime("%d.%m.%Y"),
            }

            places.append(new_place)
            request.session["places"] = places

            return redirect("places_list")
    else:
        form = PlaceForm()

    return render(
        request,
        "places/add_place.html",
        {"form": form},
    )