import folium
import pandas

data = pandas.read_csv("../pythonProjects/volcanomap/Volcanoes.txt")
latitude = list(data["LAT"])
longitude = list(data["LON"])
elevation = list(data["ELEV"])
name = list(data["NAME"])
location = list(data["LOCATION"])
voltype = list(data["TYPE"])

def color_type(elevation):
    if elevation < 1000:
        return 'lightgreen'
    elif elevation < 2000:
        return 'green'
    elif elevation < 3000:
        return 'orange'
    elif elevation < 4000:
        return 'red'
    else:
        return 'darkred'

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Stamen Terrain")

html = """<h3>Volcanic Data</h3>
Name: %s<br>
Location: %s<br>
Type: %s<br>
Elevation: %s m<br>
Latitude: %s<br>
Longitude: %s<br>
Link: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a>"""

fgp = folium.FeatureGroup(name="Population")
fg = folium.FeatureGroup(name="Volcanoes")

fgp.add_child(folium.GeoJson(data=open("../pythonProjects/volcanomap/world.json", 'r', encoding='utf-8-sig').read(), 
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 1000000 else 'orange' if 1000000 <= x['properties']['POP2005'] < 2000000 else 'red'}))
 
for lat, lon, elev, nme, vtype, loc in zip(latitude, longitude, elevation, name, voltype, location):
    iframe = folium.IFrame(html=html % (str(nme), str(loc), str(vtype), str(elev), str(lat), str(lon), nme, nme))
    popup = folium.Popup(iframe, min_width=250, max_width=250)
    fg.add_child(folium.CircleMarker(location=[lat, lon], popup=popup, fill_color=color_type(elev), radius=8, fill_opacity=0.7, color='grey'))

map.add_child(fgp)
map.add_child(fg)
map.add_child(folium.LayerControl())

map.save("../pythonProjects/volcanomap/Map1.html")