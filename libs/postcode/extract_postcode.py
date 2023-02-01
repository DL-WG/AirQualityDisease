import geojson
import shapefile
import shapely
from shapely import Polygon
from shapely.ops import unary_union


# extract the contour of London
def load_London_shp():
    sf = shapefile.Reader('data/London_Ward/London_Ward_WGS84.shp')
    polygons = sf.shapes()
    polygons_list = []
    for polygon in polygons:
        polygon = shapely.geometry.shape(polygon)
        if polygon.geom_type == 'Polygon':
            polygons_list.append(polygon)
    london_area = unary_union(polygons_list)
    return london_area


# extract postcode in London
def extract_postcode(geopath, area):
    postcodes = {}
    with open(geopath) as f:
        gj = geojson.load(f)
    for feature in gj['features']:
        if 'coordinates' in feature['geometry'].keys():
            if len(feature['geometry']['coordinates']) > 1:
                # feature['geometry']['coordinates']
                polygons = []
                for poly in feature['geometry']['coordinates']:
                    if area.intersection(Polygon(poly)):
                        polygons.append(Polygon(poly))
                if len(polygons)>0:
                    postcodes[feature['properties']['name']] = polygons
            else:
                postcode_poly = Polygon(feature['geometry']['coordinates'][0])
                if area.intersection(postcode_poly):
                    # postcode = feature
                    # postcodes.append(postcode)
                    postcodes[feature['properties']['name']] = [postcode_poly]
        else:
            pass
    return postcodes


# get the contours of London and postcode in London
def generate_contour():
    post_path = 'data/postcode/postcode_district_polygons.geojson'
    london_area = load_London_shp()
    postcode_contour = extract_postcode(post_path, london_area)
    polygons = []
    for postcode, polygon in postcode_contour.items():
        polygons.extend(polygon)
    london_contour = unary_union(polygons)
    return postcode_contour, london_contour
