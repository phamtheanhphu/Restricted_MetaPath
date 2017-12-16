# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from itertools import chain

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

n_samples = 20
n_features = 1000
n_topics = 5
n_top_words = 10

doc_corpus_data_path = 'data/dblp/paper_content_maps.txt'
doc_topic_portion_output_file_path = 'data/dblp/doc_topic_portions.txt'
doc_dict = {}
doc_contents = []

def print_phi(model, feature_names, n_top_words):
    
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        termList = []
        for term in topic.argsort()[:-n_top_words - 1:-1]:
           termList.append(feature_names[term])
        
        print(termList)

    print()

def print_theta(docTopicDisMatrix):
    
    topicHeader = '\t'
    for nTopic in range(0, n_topics):
        topicHeader+='Topic {}\t\t'.format(nTopic)
    
    print(topicHeader)
    
    for indexRow, rowVal in enumerate(docTopicDisMatrix):
        colString = '{}\t'.format(indexRow)
        for nTopic in range(0, n_topics):
           colString+='{}\t'.format(docTopicDisMatrix[indexRow, nTopic])
        print('{}\t'.format(colString))

def load_doc_id_by_content(doc_content):
    doc_local_id = -1
    for doc_index in doc_dict:
        if doc_dict[doc_index] == doc_content:
            doc_local_id = doc_index
            break
    return doc_local_id

def export_theta_2_data_file(docTopicDisMatrix, output_file_path):
    outputDataFile = open(output_file_path, 'w', encoding='utf-8')
    outputDataFile.write('number_of_topic={}\n'.format(n_topics))
    for docIndex, doc in enumerate(docTopicDisMatrix):
        colString = ''
        for nTopic in range(0, n_topics):
           colString+='{}:{}\t'.format(nTopic, docTopicDisMatrix[docIndex, nTopic])
  
        doc_id = load_doc_id_by_content(doc_contents[docIndex])
        outputDataFile.write('{}\t{}\n'.format(doc_id, colString))
    outputDataFile.close()

def load_document_from_corpus(dataFilePath, limit = -1):
    dataFile = open(dataFilePath, 'r', encoding='utf-8')
    for index, line in enumerate(dataFile):
        if limit is not -1:
            if index > limit:
                break
        splits = line.split('\t')
        doc_dict[splits[0]] = splits[1]
        doc_contents.append(splits[1])
    
    #print('Loading total document -> {}'.format(len(doc_dict)))
    
    
load_document_from_corpus(doc_corpus_data_path, -1)

#tf_vectorizer
tf_vectorizer = CountVectorizer(max_df=0.8, min_df=1,
                                max_features=n_features,
                                stop_words='english')

trainTf = tf_vectorizer.fit_transform(doc_contents)

tf_feature_names = tf_vectorizer.get_feature_names()

#lda
lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0).fit(trainTf)


print_phi(lda, tf_feature_names, n_top_words)
#docTopicDisMatrix = np.matrix(lda.transform(trainTf))

#output theta portion to file
#export_theta_2_data_file(docTopicDisMatrix, doc_topic_portion_output_file_path)











