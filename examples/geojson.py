import dash
import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx

from dash.dependencies import Output, Input

# Generate some in-memory data.
bermuda = dlx.markers_to_geojson([dict(lat=32.299507, lon=-64.790337)])
biosfera = dlx.geojson_to_geobuf(dlx.markers_to_geojson([dict(lat=29.015, lon=-118.271)]))
# Create example app.
app = dash.Dash()
app.layout = html.Div([
    dl.Map(center=[39, -98], zoom=4, children=[
        dl.TileLayer(),
        dl.GeoJSON(data=bermuda),  # in-memory geojson (slowest option)
        dl.GeoJSON(data=biosfera, format="geobuf"),  # in-memory geobuf (smaller payload than geojson)
        dl.GeoJSON(url="/assets/us-state-capitals.json", id="capitals"),  # geojson resource (faster than in-memory)
        dl.GeoJSON(url="/assets/us-states.pbf", format="geobuf", id="states"),  # geobuf resource (fastest option)
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map"),
    html.Div(id="state"), html.Div(id="capital")
])


@app.callback(Output("capital", "children"), [Input("capitals", "featureClick")])
def capital_click(feature):
    if feature is not None:
        return f"You clicked {feature['properties']['name']}"


@app.callback(Output("state", "children"), [Input("states", "featureHover")])
def state_hover(feature):
    if feature is not None:
        return f"{feature['properties']['name']}"


if __name__ == '__main__':
    app.run_server(port=7778)
