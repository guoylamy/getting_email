from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")
location = geolocator.geocode("Salem, Oregon")
add = location.address
country = add.split(' ')[-1]
print(country)