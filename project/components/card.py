from dash import html
import itertools

class Card(html.Div):
    def __init__(
        self,
        id=None, 
        className="", 
        style={}, 
        children=None, 
        header=None
    ):
        """Card is a Div component that is composed
        of a styled `card` with the option to recieve children such as graphs/components 
        to put on the dashboard.
        - `id` - component ID.
        - `className` - Addition className for the card.
        - `style` - The dash style if you want to style the card from the python code.
        - `children` - The card childrens everything that is in the card.
        - `header` - The card header if needed.
        """
        if not isinstance(children, list) and header:
            header = html.Span(
                className="card__header",
                children=header
            )
            children = [children]
            children.insert(0, header)
        elif isinstance(children, list) and header:
            children.insert(0, header)
        if id:
            super().__init__(
                id=id,
                className='card ' + className,
                style=style,
                children=children
            )
        else:
            super().__init__(
                className='card ' + className,
                style=style,
                children=children
            )

        

def card(id=None, className="", style={}, children=None, header=None):
    # If the card does not have children but does have a header
    # then create the header 
    if not isinstance(children, list) and header:
        header = html.Span(
            className="card__header",
            children=header
        )
        children = [children]
        children.insert(0, header)
    elif isinstance(children, list) and header:
        children.insert(0, header)
    if id:
        return html.Div(
            id=id,
            className='card ' + className,
            style=style,
            children=children
        )
    else:
        return html.Div(
            className='card ' + className,
            style=style,
            children=children
        )