'''
Created on Jun 17, 2014

@author: sscepano
'''
########################################################
### here we read in the previous output for commuting 
### and sum the subprefs into regions OR development poles
########################################################
from collections import defaultdict

########################################################
# just save this output for development poles, separate Abidjan
########################################################
def save_dev_poles_commuters():
    
    dev_poles_work_commuters, dev_poles_home_commuters = calculate_dev_poles_commuters()
    
    file_name = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/dev_pole_num_towork_commuters.tsv"
    f = open(file_name, "w")
    
    for pole in dev_poles_work_commuters.keys():
        f.write(str(pole) + '\t' + str(dev_poles_work_commuters[pole]) + '\n')
        
    file_name2 = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/dev_pole_num_fromhome_commuters.tsv"
    f2 = open(file_name2, "w")
    
    for pole in dev_poles_home_commuters.keys():
        f2.write(str(pole) + '\t' + str(dev_poles_home_commuters[pole]) + '\n')

########################################################
# just save this output
########################################################
def save_region_commuters():
    
    region_work_commuters, region_home_commuters = calculate_region_commuters()
    
    file_name = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/region_num_towork_commuters.tsv"
    f = open(file_name, "w")
    
    for region in region_work_commuters.keys():
        f.write(str(region) + '\t' + str(region_work_commuters[region]) + '\n')
        
    file_name2 = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/region_num_fromhome_commuters.tsv"
    f2 = open(file_name2, "w")
    
    for region in region_home_commuters.keys():
        f2.write(str(region) + '\t' + str(region_home_commuters[region]) + '\n')
        
        
########################################################
# sum subpref work into region work commute for development poles, separate Abidjan
########################################################        
def calculate_dev_poles_commuters():
    
    subpref_work_commuters, subpref_home_commuters = read_in_subpref_commuters()
    subpref_region = read_in_subpref_region()
    
    region_pole = read_in_region_poles_mapping()
    
    dev_pole_towork_commuters = defaultdict(int)
    dev_pole_fromhome_commuters = defaultdict(int)
    
    Abijan = 60
    Abijan_pole = 11
    
    dev_pole_towork_commuters[Abijan_pole] = subpref_work_commuters[Abijan]
    
    for subpref in subpref_work_commuters.keys():
        if subpref <> Abijan:
            dev_pole_towork_commuters[region_pole[subpref_region[subpref]]] += subpref_work_commuters[subpref]
            
    dev_pole_fromhome_commuters[Abijan_pole] = subpref_home_commuters[Abijan]
        
    for subpref in subpref_home_commuters.keys():
        if subpref <> Abijan:
            dev_pole_fromhome_commuters[region_pole[subpref_region[subpref]]] += subpref_home_commuters[subpref]
        
    return dev_pole_towork_commuters, dev_pole_fromhome_commuters


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

########################################################
# sum subpref work into region work commute
########################################################        
def calculate_region_commuters():
    
    subpref_work_commuters, subpref_home_commuters = read_in_subpref_commuters()
    subpref_region = read_in_subpref_region()
    
    region_towork_commuters = defaultdict(int)
    region_fromhome_commuters = defaultdict(int)
    
    for subpref in subpref_work_commuters.keys():
        region_towork_commuters[subpref_region[subpref]] += subpref_work_commuters[subpref]
        
    for subpref in subpref_home_commuters.keys():
        region_fromhome_commuters[subpref_region[subpref]] += subpref_home_commuters[subpref]
        
    return region_towork_commuters, region_fromhome_commuters

########################################################
# just pick up the previous output
########################################################
def read_in_subpref_commuters():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/work_num_commuters.tsv"
    f = open(file_name, "r")
    
    file_name2 = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/home_num_commuters.tsv"
    f2 = open(file_name2, "r")
    
    subpref_work_commuters = defaultdict(int)
    subpref_home_commuters = defaultdict(int)
    
    for line in f:
        subpref, commuters = line.split('\t')
        commuters = int(commuters)
        subpref = int(subpref)
        
        subpref_work_commuters[subpref] = commuters
        
    for line in f2:
        subpref, commuters = line.split('\t')
        commuters = int(commuters)
        subpref = int(subpref)
        
        subpref_home_commuters[subpref] = commuters
    
    return subpref_work_commuters, subpref_home_commuters

########################################################
# mask for subprefs into regions
########################################################
def read_in_subpref_region():
                  
    file_name = "/home/sscepano/DATA SET7S/D4D/Regions/Region_subprefs_mapping.csv"
    f = open(file_name, "r")
    
    subpref_region = defaultdict(int)
    
    for line in f:
        region, subpref = line.split('\t')
        region = int(region)
        subpref = int(subpref)
        
        subpref_region[subpref] = region
    
    return subpref_region


# save_region_commuters()
save_dev_poles_commuters()