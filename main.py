import sys
import os
import json
from tkinter import *
from urllib.request import urlopen
from PIL import Image
from PIL import ImageTk

selectedCountryId = 'NL'

useMap = "worldMap.geojson"



def main():
	window = Tk()
	width = 2000
	height = 1200

	window.call('wm', 'iconphoto', window._w, ImageTk.PhotoImage(Image.open('favicon.ico')))

   
	def calculateCords(point):
		return (300 + (point[0] + 190) / 400 * (width  - 300), (90 - point[1]) / 225 * (height - 200) )
	
	countryfile = open("maps/" + useMap, "r").read()
	countrydata = os.listdir("./countryData")


	countries = json.loads(countryfile)



	countrydata = list(map(lambda file:  json.loads( open("./countryData/" + file, "r").read() ) , countrydata))

	countrydata.sort(key=lambda data: data['_index'])



    
	window.title('World map')
	window.geometry(str(width) +'x' + str(height))
	c = Canvas(window, background="white", width=width, height=height)
	countryPols = {}
	
	countyName = c.create_text(width / 2 + 100 , 10,  text="country: %s" % 'NAAM')

	def mouseOverCountry(country):
		def inner(event):

			c.itemconfig(countyName, text="country: %s" % country["properties"]["NAME_ENGL"])
			_id = country["properties"]["CNTR_ID"]  
			if _id is not selectedCountryId:
				for _id in countryPols[_id]:
					c.itemconfig(_id, fill='#ff4747')
		return inner

	def mouseLeaveCountry(country):
		def inner(event):
			_id = country["properties"]["CNTR_ID"] 

			if _id is not selectedCountryId:
				for _id in countryPols[_id]:
					c.itemconfig(_id, fill='pink')
		return inner

	def mouseClickCountry(country):
		def inner(event):
			global selectedCountryId

			__id = country["properties"]["CNTR_ID"] 

			if selectedCountryId:
				for _id in countryPols[selectedCountryId]:
					c.itemconfig(_id, fill='pink')


			selectedCountryId = __id

			renderSelectedCountry(selectedCountryId)
			for _id in countryPols[selectedCountryId]:
				c.itemconfig(_id, fill='red')

		return inner

	def renderCoords(coordinates, country):
		points = []



		for point in coordinates:
			(x, y) = calculateCords(point)
			points.append(x)
			points.append(y)

		color = 'pink'
		_id = country["properties"]["CNTR_ID"]


		pol = c.create_polygon(points, outline='black',fill=color, width=1)
		c.tag_bind(pol, '<Enter>', mouseOverCountry(country))
		c.tag_bind(pol, '<Leave>', mouseLeaveCountry(country))
		c.tag_bind(pol, '<Button-1>', mouseClickCountry(country))


		if not checkKey(countryPols, key=_id):
			countryPols[_id] = []

		countryPols[_id].append(pol)

	for country in countries["features"]:
		for coordinates in country["geometry"]["coordinates"]:

			points = []

			if country["geometry"]["type"] == "Polygon":
				renderCoords(coordinates, country)

			if country["geometry"]["type"] == "MultiPolygon":
				for polygon in coordinates:
					renderCoords(polygon, country)

	img = Image.open('flag_icon/%s.png' % selectedCountryId.lower())
		
	img = img.resize((340,200))

	countrydata[0][selectedCountryId]["urlFlag"] = ImageTk.PhotoImage(img)


	flag = c.create_image(0, 0, image=countrydata[0][selectedCountryId]["urlFlag"], anchor=NW)

	c.create_rectangle(340, 0, width, height- 400, width=4)
	c.create_line(0, 200, 340, 200, width=2)
	
	dataValues = []
	y = 210


	for data in countrydata:
		configObj = {}
		
		for config in data["_config"]:


			try:
				c.create_text(0, y, anchor=NW, text=config["_name"], font='Helvetica 12 bold')
				y += 25
			except Exception as e:
				pass		

			for attr in config:
				if attr[0] != "_":
					value = config[attr]
					configObj[attr] = {"name":  value, "field": c.create_text(0,y, anchor=NW, text=value)}
					y += 20


			c.create_line(0, y, 340, y, width=1)
			y += 10
		
		dataValues.append(configObj)
	
	def renderSelectedCountry (country):
		if not checkKey(countrydata[0][country], "urlFlag"):
			img = Image.open('flag_icon/%s.png' % country.lower())
			img = img.resize((340,200), Image.ANTIALIAS)

			countrydata[0][country]["urlFlag"] = ImageTk.PhotoImage(img)

		idx = 0

		c.itemconfig(flag, image=countrydata[0][country]["urlFlag"] )

		for values in dataValues:
			for attr in values:
				d = dataValues[idx][attr]
				try:
					c.itemconfig(d['field'], state="normal", text=d["name"] % str(countrydata[idx][country][attr]) )
				except Exception as e:
					

					c.itemconfig(d['field'], state="hidden" )

			idx += 1

	
	c.pack()
	window.mainloop()         


def checkKey(dict, key): 
      
    if key in dict.keys(): 
        return True 
    else: 
        return False 

if __name__ == '__main__': 
	print('run main')
	main()
