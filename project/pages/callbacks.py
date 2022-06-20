from dash import Input, Output, ALL, State, MATCH, ctx
import vaex
from main_dash import app
import dash
import plotly.graph_objects as go
import plotly.express as px
from components.number_range import Number_range_AIO
import pandas as pd

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

df = vaex.open('assets/data/data.csv.hdf5')

@app.callback(
    Output({'type': 'sales_graph', 'index': ALL}, 'figure'),
    Input({'type':'dropdown','page':'dashboard','index':ALL}, 'value'),
    Input(Number_range_AIO.ids.input_min(ALL), 'value'),
    Input(Number_range_AIO.ids.input_max(ALL), 'value'),
    prevent_initial_call=True
)
def sales_graph_filter(dropdowns, inputs_min, inputs_max):
    #trigger = ctx.triggered_id
    # for dropdown list
    dropdown_id_list = [id['id']['index'] for id in dash.callback_context.inputs_list[0]]
    filtered_df = df
    for index in range(len(dropdown_id_list)):
        if dropdowns[index]:
            filtered_df = filtered_df[filtered_df[dropdown_id_list[index]]==dropdowns[index]]
    # for number range list
    number_range_id_list = [id['id']['aio_id'] for id in dash.callback_context.inputs_list[1]]
    for index in range(len(number_range_id_list)):
        if inputs_min[index] and inputs_max[index]:
            filtered_df = filtered_df[
                (filtered_df[number_range_id_list[index]]>=inputs_min[index]) &
                (filtered_df[number_range_id_list[index]]<=inputs_max[index])
            ]
    # If after filtering the df is empty we can't sort
    if len(filtered_df) > 0:
        filtered_df = filtered_df.sort('followers', ascending=False)[:10]
    return [bar_chart(
        df = filtered_df,
        x_axis_name='id',
        y_axis_name='followers'
    )]


@app.callback(
    Output({'type':'dropdown','page':'dashboard','index':ALL}, 'options'),
    Input({'type':'dropdown','page':'dashboard','index':ALL}, 'value'),
    Input(Number_range_AIO.ids.input_min(ALL), 'value'),
    Input(Number_range_AIO.ids.input_max(ALL), 'value'),
    Input({'type':'scatter_map_box','page':'dashboard','index':ALL}, 'selectedData'),
    prevent_initial_call=True
)
def dropdown_options_filter(dropdowns, inputs_min, inputs_max, scatter_map_selected_data):
    # for dropdown list
    dropdown_id_list = [id['id']['index'] for id in dash.callback_context.inputs_list[0]]
    filtered_dfs = []
    # We need to filter the whole data frame for each dropdown in our dashboard to 
    # see all the options available
    # if we filter by its own value we will remove all the other options
    # for dropdowns 1 2 3 we need to filter dropdown 1 options only by 2 and 3
    # filtered_dfs.append(sorted(filtered_df[dropdown_id].unique()))
    for dropdown_id in dropdown_id_list:
        filtered_df = df
        for index in range(len(dropdown_id_list)):
            if dropdowns[index] and dropdown_id_list[index] != dropdown_id:
                filtered_df = filtered_df[filtered_df[dropdown_id_list[index]]==dropdowns[index]]
        filtered_dfs.append(filtered_df)
    # for the number range list
    number_range_id_list = [id['id']['aio_id'] for id in dash.callback_context.inputs_list[1]]
    for index in range(len(number_range_id_list)):
        if inputs_min[index] and inputs_max[index]:
            for df_index in range(len(filtered_dfs)):
                filtered_dfs[df_index] = filtered_dfs[df_index][
                    (filtered_dfs[df_index][number_range_id_list[index]]>=inputs_min[index]) &
                    (filtered_dfs[df_index][number_range_id_list[index]]<=inputs_max[index])
                ]
    # for Scatter map 
    scatter_map_id_list = [id['id']['index'] for id in dash.callback_context.inputs_list[3]]
    choosen_points_indexs = [point['pointIndex'] for point in scatter_map_selected_data[0]['points']]
    for index in range(len(filtered_dfs)):
        filtered_dfs[index] = filtered_dfs[index][filtered_dfs[index]['index'].isin(choosen_points_indexs)]
    # output for dropdowns sorted
    dd_options = []
    for dropdown_id, filtered_df in zip(dropdown_id_list, filtered_dfs):
        dd_options.append(sorted(filtered_df[dropdown_id].unique()))
    
    return dd_options



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
    Input(Number_range_AIO.ids.input_min(ALL), 'value'),
    Input(Number_range_AIO.ids.input_max(ALL), 'value'),
    prevent_initial_call=True
)
def scatter_map_filter(dropdowns, inputs_min, inputs_max):
    # for dropdown list
    dropdown_id_list = [id['id']['index'] for id in dash.callback_context.inputs_list[0]]
    filtered_df = df
    for index in range(len(dropdown_id_list)):
        if dropdowns[index]:
            filtered_df = filtered_df[filtered_df[dropdown_id_list[index]]==dropdowns[index]]
    # for number range list
    number_range_id_list = [id['id']['aio_id'] for id in dash.callback_context.inputs_list[1]]
    for index in range(len(number_range_id_list)):
        if inputs_min[index] and inputs_max[index]:
            filtered_df = filtered_df[
                (filtered_df[number_range_id_list[index]]>=inputs_min[index]) &
                (filtered_df[number_range_id_list[index]]<=inputs_max[index])
            ]
    print("RETURNING A NEW ONE")
    return [
        scatter_map_box(
            latitude=filtered_df.Lat.to_numpy(strict=True),
            longitude=filtered_df.Lng.to_numpy(strict=True)
        )
    ]



@app.callback(
    Output(Number_range_AIO.ids.input_min(MATCH), 'min'),
    Output(Number_range_AIO.ids.input_max(MATCH), 'max'),
    Input({'type':'dropdown','page':'dashboard','index':ALL}, 'value'),
    Input({'type':'scatter_map_box','page':'dashboard','index':ALL}, 'selectedData'),
    prevent_initial_call=True
)
def number_range_filter(dropdowns, scatter_map_selected_data):
    # for dropdowns
    dropdown_id_list = [id['id']['index'] for id in dash.callback_context.inputs_list[0]]
    filtered_df = df
    for index in range(len(dropdown_id_list)):
        if dropdowns[index]:
            filtered_df = filtered_df[filtered_df[dropdown_id_list[index]]==dropdowns[index]]
    scatter_map_id_list = [id['id']['index'] for id in dash.callback_context.inputs_list[1]]
    choosen_points_indexs = [point['pointIndex'] for point in scatter_map_selected_data[0]['points']]
    filtered_df = filtered_df[filtered_df['index'].isin(choosen_points_indexs)]
    print(type(filtered_df))
    # print()
    print(scatter_map_id_list)
    return filtered_df.price.min(), filtered_df.price.max()