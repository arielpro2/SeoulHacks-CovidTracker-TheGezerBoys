import folium
from folium import GeoJson
from folium.features import GeoJsonPopup
import branca.colormap as cm
import json
import codecs
from tkinter import *
from tkinter import filedialog 
from pathlib import Path

#Colors needed for styling layers
colors = [
'#00ff00',
'#12ed00',
'#24db00',
'#39c600',
'#55aa00',
'#718e00',
'#8e7100',
'#aa5500',
'#c63900',
'#e31c00',
'#ff0000'
]

funcs = []

filename = ''

#Handling the data file
with codecs.open("data.json",'r','utf-8') as json_file:
    cases = json.load(json_file)

#Handling the coordinates file
with codecs.open('coords.json','r','utf-8') as handle:
    country_geo = json.loads(handle.read())    

#creating GUI window
app = Tk()


    
inDate = ''
input = Entry(app)


def setDate():
    global inDate
    inDate = input.get()
    app.quit()
#create app widgets

date = Button(app,text= "enter date",command=setDate)

#add
date.pack()
input.pack()

#start GUI
app.mainloop()

#Getting the [population,precentage]
def getCaseByDate(state, date):
    try: 
        State = cases[state]
    except:
        return None
    stateData = State["data"]
    try:
        out = [x for x in stateData if "date" in x and x["date"] == date][0]["total_cases"]
        return out,out/State["population"]*100
    except:
        return None

#Returns the function needed to style the layers
def makeStyleFunc(value):
  return lambda feature:{'fillColor':getColor(value),'weight' : 1,'fillOpacity' : 0.5}

#Retrieving a color out of 10 colors relative to the precentage value
def getColor(value):
    if value == None:
        return 'black'
    if (value > 4.5):
        return colors[10]
    return colors[round((value/4.5)*10)]




#Creating a map
map = folium.Map(location = [0,0],zoom_start=0,min_zoom=3,control_scale=True,max_bounds=True,tiles='Stamen Terrain')
map.fit_bounds(bounds=[[58.6191,101.4863],[62.3604,126.6429]])

#Building the layers for the map
for i in country_geo['features']:

    name = i['properties']['ADM0_A3'] #Getting the name of the country currently handled

    value = getCaseByDate(name,inDate) #Getting the precentage (Covid-19 cases relative to population)
    if(value == None):
        continue 
    
    #Creating a new function for styling the layer
    funcs.append(makeStyleFunc(value[1]))

    #Building the layer with the precentage and styling
    i['properties']['precentage'] = value[1]
    i['properties']['Number Of Cases'] = value[0]
    layer = folium.GeoJson(i,name=i['properties']['NAME_LONG'],style_function=funcs[len(funcs)-1], popup = GeoJsonPopup(["Number Of Cases","precentage"])).add_to(map)
    
#Adding a map legend
legendcolormap = cm.LinearColormap(colors=colors, vmin=0, vmax=4.5,caption='Precentage of cases relative to population')
legendcolormap.add_to(map)

#Building the html file
map.save("{}.html".format(inDate))
print("Map page successfully created")