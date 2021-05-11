import folium
from django.shortcuts import get_object_or_404, render
from geopy.distance import geodesic
from geopy.geocoders import Nominatim, Photon

from .forms import MeasurementModelForm
from .models import Measurement
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address

# Create your views here.

def calculateDistanceView(request):
    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Photon(user_agent='measurements')

    distance = None
    destination = None

    ip = get_ip_address(request)
    print(ip)

    country, city, lat, lon = get_geo(ip)

    location = geolocator.geocode(city)

    # location coordinates
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    # initial folium map
    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8)

    # marker
    folium.Marker([l_lat, l_lon], tooltip='Click here for more', popup=city['city'], icon=folium.Icon(color='purple')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data['destination']
        destination = geolocator.geocode(destination_)

        # destination coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude

        pointB = (d_lat, d_lon)

        distance = round(geodesic(pointA, pointB).km, 2)

        # folium map modification
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon), zoom_start=get_zoom(distance))

        # location marker
        folium.Marker([l_lat, l_lon], tooltip='Click here for more', popup=city['city'], icon=folium.Icon(color='purple')).add_to(m)
        
        # destination marker
        folium.Marker([d_lat, d_lon], tooltip='Click here for more', popup=destination, icon=folium.Icon(color='red', icon='cloud')).add_to(m)

        # draw the line between location and destination
        line = folium.PolyLine(locations=[pointA, pointB], weight=2, color='blue')
        m.add_child(line)


        instance.location = location
        instance.distance = distance
        instance.save()

    m = m._repr_html_()

        
    context = {
        'distance': distance,
        'destination': destination,
        'form': form,
        'map': m
    }

    return render(request, 'measurements/main.html', context)
