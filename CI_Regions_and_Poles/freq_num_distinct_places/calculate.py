'''
Created on Jun 19, 2014

@author: sscepano
'''
import numpy as np
########################################################
### recalculate frequency and num visited places per admin unit
### and sum the subprefs into regions OR development poles
########################################################
from collections import defaultdict

########################################################
# just save this output for development poles, separate Abidjan
########################################################
def save_dev_poles_user_stats():
    
    pole_stats = calculate_dev_pole_stat()
    
    file_name = "/home/sscepano/Project7s/D4D/CI/user_stats/Poles_median/dev_pole_fq_numDistSubpref_median.tsv"
    f = open(file_name, "w")
    
    for pole in pole_stats.keys():
        f.write(str(pole) + '\t' + str(pole_stats[pole][0]) + '\t' + str(pole_stats[pole][1]) + '\n')
        
 
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
    user_home = read_in_user_home()
    
    pole_stats = defaultdict(int)
    
    for pole in range(12):
        pole_stats[pole] = defaultdict(int)
    
    for user in user_stats.keys():
        print user
        subpref = user_home[user]
        if subpref == -1 or subpref == 0:
            continue
        if subpref <> 60:
            pole = region_pole[subpref_region[subpref]]
        else: 
            pole = 11
## this one was testing and found problem due to -1 
        if pole == 0:
            print user, subpref, subpref_region[subpref], region_pole[subpref_region[subpref]]
        else:
            pole_stats[pole][0] = pole_stats[pole].get(0, [])
            pole_stats[pole][1] = pole_stats[pole].get(1, [])
            pole_stats[pole][0].append(user_stats[user][0])
            pole_stats[pole][1].append(user_stats[user][1])
    
    pole_stats_fin = defaultdict(int)
    

        
    for pole in pole_stats.keys():
        stats1 = np.array(pole_stats[pole][0])
        stats2 = np.array(pole_stats[pole][1])
        pole_stats_fin[pole] = (np.median(stats1), np.median(stats2))
        
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
# read in user freq and num distinct places
########################################################
def read_in_user_stats():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/user_stats/OUTPUTfiles/user_frequency_numDistinctSUBPREFvisited.csv"
    f = open(file_name, "r")
    
    user_stat = defaultdict(int)
    
    for line in f:
        user, fq, dist = line.split(',')
        user = int(user)
        fq = int(fq)
        dist = int(dist)
        
        user_stat[user] = (fq, dist)
    
    return user_stat


########################################################
# read in user freq and num distinct places
########################################################
def read_in_user_home():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/urban_rural/divide_by_home/OUTPUT_files/users_home.tsv"
    f = open(file_name, "r")
    
    user_home = defaultdict(int)
    
    for line in f:
        user, home = line.split('\t')
        user = int(user)
        home = int(home)
        
        user_home[user] = home
    
    return user_home



# calculate_dev_pole_stat()
save_dev_poles_user_stats()