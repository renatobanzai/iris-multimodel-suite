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


# getting binance market data
exchange_name="binance"
binance_info_request = requests.get("https://www.binance.com/api/v3/exchangeInfo")
binance_info_json = binance_info_request.json()
binance_symbols = binance_info_json["symbols"]

# persisting data to iris globals
for symbol in binance_symbols:
    print(symbol)
    obj_irisdomestic.set(json.dumps(symbol),"symbols", exchange_name, symbol["quoteAsset"], symbol["baseAsset"])


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
                placeholder="^symbols, binance",
                value="^symbols, binance"
            )]
        ),
        html.Div(
            dcc.Graph(id="cryptocoin-market-graph")
        )
    ])

# populating the chart graph
@app.callback(Output('cryptocoin-market-graph', 'figure'),
              [Input('txt_cryptocoin_market', 'value')])
def update_cryptocoin_graph(global_text):
    global_array = tuple([x.strip() for x in global_text.split(",")])
    obj_nx = nx.Graph()
    global_chart = obj_irisdomestic.view_global_chart(obj_nx=obj_nx, *global_array)
    fig = global_chart.get_fig()
    return fig

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'), [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname, suppress_callback_exceptions=False):
    print(pathname)
    if pathname == '/cryptocoins-market':
        return get_criptocoins_market()
    else:
        return get_index_layout()


if __name__ == '__main__':
    app.layout = get_index_layout()
    app.run_server(debug=True,host='0.0.0.0')