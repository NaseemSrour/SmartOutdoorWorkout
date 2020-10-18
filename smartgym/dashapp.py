from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html

from .server import app
from . import router


app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    dcc.Link('Index', href='/'),
    ', ',
    dcc.Link('Figure 1', href='/smartgym/fig1'),
    ', ',
    dcc.Link('Figure 2', href='/smartgym/fig2'),
    html.Br(),
    html.Br(),
    html.Div(id='content')
])
