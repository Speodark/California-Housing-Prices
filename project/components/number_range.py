from components.card import Card
from dash import Output, Input, State, html, dcc, callback, MATCH
from dash.exceptions import PreventUpdate
import dash
import uuid
import ast


class Number_range_AIO(Card):  # card will be the "parent" component

    # A set of functions that create pattern-matching callbacks of the subcomponents
    class ids:
        input_max = lambda aio_id: {
            'type': 'Number_range_AIO',
            'subcomponent': 'input_max',
            'aio_id': aio_id
        }
        input_min = lambda aio_id: {
            'type': 'Number_range_AIO',
            'subcomponent': 'input_min',
            'aio_id': aio_id
        }
        range_slider = lambda aio_id: {
            'type': 'Number_range_AIO',
            'subcomponent': 'range_slider',
            'aio_id': aio_id
        }

    # Make the ids class a public class
    ids = ids

    # Define the arguments of the All-in-One component
    def __init__(
        self,
        minimum,
        maximum,
        title,
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
        # Allow developers to pass in their own `aio_id` if they're
        # binding their own callback to a particular component.
        if aio_id is None:
            # Otherwise use a uuid that has virtually no chance of collision.
            # Uuids are safe in dash deployments with processes
            # because this component's callbacks
            # use a stateless pattern-matching callback:
            # The actual ID does not matter as long as its unique and matches
            # the PMC `MATCH` pattern..
            aio_id = str(uuid.uuid4())

        # Define the component's layout
        # pass the childrens to the parent component
        super().__init__(
            children=[
                html.H2(title),
                html.Div(
                    className='number-range__input',
                    children=[
                        html.Div(
                            className='number-range__input--field',
                            children=[
                                html.Span('Min'),
                                dcc.Input(
                                    type='number', 
                                    value=minimum,
                                    min=minimum, 
                                    max=maximum, 
                                    step=None,
                                    debounce=True,
                                    id=self.ids.input_min(aio_id)
                                )
                            ]
                        ),
                        html.Span('-',className='number-range__separator'),
                        html.Div(
                            className='number-range__input--field',
                            children=[
                                html.Span('Max'),
                                dcc.Input(
                                    type='number', 
                                    value=maximum,
                                    min=minimum, 
                                    max=maximum, 
                                    step=None,
                                    debounce=True,
                                    id=self.ids.input_max(aio_id)
                                )
                            ]
                        ),
                    ]
                ),
                dcc.RangeSlider(
                    min=minimum, 
                    max=maximum, 
                    marks=None, 
                    value=[minimum, maximum], 
                    allowCross=False,
                    id=self.ids.range_slider(aio_id),
                    className='number-range__slider'
                )
            ],
            className='number-range ' + className
        )

    # Define this component's stateless pattern-matching callback
    # that will apply to every instance of this component.
    # connects the range values and input values.
    @callback(
        # outputs
        Output(ids.range_slider(MATCH), 'value'),
        Output(ids.input_min(MATCH), 'value'),
        Output(ids.input_max(MATCH), 'value'),
        # inputs
        Input(ids.input_min(MATCH), 'value'),    # input_min_value
        Input(ids.input_max(MATCH), 'value'),    # input_max_value
        Input(ids.range_slider(MATCH), 'value'), # slider_value
        # states
        Input(ids.input_min(MATCH), 'min'),      # minimum
        Input(ids.input_max(MATCH), 'max'),      # maximum
        prevent_initial_call=True
    )
    def update_subcomponents_value(input_min_value, input_max_value, slider_value, minimum, maximum):
        trigger_id = ast.literal_eval(dash.callback_context.triggered[0]["prop_id"].split(".")[0])

        # if the range slider triggered the callback
        if trigger_id['subcomponent'] == 'range_slider':
            print(slider_value)
            return slider_value, min(slider_value), max(slider_value)
            
        else:
            # if the input was a number lower than the minimum or there was no input 
            # we get None.
            if input_min_value is None:
                input_min_value = minimum
            # if the input was a lower value than the absolute minimum value accepted
            elif input_min_value < minimum:
                input_min_value = minimum
            # if the input was a number higher than the maximum or there was no input 
            # we get None.
            if input_max_value is None:
                input_max_value = maximum
            # if the input was a higher value than the absolute maximum value accepted
            elif input_max_value > maximum:
                input_max_value = maximum

            # if the minimum input triggered the callback
            if trigger_id['subcomponent'] == 'input_min':
               
                # if the input was a higher value than the absolute maximum value accepted 
                if input_min_value > maximum:
                    input_min_value = maximum
                    input_max_value = maximum
                # if the input was higher than the current maximum input
                elif input_min_value > input_max_value:
                    input_max_value = input_min_value
                # return the values after the changes
                return [input_min_value, input_max_value], input_min_value, input_max_value

            elif trigger_id['subcomponent'] == 'input_max':
                # if the input was a lower value than the absolute minimum value accepted 
                if input_max_value < minimum:
                    input_max_value = minimum
                    input_min_value = minimum
                # if the input was lower than the current minimum input
                elif input_max_value < input_min_value:
                    input_min_value = input_max_value
                return [input_min_value, input_max_value], input_min_value, input_max_value


    # changes the min and max of the slider if the set min/max of the input labels change
    @callback(
        Output(ids.range_slider(MATCH), 'min'),
        Output(ids.range_slider(MATCH), 'max'),
        Input(ids.input_min(MATCH), 'min'),
        Input(ids.input_max(MATCH), 'max'),
        prevent_initial_call=True
    )
    def update_slider_value(min, max):
        return min,max

            
    