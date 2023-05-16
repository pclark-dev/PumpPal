import pandas as pd
import requests
from datetime import datetime
from scipy.stats import boxcox
import prophet

#retrieve data from eia API
def get_data():
    response_API = requests.get('https://api.eia.gov/v2/petroleum/pri/gnd/data/?api_key=MEAvGUEmSXOprfaweBUpKhnnEgTfjLolbCOu2ccP&frequency=weekly&data[0]=value&facets[duoarea][]=SNY&facets[duoarea][]=Y05LA&facets[duoarea][]=Y05SF&facets[duoarea][]=Y35NY&facets[duoarea][]=Y44HO&facets[duoarea][]=Y48SE&facets[duoarea][]=YBOS&facets[duoarea][]=YCLE&facets[duoarea][]=YDEN&facets[duoarea][]=YMIA&facets[duoarea][]=YORD&facets[product][]=EPMM&facets[product][]=EPMP&facets[product][]=EPMR&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000') #API request
    
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
    
    #transforms to best approximation of normality
    df['y'], lam = boxcox(df['value']) 
    
    #make index DateTime
    df.set_index('period')
        
def prediction_model(df):
    m = prophet.Prophet()
    
    m.fit(df)
    
    future = m.make_future_dataframe(periods=12, freq='W')
    forecast = m.predict(future)
    m.plot(forecast)
    
#main
df = get_data()
prepare_data(df)
prediction_model(df)

