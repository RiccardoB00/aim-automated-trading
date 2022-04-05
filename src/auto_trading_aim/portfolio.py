import pandas as pd
import matplotlib.pyplot as plt
from auto_trading_aim.asset import Asset

class Portfolio(object):

    def __init__(self, allocation, prices_dict):
        self._dict_={}
        for key,value in prices_dict.items():
            self._dict_[key]=Asset(key,value,allocation[key])
    
    def __repr__(self):
        msg={}
        for key,value in self._dict_.items():
            msg[key]='{} #{} | mu: {} | sigma_squared: {}'.format(value.ticker_name,value.volume_owned,value.mean,value.sigma_squared)
        return str(msg) +'\n'

    def __add__(self,other):
        new_allocation={}
        new_prices={}
        tickers_set=set(list(self._dict_.keys())+list(other._dict_.keys()))
        self_keys=self._dict_.keys()
        other_keys=other._dict_.keys()
        for ticker in tickers_set:
            if ticker in self_keys and ticker in other_keys:
                new_allocation[ticker]=self._dict_[ticker].volume_owned + other._dict_[ticker].volume_owned
                new_prices[ticker]= self._dict_[ticker].prices
            elif ticker in other_keys:
                new_allocation[ticker]=other._dict_[ticker].volume_owned
                new_prices[ticker]=other._dict_[ticker].prices
            else:
                new_allocation[ticker]=self._dict_[ticker].volume_owned 
                new_prices[ticker]= self._dict_[ticker].prices
        return Portfolio(new_allocation,new_prices)
        
    def __getitem__(self,index):
        return self._dict_[index]
    
    def __setitem__(self,index,new_value):
        self._dict_[index]=new_value
    
    def to_df(self,):
        temp_dict={}
        for key,value in self._dict_.items():
            temp_dict[key]=value.volume_owned
        return pd.DataFrame(temp_dict, index =['Volume owned'])
   
    def total_value(self):
        flag=True
        for value in self._dict_.values():
            if flag:
                total_portfolio_value=value.total_asset_value()
                flag=False
            else:
                total_portfolio_value+=value.total_asset_value() #Somma di oggetti di tipo series
        return total_portfolio_value
    
    def hist(self):
        total_value=self.total_value()
        rend=total_value.pct_change(1)
        rend=rend[rend.notna()]  #Si calcolano,pulendo il series dai valori NaN, i rendimenti sul valore totale
        plt.hist(rend,bins=30,rwidth=0.9)
        plt.grid()
        plt.title('Total returns of portfolio')
        plt.ylabel('#Days')
        plt.show()
    
    def plot(self):
        plt.plot(self.total_value())
        plt.title('History of portfolio_value')
        plt.grid()
        plt.show()
    
