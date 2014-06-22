'''
Created on Jun 19, 2014

@author: sscepano
'''
###########################################################################################################
### from the commuting graph, we calculate here edges betweenes and plot 10 with highest value
###########################################################################################################

import networkx as nx
from collections import defaultdict, OrderedDict

###########################################################################################################
### this one tried with some output, but there was an error, as subpref id was too high
###########################################################################################################
def map_routes():
    
    G = nx.DiGraph()
    
    routes = read_in_routes()
    
    for i in routes.keys():
        r1 = int(routes[i][0])
        r2 = int(routes[i][1])
        weight = int(routes[i][2])
        G.add_edge(r1,r2, weight = weight)
            
    map_G(G)
    
    return


###########################################################################################################
### this one is the main; calls calculate betweenes and takes 10 highest value edges and plots
###########################################################################################################
def map_betweenes():
    
    routes = calculate_betweenes()
    
    G = nx.DiGraph()
    
    i = 0
    
    for k in routes.keys():
        if i == 20:
            break
        r1 = int(k[0])
        r2 = int(k[1])
        weight = float(routes[k])
        G.add_edge(r1,r2, weight = weight)
        i += 1
            
    map_G(G)
    
    return

###########################################################################################################
### this one does the plotting using Basemap and Shapefiles
###########################################################################################################
def map_G(G):
        
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap
    import matplotlib.cm as cmx
    
    import matplotlib as mpl
    mpl.rcParams['font.size'] = 10.
    mpl.rcParams['axes.labelsize'] = 8.
    mpl.rcParams['xtick.labelsize'] = 6.
    mpl.rcParams['ytick.labelsize'] = 6.
    
    from shapelib import ShapeFile
    import dbflib
    from matplotlib.collections import LineCollection
    from matplotlib import cm
    import matplotlib.colors as colors
     
    ###########################################################################################
    fig = plt.figure(3)
    #Custom adjust of the subplots
    plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
    ax = plt.subplot(111)
    
    m = Basemap(projection='cyl',\
                llcrnrlon=-9, \
                llcrnrlat=3.8, \
                urcrnrlon=-1.5, \
                urcrnrlat = 11, \
                resolution = 'h', \
#                 projection = 'tmerc', \
                lat_0 = 7.38, \
                lon_0 = -5.30)
      
    # read subpref coordinates
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
        
    if G.has_node(-1): 
        G.remove_node(-1)
    if G.has_node(0): 
        G.remove_node(0)
        
###########################################################################################################
### this is the main part: scale weights of # commuters, use colormap by work location and then plot
### all or just the routes with more that 10 commutes 
###########################################################################################################
    
#     max7s = 0
#     min7s = 10000000
#     for u,v,d in G.edges(data=True):
#         if d['weight'] > max7s:
#             max7s = d['weight']
#         if d['weight'] < min7s:
#             min7s = d['weight']
#             
#     max7s = float(max7s)
#     print "max", (max7s)
#     print "min", (min7s)
#     
#     scaled_weight = defaultdict(int)
#     
#     for i in range(len(G.edges())):
#         scaled_weight[i] = defaultdict(int)
#     for u,v,d in G.edges(data=True):
#         scaled_weight[u][v] = (d['weight'] - min7s) / (max7s - min7s)
    
    values = range(256)    
    jet = cm = plt.get_cmap('jet') 
    cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    
    for u, v, d in G.edges(data=True):
#         lo = []
#         la = []  
#         lo.append(subpref_coord[u][0])
#         lo.append(subpref_coord[v][0])
#         la.append(subpref_coord[u][1])
#         la.append(subpref_coord[v][1])
#         x, y = m(lo, la)
#         linewidth7s = scaled_weight[u][v] * 2.5 + 0.25
#         m.plot(x,y, linewidth= linewidth7s)
#         if linewidth7s > 1:
#             print (linewidth7s)
        if d['weight'] >= 0: 
            colorVal = scalarMap.to_rgba(values[v])
#             linewidth7s = scaled_weight[u][v] * 2.5 + 0.35 
#             print u, v,  d['weight'], scaled_weight[u][v]
###########################################################################################################
### no scaling vs scaling the width of the line
###########################################################################################################
#            linewidth7s = d['weight'] / 10   
            m.drawgreatcircle(subpref_coord[u][0], subpref_coord[u][1], \
                              subpref_coord[v][0], subpref_coord[v][1], linewidth= d['weight']*100, color=colorVal)

#     m.drawcoastlines()
    #m.fillcontinents()
        
    plt.savefig('/home/sscepano/Project7s/D4D/CI/commuting_centers/Igor/high_betweenes_routes4.png',dpi=700)
    #plt.show()
    
    ###################################################################################################3
    
    return

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

##########################################################
### these routes did not work
##########################################################
def read_in_routes():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/commuting_centers/Igor/edgeBtwnTop10.txt"
    f = open(file_name, "r")
    
    d = defaultdict(int)
    i = 0
    
    for line in f:
        print line
        r1, r2, btw = line.split(' ')
        r1 = int(r1)
        r2 = int(r2)
        btw = float(btw)
        
        d[i] = defaultdict(int)
        d[i] = (r1,r2,btw)
        
        i += 1
    
    return d

##########################################################
### and save to file you might need later
##########################################################
def save_betweenes():
    
    file_name = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/betweenes_edges.tsv"
    f = open(file_name, "w")
    
    btw = calculate_betweenes()
    
    for el in btw.keys():
        f.write(str(el[0]) + '\t' + str(el[1]) + '\t' + str(btw[el]) + '\n')
                          
    return

##########################################################
### here we recalculate betweenes using networkx
##########################################################
def calculate_betweenes():
    
    file_name = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/commuting_graph.tsv"
    f = open(file_name, "r")
    
    G = nx.DiGraph()
    
    for line in f:
        print line
        r1, r2, w = line.split('\t')
        r1 = int(r1)
        r2 = int(r2)
        w = float(w)
        G.add_edge(r1,r2, weight = w)
        
        
    btw = nx.edge_betweenness_centrality(G, weight = "weight")
    
    ord_btw = OrderedDict(sorted(btw.iteritems(), key=lambda t:t[1], reverse = True))
                          
    return ord_btw

##########################################################
### these routes did not work
##########################################################
# something wrong
# map_routes()

##########################################################
### this works
##########################################################
# calculate_betweenes()
# save_betweenes()
map_betweenes()