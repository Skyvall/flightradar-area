import folium
from folium.plugins import BoatMarker
from typing import List, Tuple

def create_map_from_coordinates(coordinates: List[Tuple[float, float]], center: Tuple[float, float] = (0, 0)):
    """
    Create a map from a list of coordinates.
    
    Args:
        coordinates: List of tuples containing (latitude, longitude)
        center: Tuple containing (latitude, longitude) of the center of the map
    
    Returns:
        A folium map object
    """
    map_center = center
    map = folium.Map(location=map_center, zoom_start=13)
    
    for coord in coordinates:
        folium.Marker(location=coord).add_to(map)
    
    return map

def generuj_mapke(srodek: Tuple[float, float], punkty: List[Tuple[float, float, str, str, str, int]], plik_wyj: str = "mapa.html"):
    mapa = folium.Map(location=srodek, zoom_start=9)
    folium.Marker(location=srodek, popup="Twoja lokalizacja", icon=folium.Icon(color="blue")).add_to(mapa)
    for lat, lon, lot, z, dokad, track in punkty:
        popup_text = f"Lot: {lot}<br>Z: {z}<br>Do: {dokad}"
        BoatMarker(
            location=(lat, lon),
            heading=track if track is not None else 0,
            color="red",
            popup=popup_text,
            icon_scale=1.2
        ).add_to(mapa)
    mapa.save(plik_wyj)

