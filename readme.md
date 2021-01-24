# IRIS Multimodel Suite
This is a set of modules with real world data using Intersystems IRIS Multimodel concepts.


![picture](https://raw.githubusercontent.com/renatobanzai/iris-multimodel-suite/master/img/mkt_coins_graph.gif)

## Crypto Coins Market Graph
The crypto coins market isn't only BTC (Bitcoins), if we take a look at the biggest Crypto Coin Exchange (Binance) we can
 see plenty ways to trade crypto coins. And how IRIS Multimodel Pattern can help us to do it?

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

### Demo
I have deployed the application as a demo here:
[http://iris-python-suite.eastus.cloudapp.azure.com/global-chart](http://iris-python-suite.eastus.cloudapp.azure.com/global-chart)

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

### Building and running the docker-compose
**adjust docker settings to up memory and cpu the AI demands more capacity**
- 4GB Memory (or more if you can)
- 2CPU (or more if you can)

### Need to set more memory to docker engine
![picture](https://raw.githubusercontent.com/renatobanzai/iris-python-covid19/master/img/docker_memory.png)

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
- [using-python-represent-globals-network-chart](https://community.intersystems.com/post/using-python-represent-globals-network-chart)
- [creating-chatbot-iris-and-python](https://community.intersystems.com/post/creating-chatbot-iris-and-python)
- [help-my-chatbots-learn-language](https://community.intersystems.com/post/help-my-chatbots-learn-language)


## If you don't want to run local
I deployed all the application at Azure, take a look at [http://iris-python-suite.eastus.cloudapp.azure.com/](http://iris-python-suite.eastus.cloudapp.azure.com/)
 
