from auto_trading_aim.data_loader import DataLoader
from auto_trading_aim.portfolio import Portfolio

class DataLoaderDict(object):
    
    def __init__(self,tickers, start, end, interval):
        self._dict_={}
        for ticker in tickers:
            self._dict_[ticker]=DataLoader(ticker,start,end,interval) #creo un oggetto di tipo dizionario contenente i titoli
    
    def __getitem__ (self,index):
        return self._dict_[index]

    def save(self, path):
        f=open(path,'w')
        for tk in self._dict_.values():
            print(tk.ticker_name,file=f)
            print(tk.ticker.to_string(header=True,index=True),file=f)
            print('',file=f)
        f.close()
    
    def build_portfolio(self,allocation):
        my_ticket=self._dict_.keys()
        prices_dict={}
        #Inizializzo gli input per costruire il portfolio
        for ticker_name in allocation.keys():
            if ticker_name not in my_ticket:
                raise NameError('Il ticker selezionato non appartiene all\'oggetto')
            prices_dict[ticker_name]=self._dict_[ticker_name].prices
        return Portfolio(allocation,prices_dict)
        
            



    

    

    
    