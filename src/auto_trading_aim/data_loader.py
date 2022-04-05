import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

class DataLoader(object):

    def __init__(self,ticker,start,end,interval):
        self.ticker_name=ticker
        self.start=start
        self.end=end 
        self.interval=interval
        yftk = yf.Ticker(ticker)
        self.ticker=yftk.history(start=start,end=end,interval=interval).loc[:,['Close','Volume']]# Oggetto di tipo dataframe
        self.prices=self.ticker.loc[:,'Close'] #Dataframe
        self.volume=self.ticker.loc[:,'Volume'] #Dataframe
        self.mkt_return=self.prices.pct_change(1)
        self.mkt_return=self.mkt_return[self.mkt_return.notna()]
    
    
    def __repr__(self):
        return '{} data from {} to {},{}\n\
Close -> min:{} max: {} mean:{}\n\
 first day:{} last day:{}\n\
Volume -> min:{} max:{} mean:{}\n\
 first day: {} last day:{} \n'.format(self.ticker_name,self.start,self.end,self.interval,self.prices.min(),self.prices.max(),self.prices.mean(),self.prices[0],self.prices[-1],self.volume.min(),self.volume.max(),self.volume.mean(),self.volume[0],self.volume[-1])
        
    def plot(self,data):
        if data == 'Prices':
            data='Close'
        elif data == 'Volumes':
            data='Volume'
        else:
            raise NameError('Il dato richiesto non è riconosciuto')
        self.ticker.plot(y=data, use_index=True)
        plt.title('{} of {}'.format(data,self.ticker_name))
        plt.grid()
        plt.show()



    
    

