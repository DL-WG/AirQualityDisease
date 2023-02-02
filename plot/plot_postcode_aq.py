import json
import pandas as pd
import plotly.express as px


if __name__ == '__main__':

    # DOC
    # https://plotly.com/python-api-reference/generated/plotly.express.choropleth

    # pollutant = 'pm25'
    pollutant = 'no2'

    data_path = f'./data/postcode_{pollutant}.xlsx'
    data = pd.read_excel(data_path)
    data_min = data[pollutant].min()
    data_max = data[pollutant].max()

    with open('./data/postcode_district_polygons.geojson') as f:
        regions = json.load(f)

    fig = px.choropleth(
        data,
        geojson=regions,
        locations='postcode',
        featureidkey='properties.name',
        color=pollutant,
        color_continuous_scale='viridis',
        range_color=(0, data_max),
        scope='europe',
        projection='natural earth',
        basemap_visible=False,
        title=f'Concentration of {pollutant.upper()}',
        fitbounds='locations'
    )
    fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
    fig.show()
    pollutant
