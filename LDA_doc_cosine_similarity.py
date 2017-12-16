# -*- coding: utf-8 -*-
import numpy as np

class LDA_Similarity(object):

    def __init__(self, doc_topic_portion_output_file_path=""):
        self.doc_topic_portion_output_file_path = doc_topic_portion_output_file_path
        self.theta_portions = {}
        
        self.read_LDA_theta_doc_topic_portion()
    
    def read_LDA_theta_doc_topic_portion(self):
        dataFile = open(self.doc_topic_portion_output_file_path, 'r', encoding='utf-8')
        number_of_topic = 0
        for lineIndex, line in enumerate(dataFile):
            if line.startswith('number_of_topic='):
                number_of_topic = int(line.split('=')[1])
            else:
                splits = line.split('\t')
                doc_id = int(splits[0])
                theta_portion  = []
                for topic_index in range(1, number_of_topic+1):
                    portion_splits = splits[topic_index].split(':')
                    theta_portion.append(float(portion_splits[1]))
                self.theta_portions[doc_id] = np.array(theta_portion)
        print('Fetching total topics -> [{}], theta portions -> [{}]'.format(number_of_topic, len(self.theta_portions)))
    
    #cal_cos_sim
    def cal_cos_sim(self, doc_a, doc_b):
        	dot_product = np.dot(doc_a, doc_b)
        	norm_a = np.linalg.norm(doc_a)
        	norm_b = np.linalg.norm(doc_b)
        	return dot_product / (norm_a * norm_b)
    
    
#def main():
#    
#    doc_topic_portion_output_file_path = 'PPageRank-PathSim/data/dblp/doc_topic_portions.txt'
#    lda_similarity = LDA_Similarity(doc_topic_portion_output_file_path)
#    simScore = lda_similarity.cal_cos_sim(lda_similarity.theta_portions[2097194], 
#                                          lda_similarity.theta_portions[2097195])
#    print('Cosine similarity between 2 given documents -> [{}]'.format(simScore))
#
#main()


