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
import visdcc
from plotly.callbacks import Points, InputDeviceState
import jaydebeapi

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

def get_fishfamily():
    jdbc_server = "jdbc:IRIS://"+ config["iris"]["host"] +":"+ str(config["iris"]["port"]) + "/" + config["iris"]["namespace"]
    jdbc_driver = 'com.intersystems.jdbc.IRISDriver'
    iris_jdbc_jar = "./intersystems-jdbc-3.1.0.jar"
    iris_user = config["iris"]["username"]
    iris_password = config["iris"]["password"]

    conn = jaydebeapi.connect(jdbc_driver, jdbc_server, [iris_user, iris_password], iris_jdbc_jar)
    curs = conn.cursor()
    curs.execute("SELECT family_id, family_name FROM fish.family")

    total_cache = curs.fetchall()

    result = {}
    for row in total_cache:
        result[str(row[0])] = row[1]
    return result

def ingest_fishbase():
    print("ingest_fishbase")
    dic_family = get_fishfamily()

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
                placeholder="^binance",
                value="^binance"
            )]
        ),
        html.Div(
            dcc.Graph(id="cryptocoin-market-graph")
        ),
        visdcc.Run_js(id="javascript")
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
            html.Div(id='div-img',
                     style={'float': 'left', 'max-width':'280px'})
        ])
    ])


# populating the chart graph
@app.callback(Output('cryptocoin-market-graph', 'figure'),
              [Input('txt_cryptocoin_market', 'value')],
              prevent_initial_call=True)
def update_cryptocoin_graph(global_text):
    global_array = tuple([x.strip() for x in global_text.split(",")])
    obj_nx = nx.Graph()
    global_chart = obj_irisdomestic.view_global_chart(obj_nx=obj_nx, *global_array, max_depth=1)
    fig = global_chart.get_fig()
    return fig

@app.callback(Output('txt_science_fish', 'value'),[Input('science-fish-graph', 'clickData')],
              prevent_initial_call=True)
def onclick_fish(clickData):
    print("aaaaa")
    print(clickData)
    if clickData:
        if not clickData["points"][0]["customdata"]["is_leaf"] or not clickData["points"][0]["customdata"]["value"]:
            return clickData["points"][0]["customdata"]["node"]

@app.callback(Output('txt_cryptocoin_market', 'value'),Output('javascript', 'run'),[Input('cryptocoin-market-graph', 'clickData'), Input("txt_cryptocoin_market", "value")],
              prevent_initial_call=True)
def onclick_crypto(clickData, txt_val):
    print("aaaaa")
    print(clickData)
    js = ""
    txt = txt_val
    if clickData:
        if clickData["points"][0]["customdata"]["value"]:
            js = "window.open('https://www.binance.com/en/trade/"+ clickData["points"][0]["customdata"]["value"] +"')"
            txt = txt_val
        else:
            txt = clickData["points"][0]["customdata"]["node"]

    return txt, js

@app.callback(Output('hover-text', 'children'), Output('div-img', 'children'),[Input('science-fish-graph', 'hoverData')],
              prevent_initial_call=True)
def onhover_fish(clickData):
    txt = ""
    image = ""
    if clickData and clickData["points"][0]["customdata"]["value"]:
        res = json.loads(clickData["points"][0]["customdata"]["value"])
        txt = res["text"]
        if res["image"]==None:
            image = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png"
        else:
            image = res["image"]

        image = image.replace(".de", ".us")

    img = html.Img(
        id="img_"+txt,
        src=image,
        style={'float': 'left', 'max-width': '280px'}
    )
    return txt, img

@app.callback(Output('science-fish-graph', 'figure'),
              [Input('txt_science_fish', 'value')],
              prevent_initial_call=True)
def update_science_fish_graph(global_text):
    global_array = tuple([x.strip() for x in global_text.split(",")])
    obj_nx = nx.Graph()
    depth = 1
    if len(global_array) > 1:
        depth = 2
    global_chart = obj_irisdomestic.view_global_chart(obj_nx=obj_nx, *global_array, max_depth=depth)
    fig = global_chart.get_fig()
    return fig

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'), [dash.dependencies.Input('url', 'pathname')],
              prevent_initial_call=True)
def display_page(pathname, suppress_callback_exceptions=False):
    print(pathname)
    if pathname == '/cryptocoins-market':
        return get_criptocoins_market()
    if pathname == '/science-fish':
        return get_science_fish()
    if pathname == '/full_ingestion':
        ingest_binance_markets()
        ingest_fishbase()
        return get_science_fish()


if __name__ == '__main__':
    ingest_binance_markets()
    ingest_fishbase()
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
    app.run_server(debug=False,host='0.0.0.0')