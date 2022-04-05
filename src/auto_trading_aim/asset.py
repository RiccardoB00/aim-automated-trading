import numpy as np
import matplotlib.pyplot as plt
import auto_trading_aim.portfolio as ptf

class Asset(object):

    def __init__(self, ticker_name, prices, volume_owned):
        self.ticker_name=ticker_name
        self.prices=prices
        mkt_return=self.prices.pct_change(1)
        self.mkt_return=mkt_return[mkt_return.notna()]
        self.volume_owned=volume_owned
        self.mean=self.mkt_return.mean()
        self.sigma_squared=self.mkt_return.std()**2
    
    def __repr__ (self):
        return '{} #{} | mu: {} | sigma_squared: {}'.format(self.ticker_name,self.volume_owned,self.mean,self.sigma_squared) +'\n'
    
    def __truediv__(self,fattore):
        new_volume_owned=self.volume_owned//fattore
        return Asset(self.ticker_name,self.prices,new_volume_owned)
    
    def __add__(self,asset2):
        'Sommando due asset si genera un nuovo portafolgio avente come assets la somma dei due'
        allocation={}
        prices_dict={}
        if self.ticker_name==asset2.ticker_name: # Si sommano semplicemente il numero di titoli detenuti aventi lo stesso nome, misurati rispetto allo stesso periodo
            volume_owned=self.volume_owned + asset2.volume_owned
            allocation[self.ticker_name]=volume_owned
            prices_dict[self.ticker_name]=self.prices
            return ptf.Portfolio(allocation,prices_dict)
        else:
            allocation={self.ticker_name:self.volume_owned, asset2.ticker_name:asset2.volume_owned}
            prices_dict={self.ticker_name:self.prices, asset2.ticker_name:asset2.prices}
            return ptf.Portfolio(allocation,prices_dict)
    
    def hist(self):
        plt.hist(self.mkt_return,bins=30,rwidth=0.9)
        plt.title ('Returns of {}'.format(self.ticker_name))
        plt.grid()
        plt.xlabel('Returns')
        plt.ylabel('#Days')
        plt.show()
    
    def total_asset_value(self):
        return self.prices*self.volume_owned
        
        
    