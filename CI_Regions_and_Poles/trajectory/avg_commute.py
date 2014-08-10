'''
Created on Jun 29, 2014

@author: sscepano
'''
from collections import defaultdict
import numpy as np
########################################################
# just save this output for development poles, separate Abidjan
########################################################
def save_dev_poles_user_stats():
    
    pole_stats = calculate_dev_pole_stat()
    
    file_name = "/home/sscepano/Project7s/D4D/CI/user_stats/Poles_avg/dev_pole_avg_commute.tsv"
    f = open(file_name, "w")
    
    for pole in pole_stats.keys():
        f.write(str(pole) + '\t' + str(pole_stats[pole]) + '\n')
        
 
########################################################
# YOU NEED TO RECALCULATE THIS ONE FOR -1 
########################################################          
########################################################
# sum user stats into pole (subpref --> region --> dev pole)
########################################################        
def calculate_dev_pole_stat():
    
    # this dict has tuple elements (fq, dist)
    user_stats = read_in_user_stats()
    subpref_region = read_in_subpref_region()
    region_pole = read_in_region_poles_mapping()
    
    pole_stats = defaultdict(int)
    
    for pole in range(12):
        pole_stats[pole] = []
    
    for subpref in user_stats.keys():
        if subpref == -1 or subpref == 0:
            continue
        if subpref <> 60:
            pole = region_pole[subpref_region[subpref]]
        else: 
            pole = 11
        if pole <> 0:    
            pole_stats[pole].append(user_stats[subpref])
        
    pole_stats_fin = defaultdict(int)
        
    for pole in pole_stats.keys():
        stats = np.array(pole_stats[pole])
        print stats
        pole_stats_fin[pole] = (np.average(stats))
        
    return pole_stats_fin


def read_in_region_poles_mapping():
    
    file_name = "/home/sscepano/Project7s/D4D/CI/admin_units/regions_and_poles/regions_poles_mapping.csv"
    f = open(file_name, "r")
    
    region_pole = defaultdict(int)
    
    for line in f:
        region, pole = line.split(',')
        region = int(region)
        pole = int(pole)
        
        region_pole[region] = pole
        
    print region_pole.values()
        
    return region_pole


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
# read in user avg daily commute er supref
########################################################
def read_in_user_stats():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/user_stats/Traj/avgCommTrajectory.txt"
    f = open(file_name, "r")
    
    user_stat = defaultdict(int)
    
    for line in f:
        subpref, traj = line.split('\t')
        
        try:
            subpref = int(subpref[1:-1])
            traj = float(traj)
            
            if traj <> float("inf"):
                user_stat[subpref] = traj
                print subpref, traj
        except:
            ValueError
            print subpref, traj 
    
    return user_stat


save_dev_poles_user_stats()