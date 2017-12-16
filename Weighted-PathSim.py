# -*- coding: utf-8 -*-

from Utility import *
from LDA_doc_cosine_similarity import LDA_Similarity
import numpy as np
import operator

class PathSim(object):
    '''
        input files: 
        0: relation
        1: author
        2: venue
        3: term
    '''
    def __init__(self, file_names=[]):
        
        
        self.doc_topic_portion_output_file_path = 'data/dblp/doc_topic_portions.txt'
        self.lda_similarity = LDA_Similarity(self.doc_topic_portion_output_file_path)
        
        self.author_paper_maps = file_to_dict(file_names[0])
        self.paper_author_maps = file_to_reverse_dict(file_names[0])
        
        
        self.paper_venue_maps = file_to_dict(file_names[1])
        self.venue_paper_maps = file_to_reverse_dict(file_names[1])
        
        self.author_dict = make_ID_name_dict(file_names[2])
        self.paper_dict = make_ID_name_dict(file_names[3])
        self.venue_dict = make_ID_name_dict(file_names[4])

        self.author_name_ID = make_name_ID_dict(file_names[2])
 

#        for author in self.author_paper_maps.keys():
#            for paper_of_author in self.author_paper_maps[author]:        
#                if paper_of_author in self.paper_venue_maps:            
#                    submit_at_venue = self.paper_venue_maps[paper_of_author][0]            
#                    if author in self.author_venue:
#                        if submit_at_venue in self.author_venue[author]:
#                            self.author_venue[author][submit_at_venue] += 1
#                            self.author_venue_paper_details[author][submit_at_venue].append(paper_of_author)
#                        else:
#                            self.author_venue[author].update({submit_at_venue:1})
#                            self.author_venue_paper_details[author].update({submit_at_venue:[paper_of_author]})
#                    else:
#                        self.author_venue.update({author:{submit_at_venue:1}})
#                        self.author_venue_paper_details.update({author: {submit_at_venue:[paper_of_author]}})
        
                                

    def cal_doc_sim_score(self, source_author_id, target_author_id, venue_id):
        avg_sim_score = 0
        sim_scores = []
        for source_doc in self.author_venue_paper_details[source_author_id][venue_id]:
            if int(source_doc) in self.lda_similarity.theta_portions:
                if venue_id in self.author_venue_paper_details[target_author_id]:
                    for target_doc in self.author_venue_paper_details[target_author_id][venue_id]:
                        if int(target_doc) in self.lda_similarity.theta_portions:
                            sim_score = self.lda_similarity.cal_cos_sim(self.lda_similarity.theta_portions[int(source_doc)], 
                                                                                self.lda_similarity.theta_portions[int(target_doc)])
                            if sim_score is not None:
                                sim_scores.append(sim_score)
        if len(sim_scores) > 0:
            avg_sim_score = np.mean(sim_scores)
            
        return avg_sim_score   
    
    #run_path_sim
    def run_path_sim(self, author_name=""):
        
        self.author_venue = dict()
        self.author_venue_paper_details = dict()
        
        for author in self.author_paper_maps.keys():
            for paper_of_author in self.author_paper_maps[author]:        
                if paper_of_author in self.paper_venue_maps:            
                    submit_at_venue = self.paper_venue_maps[paper_of_author][0]            
                    if author in self.author_venue:
                        if submit_at_venue in self.author_venue[author]:
                            self.author_venue[author][submit_at_venue] += 1
                            self.author_venue_paper_details[author][submit_at_venue].append(paper_of_author)
                        else:
                            self.author_venue[author].update({submit_at_venue:1})
                            self.author_venue_paper_details[author].update({submit_at_venue:[paper_of_author]})
                    else:
                        self.author_venue.update({author:{submit_at_venue:1}})
                        self.author_venue_paper_details.update({author: {submit_at_venue:[paper_of_author]}})
        
        self.target_author_name = author_name
        self.target_author_ID = self.author_name_ID[author_name]
        self.result = dict()
        
        for author in self.author_venue.keys():
            
            tmp_meta_path_count = 0
            tmp_target_self_path_count = 0
            tmp_author_self_path_count = 0
            tmp_common_venue = []
            
            
            for venue in self.author_venue[self.target_author_ID].keys():
                
                if  venue in self.author_venue[author]:
                    
                    tmp_common_venue.append(venue)
                    tmp_meta_path_count += float(
                            self.author_venue[author][venue])*float(self.author_venue[self.target_author_ID][venue])                        
                    tmp_author_self_path_count +=  float((
                            self.author_venue[author][venue]))**2
                    
                tmp_target_self_path_count +=  float((self.author_venue[self.target_author_ID][venue]))**2
                                                    
                
            s = 2*float(tmp_meta_path_count)/float(tmp_target_self_path_count+tmp_author_self_path_count)
            #print('Similarity score {} -> {}: [{}]'.format(self.target_author_name, author, s))
            self.result.update({author:s})

    
     #run_restricted_path_sim
    def run_restricted_path_sim(self, author_name="", constraint_topic_id=0):
        
        self.author_venue = dict()
        self.author_venue_paper_details = dict()
        self.author_venue_portion = dict()
        
        for author in self.author_paper_maps.keys():
            
            for paper_of_author in self.author_paper_maps[author]:  
                
                if paper_of_author in self.paper_venue_maps:
                    
                    if int(paper_of_author) in self.lda_similarity.theta_portions:
                        theta_portion_of_paper = self.lda_similarity.theta_portions[int(paper_of_author)]
                        # find the dominant topic
                        index, max_value = max(enumerate(theta_portion_of_paper), key=operator.itemgetter(1))
            
                        if constraint_topic_id == index:                            
                            
                            submit_at_venue = self.paper_venue_maps[paper_of_author][0]        
                            
                            self.author_venue_portion.update({author:{submit_at_venue: {paper_of_author: theta_portion_of_paper[index]}}})
                            
                            if author in self.author_venue:
                                if submit_at_venue in self.author_venue[author]:                                    
                                    self.author_venue[author][submit_at_venue] += (1 * theta_portion_of_paper[index])
                                    self.author_venue_paper_details[author][submit_at_venue].append(paper_of_author)
                                    
                                else:                                    
                                    self.author_venue[author].update({submit_at_venue: (1 * theta_portion_of_paper[index])})
                                    self.author_venue_paper_details[author].update({submit_at_venue:[paper_of_author]})
                                   
                            else:
                                self.author_venue.update({author:{submit_at_venue: (1 * theta_portion_of_paper[index])}})
                                self.author_venue_paper_details.update({author: {submit_at_venue:[paper_of_author]}})                  
                                
        
        
        self.target_author_name = author_name
        self.target_author_ID = self.author_name_ID[author_name]
        self.result = dict()
        
        for author in self.author_venue.keys():
            
            tmp_meta_path_count = 0
            tmp_target_self_path_count = 0
            tmp_author_self_path_count = 0
            tmp_common_venue = []
            
            
            for venue in self.author_venue[self.target_author_ID].keys():
                
                if  venue in self.author_venue[author]:
                    
                    tmp_common_venue.append(venue)
                    tmp_meta_path_count += float(
                            self.author_venue[author][venue])*float(self.author_venue[self.target_author_ID][venue])                        
                    tmp_author_self_path_count +=  float((
                            self.author_venue[author][venue]))**2
                    
                tmp_target_self_path_count +=  float((self.author_venue[self.target_author_ID][venue]))**2
                
                                                    
            s = 2*float(tmp_meta_path_count)/float(tmp_target_self_path_count+tmp_author_self_path_count)
            #print('Similarity score {} -> {}: [{}]'.format(self.target_author_name, author, s))
            self.result.update({author:s})
    
    def find_top_n(self, n):
        
        result = dict()
        del(self.result[self.target_author_ID])
        sorted_keys = sorted(self.result, key=self.result.__getitem__)
        
        for key in sorted_keys[len(self.result) - (n+1) :len(self.result)]:
            result.update({key:self.result[key]})

        return result


def main():
    
    output_file = open('output.txt', 'w', encoding='utf-8')
    
    file_names = []
    
    #relations
    file_names.append("data/dblp/author_paper_maps.txt")
    file_names.append("data/dblp/paper_venue_maps.txt")
    
    #objects
    file_names.append("data/dblp/authors.txt")
    file_names.append("data/dblp/papers.txt")
    file_names.append("data/dblp/venues.txt")
    
    #target_author_name = "Philip S. Yu"
    #target_author_name = "Jiawei Han"
    #target_author_name = "Christos Faloutsos"
    target_author_name = "AnHai Doan"
    
    pathSim = PathSim(file_names)

    print("Find top 10 similar researchers for ", target_author_name, " using APVPA")
    
#    print('**Runing traditional PathSim')
#    pathSim.run_path_sim(author_name=target_author_name)
#    result = pathSim.find_top_n(5)
#
#    sorted_result = sorted(result, key=result.__getitem__)
#
#    for i in range(len(sorted_result)):
#        key = sorted_result[len(sorted_result)-1-i]
#        print('{}\t{}'.format(pathSim.author_dict[key], result[key]))
#        output_file.write('{}\t{}\n'.format(pathSim.author_dict[key], result[key]))

#    print("\n")
    
    print('**Runing novel Restricted PathSim')
    for i in range(0, 5):
        pathSim.run_restricted_path_sim(author_name=target_author_name, constraint_topic_id=i)
        result = pathSim.find_top_n(5)
    
        sorted_result = sorted(result, key=result.__getitem__)
    
        for i in range(len(sorted_result)):
            key = sorted_result[len(sorted_result)-1-i]
            print('{}\t{}'.format(pathSim.author_dict[key], result[key]))
            output_file.write('{}\t{}\n'.format(pathSim.author_dict[key], result[key]))
    
        output_file.write('\n')
        print("\n")
        
    output_file.write('\n')
    output_file.close()
    
main() 

