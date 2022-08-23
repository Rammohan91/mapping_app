from textwrap import fill
from turtle import fillcolor
import folium
import pandas

data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def colorproducer(elev):
    if elev < 1000:
        return 'green'
    elif elev >= 1000 and elev < 2000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[38.58, -99.09],zoom_start=6, tiles="Stamen Terrain")
fg1 = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el,name in zip(lat, lon, elev,name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    #fg.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color=colorproducer(el))))
    fg1.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe), radius = 6, 
    fill_color=colorproducer(el), fill_opacity = 0.7, fill=True, color = 'grey'))

fg2 = folium.FeatureGroup(name="Population")
fg2.add_child(folium.GeoJson(data=(open("world.json",'r', encoding='utf-8-sig').read()),
style_function=lambda x: {'fillColor':'yellow' if x['properties']['POP2005']<10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 200000000 else 'red'}))

map.add_child(fg1)
map.add_child(fg2)
map.add_child(folium.LayerControl())
map.save("Map1.html")