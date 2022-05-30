from dash import html, dcc
from main_dash import app
from pages.dashboard import dashboard

# Generate the app layout
def generateAppLayout():
    return html.Div(
        className="container",
        children=[
            dcc.Location(id='url', refresh=False),
            dashboard()
        ]
    )


app.layout = generateAppLayout

if __name__ == "__main__":
    app.run_server(debug=True, port=5050, host="0.0.0.0")