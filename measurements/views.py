from django.shortcuts import render, get_object_or_404
from .forms import MeasurementModelForm
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim, Photon
from .utils import get_geo
# Create your views here.

def calculateDistanceView(request):
    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Photon(user_agent='measurements')

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data['destination']
        destination = geolocator.geocode(destination_)
        # print(destination)
        printd_lat = destination.latitude
        d_lon = destination.longitude

        instance.location = 'San Francisco'
        instance.distance = 5000.00
        # instance.save()

        
    context = {
        'distance': obj,
        'form': form
    }

    return render(request, 'measurements/main.html', context)
