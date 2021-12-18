import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import requests
import re

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div(children=[

    #html.Iframe(src="https://www.googletagmanager.com/ns.html?id=GTM-WCXQSN7", height="0", width="0", style={"display":"none", "visibility":"hidden"}),
    html.H1(children='SurfCrowds.ai'),

    html.Img(src='https://raw.githubusercontent.com/daniel-furman/RandomDS/main/firstpoint.jpg', width = "450", height = "300"),

    html.Br(),

    html.H3(children='Forecasting crowd size at First Point, Malibu (@9:00 am)', style={'text-decoration': 'underline'}),

    html.Div([
        html.Label('Minimum Wave Height (Feet)    '),
        dcc.Input(value='2', type='text', id='Minimum Wave Height (ft)'),
    ]),
    html.Div([
        html.Label('Maximum Wave Height (Feet)    '),
        dcc.Input(value='3', type='text', id='Maximum Wave Height (ft)'),
    ]),
    html.Div([
        html.Label('Day of Week (0-6  |  Mon-Sun) '),
        dcc.Input(value='0', type='text', id='Day of Week (0-6 | Mon-Sun)'),
    ]),
    html.P([
        html.Label('Crowd Size Prediction '),
        dcc.Input(value='0', type='text', id='pred')
    ]),
])


@app.callback(
    Output(component_id='pred', component_property='value'),
    [Input(component_id='Minimum Wave Height (ft)', component_property='value'),
     Input(component_id='Maximum Wave Height (ft)', component_property='value'),
     Input(component_id='Day of Week (0-6 | Mon-Sun)', component_property='value')]
)
def update_prediction(mini, maxi, day):

    result = requests.post("", #private api

        json = {"Minimum Wave Height (ft)": mini,
                "Maximum Wave Height (ft)": maxi,
                "Day of Week (0-6 | Mon-Sun)": day,
                "Holiday (0/1 | No/Yes)": '0'})

    split = re.split(r"\s+", result.text)[2]
    test = re.findall(r'\d+', split)

    if int(test[1][0]) >=5:
        test = str(int(test[0])+1)
    else:
        test = test[0]

    return test

if __name__ == '__main__':
    app.run_server(debug=True)
