'''
Created on Jun 16, 2014

@author: sscepano
'''
from collections import defaultdict


def save_num_users_per_region():
    
    subpref_region = read_in_subpref_region()
    subpref_users = read_in_subpref_num_users()
    
    region_users = defaultdict(int)
    
    for subpref in subpref_region.keys():
        region_users[subpref_region[subpref]] += subpref_users[subpref]
        
    file_name = "/home/sscepano/Project7s/D4D/CI/users_population_density/region_num_users.tsv"
    f = open(file_name, "w")
    
    for region in region_users.keys():
        f.write(str(region) + '\t' + str(region_users[region]) + '\n')
        
        
def save_comparison():
    
    file_name = "/home/sscepano/Project7s/D4D/CI/users_population_density/region_num_users.tsv"
    f = open(file_name, "r")
    
    region_users = defaultdict(int)
    
    for line in f:
        region, users = line.split('\t')
        region = int(region)
        users = int(users)
        region_users[region] = users
        
    file_name2 = "/home/sscepano/DATA SET7S/D4D/Regions/region_id_pop_dens.csv"
    f2 = open(file_name2, "r")
    
    file_name3 = "/home/sscepano/Project7s/D4D/CI/users_population_density/region_pop_vs_num_users.csv"
    f3 = open(file_name3, "w")
    
    for line in f2:
        region_id, population, density = line[:-1].split(',')
        f3.write(line[:-1] + ',' + str(region_users[int(region_id)]) + '\n' )
        

def read_in_subpref_num_users():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/urban_rural/divide_by_home/OUTPUT_files/home_num_users.tsv"
    f = open(file_name, "r")
    
    subpref_users = defaultdict(int)
    
    for line in f:
        user, home = line.split('\t')
        user = int(user)
        home = int(home)
              
        subpref_users[user] = home
    
    return subpref_users

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


# save_num_users_per_region()

# save_comparison()