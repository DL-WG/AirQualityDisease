import json
import pandas as pd
import plotly.express as px


if __name__ == '__main__':

    # DOC
    # https://plotly.com/python-api-reference/generated/plotly.express.choropleth

    # disease in ['Cystic Fibrosis', 'COVID', 'ABPA', 'Asthma']
    disease = 'Asthma'

    data_path = f'../data/postcode_diseases.xlsx'
    data = pd.read_excel(data_path)
    data_min = data[disease].min()
    data_max = data[disease].max()

    with open('../data/postcode/postcode_district_polygons.geojson') as f:
        regions = json.load(f)

    fig = px.choropleth(
        data,
        geojson=regions,
        locations='postcode',
        featureidkey='properties.name',
        color=disease,
        color_continuous_scale='viridis',
        range_color=(0, data_max),
        scope='europe',
        projection='natural earth',
        basemap_visible=False,
        title=f'Disease of {disease.upper()}',
        fitbounds='locations'
    )
    fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
    fig.show()
