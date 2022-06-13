from dash import Input, Output, ALL, State, MATCH
import vaex
from main_dash import app
import dash
import plotly.graph_objects as go
import plotly.express as px
from components.number_range import Number_range_AIO


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

df = vaex.open('assets/data/data.csv.hdf5')

@app.callback(
    Output({'type': 'sales_graph', 'index': ALL}, 'figure'),
    Input({'type':'dropdown','page':'dashboard','index':ALL}, 'value'),
    prevent_initial_call=True
)
def sales_graph_filter(dropdowns):
    dropdown_id_list = [id['id']['index'] for id in dash.callback_context.inputs_list[0]]
    filtered_df = df
    for index in range(len(dropdown_id_list)):
        if dropdowns[index]:
            filtered_df = filtered_df[filtered_df[dropdown_id_list[index]]==dropdowns[index]]
    return [bar_chart(
        df = filtered_df.sort('followers', ascending=False)[:10],
        x_axis_name='id',
        y_axis_name='followers'
    )]


@app.callback(
    Output({'type':'dropdown','page':'dashboard','index':ALL}, 'options'),
    Input({'type':'dropdown','page':'dashboard','index':ALL}, 'value'),
    prevent_initial_call=True
)
def dropdown_options_filter(dropdowns):
    dropdown_id_list = [id['id']['index'] for id in dash.callback_context.inputs_list[0]]
    filtered_df = df
    for index in range(len(dropdown_id_list)):
        if dropdowns[index]:
            filtered_df = filtered_df[filtered_df[dropdown_id_list[index]]==dropdowns[index]]
    
    return [
        sorted(filtered_df[dropdown_id_list[index]].unique()) 
        for index in range(len(dropdown_id_list))
    ]


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




@app.callback(
    Output({'type':'scatter_map_box','page':'dashboard','index':ALL}, 'figure'),
    Input({'type':'dropdown','page':'dashboard','index':ALL}, 'value'),
    prevent_initial_call=True
)
def scatter_map_filter(dropdowns):
    dropdown_id_list = [id['id']['index'] for id in dash.callback_context.inputs_list[0]]
    filtered_df = df
    for index in range(len(dropdown_id_list)):
        if dropdowns[index]:
            filtered_df = filtered_df[filtered_df[dropdown_id_list[index]]==dropdowns[index]]
    
    return [
        scatter_map_box(
            latitude=filtered_df.Lat.to_numpy(strict=True)[:200000],
            longitude=filtered_df.Lng.to_numpy(strict=True)[:200000]
        )
    ]



@app.callback(
    Output(Number_range_AIO.ids.input_min(MATCH), 'min'),
    Output(Number_range_AIO.ids.input_max(MATCH), 'max'),
    Input({'type':'dropdown','page':'dashboard','index':ALL}, 'value'),
    prevent_initial_call=True
)
def number_range_filter(dropdowns):
    dropdown_id_list = [id['id']['index'] for id in dash.callback_context.inputs_list[0]]
    filtered_df = df
    for index in range(len(dropdown_id_list)):
        if dropdowns[index]:
            filtered_df = filtered_df[filtered_df[dropdown_id_list[index]]==dropdowns[index]]
    print(filtered_df.price.min(), filtered_df.price.max())
    return filtered_df.price.min(), filtered_df.price.max()