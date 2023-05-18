import pandas as pd
import requests
from datetime import datetime
from prophet import Prophet
from flask import Flask, render_template, request

#retrieve data from eia API
def get_data():
    response_API = requests.get('https://api.eia.gov/v2/petroleum/pri/gnd/data/?api_key=MEAvGUEmSXOprfaweBUpKhnnEgTfjLolbCOu2ccP&frequency=weekly&data[0]=value&facets[duoarea][]=Y05LA&facets[duoarea][]=Y05SF&facets[duoarea][]=Y35NY&facets[duoarea][]=Y44HO&facets[duoarea][]=Y48SE&facets[duoarea][]=YBOS&facets[duoarea][]=YCLE&facets[duoarea][]=YDEN&facets[duoarea][]=YMIA&facets[duoarea][]=YORD&facets[product][]=EPMM&facets[product][]=EPMP&facets[product][]=EPMR&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000') #API request
    
    #validate response code
    if(response_API.status_code == 200):    #valid response
        json = response_API.json()  #json file for data
        df = pd.DataFrame(json['response']['data']) #create dataframe using pandas from json data
        return df   #return dataframe
    else:   #error retrieving data
        print(response_API.status_code)

#prepare date (string) for Prophet training (datetime)
def prepare_data(df):
    #iterate through dataframe
    for i in df.index: 
        date_str = df.loc[i, 'period']  #get date string from dataframe
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()   #create new date object from date string
        df.loc[i, 'period'] = date_obj  #update period with converted date object
    
    #create clone of date and price
    df['ds'] = df['period']
    df['y'] = df['value']
    
    #make index DateTime
    df.set_index('ds')
    
    return df

#prepare data using main dataframe and specified area
def duoareaData(dfAll, duoarea):
    #create new dataframe filtering the area data
    area_filtered_df = pd.DataFrame()
    area_filtered_df = dfAll.loc[dfAll['duoarea']==duoarea] 
    
    #create new columns for prophet fitting
    area_filtered_df['ds'] = area_filtered_df['period']
    area_filtered_df['y'] = area_filtered_df['value']
    
    #make index DateTime
    area_filtered_df.set_index('ds')
    
    #return the new filtered dataframe
    return area_filtered_df

#prepare completely filtered data with area filtered dataframe and the specified gasoline type
def gasData(area_filtered_df, gasoline_type):
    #create new dataframe filtering the specified gas type
    gas_filtered_df = pd.DataFrame()
    gas_filtered_df = area_filtered_df.loc[area_filtered_df['product']==gasoline_type]
    
    #create new columns for prophet fitting
    gas_filtered_df['ds'] = gas_filtered_df['period']
    gas_filtered_df['y'] = gas_filtered_df['value']
    
    #set index to DateTime
    gas_filtered_df.set_index('ds')
    
    #return final filtered dataframe
    return gas_filtered_df
    
#predicts overall gas prices using every gas type in every area
def prediction_model(dfAll):
    #instantiate new prophet model
    m = Prophet()
    
    #fit data to model
    m.fit(dfAll)
    
    #predict data
    future = m.make_future_dataframe(periods=52, freq='W') #a year worth of predictions in one week intervals
    forecast = m.predict(future) #create forecast
   
    #uncomment below to plot data 
    #plot_plotly(m, forecast).show()
    
    #return prediction
    return forecast
    
#prediction model for area given the filtered dataframe based on gas type
def predictArea(gas_filtered_df):
    #instantiate new prophet model
    m = Prophet()
    
    #fit prophet model with final filtered data
    m.fit(gas_filtered_df)
    
    #create prediction
    future = m.make_future_dataframe(periods=52, freq='W')  #year predictions in week intervals
    forecast = m.predict(future)    #create forecast
    
    #return final forecast for area
    return forecast
    
    
#main
#dictionary of area and duoarea codes
duoareas = {
    'LA':'Y05LA', 
    'NY':'Y35NY',
    'SE':'Y48SE',
    'CLE':'YCLE',
    'MIA':'YMIA',
    'SF':'Y05SF',
    'HO':'Y44HO',
    'BOS':'YBOS',
    'DEN':'YDEN',
    'ORD':'YORD',
    }

#dictionary of gas types and codes
gasoline_types={
    'regular':'EPMR',
    'midgrade':'EPMM',
    'premium':'EPMP'
}

dfAll = get_data()
prepare_data(dfAll)
#area_filtered_df = duoareaData(dfAll, duoareas['LA'])
#gas_filtered_df = gasData(area_filtered_df, gasoline_types['regular'])
#print(predictArea(gas_filtered_df))

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = []
    city = ''
    gas = ''
    current_price = 0
    if request.method == 'POST':
        city = request.form.get('city')
        gas = request.form.get('gas')
        area_filtered_df = duoareaData(dfAll, duoareas[city])
        gas_filtered_df = gasData(area_filtered_df, gasoline_types[gas])
        forecast = predictArea(gas_filtered_df)
        current_price = round(forecast.iloc[-1]['yhat'], 2)  # Get the most recent predicted price and round it
        # Convert the forecast dataframe to a list of dictionaries
        prediction = forecast[['ds', 'yhat']].to_dict('records')
        for p in prediction:  # Round all the predictions and convert dates to string format
            p['yhat'] = round(p['yhat'], 2)
            p['ds'] = p['ds'].strftime('%Y-%m-%d')  # Convert to string and format to only show date
            
    return render_template('index.html', prediction=prediction, city=city, gas=gas, current_price=current_price)




 
if __name__=='__main__':
    app.run(debug = True, host="0.0.0.0", port=5000)