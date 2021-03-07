from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr')
temp = [] #initiating a tuple

for i in list(range(1, 12)) + list(range(14, 36)) + list(range (38,130)):
    row = table.find_all('tr') [i]
#insert the scrapping process here
    #get tanggal
    Tanggal = row.find_all('td')[0].text
    Tanggal = Tanggal.strip()
    
    #get usd_idr
    USD_IDR = row.find_all('td')[2].text
    USD_IDR = USD_IDR.replace('IDR','')
    USD_IDR = USD_IDR.replace(',','')
    USD_IDR = USD_IDR.strip()
    
    #scrapping process
    temp.append((Tanggal,USD_IDR))

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns =('Tanggal','USD_IDR'))

#insert data wrangling here
df['USD_IDR'] = df['USD_IDR'].astype('float64')
df['Tanggal'] = df['Tanggal'].astype('datetime64')
df=df.round(2)
df = df.set_index('Tanggal')
period = pd.date_range(start="2020-10-15", end="2021-03-04")
df = df.reindex(period)
df.ffill().plot.line()
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["USD_IDR"].mean().round(2)}'

	# generate plot
	ax = df.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
