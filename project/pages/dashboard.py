import plotly.graph_objects as go
import plotly.express as px

import vaex
from dash import html, dcc
from components.card import card
from components.number_range import Number_range_AIO



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
        # legend=dict(
        #     yanchor="middle",
        #     y=1.1,
        #     xanchor="center",
        #     x=0.5,
        #     title={'text': None}
        # ),
        # margin={"t": 30, "b": 0, "r": 20, "l": 0, "pad": 0},
    )
    # fig.update_yaxes(title_text='')
    return fig


def houses_scatter_map_box(df):
    return card(
        header='houses on a map!',
        children=dcc.Graph(
            figure=scatter_map_box(
                latitude=df.Lat.to_numpy(strict=True)[:100000],
                longitude=df.Lng.to_numpy(strict=True)[:100000]
            ),
            className='fill-parent-div'
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
            className="fill-parent-div"
        ),
        className='dashboard__popular-houses'
    )

def dashboard():
    df = vaex.open('assets/data/new.csv.hdf5')
    return html.Div(
        className='dashboard',
        children=[
            houses_scatter_map_box(df),
            most_popular_houses(df),
            Number_range_AIO(minimum=0,maximum=100,title='Price Range', className='dashboard__number-range'),
        ]
    )