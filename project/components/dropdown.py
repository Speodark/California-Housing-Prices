from components.card import Card
import dash_mantine_components as dmc
from dash import Output, Input, State, html, dcc, callback, MATCH
from dash.exceptions import PreventUpdate
import dash
import uuid
import ast


class Dropdown(html.Div):  # card will be the "parent" component

    # A set of functions that create pattern-matching callbacks of the subcomponents
    class ids:
        value = lambda aio_id: {
            'component': 'Dropdown_AIO',
            'subcomponent': 'value',
            'aio_id': aio_id
        }

        item = lambda aio_id: {
            'component': 'Dropdown_AIO',
            'subcomponent': 'item',
            'aio_id': aio_id
        }

        for_checkbox = lambda aio_id: {
            'component': 'Dropdown_AIO',
            'subcomponent': 'for_checkbox',
            'aio_id': aio_id
        }


    # Make the ids class a public class
    ids = ids
    

    # Define the arguments of the All-in-One component
    def __init__(
        self,
        className='',
        aio_id=None
    ):
        """Number_range_AIO is an All-in-One component that is composed
        of a parent `card` with 2 `dcc.Input` to represent the minimum and maximum number and a
        `dcc.RangeSlider` ("`range_slider`") component as children.
        - `maximum` - The maximum number. (required)
        - `minimum` - The minimum number. (required)
        - `title` - The component title, a number range of what? price?. (required)
        - `className` - Addition className for the card.
        - `aio_id` - The All-in-One component ID used to generate the markdown and dropdown components's dictionary IDs.

        The All-in-One component dictionary IDs are available as
        - Number_range_AIO.ids.input_max(aio_id)
        - Number_range_AIO.ids.input_min(aio_id)
        - Number_range_AIO.ids.range_slider(aio_id)
        """
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # Define the component's layout
        # pass the childrens to the parent component
        super().__init__(
            children=[
                html.Label(
                    htmlFor=str(self.ids.for_checkbox(aio_id)),
                    children=html.Span('TITLE')
                ),
                html.Ul(
                    className='dropdown__slide dropdown__slide--active',
                    children=[
                        html.Li("something"),
                        html.Li("something"),
                        html.Li("something"),
                        html.Li("something"),
                        html.Li("something")
                    ]
                )
            ],
            className='dropdown ' + className
        )

    
    