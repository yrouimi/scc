import matrix_opers as mopers
from plotly.subplots import make_subplots
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import time
import random
import pandas as pd
import dash_daq as daq
import textwrap

#Set the seed for the charts
i_chartseed = 12345
random.seed(i_chartseed) # Set a fixed seed value

#import plotly_charts as chartlib
#https://plotly.com/python/custom-buttons/


##########################
#########TODO############
##########################
# Working map
# Place components
# Scenario tool

# Tabs
#Styling of charts https://towardsdatascience.com/a-clean-style-for-plotly-charts-250ba2f5f015 
# Major producers, importers, exporters
# Market share analysis - electronic/computer products for cars, defense etc. By stage of supply (share of each country in the supply of tier3 electronic products)
#GHG breakdown - See picture of 20 april 2023


##########################
#########Charting#########
##########################

import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.title = "Supply Chain Companion (SCC)"
app._favicon = "icon_cropped2.ico"

SIDEBAR_STYLE = {"position": "fixed","top": 0,"left": 0,"bottom": 0,"width": "16rem","padding": "2rem 1rem","background-color": "#f8f9fa","overflow-y": "auto"}

# The styles for the main content position it to the right of the sidebar and add some padding.
CONTENT_STYLE = {"margin-left": "18rem","margin-right": "2rem","padding": "2rem 1rem"}

Visos = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][0],True);Vsecs = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][1],False)

Disooptions = [{'label':Siso,'value':Siso} for Siso in Visos];Dsecoptions = [{'label':Ssec,'value':Ssec} for Ssec in Vsecs]

Dvaroptions = [{'label':'Output','value':'Output'},{'label':'Employment','value':'Employment'},{'label':'Value added','value':'Value added'},{'label':'Co2 emissions','value':'Co2 emissions'}]

sidebar2 = html.Div(
    [
        html.H2("Understand your supply chain", className="sidebar-heading text-center"),
        html.Hr(),
        html.P(
            "Your industry of operation", className="lead text-center"
        ),
        dbc.Nav(
            [html.H6("Segment",style={'text-align': 'center'}),
            dcc.Dropdown(id='Ssecref_t1',options=Dsecoptions,value=Vsecs[0],placeholder="Select a sector",clearable=True,style={'width': '100%','text-align': 'center'}),
            html.Br(),
            html.H6("Geography",style={'text-align': 'center'}),
            dcc.Dropdown(id='Sisoref_t1',options=Disooptions,value=Visos[0],placeholder="Select a country",clearable=True,style={'width': '100%','text-align': 'center'}),
            html.Br(),
            html.H6("Your turnover ($mln)",style={'text-align': 'center'}),
            dcc.Input(id="Sturnover_t1", type="text", value='100',placeholder='100', debounce=True,style={'width': '100%','text-align': 'center'})
            ],
            className="justify-content-center",
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.P("Jump to sections", className="lead text-center"),
        html.A("Global requirements to reach target output", href='#graph_t1_totreq',style={'display': 'block', 'text-align': 'center'}),
        html.Br(),
        html.A("Country/region position in value chain and transactions with RoW", href='#graph_t1_countrytransactions',style={'display': 'block', 'text-align': 'center'}),
        html.Br(),
        html.A("Interventions at every stage of production", href='#graph_t1_countrytransactions4',style={'display': 'block', 'text-align': 'center'}),
        html.Br(),
        html.A("Co2 efficiency comparisons", href='#graph_t1_countrytransactions4',style={'display': 'block', 'text-align': 'center'}),
    ],
    style=SIDEBAR_STYLE,
)

roundbutton = {"border": 0,"border-radius": "50%","padding": 0,"backgroundColor": "white","color": "black","textAlign": "center","display": "block","fontSize": 15+2,"height": 30,"width": 30,"margin": 15,"align-items": "center","justify-content": "center"}

#style={'display': 'flex', 'justify-content': 'center'}
Vrevbuttons = [html.Button("⇅", style=roundbutton, id='lvl' + str(i) + '-' +str(i+1) + '_reversebutton') for i in range(2,6)]
Vdownbuttons = [html.Button("↓", style={**roundbutton,**{"fontSize":26,"display": "flex","border": 0}})]

Vbuttons = [dbc.Button('Global requirements',color='success'),dbc.Button('Continent',id='lvl2_layer',color='light'),dbc.Button('Region',id='lvl3_layer',color='light'),
            dbc.Button('Broad segment',id='lvl4_layer',color='success'),dbc.Button('Segment',id='lvl5_layer',color='light'),dbc.Button('Supplier tier',id='lvl6_layer',color='success')]

button_div = dbc.Card([
    dbc.CardHeader("Treemap slicing - Add/remove layers and change order", style={'width': '100%', 'text-align': 'center'}),
    dbc.CardBody([
        html.Label('Concept', style={'text-align': 'center', 'text-decoration': 'underline'}),
        html.Hr(),
        dcc.Dropdown(id='Svarref_t1', options=Dvaroptions, value='Output', placeholder="Select a metric", clearable=True, style={'width': '100%'}),
        html.Hr(),
        html.Label('Layer order', style={'text-align': 'center', 'text-decoration': 'underline'}),
        html.Hr(),
        # Example of wrapping each button for centering, repeated for all buttons in your arrays
        html.Div(Vbuttons[1], style={'text-align': 'center'}),
        html.Div(Vrevbuttons[0], style={'display': 'flex', 'justify-content': 'center'}),
        html.Div(Vbuttons[2], style={'text-align': 'center'}),
        html.Div(Vrevbuttons[1], style={'display': 'flex', 'justify-content': 'center'}),
        html.Div(Vbuttons[3], style={'text-align': 'center'}),
        html.Div(Vrevbuttons[2], style={'display': 'flex', 'justify-content': 'center'}),
        html.Div(Vbuttons[4], style={'text-align': 'center'}),
        html.Div(Vrevbuttons[3], style={'display': 'flex', 'justify-content': 'center'}),
        html.Div(Vbuttons[5], style={'text-align': 'center'}),
        # Add more buttons as needed, wrapped in html.Div with text-align: center
    ], style={"overflow": "auto", 'display': 'flex', 'flex-direction': 'column'}),
], style={"height": "450px", "display": "flex", "flex-direction": "column"})

button_div2 = dbc.Card([
    dbc.CardHeader("Detail on region's potion in value chain", style={'width': '100%', 'text-align': 'center'}),
    dbc.CardBody([
        html.Label('Concept', style={'text-align': 'center', 'text-decoration': 'underline'}),
        html.Hr(),
        dcc.Dropdown(id='Svarref_t1b', options=Dvaroptions, value='Output', placeholder="Select a metric", clearable=True, style={'width': '100%'}),
        html.Hr(),
        html.Label('Which region?', style={'text-align': 'center', 'text-decoration': 'underline'}),
        html.Hr(),
        dcc.Dropdown(id='Sisodep_t1',options=Disooptions,value=Visos[1],placeholder="Select a country",clearable=True,style={'width': '100%'}),
        html.Hr(),
        html.Label('# Industries to display', style={'text-align': 'center', 'text-decoration': 'underline'}),
        html.Hr(),
        dcc.Input(id='nsecs_t1', type='text', placeholder='nsecs',value='4'),
        html.Hr(),
        daq.BooleanSwitch(id='Bresid_sankey_t1',on=False, labelPosition="top",label="Balance other cat in Sankey",vertical=False),
    ], style={"overflow": "auto", 'display': 'flex', 'flex-direction': 'column'}),
], style={"height": "450px", "display": "flex", "flex-direction": "column"})

button_div3 = dbc.Card([
    dbc.CardHeader("Detail on stage requirements", style={'width': '100%', 'text-align': 'center'}),
    dbc.CardBody([
        html.Label('Concept', style={'text-align': 'center', 'text-decoration': 'underline'}),
        html.Hr(),
        dcc.Dropdown(id='Svarref_t1c', options=Dvaroptions, value='Output', placeholder="Select a metric", clearable=True, style={'width': '100%'}),
        html.Hr(),
        html.Label('Chart 1 - Position of which region?', style={'text-align': 'center', 'text-decoration': 'underline'}),
        html.Hr(),
        dcc.Dropdown(id='Sisodep_t1b',options=Disooptions,value=Visos[1],placeholder="Select a country",clearable=True,style={'width': '100%'}),
        html.Hr(),
        html.Label('How many stages?', style={'text-align': 'center', 'text-decoration': 'underline'}),
        html.Hr(),
        dcc.Input(id='nstages', type='text', placeholder='nstages',value='6'),
        html.Hr(),
        html.Label('Click on element of second chart to get country detail of who intervenes at a given stage in a given industry', style={'text-align': 'center', 'text-decoration': 'underline'}),
        ], style={"overflow": "auto", 'display': 'flex', 'flex-direction': 'column'}),
], style={"height": "450px", "display": "flex", "flex-direction": "column"})

Dcharts = {'Chart totreqs':dcc.Loading(id="loading-chart",type="default",children=[dcc.Graph(id='graph_t1_totreq',style={'height': '500px'})],fullscreen=False),
           'Treemap':dcc.Loading(id="loading-chart",type="default",children=[dcc.Graph(id='graph_t1_dirindir',style={'height': '100%'})],fullscreen=False),
           'Sankey1':dcc.Loading(id="loading-chart",type="default",children=[dcc.Graph(id='graph_t1_sankey',style={'height': '100%'})],fullscreen=False),
           'Sankey2':dcc.Loading(id="loading-chart",type="default",children=[dcc.Graph(id='graph_t1_countrytransactions',style={'height': '100%'})],fullscreen=False),
           'Trade chart':dcc.Loading(id="loading-chart",type="default",children=[dcc.Graph(id='graph_t1_countrytransactions2',style={'height': '100%'})],fullscreen=False),
           'Trade chart2':dcc.Loading(id="loading-chart",type="default",children=[dcc.Graph(id='graph_t1_countrytransactions3',style={'height': '100%'})],fullscreen=False),
           'Trade chart3':dcc.Loading(id="loading-chart",type="default",children=[dcc.Graph(id='graph_t1_countrytransactions4',style={'height': '100%'})],fullscreen=False),
           'Stage1':dcc.Loading(id="loading-chart",type="default",children=[dcc.Graph(id='graph_t1_suppliertier1',style={'height': '100%'})],fullscreen=False),
           'Stage2':dcc.Loading(id="loading-chart",type="default",children=[dcc.Graph(id='graph_t1_suppliertier2',style={'height': '100%'})],fullscreen=False),
           'Emissions':dcc.Loading(id="loading-chart",type="default",children=[dcc.Graph(id='graph_t1_co2emissions',style={'height': '100%'})],fullscreen=False)
           }
       

#dcc.Loading(id="loading1",type="default",children=html.Div(id="graph_t1_totreq"))
content2 = html.Div([dcc.Store(id='t1_treemap_data'),dcc.Store(id='t1_treemap_actlayers'),dcc.Store(id='t1_memstages',data={'Clickdata':None,'Restyledata':None,'Xaxis labels':[],'Legend labels':[],'Selection':[]}),
                    dbc.Row(Dcharts['Chart totreqs']),
                    dbc.Row([dbc.Col(button_div,align='center',width=2),dbc.Col(Dcharts['Treemap'],width=5),dbc.Col(Dcharts['Sankey1'],width=5)],style={"height": "450px"}),
                    html.Hr(),
                    dbc.Row([dbc.Col(button_div2,align='center',width=2),dbc.Col(Dcharts['Sankey2'],width=10)],style={"height": "450px"}),
                    dbc.Row([dbc.Col(Dcharts['Trade chart'],width = 6),dbc.Col(Dcharts['Trade chart2'],width = 6)]),
                    html.Hr(),
                    dbc.Row([dbc.Col(button_div3,align='center',width=2),dbc.Col(Dcharts['Trade chart3'],width = 3),dbc.Col(Dcharts['Stage1'],width = 4),dbc.Col(Dcharts['Stage2'],width = 3)]),
                    dbc.Row([dbc.Col(Dcharts['Emissions'],width = 12)])
                    ],style={'margin-left': '15%'}
                    )


tab1 = html.Div([html.Button('Coming up...')])

tab2 = html.Div(
    [
        sidebar2,
        content2
    ]
)

tabs = dcc.Tabs(
    [
        dcc.Tab(tab2, label="Explore your supply chain"),
        dcc.Tab(tab1, label="Economic impact analysis and scenario")
        #dcc.Tab(tab2, label="Economic impact analysis and scenario")
    ]
)

app.layout = html.Div(children=[tabs])

@app.callback(Output("loading-output-1", "children"), Input("loading-input-1", "value"))
def input_triggers_spinner(value):
    return value


@app.callback(Output('t1_treemap_data', 'data'), 
              Input('Sisoref_t1', 'value'),Input('Ssecref_t1', 'value'),Input('Sturnover_t1', 'value'))
def fn_update_storeddata(Sisoref,Ssecref,Sturnover):

     # some expensive data processing step
     Vmat = mopers.fn_calc_intermediatereqs_stal(Sisoref,Ssecref,'Output',Sturnover) #No Svarref, will need to convert as per each function

     return Vmat

@app.callback(Output('t1_treemap_actlayers', 'data'), Input('lvl2_layer', 'n_clicks'),Input('lvl3_layer', 'n_clicks'),Input('lvl4_layer', 'n_clicks'),Input('lvl5_layer', 'n_clicks'),Input('lvl6_layer', 'n_clicks'),
                Input('lvl2-3_reversebutton', 'n_clicks'),Input('lvl3-4_reversebutton', 'n_clicks'),Input('lvl4-5_reversebutton', 'n_clicks'),Input('lvl5-6_reversebutton', 'n_clicks'),
                State('lvl2_layer', 'color'),State('lvl3_layer', 'color'),State('lvl4_layer', 'color'),State('lvl5_layer', 'color'),State('lvl6_layer', 'color'))
def fn_actdeact_layers(click2,click3,click4,click5,click6,click23,click34,click45,click56,lvl2_color,lvl3_color,lvl4_color,lvl5_color,lvl6_color):

    ctx = dash.callback_context
    firedcomp_id = ctx.triggered[0]['prop_id'].split('.')[0]

    Dcurrentcolors= {'lvl2_layer':lvl2_color, 'lvl3_layer':lvl3_color,'lvl4_layer':lvl4_color,'lvl5_layer':lvl5_color,'lvl6_layer':lvl6_color}
    Vreversebuttonids = ['lvl2-3_reversebutton','lvl3-4_reversebutton','lvl4-5_reversebutton','lvl5-6_reversebutton']
    color_tupple = (lvl2_color, lvl3_color,lvl4_color,lvl5_color,lvl6_color)
 
    if firedcomp_id in Vreversebuttonids:
        
        # if firedcomp_id == 'lvl2-3_reversebutton':
            # color_tupple = (lvl3_color, lvl2_color,lvl4_color,lvl5_color,lvl6_color)
        # if firedcomp_id == 'lvl3-4_reversebutton':
            # color_tupple=(lvl2_color, lvl4_color,lvl3_color,lvl5_color,lvl6_color)
        # if firedcomp_id == 'lvl4-5_reversebutton':
            # color_tupple =  (lvl2_color, lvl3_color,lvl5_color,lvl4_color,lvl6_color)
        # if firedcomp_id == 'lvl5-6_reversebutton':
            # color_tupple =  (lvl2_color, lvl3_color,lvl4_color,lvl6_color,lvl5_color)
        
        return color_tupple
 
    elif firedcomp_id != '':

        Sfiredcolor = Dcurrentcolors[firedcomp_id]

        #Is the fired button active or not? 
        Scolor = 'light' if Sfiredcolor=='success' else 'success'
        Dcurrentcolors[firedcomp_id] =  Scolor

        res_tupple = (Dcurrentcolors['lvl2_layer'],Dcurrentcolors['lvl3_layer'],Dcurrentcolors['lvl4_layer'],Dcurrentcolors['lvl5_layer'],Dcurrentcolors['lvl6_layer'])
      
        return res_tupple
        
    else:
        
        res_tupple = (Dcurrentcolors['lvl2_layer'],Dcurrentcolors['lvl3_layer'],Dcurrentcolors['lvl4_layer'],Dcurrentcolors['lvl5_layer'],Dcurrentcolors['lvl6_layer'])

        return res_tupple

@app.callback(Output('graph_t1_totreq', 'figure'),
              Input('t1_treemap_data', 'data'),State('Sisoref_t1', 'value'),State('Ssecref_t1', 'value'),State('Sturnover_t1', 'value'))
def update_figure(Vireqs,Sisoref,Ssecref,Sturnover):  #Reliance of Ssecref_Sisoref towards the industries of Sisodep in terms of supply

    Vcons = ['Output','Value added','Employment','Co2 emissions']
    Vsecs = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][1],False)
    Visos = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][0],True)
    Vgroups = mopers.Dstructuralarrays['Slicing_vecs']
    
    fig = make_subplots(rows=1, cols=4,subplot_titles = ('Output ($mln)','Value added ($mln)','Employment (thous. jobs)','Co2 emissions (mmt)'),horizontal_spacing = 0.05,vertical_spacing = 0.15)
    Dpos = {1:[1,1],2:[1,2],3:[1,3],4:[1,4]}
    
    Vireqs = np.array(Vireqs).sum(axis=1)
    
    for i, Svarref in enumerate(Vcons):
        
        Vres = mopers.fn_convert_prodmat(Vireqs,Svarref)
        
        Vy = []
        
        for Ssec in Vsecs:
        
            Vy2 = []
        
            for Siso in Visos:
            
                #res = mopers.fn_calcconditional_sum(Vres,Vgroups,Vgroups,[Ssec,Siso],[]) 
                res = mopers.fn_calcconditional_sum([Vres],[["xxx"]],Vgroups,[["xxx"]],[Ssec,Siso]) #Valid for simple vector

                Vy2.append(res)        
            
            fig.add_trace(go.Bar(y=Vy2,x=[val.replace(" ", "<br>") for val in Visos],legendgroup=Ssec,showlegend=(i == 0),name=Ssec,marker_color=mopers.fn_generate_hexcolor(Ssec)),row=Dpos[i+1][0],col=Dpos[i+1][1])
    
    fig.update_traces(width=0.33)        
    Stitle = 'Intermediate requirements by industry/geography for ' + Ssecref + ' industry in ' + Sisoref + ' to reach desired turnover'
    fig.update_layout(barmode='relative',title=Stitle) #legend=dict(orientation="h",yanchor="bottom",y=-0.15,xanchor="center",x=0.5)

    fig.update_xaxes(tickangle=0)
    
    return fig    

@app.callback(Output('lvl2_layer', 'children'),Output('lvl3_layer', 'children'),Output('lvl4_layer', 'children'),Output('lvl5_layer', 'children'),Output('lvl6_layer', 'children'),
                Output('lvl2_layer', 'color'),Output('lvl3_layer', 'color'),Output('lvl4_layer', 'color'),Output('lvl5_layer', 'color'),Output('lvl6_layer', 'color'),Output('graph_t1_dirindir', 'figure'),
                
                Input('lvl2-3_reversebutton', 'n_clicks'),Input('lvl3-4_reversebutton', 'n_clicks'),Input('lvl4-5_reversebutton', 'n_clicks'),Input('lvl5-6_reversebutton', 'n_clicks'),
                Input('lvl2_layer', 'n_clicks'),Input('lvl3_layer', 'n_clicks'),Input('lvl4_layer', 'n_clicks'),Input('lvl5_layer', 'n_clicks'),Input('lvl6_layer', 'n_clicks'),

                State('Sisoref_t1', 'value'),State('Ssecref_t1', 'value'),Input('Svarref_t1','value'),State('Sturnover_t1', 'value'),
                State('lvl2_layer', 'children'),State('lvl3_layer', 'children'),State('lvl4_layer', 'children'),State('lvl5_layer', 'children'),State('lvl6_layer', 'children'),
                
                Input('t1_treemap_actlayers', 'data'),Input('t1_treemap_data', 'data'))   #Does not work with State for the dcc.store...             
def fn_genr_treemap(click23,click34,click45,click56,click2,click3,click4,click5,click6,
                    Sisoref,Ssecref,Svarref,Sturnover,lvl2_label,lvl3_label,lvl4_label,lvl5_label,lvl6_label, Vactdeact,Vireqs):
    
    ctx = dash.callback_context
    firedcomp_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    res_tupple = (lvl2_label, lvl3_label,lvl4_label,lvl5_label,lvl6_label)
    color_tupple = tuple(Vactdeact)
    lvl2_color, lvl3_color,lvl4_color,lvl5_color,lvl6_color = color_tupple
    
    if firedcomp_id == 'lvl2-3_reversebutton':
        res_tupple = (lvl3_label, lvl2_label,lvl4_label,lvl5_label,lvl6_label)
        color_tupple = (lvl3_color, lvl2_color,lvl4_color,lvl5_color,lvl6_color)
    if firedcomp_id == 'lvl3-4_reversebutton':
        res_tupple = (lvl2_label, lvl4_label,lvl3_label,lvl5_label,lvl6_label)
        color_tupple=(lvl2_color, lvl4_color,lvl3_color,lvl5_color,lvl6_color)
    if firedcomp_id == 'lvl4-5_reversebutton':
        res_tupple = (lvl2_label, lvl3_label,lvl5_label,lvl4_label,lvl6_label)
        color_tupple =  (lvl2_color, lvl3_color,lvl5_color,lvl4_color,lvl6_color)
    if firedcomp_id == 'lvl5-6_reversebutton':
        res_tupple = (lvl2_label, lvl3_label,lvl4_label,lvl6_label,lvl5_label)
        color_tupple =  (lvl2_color, lvl3_color,lvl4_color,lvl6_color,lvl5_color)
    
    Vlayers=[];Vlayers.append(px.Constant("Global requirements"))
    
    for i,Slayer in enumerate(res_tupple):
        
        if color_tupple[i] == 'success':
        
            Vlayers.append(Slayer)
           
    fig = fn_fill_treemap(Vireqs,Vlayers,Sisoref,Ssecref,Svarref)
    
    new_tupple = res_tupple + color_tupple + (fig,)
    
    return new_tupple
               
def fn_fill_treemap(Vmat,Vlayers,Sisoref,Ssecref,Svarref):  #Reliance of Ssecref_Sisoref towards the industries of Sisodep in terms of supply
       
    Vsecs = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][1],False)
    Visos = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][0],False)
    Vgroups = mopers.Dstructuralarrays['Slicing_vecs']
    
    Dsecs = {'Agriculture':'Agriculture','Fishing':'Agriculture','Energy mining':'Mining','Mining of metals':'Mining','Mining support activities':'Mining','Food, beverages, tobacco':'Food, beverages, tobacco',
    'Textiles':'Textile','Wood':'Wood and paper','Paper products':'Wood and paper','Refined petroleum':'Material manufacturing','Chemical products':'Material manufacturing','Pharmaceutical products':'Material manufacturing',
    'Rubber and plastics':'Material manufacturing','Other non-metallic minerals':'Material manufacturing','Basic metals':'Material manufacturing','Fabricated metal products':'Material manufacturing','Computer, electronics':'Machinery and equipement',
    'Electrical equipment':'Machinery and equipement','Machines, equipment nec ':'Machinery and equipement','Motor vehicles':'Transport equipment','Aircraft, ship manufacturing':'Transport equipment','Misc manufacturing':'Other manufacturing',
    'Utilities':'Utilities','Water supply, remediation':'Utilities','Construction':'Construction','Wholesale, retail':'Distributive trade','Land transport':'Transport services','Water transport':'Transport services','Air transport':'Transport services'
    ,'Warehousing':'Transport services','Postal and courier':'Transport services','Hotels, restaurants':'Accommodation','Audiovisual, broadcasting':'Information and communication','Telecommunications':'Information and communication',
    'Information services':'Information and communication','Finance':'Finance and real estate','Real estate':'Finance and real estate','Professional services':'Renting and business activities','Admin., support services':'Renting and business activities',
    'Public admin., defence':'Public admin, defence; education and health','Education':'Public admin, defence; education and health','Human health, social work':'Public admin, defence; education and health','Arts, entertainment':'Other social and personal services',
    'Other service activities':'Other social and personal services','Households as producers':'Other social and personal services'}

    Disos = {'Latin America':'Americas','Asia Pacific':'Asia','European Union':'Europe','North America':'Americas','Other Europe':'Europe','MENA':'MENA, SSA and RoW','SSA and RoW':'MENA, SSA and RoW'}
    
    Vlegend = ['Direct','Indirect'];Vres = [];Ddic = {'Broad segment':[],'Segment':[],'Continent':[],'Region':[],'Supplier tier':[],Svarref:[]}

    Vmat = mopers.fn_convert_prodmat(np.array(Vmat),Svarref)

    for Sisodep in Visos:
    
        for Ssecdep in Vsecs:
        
            direct_flow = mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Ssecdep,Sisodep],[Ssecref,Sisoref])
            total_flow = mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Ssecdep,Sisodep],[])
            indirect_flow = total_flow-direct_flow           
            
            Ddic[Svarref].append(direct_flow)
            Ddic['Supplier tier'].append('Tier 1');Ddic['Segment'].append(Ssecdep);Ddic['Region'].append(Sisodep)
            Ddic['Broad segment'].append(Dsecs[Ssecdep]);Ddic['Continent'].append(Disos[Sisodep])

            Ddic[Svarref].append(indirect_flow)
            Ddic['Supplier tier'].append('Tier > 1');Ddic['Segment'].append(Ssecdep);Ddic['Region'].append(Sisodep)
            Ddic['Broad segment'].append(Dsecs[Ssecdep]);Ddic['Continent'].append(Disos[Sisodep])

    df = pd.DataFrame(data=Ddic)
   
    Diccolor = {Ssec:mopers.fn_generate_hexcolor(Ssec) for Ssec in Ddic[Vlayers[1]]}
    Diccolor.update({"World industries": "lightgrey"})    
              
    fig = px.treemap(df, path=Vlayers, color_discrete_sequence=['lightgrey'],values=Svarref, color=Vlayers[1],color_discrete_map=Diccolor)
    fig.update_traces(root_color="lightgrey")
    
    Stitle = 'Breakdown of direct (eg tier-1) and indirect (tier > 1) purchases - ' + Svarref
    fig.update_layout({"uirevision": True})
    fig.update_layout({'title': Stitle,"margin": {"l": 0, "r": 25, "b": 0, "t": 50}, "autosize": True})#margin = dict(t=50, l=25, r=25, b=25))
    
    return fig

@app.callback(Output('graph_t1_sankey', 'figure'),Input('graph_t1_dirindir', 'clickData'),Input('Sisoref_t1', 'value'),Input('Ssecref_t1', 'value'),Input('Svarref_t1','value'),Input('Sturnover_t1', 'value'),State('t1_treemap_data', 'data'))
def genr_sankey1(click_data,Sisoref,Ssecref,Svarref,Sturnover,Vireqs):
    
    # check if the click data is not None
    Vid = []
    if click_data is not None:
        
        Slabel = click_data['points'][0]['id']
        Vid = Slabel.split("/")

    Vgroups = mopers.Dstructuralarrays['Slicing_vecs']    
    Vdimdeps = [Sid for Sid in Vid if Sid in Vgroups]

    fig = fn_fill_sankey1(Vireqs,Sisoref, Ssecref,Vdimdeps,Svarref,Sturnover)

    return fig
       
def fn_fill_sankey1(Vmat,Sisoref,Ssecref,Vdimdeps,Svarref,Sturnover): 

    # We want to see how the selection is used directly and indirectly with more detail on the indirect: thorugh which channels does it happen
    # 1) Direct linkage
    # 2) Indirect linkage - 1) Which regions purchase from it and are direct suppliers.
    
    Smnemoref = Ssecref + ' - ' + Sisoref

    Ssecdep = "\n".join(Vdimdeps) if len(Vdimdeps) > 0  else 'Global requirements'
    
    Vsecs = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][1],False)
       
    Vu = np.concatenate(([Smnemoref, Ssecdep + '<br>Direct'], Vsecs,['Other industries'], [Ssecdep + '<br>Indirect']))
    Vu2 = np.concatenate(([Ssecref,Ssecdep], Vsecs,['Other industries'], [Ssecdep]))
    Vuniverse = Vu.tolist()
    Vuniverse2 = Vu2.tolist()
        
    Vgroups = mopers.Dstructuralarrays['Slicing_vecs']    
    
    Vmat = mopers.fn_calc_intermediatereqs_stal(Sisoref,Ssecref,Svarref,Sturnover)

    Vlinecolors = []
    
    # First, ref sector direct purchases from sector in question
    Vsources = [Vuniverse.index(Ssecdep + '<br>Direct')]
    Vlinecolors.append(Vdimdeps[0]) if len(Vdimdeps) > 0 else Vlinecolors.append('gray')
    Vtargets = [Vuniverse.index(Smnemoref)]
    dirpurch=mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, Vdimdeps,[Sisoref, Ssecref])#.fn_assess_dep('Supply',Sisoref,Ssecref,'*',Ssecdep,Svarref)[0]
    Vvalues = [dirpurch]

    #  NOTE: THE SECTOR PURCHASES THINGS FROM ITSELF TOO, therefore indirectly
    # Second, flows from indirect to intermediary
    Vbuffer = []
    for Ssec in Vsecs:
        val = mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, Vdimdeps,[Ssec])#*(Ssec!=Ssecref)
        if Ssec==Ssecref:
           val=val-mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, Vdimdeps,[Sisoref,Ssec]) 
        Vbuffer.append(val)
        
    c_val = sorted(Vbuffer)[-6]
    
    for i,Ssec in enumerate(Vsecs):
    
        val = Vbuffer[i]

        if val>=c_val:

            Vsources.append(Vuniverse.index(Ssecdep + '<br>Indirect'))
            Vlinecolors.append(Ssecdep)
            Vtargets.append(Vuniverse.index(Ssec))
            Vvalues.append(val)

            # Third, flows from intermediary to final    
            Vsources.append(Vuniverse.index(Ssec))
            Vlinecolors.append(Ssec)
            Vtargets.append(Vuniverse.index(Smnemoref))
            Vvalues.append(val)
    
    val = sum(Vbuffer)-sum(val for val in Vbuffer if val >= c_val)
    Vsources.append(Vuniverse.index(Ssecdep + '<br>Indirect'))
    Vlinecolors.append(Ssecdep)
    Vtargets.append(Vuniverse.index('Other industries'))
    Vvalues.append(val)

    # Third, flows from intermediary to final    
    Vsources.append(Vuniverse.index('Other industries'))
    Vlinecolors.append('Other industries')
    Vtargets.append(Vuniverse.index(Smnemoref))
    Vvalues.append(val)

    Vlink_colors = [mopers.fn_generate_hexcolor(Stxt) for Stxt in Vlinecolors]
    Vnodecolors = [mopers.fn_generate_hexcolor(Stxt) for Stxt in Vuniverse2]

    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = Vuniverse,
      color = Vnodecolors
    ),
    link = dict(
      source = Vsources, # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = Vtargets,
      value = Vvalues,
      color = Vlink_colors
    ))]) 


    Stitle = "Click on treemap element to get detail on type of exposure<br>(direct or through other type of goods/services)"
    #Stitle = Stitle + ' - ' + Svarref

    fig.update_layout(title = Stitle,title_x=0.5, margin = dict(t=80, l=25, r=25, b=25))
    
    return fig

 #Transactions by each industry in a given country
@app.callback(Output('graph_t1_countrytransactions', 'figure'),
              Input('t1_treemap_data', 'data'),Input('Sisoref_t1', 'value'),Input('Ssecref_t1', 'value'),Input('Svarref_t1b', 'value'),Input('Sisodep_t1', 'value'),Input('nsecs_t1', 'value'),Input('Bresid_sankey_t1','on'))
def genr_sankey2(Vireqs,Sisoref, Ssecref,Svarref,Sisozoom,nsecs,Bbalancedresid):
   
    fig = fn_update_sankey2(Vireqs,Sisoref,Ssecref,Sisozoom,Svarref,'100',nsecs,Bbalancedresid) 

    cols = ["Imports","Domestic importers","Domestic exporters", "Exports"]
    for x_coordinate, column_name in enumerate(cols):
      fig.add_annotation(
              x=x_coordinate / (len(cols) - 1),
              y=1.05,
              xref="paper",
              yref="paper",
              text=column_name,
              showarrow=False,
              font=dict(
                  family="Courier New, monospace",
                  size=16,
                  color="tomato"
                  ),
              align="center",
              )

    return fig

def fn_update_sankey2(Vmat,Sisoref,Ssecref,Sisodep,Svarref,Sturnover,nsecs,B_sameresid): 
    
    n = int(nsecs)

    Vmat = mopers.fn_convert_prodmat(np.array(Vmat),Svarref)

    Vsecs = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][1],False)
    Vgroups = mopers.Dstructuralarrays['Slicing_vecs']        
    
    Vu = np.concatenate([[Ssec + ' -M-' for Ssec in Vsecs], [Ssec + ' -M2-' for Ssec in Vsecs], [Ssec + ' -M3-' for Ssec in Vsecs], ['Other segments -M-','Other segments -M2-','Other segments -M3-']])
    Vu2 = np.concatenate(([Ssec for Ssec in Vsecs], [Ssec for Ssec in Vsecs], [Ssec for Ssec in Vsecs], ['Other segments','Other segments','Other segments']))
    
    Vuniverse = Vu.tolist(); Vuniverse2 = Vu2.tolist()
    Vuniverse.append('X'); Vuniverse2.append('X')
    
    #Vmat = mopers.fn_calc_intermediatereqs_stal(Sisoref,Ssecref,Svarref)

    Vsources, Vtargets,Vvalues = [],[],[]
    Vlinecolors = []
    Dnodesizes = {'Nodenames':[],'Weights':[]}
    
    # First, calculate size of each node to display only the n largest
    for Ssrc in Vsecs:
        
        #First layer: product imports
        Dnodesizes['Nodenames'].append(Ssrc + ' -M-')
        totpurch=mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Ssrc],[Sisodep])
        dompurch=mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Ssrc, Sisodep],[Sisodep])
        Dnodesizes['Weights'].append(totpurch-dompurch)
    
        #Second layer: domestic sectors producing for domestic use
        Dnodesizes['Nodenames'].append(Ssrc + ' -M2-')
        domsales=mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Ssrc, Sisodep],[Sisodep])
        Dnodesizes['Weights'].append(domsales)
    
        #Third layer: domestic sectors exporting
        totsales=mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Ssrc,Sisodep],[])
        Dnodesizes['Nodenames'].append(Ssrc + ' -M3-')
        Dnodesizes['Weights'].append(totsales-domsales)        
    
    #Second, filter the dataframe and get only the n largest values
    df = pd.DataFrame(data=Dnodesizes)  
    df1 = mopers.fn_keep_topdfvals(df, 'Weights', n-1, False, 'Nodenames',' -M-')
    df2 = mopers.fn_keep_topdfvals(df, 'Weights', n-1, False, 'Nodenames',' -M2-')
    df3 = mopers.fn_keep_topdfvals(df, 'Weights', n-1, False, 'Nodenames',' -M3-')    # ----- > At that point we have the n-1 top sectors in each node. 
        
    #Store all the values that will need to make it into the final figure
    Vsrcdest_tokeep = df1['Nodenames'].tolist() + df2['Nodenames'].tolist() + df3['Nodenames'].tolist() + ['X','Other segments -M-','Other segments -M2-','Other segments -M3-']  
        
    if B_sameresid == True:
    
            Vignore = ['X']
            Vsrcdest = pd.Series([str(x) for x in Vsrcdest_tokeep]).str.replace(' -M-| -M2-| -M3-', '', regex=True).tolist()
            Vsrcdest = mopers.fn_removelist_duppli(Vsrcdest,False)
            Vsrcdest_tokeep = [Ssec for Ssec in Vsrcdest]
            Vsrcdest_tokeep = [f"{Ssec} -M{Sext}-" for Ssec in Vsrcdest_tokeep if Ssec not in Vignore for Sext in ['','2','3']]
            Vsrcdest_tokeep.extend(Vignore)
            #Remake df1 and stuff as they are being reused later, otherwise you get inconsistencies
            df1 = pd.DataFrame(data={'Nodenames':[s for s in Vsrcdest_tokeep if ' -M-' in s]})
            df2 = pd.DataFrame(data={'Nodenames':[s for s in Vsrcdest_tokeep if ' -M2-' in s]})
            df3 = pd.DataFrame(data={'Nodenames':[s for s in Vsrcdest_tokeep if ' -M3-' in s]})
            
    
    #################################################
    #Calculate full vectors, we'll work on them after
    #################################################
    
    # First, RoW exports to domestic sectors (M to M2)
    for i in Vsecs: #df1['Nodenames'].tolist():
        
        Ssrc = i + ' -M-'
        
        for j in Vsecs:
        
            Sdest = j + ' -M2-'

            Vsources.append(Ssrc);Vtargets.append(Sdest)          
            totpurch=mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [i],[Sisodep, j])
            dompurch=mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [i, Sisodep],[Sisodep, j])
            Vvalues.append(totpurch-dompurch)       
    
    # Second, Domestic sector sales to other domestic sectors (M2 to M3)
    for i in Vsecs: #df1['Nodenames'].tolist():
        
        Ssrc = i + ' -M2-'
        
        for j in Vsecs:
        
            Sdest = j + ' -M3-'

            Vsources.append(Ssrc);Vtargets.append(Sdest)          
            dompurch=mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [i, Sisodep],[j, Sisodep])
            Vvalues.append(dompurch)

    # Third, Domestic sector sales to rest of the world (M3 to X)
    for i in Vsecs: #df1['Nodenames'].tolist():
        
        Ssrc = i + ' -M3-'
        
        for j in ['X']:
        
            Sdest = 'X'

            Vsources.append(Ssrc);Vtargets.append(Sdest)
            totsales=mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [i,Sisodep],[])
            domsales=mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [i, Sisodep],[Sisodep])
            Vvalues.append(totsales-domsales)

    #################################################
    #At that point we have all transactions calculated, and the sectors to keep
    #################################################    
  
    
    #Openai: if you change the elements in the Vsources array, it will not be automatically reflected in the dfalltransactions DataFrame
    dfalltransactions = pd.DataFrame(data={'Sources':Vsources,'Destinations':Vtargets,'Values':Vvalues}) 
    
    #Transactions from resid of -M- to sectors of M2 
    df_filtered = mopers.fn_filter_df(dfalltransactions, 'Sources', condition= ' -M-')
    for Sdest in df2['Nodenames'].tolist():
               
        mask1 = ~df_filtered['Sources'].isin(df1['Nodenames'].tolist()) #Values that are not in df1
        mask2 = df_filtered['Destinations'] == Sdest #And export to Sdest

        Vsources.append('Other segments -M-');Vtargets.append(Sdest)
        Vvalues.append(df_filtered.loc[mask1 & mask2, 'Values'].sum())
    
    #Transactions from sectors of M to resid of M2
    df_filtered = mopers.fn_filter_df(dfalltransactions, 'Destinations', condition= ' -M2-')
    for Ssrc in df1['Nodenames'].tolist():
                
        mask1 = ~df_filtered['Destinations'].isin(df2['Nodenames'].tolist()) #Values that are not in df2
        mask2 = df_filtered['Sources'] == Ssrc #And export to Sdest

        Vsources.append(Ssrc);Vtargets.append('Other segments -M2-')
        Vvalues.append(df_filtered.loc[mask1 & mask2, 'Values'].sum())
    
    #Transactions from resid of M to resid of M2
    df_filtered = mopers.fn_filter_df(dfalltransactions, 'Sources', condition= ' -M-')
    df_filtered = mopers.fn_filter_df(df_filtered, 'Destinations', condition= ' -M2-')
    
    mask1 = ~df_filtered['Sources'].isin(df1['Nodenames'].tolist()) #Values that are not in df1
    mask2 = ~df_filtered['Destinations'].isin(df2['Nodenames'].tolist()) #And export to Sdest    
        
    Vsources.append('Other segments -M-');Vtargets.append('Other segments -M2-')
    Vvalues.append(df_filtered.loc[mask1 & mask2, 'Values'].sum())
  
    ##########################
    #Transactions from resid of -M2- to sectors of M3 
    df_filtered = mopers.fn_filter_df(dfalltransactions, 'Sources', condition= ' -M2-')
    for Sdest in df3['Nodenames'].tolist():
               
        mask1 = ~df_filtered['Sources'].isin(df2['Nodenames'].tolist()) #Values that are not in df1
        mask2 = df_filtered['Destinations'] == Sdest #And export to Sdest

        Vsources.append('Other segments -M2-');Vtargets.append(Sdest)
        Vvalues.append(df_filtered.loc[mask1 & mask2, 'Values'].sum())
    
    #Transactions from sectors of M2 to resid of M3
    df_filtered = mopers.fn_filter_df(dfalltransactions, 'Destinations', condition= ' -M3-')
    for Ssrc in df2['Nodenames'].tolist():
                
        mask1 = ~df_filtered['Destinations'].isin(df3['Nodenames'].tolist()) #Values that are not in df2
        mask2 = df_filtered['Sources'] == Ssrc #And export to Sdest

        Vsources.append(Ssrc);Vtargets.append('Other segments -M3-')
        Vvalues.append(df_filtered.loc[mask1 & mask2, 'Values'].sum())
    
    #Transactions from resid of M2 to resid of M3
    df_filtered = mopers.fn_filter_df(dfalltransactions, 'Sources', condition= ' -M2-')
    df_filtered = mopers.fn_filter_df(df_filtered, 'Destinations', condition= ' -M3-')
    
    mask1 = ~df_filtered['Sources'].isin(df2['Nodenames'].tolist()) #Values that are not in df1
    mask2 = ~df_filtered['Destinations'].isin(df3['Nodenames'].tolist()) #And export to Sdest    
        
    Vsources.append('Other segments -M2-');Vtargets.append('Other segments -M3-')
    Vvalues.append(df_filtered.loc[mask1 & mask2, 'Values'].sum())

    ##########################
    #Transactions from resid of -M3- to X 
    df_filtered = mopers.fn_filter_df(dfalltransactions, 'Sources', condition= ' -M3-')
    Sdest = 'X'
    mask1 = ~df_filtered['Sources'].isin(df3['Nodenames'].tolist()) #Values that are not in df1
    mask2 = df_filtered['Destinations'] == Sdest #And export to Sdest

    Vsources.append('Other segments -M3-');Vtargets.append(Sdest)
    Vvalues.append(df_filtered.loc[mask1 & mask2, 'Values'].sum())
    
    ###########################################################
    #### Final filtering
    dfalltransactions = pd.DataFrame(data={'Sources':Vsources,'Destinations':Vtargets,'Values':Vvalues}) 
    mask = (dfalltransactions['Sources'].isin(Vsrcdest_tokeep)) & (dfalltransactions['Destinations'].isin(Vsrcdest_tokeep))
    dfalltransactions = dfalltransactions[mask]
    
   # dfalltransactions.to_excel('my_data.xlsx', index=False)
    
    Vsources = dfalltransactions['Sources'].tolist();Vtargets = dfalltransactions['Destinations'].tolist();Vvalues = dfalltransactions['Values'].tolist()
        
    Vlinecolors = pd.Series([str(x) for x in Vsources]).str.replace(' -M-| -M2-| -M3-', '', regex=True).tolist()
    
    Vsources = [Vuniverse.index(Stxt) for Stxt in Vsources]
    Vtargets = [Vuniverse.index(Stxt) for Stxt in Vtargets]
    
    #Vlink_colors = pd.Series(Vsources).str.replace('-M-|-M2-|-M3-', '', regex=True).tolist()
    Vlinecolors = [mopers.fn_generate_hexcolor(Stxt) for Stxt in Vlinecolors]    
    Vnodecolors = [mopers.fn_generate_hexcolor(Stxt) for Stxt in Vuniverse2]

    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = Vuniverse2,
      color = Vnodecolors#"blue"
    ),
    link = dict(
      source = Vsources, # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = Vtargets,
      value = Vvalues,
      color = Vlinecolors
    ))]) 

    Stitle = Sisodep + ' insertion into supply chain'    

    fig.update_layout(title = Stitle, margin = dict(t=50, l=25, r=25, b=25))
    
    return fig


 #Transactions by each industry in a given country
@app.callback(Output('graph_t1_countrytransactions2', 'figure'),
              Input('t1_treemap_data', 'data'),Input('Sisoref_t1', 'value'),Input('Ssecref_t1', 'value'),Input('Sisodep_t1', 'value'),Input('Svarref_t1b', 'value'),Input('Sturnover_t1', 'value'),Input('nsecs_t1', 'value'))
def update_figure(Vmat,Sisoref,Ssecref,Sisozoom,Svarref,Sturnover,nsecs):

    nsecs = int(nsecs)
    Vsecs = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][1],False)
    Vgroups = mopers.Dstructuralarrays['Slicing_vecs']
    
    Vres = []
    
    Ddic = {'Domestic sales':[],'Exports':[],'Domestic purchases':[],'Imports':[],'Net':[],'Industry':[]}
    
    Vmat = mopers.fn_convert_prodmat(np.array(Vmat),Svarref)
    
    for Ssec in Vsecs:
        
        Ddic['Industry'].append(Ssec) 
        Ddic['Domestic sales'].append(mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Sisozoom,Ssec],[Sisozoom])) 
        Ddic['Exports'].append(mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Sisozoom,Ssec],[])-Ddic['Domestic sales'][-1]) 
        Ddic['Domestic purchases'].append(mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Sisozoom],[Sisozoom,Ssec]))    
        Ddic['Imports'].append(mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [],[Sisozoom,Ssec])-Ddic['Domestic purchases'][-1]) 
        Ddic['Domestic purchases'][-1]=-Ddic['Domestic purchases'][-1];Ddic['Imports'][-1]=-Ddic['Imports'][-1]
        
        Ddic['Net'].append(Ddic['Domestic sales'][-1]+ Ddic['Exports'][-1]+Ddic['Domestic purchases'][-1]+Ddic['Imports'][-1])
     
    df = pd.DataFrame(data=Ddic)
    
    df_clean = mopers.fn_keep_topdfvals(df,'Exports',nsecs,True)
   
    # Create an empty list to store the traces
    traces = []

    Vcols_to_skip = ['Industry']

    # Loop through each column and create a bar trace for it
    for Scol in [c for c in df_clean.columns if c not in Vcols_to_skip]:

        if Scol !='Net':
            trace = go.Bar(x=df_clean[Scol], y=df_clean['Industry'], orientation='h', name=Scol)
        else:
            trace = go.Scatter(x=df_clean[Scol], y=df_clean['Industry'], mode='markers', marker=dict(symbol='circle', size=14, color='black'), name='Net')

        traces.append(trace)

    # Create the figure and add the traces to it
    fig = go.Figure(data=traces)

    Stitle = Sisozoom + ' insertion into supply chain'

    #legend=dict(y=-0.2, orientation="h", yanchor="top"),

    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal orientation
            yanchor="top",
            y=-0.2,  # Position of legend relative to the bottom of the chart
            xanchor="center",
            x=0.5  # Center the legend horizontally
        ),
        # Adjust the bottom margin to ensure the x-axis labels are visible
        margin=dict(
            b=0  # Increase bottom margin; adjust this value as needed
        )
    )

    fig.update_layout(barmode='relative', title=Stitle)

    return fig

@app.callback(Output('graph_t1_countrytransactions3', 'figure'),
              Input('t1_treemap_data', 'data'),Input('Sisoref_t1', 'value'),Input('Ssecref_t1', 'value'),Input('Sisodep_t1', 'value'),Input('Svarref_t1b', 'value'),Input('Sturnover_t1', 'value'))
def update_figure(Vmat,Sisoref,Ssecref,Sisozoom,Svarref,Sturnover):

    Vsecs = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][1],False)
    Visos = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][0],False)
    Vgroups = mopers.Dstructuralarrays['Slicing_vecs']
    
    Vres = [];  Ddic = {'Country':[],'Exports':[],'Imports':[]}
    
    Vmat = mopers.fn_convert_prodmat(np.array(Vmat),Svarref)
    
    # Create the figure and add the traces to it
    fig = make_subplots(rows=1, cols=2,subplot_titles = ('Major import sources','Major export destinations'))

    #for i, Svarref in enumerate(Vcons):
    
    for i,Stransaction in enumerate(['Imports','Exports']):
        
        Ddic = {'Country':[],Stransaction:[]}

        for Siso in Visos:

            if Siso != Sisozoom:

                Ddic['Country'].append(Siso) 

                if Stransaction == 'Exports':
                    Ddic['Exports'].append(mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Sisozoom],[Siso])) 
                else:
                    Ddic['Imports'].append(mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Siso],[Sisozoom]))

        df = pd.DataFrame(data=Ddic)

        df_clean = mopers.fn_keep_topdfvals(df,Stransaction,10,True)

        # Create an empty list to store the traces
        traces = []
        Vcols_to_skip = ['Country']

        # Loop through each column and create a bar trace for it
        # for Scol in [c for c in df_clean.columns if c not in Vcols_to_skip]:

            # trace = go.Bar(x=df_clean[Scol], y=df_clean['Country'], orientation='h', name=Scol)
            # traces.append(trace)

        fig.add_trace(go.Bar(y=df_clean['Country'],x=df_clean[Stransaction],orientation = 'h',name = Stransaction),row=1,col=i+1)
        #fig.add_trace(go.Bar(y=Vy2,x=Visos,legendgroup=Ssec,showlegend=(i == 0),name=Ssec,marker_color=mopers.fn_generate_hexcolor(Ssec)),row=1,col=i+1)
    Stitle  = 'Major trade partners of ' + Sisozoom + ' in selected supply chain'
    fig.update_layout({'barmode':'stack','title':Stitle}) #legend=dict(orientation="h",yanchor="bottom",y=-0.15,xanchor="center",x=0.5)
    
    return fig

@app.callback(Output('graph_t1_countrytransactions4', 'figure'),
    Input('t1_treemap_data', 'data'),Input('Sisoref_t1', 'value'),Input('Ssecref_t1', 'value'),Input('Sisodep_t1b', 'value'),Input('Svarref_t1c', 'value'),Input('Sturnover_t1', 'value'))
def update_figure(Vmat,Sisoref, Ssecref,Sisozoom,Svarref,Sturnover):
       
    Vmat = mopers.fn_convert_prodmat(np.array(Vmat),Svarref)
    
    Visos = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][0],True)
    Vsecs = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][1],False)
    Vgroups = mopers.Dstructuralarrays['Slicing_vecs']
    
    Vprodstages = mopers.fn_decompose_prodstages(Sisoref,Ssecref,Svarref,Sturnover)
    
    Vstagenums = [str(i) for i in range(len(Vprodstages))]
    
    Ddic = {'Industry':[],'Total':[]}
        
    for Ssec in Vsecs:

        tot = mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Sisozoom,Ssec],[])
        Ddic['Industry'].append(Ssec)
        Ddic['Total'].append(tot)

    df = pd.DataFrame(data=Ddic)
    df_clean = mopers.fn_keep_topdfvals(df,'Total',8,False,None)
    max_x = df["Total"].max();bubble_x = max_x + 0.1 * max_x
    Ddictot = {}
    
    Ddic = {'Industry':[],'Supplier tier':[],'Value':[]}
    
    for Ssec in df_clean['Industry']:
    
        for i in Vstagenums:
           
            x = mopers.fn_calcconditional_sum(Vprodstages,[Vstagenums],Vgroups, [i],[Sisozoom,Ssec])
            Ddic['Industry'].append(Ssec)
            Ddic['Supplier tier'].append(int(i))
            Ddic['Value'].append(x)
        
    df = pd.DataFrame(data=Ddic)
    #df['Value'][df['Industry'] == Ssec].sum()

    fig = px.bar(df, x="Value", y="Industry", color="Supplier tier", orientation="h", title=Sisozoom + ' - Industry ' + Svarref + '<br>by stage and position in value chain',
                 color_continuous_scale=[[0, 'black'], [0.2, 'red'], [0.4, 'pink'], [0.6, 'orange'], [0.8, 'yellow'], [1.0, 'rgb(255, 255, 255)']])

    # Retrieve the bar trace from the Figure
    bar_trace = fig.data[0]

    Vsecs = mopers.fn_removelist_duppli(df['Industry'],False)

    VSCpositions = [mopers.fn_calc_SCsupplyposition(Sisoref,Ssecref,Sisozoom,Ssec,Svarref) for Ssec in Vsecs]

    # Add a scatter trace for the bubbles
    bubble_trace = go.Scatter(
        x=[bubble_x] * len(Vsecs),
        y=[Ssec for Ssec in Vsecs],
        mode="markers",
        name='Average tier',
        marker=dict(
            size=[200 for Ssec in Vsecs],
            sizemode='area',
            sizemin=2,
            color=VSCpositions,
            coloraxis=bar_trace.marker.coloraxis,
            showscale=True
        ),
        # Use hovertemplate for custom hover text
        hovertemplate=[
            f"Position in SC: {val:.2f}<extra></extra>" for val in VSCpositions
        ]
    )

    # Add the scatter trace to the Figure
    fig.add_trace(bubble_trace)

    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal orientation
            yanchor="bottom",
            y=-0.2,  # Adjust vertical position
            xanchor="center",
            x=0.5,  # Center horizontally
        )
    )

    return fig

@app.callback(Output('graph_t1_suppliertier1', 'figure'),
    Input('t1_treemap_data', 'data'),Input('Sisoref_t1', 'value'),Input('Ssecref_t1', 'value'),Input('Svarref_t1c', 'value'),Input('nstages', 'value'),Input('Sturnover_t1', 'value'))
def update_figure(Vmat,Sisoref, Ssecref,Svarref,Snstages,Sturnover):
       
    Sdim = 'Industries'
    nstages = int(Snstages)

    Vmat = mopers.fn_convert_prodmat(np.array(Vmat),Svarref)
    
    Visos = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][0],True)
    Vsecs = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][1],False)
    Vgroups = mopers.Dstructuralarrays['Slicing_vecs']
    
    Vbreakdown = Vsecs if Sdim == 'Industries' else Visos
        
    Vprodstages = mopers.fn_decompose_prodstages(Sisoref,Ssecref,Svarref,Sturnover,nstages)[1:]

    Vstagenums = [str(i+1) for i in range(len(Vprodstages)-1)]
    Vstagenums.append(str(len(Vprodstages)) + ' and more')
    
    Ddic = {Sdim:[],'Total':[]}
        
    for Sitem in Vbreakdown:

        tot = mopers.fn_calcconditional_sum(Vmat,Vgroups,Vgroups, [Sitem],[])
        Ddic[Sdim].append(Sitem)
        Ddic['Total'].append(tot)

    df = pd.DataFrame(data=Ddic)
    df_clean = mopers.fn_keep_topdfvals(df,'Total',10,False,None)
    Ddictot = {}
    
    Ddic = {Sdim:[],'Supplier tier':[],'Value':[]}
    
    for  i in Vstagenums:
    
        mem = 0
    
        for Sitem in df_clean[Sdim]:
           
            x = mopers.fn_calcconditional_sum(Vprodstages,[Vstagenums],Vgroups, [i],[Sitem])
            Ddic[Sdim].append(Sitem)
            Ddic['Supplier tier'].append(i)
            Ddic['Value'].append(x)
            mem = mem+x
        
        tot = mopers.fn_calcconditional_sum(Vprodstages,[Vstagenums],Vgroups, [i],[])
        Ddic[Sdim].append('Other items')
        Ddic['Supplier tier'].append(i)
        Ddic['Value'].append(tot-mem)
        
    df = pd.DataFrame(data=Ddic)

    fig = px.bar(df, x="Supplier tier", y="Value", color=Sdim, title='World - Industry ' + Svarref + ' by stage',color_discrete_map ={Ssec: mopers.fn_generate_hexcolor(Ssec) for Ssec in Ddic[Sdim]})

    return fig

@app.callback(Output('graph_t1_suppliertier2', 'figure'),Output('t1_memstages', 'data'), 
                Input('graph_t1_suppliertier1', 'clickData'),Input('graph_t1_suppliertier1', 'restyleData'),Input('graph_t1_suppliertier1', 'figure'),Input('t1_memstages', 'data'),
                Input('Sisoref_t1', 'value'),Input('Ssecref_t1', 'value'),Input('Svarref_t1c', 'value'),Input('Sturnover_t1', 'value'), )
def store_click_data(click_data, restyle_data, Dfig1, Dmem,Sisoref, Ssecref,Svarref,Sturnover):
    
    Dmem = fn_harvest_click(click_data, Dmem, Dfig1)
    
    Vdashparams = [Sisoref, Ssecref,Svarref, Sturnover]
    Dfig = fn_add_subplot(Dmem, Vdashparams)
    


            
    return Dfig, Dmem

def fn_harvest_click(Dclickdata, Dmem, Dorigfig): 
    # Dclickdata contains coordinates of click
    # Dmem contains history of previous clicks and all sorts of information
    # Dorigfig contains figure in current state so one can retrieve the legend

    Dclickdata_old = Dmem['Clickdata']
    Vlegend =[trace['name'] for trace in Dorigfig['data']]

    if Dclickdata is not None and Dclickdata_old != Dclickdata:

        Sx = Dclickdata['points'][0]['x'] #x coordinate of point clicked
        ilegend = Dclickdata['points'][0]['curveNumber'];Slegend = Vlegend[ilegend] #legend coordinate of point clicked
        Dmem['Clickdata'] = Dclickdata;Dmem['Selection'] = [Slegend,Sx]

    return Dmem

def fn_add_subplot(Dmem,Vdashparams): 

    Sisoref, Ssecref,Svarref, Sturnover = Vdashparams
    Vgroups = mopers.Dstructuralarrays['Slicing_vecs']
    
    Sx = '';Slegend = ''

    if Dmem['Selection']!= []:
        [Slegend,Sx] = Dmem['Selection']
    
    Visos = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][0],True)
    Vprodstages = mopers.fn_decompose_prodstages(Sisoref,Ssecref,Svarref,Sturnover,6)[1:]

    Vstagenums = [str(i+1) for i in range(len(Vprodstages)-1)]
    Vstagenums.append(str(len(Vprodstages)) + ' and more')
      
    Ddic = {'Geographies':[],'Value':[]}
      
    for Siso in Visos:
        #x = mopers.fn_calcconditional_sum(Vprodstages,[Vstagenums],Vgroups, [i],[Sisozoom,Ssec])
        #x = mopers.fn_calcconditional_sum(Vprodstages,[Vstagenums],Vgroups, [i],[Sitem])       
        x = mopers.fn_calcconditional_sum(Vprodstages,[Vstagenums],Vgroups, [Sx],[Siso,Slegend])
        Ddic['Geographies'].append(Siso)
        Ddic['Value'].append(x)
        
    df = pd.DataFrame(data=Ddic)

    n = len(Dmem['Selection'])
    if n == 0:
        Stitle = 'Click on chart to the left for geo detail'
    else:
        Stitle = "Breakdown of " + Svarref + " at stage " + Sx + '<br> in ' + Slegend + ' industry'

    fig = px.bar(df, x="Geographies", y="Value", color='Geographies', title=Stitle,
                 color_discrete_map ={Siso: mopers.fn_generate_hexcolor(Siso) for Siso in Visos})
    
    fig.update_layout(showlegend=False)

    return fig




@app.callback(Output('graph_t1_co2emissions', 'figure'),
              Input('Sisoref_t1', 'value'),Input('Ssecref_t1', 'value'),Input('Sturnover_t1', 'value'))
def update_figure(Sisoref,Ssecref,Sturnover):  #Reliance of Ssecref_Sisoref towards the industries of Sisodep in terms of supply

    Scon = 'Co2 emissions'
    Vsecs = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][1],False)
    Visos = mopers.fn_removelist_duppli(mopers.Dstructuralarrays['Slicing_vecs'][0],True)
    Vgroups = mopers.Dstructuralarrays['Slicing_vecs']
    
    Dtotreqs = {}
    
    for Siso in Visos:
        
        Vres = mopers.fn_calc_totreqs_stal(Siso,Ssecref,True,Scon,Sturnover)
        Dtotreqs[Siso] = Vres
        
    Vy = [];fig = go.Figure()

    for Ssec in Vsecs:

        Vy2 = []

        for Siso in Visos:
        
            Vtotreqs = Dtotreqs[Siso]
            
            #res = mopers.fn_calcconditional_sum(Vres,Vgroups,Vgroups,[Ssec,Siso],[]) 
            res = mopers.fn_calcconditional_sum([Vtotreqs],[["xxx"]],Vgroups,[["xxx"]],[Ssec]) #Valid for simple vector
            Vy2.append(res)
            
        fig.add_trace(go.Bar(y=Vy2,x=Visos,name=Ssec,marker_color=mopers.fn_generate_hexcolor(Ssec)))
            
    Stitle = 'Co2 emissions VS competitors to reach desired turnover'
    fig.update_layout(barmode='relative',title=Stitle) #legend=dict(orientation="h",yanchor="bottom",y=-0.15,xanchor="center",x=0.5)

    fig.update_xaxes(tickangle=270)
    
    return fig 


if __name__ == '__main__':
    app.run_server(debug=False)
