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
from matplotlib import cm
import matplotlib.colors as colors
from collections import defaultdict

##############################################################################################
### here we just plot the subprefs on the map with the ids, and save department names with
### the corresponding subpref ids in a file
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

mpl.rcParams['font.size'] = 4.4

###########################################################################################
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

# read the file showing how many users we found per each subpref
# file_name = '/home/sscepano/D4D res/ORGANIZED/SET3/Night Homes/Num_of_users_per_home_subpref.tsv'
# f = open(file_name, 'r')
# 
# no_users = {}
# 
# for line in f:
#     subpref, no = line.split('\t')
#     subpref = int(subpref[:-1])
#     no = int(no)
#     no_users.keys().append(subpref)
#     if subpref <> -1:
#         no_users[subpref] = no

# read subpref coordinates

#read the file showing how many users we found per each subpref
file_name2 = '/home/sscepano/Project7s/D4D/CI/admin_units/regions_and_poles/department_names_subpref_ids.tsv'
f2 = open(file_name2, 'w')

subpref_coord = read_in_subpref_lonlat()

shp = ShapeFile(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
dbf = dbflib.open(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')

for npoly in range(shp.info()[0]):
    shpsegs = []
    shpinfo = []
       
    shp_object = shp.read_object(npoly)
    verts = shp_object.vertices()
    rings = len(verts)
    for ring in range(rings):
        lons, lats = zip(*verts[ring])
#        if max(lons) > 721. or min(lons) < -721. or max(lats) > 91. or min(lats) < -91:
#            raise ValueError,msg
        x, y = m(lons, lats)
        shpsegs.append(zip(x,y))
        if ring == 0:
            shapedict = dbf.read_record(npoly)
        #print shapedict
        name = shapedict["ID_DEPART"]
        subpref_id = shapedict["ID_SP"]
        print name, subpref_id
        f2.write(str(name) + '\t' + str(subpref_id) + '\n')
        # add information about ring number to dictionary.
        shapedict['RINGNUM'] = ring+1
        shapedict['SHAPENUM'] = npoly+1
        shpinfo.append(shapedict)
    #print subpref_id
    #print name
    lines = LineCollection(shpsegs,antialiaseds=(1,))
#         lines.set_facecolors(col[subpref_id])
    lines.set_edgecolors('gray')
    lines.set_linewidth(0.1)
    ax.add_collection(lines)  

# data to plot on the map    
lons = []
lats = []
num = []

# if wanna plot number of users whose this is home subpref
# for subpref in no_users.iterkeys():
#     print(subpref)
#     lons.append(subpref_coord[subpref][0])
#     lats.append(subpref_coord[subpref][1])
#     num.append(no_users[subpref])

# if wanna plot subpref ids only
for subpref in range(1,256):
#     if subpref in [22, 32, 38, 49, 51, 72, 81, 83, 87, 88, 98, 105, 111, 112, 135, 136, 221, 239, 245, 255]:
    lons.append(subpref_coord[subpref][0])
    lats.append(subpref_coord[subpref][1])
    num.append(subpref)    
    
x, y = m(lons, lats)
m.scatter(x, y, color='white')

for name, xc, yc in zip(num, x, y):
    # draw the pref name in a yellow (shaded) box
    plt.text(xc, yc, name)

# draw coast lines and fill the continents
# m.drawcoastlines()
# m.fillcontinents()

# m.plot()

# f.close()
# f2.close()

plt.savefig('/home/sscepano/Project7s/D4D/CI/admin_units/subprefs/subpref_ids_7s.png',dpi=500)
