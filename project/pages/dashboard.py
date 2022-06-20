import plotly.graph_objects as go
import plotly.express as px

import vaex
from dash import html, dcc
from components.card import card, Card
from components.number_range import Number_range_AIO
from components.dropdown import Dropdown
from pages.callbacks import *


def scatter_map_box(latitude, longitude):
    token = "pk.eyJ1Ijoic3Blb2RhcmsiLCJhIjoiY2wzbTF6bnpyMDBjZjNpcjN1bGtpaWNuaiJ9.XokhbqUwdZy9roHnfhewyg"

    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            lat=latitude,
            lon=longitude,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=8,
                opacity=0.7
            ),
            text='hello',
            hoverinfo='text',
            selected={
                'marker':{
                    'color':'red'
                }
            }
        )
    )

    fig.update_layout(
        title='houses on a map!',
        mapbox = dict(
            accesstoken= token,
            center=dict(
                lat=40,
                lon=116.4
            ),
            zoom = 7.5,
            style = "outdoors"
        ),
        showlegend = False,
        margin = dict(l = 0, r = 0, t = 0, b = 0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def bar_chart(df=None, x_axis_name=None, y_axis_name=None):
    fig = px.bar(
        df.to_dict(),
        x=x_axis_name,
        y=y_axis_name,
    )
    fig.update_layout(
        title='top 10 houses by popularity',
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def houses_scatter_map_box(df):
    return card(
        header='houses on a map!',
        children=dcc.Graph(
            figure=scatter_map_box(
                latitude=df.Lat.to_numpy(strict=True),
                longitude=df.Lng.to_numpy(strict=True)
            ),
            className='fill-parent-div',
            id = {'type':'scatter_map_box','page':'dashboard','index':'houses'}
        ),
        className='dashboard__scatter-map center_items_vertical'
    )


def most_popular_houses(df):
    return card(
        children=dcc.Graph(
            figure = bar_chart(
                df = df.sort('followers', ascending=False)[:10],
                x_axis_name='id',
                y_axis_name='followers'
            ),
            responsive=True, 
            className="fill-parent-div",
            id = {'type': 'sales_graph', 'index': 'popular_houses'}
        ),
        className='dashboard__popular-houses'
    )


def dropdowns(df):
    return Card(
        children=[
            # living rooms
            html.Span('Select number of living rooms'),
            dcc.Dropdown(
                sorted(df.livingRoom.unique()),
                placeholder='Select number of living rooms',
                searchable=False,
                id = {'type':'dropdown','page':'dashboard','index':'livingRoom'}
            ),
            # drawing rooms
            html.Span('Select number of drawing rooms'),
            dcc.Dropdown(
                sorted(df.drawingRoom.unique()),
                placeholder='Select number of drawing rooms',
                searchable=False,
                id = {'type':'dropdown','page':'dashboard','index':'drawingRoom'}
            ),
            # kitchens
            html.Span('Select number of kitchens'),
            dcc.Dropdown(
                sorted(df.kitchen.unique()),
                placeholder='Select number of kitchens',
                searchable=False,
                id = {'type':'dropdown','page':'dashboard','index':'kitchen'}
            ),
            # bathrooms 
            html.Span('Select number of bathRooms'),
            dcc.Dropdown(
                sorted(df.bathRoom.unique()),
                placeholder='Select number of bathRooms',
                searchable=False,
                id = {'type':'dropdown','page':'dashboard','index':'bathRoom'}
            ),
            # building type
            html.Span('Select number of building Type'),
            dcc.Dropdown(
                sorted(df.buildingType.unique()),
                placeholder='Select number of building Type',
                searchable=False,
                id = {'type':'dropdown','page':'dashboard','index':'buildingType'}
            )
        ],
        className='dashboard__living-room',
    )


def dashboard():
    df = vaex.open('assets/data/data.csv.hdf5')
    return html.Div(
        className='dashboard',
        children=[
            houses_scatter_map_box(df),
            most_popular_houses(df),
            Number_range_AIO(
                minimum=df.price.min(),
                maximum=df.price.max(),
                title='Price Range', 
                className='dashboard__number-range',
                aio_id='price'
            ),
            dropdowns(df),
        ]
    )

