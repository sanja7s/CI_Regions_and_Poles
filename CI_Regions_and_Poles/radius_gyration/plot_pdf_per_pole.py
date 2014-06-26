'''
Created on Jun 24, 2014

@author: sscepano
'''
from collections import defaultdict, OrderedDict
import matplotlib.pyplot as plt
from os.path import isfile, join

def read_in_rg(file_id):
    
    file_name = "rg_POLE_" + str(file_id) + ".tsv" 
    
    file_loc = "/home/sscepano/Project7s/D4D/CI/user_stats/Rg/perPOLE"
    f_path = join(file_loc,file_name)
    
    nits = []
    its = []
    
    # a loop where we populate those two arrays from the file
    i = 0
    f = open(f_path, 'r')    
    # read the file
    for line in f:
        i = i + 1
        it, nit = line.split('\t')
        nit = float(nit)
        it = int(it)
        nit = int(nit)
        nits.append(nit)
        its.append(it)
        
    return nits, its

def rg_pdf():
    
    file_id_lst = [1,2,3,4,5,6,7,8,9,0]
    plt.figure(1)
    
    for file_id in file_id_lst:
        nits, its = read_in_rg(file_id)
    
        mi = min(nits)
        mx = max(nits)
        print("Minimum radius of gyr ", mi)
        print("Maximum radius of gyr ", mx)
        
        total_nit = float(sum(nits))
        print("Total radius of gyr ", total_nit)
        
        pdf_nits = defaultdict(int)
        
        for j in range(0, len(nits)):
            pdf_nits[nits[j]] += 1
            
        ordered = OrderedDict(sorted(pdf_nits.items(), key=lambda t: t[0]))
        
        nits7s = []
        its7s = []
        
        test = 0
        
        for j in ordered.iterkeys():
            nits7s.append(ordered[j]/float(len(nits)))
            test += ordered[j]/float(len(nits))
            its7s.append(j)
            
        print test
            
    ############################################################################################################################
    # THIS is to plot number of users pdf
    ############################################################################################################################
    
        plt.plot(its7s, nits7s, '.', linewidth=0.5, label= 'P' + str(file_id))
    
    plt.xlabel('rg [km]')
    plt.ylabel('P(rg)')
    plt.legend()   
    
    # this is if we want loglog lot, otheriwse comment and uncomment next line for regular plot file   
    plt.yscale('log')
    plt.xscale('log')
    figure_name = "/home/sscepano/Project7s/D4D/CI/user_stats/Rg/perPOLE/pdf/rg_total.png"
          
    print(figure_name)
    plt.savefig(figure_name, format = "png", dpi=300) 
    
    
rg_pdf()