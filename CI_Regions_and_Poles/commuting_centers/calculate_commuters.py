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
# find ratio between to and from commuters
########################################################
def calc_save_subpref_commuters_ratio():
    
    work_com, home_com = read_in_subpref_commuters()
        
    file_name3 = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/subpref_ratio_commuters.tsv"
    f3 = open(file_name3, "w")    
    
    ratio = defaultdict(float)
    
    for subpref in home_com.keys():
        if home_com[subpref] <> 0:
            f3.write(str(subpref) + '\t' +  str(work_com[subpref]/float(home_com[subpref])) + '\n')
            ratio[subpref] = work_com[subpref]/float(home_com[subpref])
        else: 
            f3.write(str(subpref) + '\t' +  str(float(0)) + '\n')
            ratio[subpref] = 0
            
    return ratio
    

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

########################################################
# sum subpref commute ratio for development poles, separate Abidjan
########################################################        
def calc_save_dev_poles_commuter_ratio():
    
    ratio = calc_save_subpref_commuters_ratio()
    subpref_region = read_in_subpref_region()
    
    region_pole = read_in_region_poles_mapping()
    
    dev_pole_ratio = defaultdict(int)
    dev_pole_subprefs = defaultdict(int)
    
    Abijan = 60
    Abijan_pole = 11
    
    dev_pole_ratio[Abijan_pole] = ratio[Abijan]
    dev_pole_subprefs[Abijan_pole] = 1
    
    for subpref in ratio.keys():
        if subpref <> Abijan and subpref <> 0:
            pole = region_pole[subpref_region[subpref]]
            dev_pole_ratio[pole] += ratio[subpref]
            dev_pole_subprefs[pole] += 1
            
    file_name3 = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/pole_ratio_commuters.tsv"
    f3 = open(file_name3, "w")      
    
    for pole in dev_pole_ratio.keys():
        if dev_pole_subprefs[pole] <> 0:
            f3.write(str(pole) + '\t' +  str(dev_pole_ratio[pole]/float(dev_pole_subprefs[pole])) + '\n')
        
    return dev_pole_ratio 

### do remember to take care about Abijan, manually
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
        region, subpref = line.split(',')
        region = int(region)
        subpref = int(subpref)
        
        subpref_region[subpref] = region
    
    return subpref_region

########################################################
# just pick up the previous output -- this one we need for pole 2 pole commuting
########################################################
def read_in_home_work_output():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/urban_rural/home_work/OUTPUT_files/users_work_home.tsv"
    f = open(file_name, "r")
    
    user_home_work = defaultdict(int)
    
    for line in f:
        user, home, work, nothing = line.split('\t')
        user = int(user[:-1])
        home = int(home)
        work = int(work)
        
        user_home_work[user] = defaultdict(int)
        user_home_work[user][0] = home
        user_home_work[user][1] = work
    
    return user_home_work

def read_in_region_num_users():
    
    file_name = "/home/sscepano/Project7s/D4D/CI/users_population_density/region_num_users.tsv"
    f = open(file_name, "r")
    
    region_users = defaultdict(int)
    
    for line in f:
        region, users = line.split('\t')
        users = int(users)
        region = int(region)
        
        region_users[region] = users
    
    return region_users

def calc_save_pole_users():
    
    region_users =  read_in_region_num_users()
    region_pole = read_in_region_poles_mapping()
    
    pole_users = defaultdict(int)

    Abijan_users = 153192
    Abijan_pole = 11
    Lagunes_pole = 9
    
    for region in region_pole.keys():
        pole = region_pole[region]
        pole_users[pole] += region_users[region]
        
    pole_users[Lagunes_pole] -= Abijan_users
    pole_users[Abijan_pole] = Abijan_users
    
    file_name = "/home/sscepano/Project7s/D4D/CI/users_population_density/pole_num_users.tsv"
    f = open(file_name, "w")
    
    for pole in pole_users.keys():
        f.write(str(pole) + '\t' + str(pole_users[pole]) + '\n')
    
    return pole_users
        
    
    

def pole2pole_commuting():
    
    user_home_work = read_in_home_work_output()
    subpref_region = read_in_subpref_region()
    region_pole = read_in_region_poles_mapping()
    pole_users = calc_save_pole_users()
    
    pole2pole = defaultdict(int)
    pole2pole['out'] = defaultdict(int)
    pole2pole['in'] = defaultdict(int)
    
    Abijan = 60
    Abijan_pole = 11
    
    for user in user_home_work.keys():
        home = user_home_work[user][0]
        work = user_home_work[user][1]
        if home <> work and home <> -1 and work <> -1:
            home_pole = region_pole[subpref_region[home]]
            work_pole = region_pole[subpref_region[work]]
            if home == Abijan:
                home_pole = Abijan_pole
            if work == Abijan:
                work_pole = Abijan_pole
            if home_pole <> work_pole: 
                if work_pole == Abijan:
                    print "A", home_pole
                pole2pole['out'][home_pole] += 1
                pole2pole['in'][work_pole] += 1
                
    file_name = "/home/sscepano/Project7s/D4D/CI/commuting_centers/Pole/pole_out_commuters.tsv"
    f = open(file_name, "w")      
    
    file_name2 = "/home/sscepano/Project7s/D4D/CI/commuting_centers/Pole/pole_in_commuters.tsv"
    f2 = open(file_name2, "w")
    
    file_name3 = "/home/sscepano/Project7s/D4D/CI/commuting_centers/Pole/pole_out_commuters_percent.tsv"
    f3 = open(file_name3, "w")     
    
    file_name4 = "/home/sscepano/Project7s/D4D/CI/commuting_centers/Pole/pole_in_commuters_percent.tsv"
    f4 = open(file_name4, "w")  
    
    for pole in pole2pole['out'].keys():
        f.write(str(pole) + '\t' +  str(pole2pole['out'][pole]) + '\n')
        
    for pole in pole2pole['in'].keys():
        f2.write(str(pole) + '\t' +  str(pole2pole['in'][pole]) + '\n')
        f3.write(str(pole) + '\t' +  str(float(pole2pole['out'][pole])/pole_users[pole]) + '\n')
        f4.write(str(pole) + '\t' +  str(float(pole2pole['in'][pole])/pole_users[pole]) + '\n')


# save_region_commuters()
# save_dev_poles_commuters()

# calc_save_dev_poles_commuter_ratio()

pole2pole_commuting()