from flask import Flask, render_template, request
import os
import re
import time
import folium
from folium.plugins import Fullscreen
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/",methods = ['POST','GET'])
def get_well():
	global location, company, info
	location=''
	company=''
	info=''
	if request.method == 'POST' and 'well' in request.form:
		url_offer = request.form.get('well')
		#options to remove chrome errors
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--no-sandbox")
		chrome_options.binary_location = "/usr/bin/firefox"
		driver = webdriver.Firefox(executable_path="./driver/geckodriver")

		#connect to the website
		driver.get(url_offer)

		#link = driver.find_element_by_link_text(wells)
		#link.click()

		well = WebDriverWait(driver,5).until(
				EC.presence_of_all_elements_located(((By.CSS_SELECTOR,'#applyCol'))))
			
		company = driver.find_element_by_css_selector('.icl-u-lg-mr--sm > a:nth-child(1)')

		location = WebDriverWait(driver,5).until(
				EC.presence_of_all_elements_located(((By.CSS_SELECTOR, '.jobsearch-JobInfoHeader-subtitle > div:nth-child(2)'))))
		
		informations = WebDriverWait(driver,5).until(
                EC.presence_of_all_elements_located(((By.CSS_SELECTOR, '#jobDescriptionText > div:nth-child(2) > div:nth-child(2) > p:nth-child(1)'))))
		
		for (a, b, c, d) in zip(well, company, location, informations):
				name = {'company name': b.text}
				location = {'location': c.text}
				info = {'Summary': d.text}
		

	return render_template("home.html", location = location, name = name, info = info)
"""
@app.route('/map')

def well_map():
	map_NM = folium.Map([61.222303, 3.440436],
			   zoom_start=7,
			   tiles='cartodbdark_matter',
			   control_scale=True)

	label = name['Well']
	label = folium.Popup(label)
	
	folium.CircleMarker([coord['Lat'], coord['Long']],
	radius=5,
	popup=label,
	color='#ffb732',
	fill=True,
	fill_color='#FFD27F',
	fs = Fullscreen(),
	fill_opacity=0.7).add_to(map_NM) 

	return map_NM._repr_html_()
"""
if __name__ == "__main__":
	app.run(debug=True)