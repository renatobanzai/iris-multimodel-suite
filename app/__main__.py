import json
import requests
from flask import Flask, render_template, request
from iris_python_suite import irisdomestic
import yaml
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import networkx as nx
import dash_bootstrap_components as dbc
import csv
from plotly.callbacks import Points, InputDeviceState


# todo: demonstrate a profile of different aproachs in code
try:
    with open("../data/config.yaml", "r") as file:
        config = yaml.safe_load(file)
except Exception as e:
    print('Error reading the config file')

# dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Class with IRIS Persistence
obj_irisdomestic = irisdomestic(config["iris"])

def ingest_binance_markets():
    # getting binance market data
    print("ingest_binance_markets")
    exchange_name="binance"
    binance_info_request = requests.get("https://www.binance.com/api/v3/exchangeInfo")
    binance_info_json = binance_info_request.json()
    binance_symbols = binance_info_json["symbols"]

    # persisting data to iris globals
    for symbol in binance_symbols:
        # print(symbol)
        obj_irisdomestic.set(symbol["symbol"], exchange_name, symbol["quoteAsset"], symbol["baseAsset"])

def ingest_fishbase():
    print("ingest_fishbase")

    dic_family = {}

    with open('../data/fishbase_family.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            dic_family[row[0]] = row[1]

    offset = 0
    limit = 3500

    for i in range(10):
        fishbase_request = requests.get("https://fishbase.ropensci.org/species?limit="+str(limit)+"&offset="+str(offset)+"")
        fishbase_json = fishbase_request.json()
        for spec in fishbase_json["data"]:
            obj_irisdomestic.set(json.dumps({"text":spec["Genus"] + " " +spec["Species"],"image":spec["image"]}),
                                 "fish", dic_family[str(spec["FamCode"])], spec["Genus"], spec["Species"])

        offset+=limit

# index page
def get_index_layout():
    navbar = dbc.NavbarSimple(id="list_menu_content",
                              children=[
                                  dbc.NavItem(dbc.NavLink("CryptoCoin Markets", href="/cryptocoins-market")),
                                  dbc.NavItem(dbc.NavLink("Vote in iris-multimodel-suite!",
                                                          href="https://openexchange.intersystems.com/contest/current",
                                                          target="_blank"))
                              ],
                              brand="IRIS Multimodel Suite - by Banzai",
                              brand_href="/",
                              color="dark",
                              dark=True,
                              )
    return html.Div([
                # html.H1(children='IRIS Multimodel Suite'),
                dcc.Location(id='url', refresh=False),
                html.Div(navbar),
                html.Div(id='page-content')
                ])
                # represents the URL bar, doesn't render anything

# grap view page
def get_criptocoins_market():
    return html.Div(children=[
        html.Div([
            html.Br(),
            html.Label('View BINANCE Market Graph: '),
            dcc.Input(
                id="txt_cryptocoin_market",
                type="text",
                placeholder="^binance, BTC",
                value="^binance, BTC"
            )]
        ),
        html.Div(
            dcc.Graph(id="cryptocoin-market-graph")
        )
    ])

# grap view page
def get_science_fish():
    return html.Div(children=[
        html.Div([
            html.Br(),
            html.Label('View fish species database Graph: '),
            dcc.Input(
                id="txt_science_fish",
                type="text",
                placeholder="^fish",
                value="^fish",
                size="100"
            )]
        ),
        html.Div(
            dcc.Graph(id="science-fish-graph")
        ),
        html.Div([
            html.Label(id="hover-text",
                       style={'float': 'left'}),
            html.Img(id='hover-img',
                     style={'float': 'left', 'max-width':'280px'})
        ])
    ])


# populating the chart graph
@app.callback(Output('cryptocoin-market-graph', 'figure'),
              [Input('txt_cryptocoin_market', 'value')])
def update_cryptocoin_graph(global_text):
    global_array = tuple([x.strip() for x in global_text.split(",")])
    obj_nx = nx.Graph()
    global_chart = obj_irisdomestic.view_global_chart(obj_nx=obj_nx, *global_array, max_depth=1)
    fig = global_chart.get_fig()
    return fig

@app.callback(Output('txt_science_fish', 'value'),[Input('science-fish-graph', 'clickData')])
def onclick_fish(clickData):
    print("aaaaa")
    print(clickData)
    if not clickData["points"][0]["customdata"]["is_leaf"]:
        return clickData["points"][0]["customdata"]["node"]

@app.callback(Output('txt_cryptocoin_market', 'value'),[Input('cryptocoin-market-graph', 'clickData')])
def onclick_crypto(clickData):
    print("aaaaa")
    print(clickData)
    return clickData["points"][0]["customdata"]["node"]

@app.callback(Output('hover-text', 'children'), Output('hover-img', 'src'),[Input('science-fish-graph', 'hoverData')])
def onhover_fish(clickData):
    res = json.loads(clickData["points"][0]["customdata"]["value"])
    if res["image"]==None:
        image = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png"
    else:
        image = res["image"]

    return res["text"], image

@app.callback(Output('science-fish-graph', 'figure'),
              [Input('txt_science_fish', 'value')])
def update_science_fish_graph(global_text):
    global_array = tuple([x.strip() for x in global_text.split(",")])
    obj_nx = nx.Graph()
    global_chart = obj_irisdomestic.view_global_chart(obj_nx=obj_nx, *global_array, max_depth=2)
    fig = global_chart.get_fig()
    return fig

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'), [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname, suppress_callback_exceptions=False):
    print(pathname)
    if pathname == '/cryptocoins-market':
        return get_criptocoins_market()
    if pathname == '/science-fish':
        return get_science_fish()


if __name__ == '__main__':

    # ingest_binance_markets()
    # ingest_fishbase()
    navbar = dbc.NavbarSimple(id="list_menu_content",
                              children=[
                                  dbc.NavItem(dbc.NavLink("CryptoCoin Markets", href="/cryptocoins-market")),
                                  dbc.NavItem(dbc.NavLink("Science Fish", href="/science-fish")),
                                  dbc.NavItem(dbc.NavLink("Vote in iris-multimodel-suite!",
                                                          href="https://openexchange.intersystems.com/contest/current",
                                                          target="_blank"))
                              ],
                              brand="IRIS Multimodel Suite - by Banzai",
                              brand_href="/",
                              color="dark",
                              dark=True,
                              )
    app.layout = html.Div([
        # html.H1(children='IRIS Multimodel Suite'),
        dcc.Location(id='url', refresh=False),
        html.Div(navbar),
        html.Div(id='page-content')
    ])
    # represents the URL bar, doesn't render anything
    app.run_server(debug=True,host='0.0.0.0')