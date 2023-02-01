import rasterio
import pandas as pd
from rasterstats import zonal_stats
from libs.postcode.extract_postcode import generate_contour


def map_ap_postcode(aq_path, air_pollution):

    postcode_shp, london_poly = generate_contour()
    dataset = rasterio.open(aq_path)
    arr = dataset.read(1)
    affine = dataset.transform

    stats_pd = {
        air_pollution: [],
        'postcode': [],
        'polygons': []

    }

    for postcode, poly in postcode_shp.items():
        stats = zonal_stats(poly, arr, affine=affine)
        stats_pd[air_pollution].append(stats[0]['mean'])
        stats_pd['postcode'].append(postcode)
        stats_pd['polygons'].append(poly)

    df = pd.DataFrame(stats_pd)
    df = df[['postcode', air_pollution, 'polygons']]

    return df


if __name__ == '__main__':
    aq_raster_path = 'data/pm25.tif'
    output_path = 'data/postcode_pm25.xlsx'
    df = map_ap_postcode(aq_raster_path, 'pm25')
    df.to_excel(output_path, index=False)

