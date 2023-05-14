import pandas as pd
import requests

def get_data():
    response_API = requests.get('https://api.eia.gov/v2/petroleum/pri/gnd/data/?api_key=MEAvGUEmSXOprfaweBUpKhnnEgTfjLolbCOu2ccP&frequency=weekly&data[0]=value&facets[duoarea][]=SNY&facets[duoarea][]=Y05LA&facets[duoarea][]=Y05SF&facets[duoarea][]=Y35NY&facets[duoarea][]=Y44HO&facets[duoarea][]=Y48SE&facets[duoarea][]=YBOS&facets[duoarea][]=YCLE&facets[duoarea][]=YDEN&facets[duoarea][]=YMIA&facets[duoarea][]=YORD&facets[product][]=EPMM&facets[product][]=EPMP&facets[product][]=EPMR&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000')
    
    if(response_API.status_code == 200):
        json = response_API.json()
        df = pd.DataFrame(json['response']['data'])
    else:
        print(response_API.status_code)

get_data()