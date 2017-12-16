#Xinbo Wu
#Personalized PageRank for APVPA

from Utility import *
from Personalized_PageRank import *

def main():
    #use APVPA'
    
    #small dataset
    #net_file_name = "data/small/APVPA.txt"
    #name_ID_file_name = "data/small/author.txt"
    
    #medium dataset
    #net_file_name = "data/medium/APVPA.txt"
    #name_ID_file_name = "data/medium/author.txt"
    
    #large dataset
    net_file_name = "data/APVPA.txt"
    name_ID_file_name = "data/author.txt"
    
    #name1 = "Author_1"
    #name1 = "Mike"
    name1 = "Christos Faloutsos"
    #name2 = "AnHai Doan"

    p_prank = P_PageRank(net_file_name, name_ID_file_name, c=0.15)

    p_prank.set_preference([name1])

    #Find top 10 similar researchers for Christos Faloutsos using APVPA
    #print "Find top 10 similar researchers for ", name1, " using APVPA" 
    p_prank.run(num_iter=10)

    key = p_prank.name_ID_dict[name1]
    
    #print p_prank.v[key]

    result = p_prank.find_top_n(15)

    sorted_result = sorted(result, key=result.__getitem__)

    for i in range(len(sorted_result)):
        key = sorted_result[len(sorted_result)-1-i]
        print('{}\t{}'.format(p_prank.ID_name_dict[key], result[key]))

#    p_prank.set_preference([name2])
#
#    #Find top 10 similar researchers for AnHai Doan using APVPA
#    print "Find top 10 similar researchers for ", name2, " using APVPA"
#    p_prank.run(num_iter=10)
#    
#    result = p_prank.find_top_n(10)
#
#    sorted_result = sorted(result, key=result.__getitem__)
#
#    for i in xrange(len(sorted_result)):
#        key = sorted_result[len(sorted_result)-1-i]
#        print i+1, ". ", p_prank.ID_name_dict[key], '%.15f' % result[key]

main()
