import shapely
import matplotlib.pyplot as plt
from shapely.plotting import plot_polygon
from libs.postcode.extract_postcode import generate_contour

postcode_contour, london_contour = generate_contour()
postcode_polygons = []
for postcode, poly in postcode_contour.items():
    postcode_polygons.extend(poly)

postcode_polygons = shapely.geometry.MultiPolygon(postcode_polygons)
fig = plt.figure(1)
ax = fig.add_subplot(111)
plot_polygon(postcode_polygons, add_points=False, alpha=0.5)
plt.show()
plt.savefig('postcode_contour.png')
