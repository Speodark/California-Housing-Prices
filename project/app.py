from dash import html, dcc
from main_dash import app


# Generate the app layout
def generateAppLayout():
    return html.Div(
        className="container",
        children=[
            dcc.Location(id='url', refresh=False),
        ]
    )


app.layout = generateAppLayout

if __name__ == "__main__":
    app.run_server(debug=True, port=5050, host="0.0.0.0")