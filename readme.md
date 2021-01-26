# IRIS Multimodel Suite
This is a set of modules with real world data using Intersystems IRIS Multimodel concepts.

![picture](https://raw.githubusercontent.com/renatobanzai/iris-multimodel-suite/master/img/mkt_coins_graph2.gif)

## Demo
You can see it working at:
[http://iris-multimodel-suite.eastus.cloudapp.azure.com/cryptocoins-market](http://iris-multimodel-suite.eastus.cloudapp.azure.com/cryptocoins-market)

## Crypto Coins Market Graph
The crypto coins market isn't only BTC (Bitcoins), if we take a look at the biggest Crypto Coin Exchange (Binance) we can
 see plenty ways to trade crypto coins. And how IRIS Multimodel Pattern can help us to do it? In this particular case this application
  uses IRIS with 2 datamodels. 1st to ilustrate the link between market crypto coins and altcoins I am using the globals and the value
  stored is a json document like. Using this graph you can click at each symbol to trade using the binance home broker, but
  if you want, you can create your own home broker using all the features of python + Intersystems Iris.

![picture](https://raw.githubusercontent.com/renatobanzai/iris-multimodel-suite/master/img/fish_science.gif)

## Fish Species Database Using Globals
Ingesting data from fishbase we can store all relations between family, genus and species of fish. And by click or text we
can query to see what we want + the fish picture. This is an interactive graph which can make easier the learning path of each specie.
And depending on which data is ingested, is simple to render this graph.

## Multimodel?
Almost market developers used to use one technology for each data model concept. With Intersystems Iris you can do it with
the same systems. In a short time we can storage a graph data structured into Iris Globals, a document and a common SQL model.
On crypto coins markets, I have put each cryptocoin into a global carrying it's name. And if the cryptocoin has any other
cryptocoin which can be traded, you can easily create a link between then with a comma =)

## How to persist data into IRIS Globals?
You can use plenty languages to do it e.g.: ObjectScript, Java, .Net, Python (my case). In this project I get all Binance data
connect an Python application to the Exchange API and ingest all data using Native API in Python is just a matter of preference
by the developer.

![picture](https://raw.githubusercontent.com/renatobanzai/iris-python-covid19/master/img/global_chart.gif)

## Tools

A set of classes in python using the IRIS Native API: 

- irisdomestic: A class that I made to show one way I use the Native API extending the native api.  

```
#has the same methods of irisnative + factory of irisglobal class
```

- irisglobalchart: A component to plot any global as a network graph chart.

- irisglobal: A class that I made to be filled as a Graph Data Structure and all recursive. So if you instatiate one irisglobal
object all global data will be in memory in this object.

Imagine a global like this*

```
^covid19("countries", "us")=5000
^covid19("countries", "us", "newyork")=10
^covid19("countries", "brazil", )=100
```

With my class irisglobal in python you have just to instatiate 
to have access to all global nodes in memory and indexed as a dictionary. 

```
obj_global = irisglobal("^covid19")
print(obj_global.subscripts["countries"].subscripts["brazil"].value)
100
```

## Getting started

### Prerequisites
* git
* docker and docker-compose **adjust docker settings to up memory and cpu the AI demands more capacity**
* access to a terminal in your environment

### Installing
After cloning this repo open a terminal go to the iris-python-covid19 folder and type these commands:

```
git clone https://github.com/renatobanzai/iris-multimodel-suite.git
```

### Running in linux and MacOS
```
docker-compose build

docker-compose up
```

### Estimated time to up containers
1st time running will depend of your internet link to download the images and dependencies. 
If it last more than 15 minutes probably something goes wrong feel free to communicate here.
After the 1st time running the next ones will perform better and take less then 2 minutes.


### If is everything ok
After a while you can open your browser and go to the address:

- Main Menu: [http://localhost:8050](http://localhost:8050)

### Main Menu
The project has a main menu that points you to all the examples. Feel free to navigate.  

- Cryptocoins Market Graph


### You should look at IRIS Admin Portal

I'm using for now the USER namespace (todo: create my onw namespace)

```
http://localhost:52773
user: _SYSTEM
pass: SYS
```

## How does it work?
This is a python application using the IRIS service to persist and read data. I use globals to store raw data from JHU and plot it using Python community libraries. All code in ./app folder.
Here some articles link to understant better the application: 
- [iris-python-suite-hitchhikers-guide-global-1](https://community.intersystems.com/post/iris-python-suite-hitchhikers-guide-global-1)
- [using-python-represent-g[https://openexchange.intersystems.com/contest/current]

## If you enjoyed this application please vote in iris-multimodel-suite!
[https://openexchange.intersystems.com/contest/current])(https://openexchange.intersystems.com/contest/current)