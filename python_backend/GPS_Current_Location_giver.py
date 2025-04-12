import geocoder

def get_location():
    """Fetch the user's location details using IP address"""
    g = geocoder.ip('me')
    if g.ok:
        location_data = {
            "latitude": g.latlng[0] if g.latlng else None,
            "longitude": g.latlng[1] if g.latlng else None,
            "city": g.city,
            "state": g.state,
            "country": g.country
        }
        return location_data
    else:
        return {"error": "Unable to retrieve location"}
    


