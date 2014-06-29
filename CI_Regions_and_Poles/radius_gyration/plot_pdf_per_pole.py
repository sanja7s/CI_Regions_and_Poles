'''
Created on Jun 24, 2014

@author: sscepano
'''
from collections import defaultdict, OrderedDict
import matplotlib.pyplot as plt
from os.path import join
import prettyplotlib as ppl
from scipy import interpolate

from matplotlib.font_manager import FontProperties

fontP = FontProperties()
fontP.set_size('small')

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
    
    file_id_dict = {1: ("Southwest", "-"),2: ("West","-"),3: ("Northwest", "-"),4: ("North", "-"),\
                    5: ("Northeast", "-"),6: ("Central East", "-"),7: ("Central West", "-"),\
                    8: ("Central North", "-") ,9: ("South", "-"), 10: ("Center", "-"), 11: ("Abidjan", "-"), \
                    0: ("ALL", "-")}
    plt.figure(1)
    
    for file_id in file_id_dict.keys():
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
            
        f = interpolate.interp1d(its7s, nits7s, kind="nearest")
            
        print test
            
        xnew = its7s
        ynew = f(its7s) 
    ############################################################################################################################
    # THIS is to plot number of users pdf
    ############################################################################################################################
    
#         ppl.plot(its7s, nits7s, file_id_dict[file_id][1], linewidth=0.5, label= file_id_dict[file_id][0])
        
        ppl.plot(xnew, ynew, file_id_dict[file_id][1], linewidth=0.5, label= file_id_dict[file_id][0])
    
    plt.xlabel('rg [km]')
    plt.ylabel('P(rg)')
    ax = ppl.legend([ppl], "title", prop = fontP)
    ppl.legend(bbox_to_anchor=(1.1, 1.05), prop = fontP)
    
#     ax = ppl.legend()  
    
    # this is if we want loglog lot, otheriwse comment and uncomment next line for regular plot file   
    plt.yscale('log')
    plt.xscale('log')
    figure_name = "/home/sscepano/Project7s/D4D/CI/user_stats/Rg/perPOLE/pdf/rg_per_Pole.png"
          
    print(figure_name)
    plt.savefig(figure_name, format = "png", dpi=300) 
    
    
rg_pdf()