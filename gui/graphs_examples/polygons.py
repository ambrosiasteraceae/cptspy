import matplotlib.pyplot as plt
from shapely import Polygon

def gen_polygon(x, y, l):
    return Polygon([(x - l, y - l), (x - l, y + l), (x + l, y + l), (x + l, y - l), ])


poly = gen_polygon(0,0,25)
plt.plot(poly.exterior.xy[0], poly.exterior.xy[1], color='g')

plt.gca().set_aspect('equal')  # Set aspect ratio to 'equal'
plt.show()

