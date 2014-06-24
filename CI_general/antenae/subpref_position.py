'''
Created on Jun 24, 2014

@author: sscepano
'''
###########################################################################################################
### find for each antenae in which subpref it is
###########################################################################################################

from collections import defaultdict
from shapelib import ShapeFile
import dbflib
from os.path import isfile, join

from shapely.geometry import Polygon, Point 

def map_antenae():
    
    shp = ShapeFile(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
#     dbf = dbflib.open(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
    
###########################################################################################################
### test a single antenae
###########################################################################################################
    
    Point1 = Point(-3.303137,   9.802884)
    poly = shp.read_object(218).vertices()[0]
    print poly
    poly = Polygon(poly)
    print poly.contains(Point1)
 
 
###########################################################################################################
### find for all antenae
###########################################################################################################    
    antenae_pos = read_in_ant_pos_file()
    Point_antenae = defaultdict(int)
     
    file_name = "/home/sscepano/Project7s/D4D/CI/antenae/antenae_subpref.tsv"
    f = open(file_name, "w")
    
    # put antenae to points for python polygon check 
    for ant in antenae_pos.keys():
        Point_antenae[ant] = Point(antenae_pos[ant][0], antenae_pos[ant][1])
          
    for ant in Point_antenae.keys():    
        Point1 = Point_antenae[ant]
 
    # go through the shapes and make python polygon from them and then check in point is in
    for npoly in range(shp.info()[0]):
        shp_object = shp.read_object(npoly)
        verts7s = shp_object.vertices()[0]
        poly7s = Polygon(verts7s)
         
        if poly7s.contains(Point1):
            print "found", npoly+1
            f.write(str(ant) + '\t' + str(npoly + 1) + '\n')
            break
    return


def read_in_ant_pos_file():
    
    ant_pos_data = defaultdict(int)
    for i in range(1239):
        ant_pos_data[i] = defaultdict(int)
    
    D4D_path_SET3 = "/home/sscepano/DATA SET7S/D4D"
    file_name = "ANT_POS.TSV"
    f_path = join(D4D_path_SET3,file_name)
    if isfile(f_path) and file_name != '.DS_Store':
            file7s = open(f_path, 'r')
            for line in file7s:
                ant, lon, lat = line.split('\t')
                ant = int(ant)
                lon = float(lon)
                lat = float(lat)
                ant_pos_data[ant][0] = lon
                ant_pos_data[ant][1] = lat
                
    return ant_pos_data


map_antenae()