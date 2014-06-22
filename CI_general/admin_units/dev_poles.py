'''
Created on Jun 19, 2014

@author: sscepano
'''
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl
from shapelib import ShapeFile
import dbflib
from matplotlib.collections import LineCollection
from matplotlib import cm as cmx
import matplotlib.colors as colors
from collections import defaultdict

##############################################################################################
### here we just plot development poles and the subprefs on the map with the ids
##############################################################################################

def read_in_subpref_lonlat():
    
    file_name = "/home/sscepano/DATA SET7S/D4D/SUBPREF_POS_LONLAT.TSV"
    f = open(file_name, "r")
    
    subpref_pos = defaultdict(int)
    
    for line in f:
        subpref, lon, lat = line.split('\t')
        subpref = int(subpref)
        lon = float(lon)
        lat = float(lat)
        subpref_pos[subpref] = defaultdict(int)
        subpref_pos[subpref][0] = lon
        subpref_pos[subpref][1] = lat
        
    return subpref_pos


########################################################
# mask for subprefs into regions
########################################################
def read_in_subpref_region():
                  
    file_name = "/home/sscepano/DATA SET7S/D4D/Regions/Region_subprefs_mapping.csv"
    f = open(file_name, "r")
    
    subpref_region = defaultdict(int)
    
    for line in f:
        region, subpref = line.split(',')
        region = int(region)
        subpref = int(subpref)
        
        subpref_region[subpref] = region
    
    return subpref_region

########################################################
# mask for regions to poles
########################################################
def read_in_region_poles_mapping():
    
    file_name = "/home/sscepano/Project7s/D4D/CI/admin_units/regions_and_poles/regions_poles_mapping.csv"
    f = open(file_name, "r")
    
    region_pole = defaultdict(int)
    
    for line in f:
        print line
        region, pole = line.split(',')
        region = int(region)
        pole = int(pole)
        
        region_pole[region] = pole
        
    return region_pole

###########################################################################################
###########################################################################################
###########################################################################################

mpl.rcParams['font.size'] = 5.5

fig = plt.figure(3)
#Custom adjust of the subplots
plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
ax = plt.subplot(111)

m = Basemap(llcrnrlon=-9, \
                llcrnrlat=3.8, \
                urcrnrlon=-1.5, \
                urcrnrlat = 11, \
                resolution = 'h', \
                projection = 'tmerc', \
                lat_0 = 7.38, \
                lon_0 = -5.30)
    

# read the shapefile archive
s = m.readshapefile('/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE', 'subpref')

subpref_coord = read_in_subpref_lonlat()

shp = ShapeFile(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
dbf = dbflib.open(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')

subpref_region = read_in_subpref_region()
region_pole = read_in_region_poles_mapping()

values = range(11)    
jet = cm = plt.get_cmap('jet') 
cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

for npoly in range(shp.info()[0]):
    shpsegs = []
    shpinfo = []
       
    shp_object = shp.read_object(npoly)
    verts = shp_object.vertices()
    rings = len(verts)
    for ring in range(rings):
        lons, lats = zip(*verts[ring])
        x, y = m(lons, lats)
        shpsegs.append(zip(x,y))
        if ring == 0:
            shapedict = dbf.read_record(npoly)
        #print shapedict
        name = shapedict["ID_DEPART"]
        subpref_id = shapedict["ID_SP"]
        # add information about ring number to dictionary.
        shapedict['RINGNUM'] = ring+1
        shapedict['SHAPENUM'] = npoly+1
        shpinfo.append(shapedict)
    lines = LineCollection(shpsegs,antialiaseds=(1,))
    if subpref_id <> 60:
        colorVal = scalarMap.to_rgba(values[region_pole[subpref_region[subpref_id]]])
    else:
        colorVal = 'y'
    print name, subpref_id, colorVal
    lines.set_facecolors(colorVal)
    lines.set_edgecolors('gray')
    lines.set_linewidth(0.1)
    ax.add_collection(lines)  

# data to plot on the map    
lons = []
lats = []
num = []

# if wanna plot subpref ids only
for subpref in range(1,256):
    lons.append(subpref_coord[subpref][0])
    lats.append(subpref_coord[subpref][1])
    num.append(subpref)    

###show or hinde subpref ids
x, y = m(lons, lats)
m.scatter(x, y, color='yellow')
  
for name, xc, yc in zip(num, x, y):
    plt.text(xc, yc, name)

# draw coast lines and fill the continents
# m.drawcoastlines()
# m.fillcontinents()

plt.savefig('/home/sscepano/Project7s/D4D/CI/admin_units/regions_and_poles/poles_subpref_ids.png',dpi=700)
