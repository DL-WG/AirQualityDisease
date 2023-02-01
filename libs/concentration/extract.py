import pandas as pd

from pyproj import Transformer


CONC_FILE = {
    'no2':  'laei_LAEI2019v3_CorNOx15_NO2.csv',
    'nox':  'laei_LAEI2019v3_CorNOx15_NOx.csv',
    'pm25': 'laei_LAEI2019v3_CorNOx15_PM25.csv',
    'pm10': 'laei_LAEI2019v3_CorNOx15_PM10d.csv'
    # 'pm10':  'laei_LAEI2019v3_CorNOx15_PM10m.csv'
}


def load_concentration(data_path, transfor=False):

    conc_data = pd.read_csv(data_path)
    x = conc_data['x'].values
    y = conc_data['y'].values

    if transfor:
        transformer = Transformer.from_crs('epsg:27700', 'epsg:4326')
        lats, lons = transformer.transform(x, y)

        # conc_data['latitude'] = lats
        # conc_data['longitude'] = lons
        conc_data['x'] = lats
        conc_data['y'] = lons
        conc_data['code'] = list(range(len(conc_data)))
        # conc_data.drop(columns=['x', 'y'], inplace=True)
    else:
        conc_data['code'] = list(range(len(conc_data)))

    return conc_data
