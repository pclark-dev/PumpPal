import pandas as pd
import requests
from datetime import datetime
from scipy.stats import boxcox
from scipy.special import inv_boxcox
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import matplotlib.pyplot as plt
import flask as Flask

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

def duoareaData(dfAll, duoarea):
    area_filtered_df = pd.DataFrame()
    area_filtered_df = dfAll.loc[dfAll['duoarea']==duoarea]
    
    area_filtered_df['ds'] = area_filtered_df['period']
    area_filtered_df['y'] = area_filtered_df['value']
    
    area_filtered_df.set_index('ds')
    
    return area_filtered_df

def gasData(area_filtered_df, gasoline_type):
    gas_filtered_df = pd.DataFrame()
    gas_filtered_df = area_filtered_df.loc[area_filtered_df['product']==gasoline_type]
    
    gas_filtered_df['ds'] = gas_filtered_df['period']
    gas_filtered_df['y'] = gas_filtered_df['value']
    
    gas_filtered_df.set_index('ds')
    
    return gas_filtered_df
    
def prediction_model(dfAll):
    m = Prophet()
    
    m.fit(dfAll)
    
    future = m.make_future_dataframe(periods=52, freq='W')
    forecast = m.predict(future)
   
    #plot_plotly(m, forecast).show()
    return forecast
    
    
def predictArea(gas_filtered_df):
    m = Prophet()
    
    m.fit(gas_filtered_df)
    
    future = m.make_future_dataframe(periods=52, freq='W')
    forecast = m.predict(future)
    
    return forecast
    
    
#main
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

gasoline_types={
    'regular':'EPMR',
    'midgrade':'EPMM',
    'premium':'EPMP'
}

dfAll = get_data()
prepare_data(dfAll)
area_filtered_df = duoareaData(dfAll, duoareas['LA'])
gas_filtered_df = gasData(area_filtered_df, gasoline_types['regular'])
print(predictArea(gas_filtered_df))
