import numpy as np
from auto_trading_aim.portfolio import Portfolio

class PortfolioBuilder(object):
    def __init__(self,capital, data, min_invest):
        self.capital=capital
        self.keys_in_order=list(data._dict_.keys()) #necessario per evitare di ciclare su chiavi diverse con ordini diversi
        self.data=data
        self.min_invest=min_invest
        self.mkt_return=[]
        for asset in self.keys_in_order:
            self.mkt_return.append(self.data._dict_[asset].mkt_return)
        self.mkt_return=np.array(self.mkt_return)
        self.V=np.cov(self.mkt_return) #Matrice varianze-covarianze dei rendimenti dove le colonne si riferiscono ai titoli nell'ordine dato da self.keys_in_order
        self.portfolio_dim=self.V.shape[0]
    
    def min_var(self):
        'Poichè il capitale totale investito incide quadraticamente sulla varianza del portafoglio, si vuole investire il minimo capitale possibile'
        inv_V=np.linalg.inv(self.V)
        one=np.ones(self.portfolio_dim)
        w_mvp=np.matmul(one.T,inv_V)
        den=np.matmul(w_mvp,one)
        w_mvp=w_mvp/den #Sono i pesi(che sommano a 1) di capitale da investire in ognuno dei 10 asset presenti in data loader dict
        allocation=dict(zip(self.keys_in_order,w_mvp))
        prices_dict={}
        for key in self.keys_in_order:
            allocation[key]=int(np.around(self.capital*self.min_invest*allocation[key]/self.data._dict_[key].prices[-1])) #Si compra al prezzo dell'ultimo giorno dell'anno 
            prices_dict[key]=self.data._dict_[key].prices
        prova=np.matmul(w_mvp.T,self.V)
        return Portfolio(allocation,prices_dict)
    
    def rate_mean_std(self):
        'Essendo dato dal rapporto tra mean e std, la composizione del portafoglio non risente dell\'ammontare del capitale investito'
        n_iter=40000
        e=np.array([])
        for key in self.keys_in_order:
            mean=np.mean(self.data._dict_[key].mkt_return)
            e=np.append(e,mean) #Si costruisce np.array dei rendimenti medi ordinati secondo l'ordine fissato delle chiavi
        best_w=np.array([])
        max_ratio=-1
        np.random.seed(2)
        for i in range(n_iter):
            random_w=np.random.random(self.portfolio_dim)*2-1 #traslazione per creare pesi tra -1 ed 1. Il modo in cui genero nasce da una ipotesi
            random_w=random_w/(np.sum(random_w)) #Normalizzando la somma è pari ad uno
            mean=np.matmul(random_w.T,e) #Rendimento atteso di portafoglio con peso w
            std=np.matmul(random_w.T,self.V)
            std=np.sqrt(np.matmul(std,random_w))
            ratio=mean/std
            if ratio>max_ratio:
                max_ratio=ratio
                best_w=random_w
        allocation={}
        prices_dict={}
        i=0
        for key in self.keys_in_order:
            allocation[key]=int(self.capital*best_w[i]/self.data._dict_[key].prices[-1])#Si compra al prezzo dell'ultimo giorno dell'anno 
            prices_dict[key]=self.data._dict_[key].prices
            i+=1
        print('Best ratio = {}'.format(max_ratio))
        print('''\nIl massimo ratio teorico ottenibile dovrebbe essere contenuto, dati i rendimenti a disposizione, in I=[0.18 ; 0.21] per via degli errori di
        approssimazione dovuti dal calcolo. Si ottengono,a seconda del seed, valori in tale intervallo. Si è notato che l'uso di
        del metodo DataFrame.cov() anzichè np.cov() genera perturbazioni dela valore minori''')
        return Portfolio(allocation,prices_dict)
            

        


       



