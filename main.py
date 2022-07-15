import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px

def dN(age,ger,dropout,date,date1):
    labels = age.columns[1:]
    for i in labels:
        print(i, 'em',date)
        a = age[i].values
        g = ger[i][ger['year'] == date][ger['State_UT']!='Telangana'].values/100
        drop = dropout[i][dropout['year'] == date][dropout['State_UT']!='Telangana'].values/100
        N = g*(1 - drop)/(1+drop)
        E = g*drop*a
        M0 = ger[i][ger['year'] == date][ger['State_UT']!='Telangana'].values/100*a
        M1 = ger[i][ger['year'] == date1][ger['State_UT']!='Telangana'].values/100*a
        print(np.sum(M1[:-1]-M0[:-1]))
        print(np.sum(E[:-1]))
        label = dropout['State_UT'][dropout['State_UT']!='Telangana'].unique()
        max_ = np.max(E[:-1])
        min_ = np.min(E[:-1])
        #print('A região com maior saldo de Matrículas:',label[indexOf(max_,E[:-1])],format(max_,'.1E'))
        #print('A região com menor saldo de Matrículas:',label[indexOf(min_,E[:-1])],format(min_,'.1E'))
        #print('O saldo de Matrículas da Índia é:',format(E[-1],'.1E'))

def createCSV(age,labels):
    idade = [[6,11,14,16],[11,14,16,18]]
    b = []
    for i,j in zip(idade[0],idade[1]):
        text = ''
        match i:
            case 6:
                text = 'Primary'
            case 11:
                text = 'Upper Primary'
            case 14:
                text = 'Secondary _'
            case 16:
                text = 'HrSecondary_'
        idades = np.arange(i,j+1,1)
        save = age[age['Age-group'].isin(idades)].groupby(['Area Name']).sum()[['Total - Males','Total - Females','Total - Persons']]
        names = ['Total - Males','Total - Females','Total - Persons']
        names2 = ['Males','Females','Total']
        for name,name2 in zip(names,names2):
            save = save.rename(columns={name:text + name2})
        if(i==6):
            b = save
        else:
            b = b.join(save)
        display(b.head())
    b.insert(0, 'States', b.index)
    b = pd.concat([b,b[b['States']=='INDIA']])
    b = b.iloc[1: , :]
    del b['States']
    b.insert(0, 'States', labels)
    df = b.reset_index(drop=True)
    df.to_csv('./data/states.csv', index=True)
    return df

def checkin(lista1,lista2):
    a = []
    for i in lista1:
        if not i in lista2:
            print(i)
            a.append(i)
    print('==============================')
    for i in lista2:
        if not i in lista1:
            print(i)
            a.append(i)

def _(s):
    try:
        return float(s)
    except:
        return -25

def ajeita_mean(data):
    for i in data.columns[2:]:
        if(data[i].values.dtype == 'object'):
            mean = np.array(list(map(_, data[i].values)))
            mean2 = np.mean(mean[mean!=-25])
            data[i] = data[i].replace(data[i][mean==-25].values,mean2)
            data[i] = data[i].astype(float)
    return data

def transform(data):
    data = ajeita_mean(data)
    data['State_UT'] = data['State_UT'].replace(['A & N Islands'],'Andaman & Nicobar Islands')
    data['State_UT'] = data['State_UT'].replace(['Jammu & Kashmir'],'Jammu And Kashmir')
    data['State_UT'] = data['State_UT'].replace(['Arunachal  Pradesh'],'Arunachal Pradesh')
    data['State_UT'] = data['State_UT'].replace(['Madhya  Pradesh'],'Madhya Pradesh')
    data['State_UT'] = data['State_UT'].replace(['Tamil  Nadu'],'Tamil Nadu')
    display(data.head())
    return data

def MultipleBar(data,labels,year,coluna,width = 2.2):
    if("Telangana" in labels):
        labels = np.delete(labels,indexOf("Telangana",labels))
    x = np.array(list(map(lambda a : data[coluna][a == data['State_UT']].values.astype(float), labels ))).T
    b = np.array(list(map(lambda a: a.replace(' ','\n'),labels)))
    X = np.arange(len(labels))
    X = np.arange(0,len(b)*4*width,width)
    repeat = np.tile([1,2,3,0],len(b))
    fig = plt.figure(figsize = [8,6])
    ax = fig.add_axes([0,0,1.5,1.5])
    ax.set_xticks(X[repeat==2], b,c = 'white')
    ax.set_title(coluna, fontsize=12, pad=10,c = 'white')
    
    fig1 = ax.bar(X[repeat==1], x[0], color = 'teal', width = width,label = year[0])
    fig2 = ax.bar(X[repeat==2], x[1], color = 'firebrick', width = width,label = year[1])
    fig3 = ax.bar(X[repeat==3], x[2], color = 'olivedrab', width = width,label = year[2])
    
    ax.legend()
    ax.bar_label(fig1)
    ax.bar_label(fig2)
    ax.bar_label(fig3)
    plt.show()

def generateGraphs(data,column):
    # Primary_Total
    # Upper Primary_Total
    # Secondary _Total
    # HrSecondary_Total
    year = data['year'].unique()
    labels = data['State_UT'].unique()
    for i in range(0,36,6):
        MultipleBar(data,labels[i:i+6],year,column)

def MultipleBarIndia(data,colunas,year,width = 0.2,titulo = ''):
    x = np.array(list(map(lambda a: data[a]['All India' == data['State_UT']].values.astype(float), colunas ))).T
    X = np.arange(0,len(colunas)*4*width,width)
    repeat = np.tile([1,2,3,0],4)
    
    fig = plt.figure(figsize = [8,6])
    ax = fig.add_axes([0,0,1,1])
    ax.set_xticks(X[repeat==2], colunas)
    ax.set_title(titulo, fontsize=12, pad=10)
    
    fig1 = ax.bar(X[repeat==1], x[0], color = 'teal', width = width,label = year[0])
    fig2 = ax.bar(X[repeat==2], x[1], color = 'firebrick', width = width,label = year[1])
    fig3 = ax.bar(X[repeat==3], x[2], color = 'olivedrab', width = width,label = year[2])
    
    ax.legend()
    ax.bar_label(fig1)
    ax.bar_label(fig2)
    ax.bar_label(fig3)
    plt.show()

def generate_graphs_india(data,coluna,titulo):
    year = data['year'].unique()
    labels = data['State_UT'].unique()
    total = data.columns[data.columns.str.contains(coluna)]
    MultipleBarIndia(data,total,year,1.2,titulo)
    #MultipleBarIndia(data,['Primary_Boys','Upper Primary_Boys','Secondary _Boys','HrSecondary_Boys'],year)
    #MultipleBarIndia(data,['Primary_Girls','Upper Primary_Girls','Secondary _Girls','HrSecondary_Girls'],year)

def max_min(vetor,labels,txt):
    maior = np.max(vetor)
    menor = np.min(vetor)
    txt1 = txt.replace("__", "maior")
    txt2 = txt.replace("__", "menor")
    print(txt1,labels[indexOf(maior,vetor)])
    print(txt2,labels[indexOf(menor,vetor)])

def corr(s1,s):
    if((s1 - np.mean(s1) == 0)[0] & (s1 - np.mean(s1) == 0)[1]):
        return 0
    if(len(s1)==2):
        s = s[:2]
    return np.dot((s1-np.mean(s1)),(s-np.mean(s)))/np.sqrt(np.dot((s1-np.mean(s1)),(s1-np.mean(s1)))*np.dot((s-np.mean(s)),(s-np.mean(s))))
def indexOf(element,vetor):
    return np.arange(0,len(vetor))[vetor==element][0]

def correlacao(colunas,data,labels):
    s1 = np.array([1,2,3])
    if("Telangana" in labels):
        labels = np.delete(labels,indexOf("Telangana",labels))
    corr_ = np.zeros(len(labels))
    for coluna in colunas:
        corr_total = np.array(list(map(lambda x:corr(data[coluna][data['State_UT'] == x].values,s1),labels)))
        std = np.array(list(map(lambda x:np.std(data[coluna][data['State_UT'] == x].values),labels)))
        media = np.array(list(map(lambda x:np.mean(data[coluna][data['State_UT'] == x].values),labels)))
        print(coluna)
        #print('A média de correlação é',np.mean(media),'para',coluna)
        #print('Quantidade de Correlação Negativa é:',corr_total[corr_total < -0.5].shape[0])
        #print('Quantidade de Correlação Positiva é:',corr_total[corr_total > 0.5].shape[0])
        #print('Quantidade de Não Correlação é:',corr_total[(corr_total < 0.5) & (corr_total > -0.5)].shape[0])
        corr_total = std*corr_total
        max_min(corr_total,labels,'A região com __ crescimento correlação é')
        corr_ += corr_total
        std = std/media
        a = 0
        b = 1000
        c = 1000
        d = 1000
        for i,j in zip(media,std):
            if((i>a) & (j<b)):
                a = i
                b = j
            if((i<c)):
                c = i
        print('A região com maior Média é',labels[indexOf(a,media)])
        print('A região com menor Média é',labels[indexOf(c,media)], '\n')
        #print('A região com menor correlação é',labels[indexOf(menor,corr_total)])
        #print('\n')
    max_min(corr_,labels,'A região com __ crescimento correlação total é')

def geo_plot(df,data,ano,colunas,cmap):
    geo = df[['NAME_1','geometry']]
    count = 2
    s = 0
    u = [
        [0,0],
        [0,1],
        [1,0],
        [1,1]
    ]
    fig, axs = plt.subplots(2,2, figsize=(15,8))
    for coluna in colunas:
        geo.insert(count, coluna, data[data['year']==ano][coluna].values, True)
        geo.iloc[-6:,count] = data[data['year']==ano][coluna].values[-7:-1]
        a = count - 2
        legenda = False
        if(a==len(colunas)-1):
            legenda = True
        geo.plot(column=coluna, cmap=cmap, linewidth=1, ax=axs[u[a][0],u[a][1]], edgecolor='0.9',legend = True)
        axs[u[a][0],u[a][1]].axis('off')
        axs[u[a][0],u[a][1]].set_title(coluna, fontsize=14)
        count += 1
        s += 1
    plt.title(coluna)
    plt.tight_layout()
    plt.show()

