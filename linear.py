__author__ = 'ASUS'
#coding:utf8
import sys
import matplotlib.pyplot as plt
import numpy  as np
import pandas as pd



def ToData():
    path="Data.txt"
    data=pd.read_csv(path,header=None,names=['x','y'])
    return data

def costfun(X,y,Theta):
    inner=np.power(((X*Theta.T)-y),2)
    return np.sum(inner)/(2*len(X))

def data_taking(data):


    data.insert(0,'Ones',1)

    cols=data.shape[1]
    X=data.iloc[:,0:cols-1]
    y=data.iloc[:,cols-1:cols]

    X=np.matrix(X.values)
    y=np.matrix(y.values)
    Theta=np.matrix(np.zeros(X.shape[1]))
    return X,y,Theta

# print (costfun(X,y,theta))

def gradientDescent(X,y,Theta,alpha,iters):
    temp=np.matrix(np.zeros(Theta.shape))
    parameters=int(Theta.ravel().shape[1])
    cost=np.zeros(iters)

    for i in range(iters):
        error=(X*Theta.T)-y

        for j in range(parameters):
            term=np.multiply(error,X[:,j])
            temp[0,j]=Theta[0,j]-((alpha/len(X))*np.sum(term))

        Theta=temp
        cost[i]=costfun(X,y,Theta)
    return Theta,cost

def Draw_close_line():
    alpha=0.01
    N=1000#迭代次数
    data=ToData()
    X,y,Theta=data_taking(data)
    g,cost=gradientDescent(X,y,Theta,alpha,N)
    # print (g)
    # print (cost)

    x=np.linspace(data.x.min(),data.x.max(),100)
    f=g[0,0]+(g[0,1]*x)

    fig,ax=plt.subplots(figsize=(12,8))
    ax.plot(x,f,'r',label='拟合曲线')
    ax.scatter(data.x,data.y,label='散点图')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('单变量线性回归')



