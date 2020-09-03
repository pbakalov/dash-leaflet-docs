import dash
import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx

from dash.dependencies import Output, Input
from dash_leaflet.geojson import choropleth
from dash_transcrypt import inject_js, module_to_props


def get_info(feature=None):
    header = [html.H4("US Population Density")]
    if not feature:
        return header + ["Hoover over a state"]
    return header + [html.B(feature["properties"]["name"]), html.Br(),
                     "{:.3f} people / mi".format(feature["properties"]["density"]), html.Sup("2")]


marks = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)
# Create colorbar.
ctg = ["{}+".format(mark, marks[i + 1]) for i, mark in enumerate(marks[:-1])] + ["{}+".format(marks[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
# Create geojson.
js = module_to_props(choropleth, colorscale=colorscale, marks=marks, style=style, color_prop="density")
geojson = dl.GeoJSON(url="/assets/us-states.json",  # url to geojson file
                     options=dict(style=choropleth.discrete),  # how to style each polygon
                     zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                     zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                     hoverStyle=dict(weight=5, color='#666', dashArray=''),  # special style applied on hover
                     id="geojson")
# Create info control.
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})
# Create app.
app = dash.Dash(prevent_initial_callbacks=True)
app.layout = html.Div([dl.Map(children=[dl.TileLayer(), geojson, colorbar, info])],
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map")
inject_js(app, js)


@app.callback(Output("info", "children"), [Input("geojson", "hover_feature")])
def info_hover(feature):
    return get_info(feature)


if __name__ == '__main__':
    app.run_server()