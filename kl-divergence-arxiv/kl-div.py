# coding: utf-8

""" Compute the KL divergence between two abstracts. """

from __future__ import division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os, sys
import re
import collections

# Third-party
import matplotlib.pyplot as plt
from astropy.io.misc import fnunpickle
import numpy as np
import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.tag import pos_tag, simplify_tag

def parse_abstract(text):
    """ Remove to, the, and, etc. and punctuation from the abstracts """
    
    parsed = []
    for word,tag in pos_tag(wordpunct_tokenize(text)):
        if len(word) < 2 or simplify_tag(tag) in ["T", "I", "C", "D", ":"] \
            or "$" in word: continue
        
        parsed.append(word)
    
    return parsed

def kl_divergence(freqdist1, freqdist2):
    """ """
    freq1 = np.array(freqdist1.values()).astype(float) / freqdist1.N()
    freq2 = np.array(freqdist2.values()).astype(float) / freqdist2.N()
    vocab_diff = set(freqdist1.keys()).difference(set(freqdist2.keys()))
    
    epsilon = min(freq1.min(), freq2.min()) * 0.001
    gamma = 1. - len(vocab_diff) * epsilon
    
    div = 0.
    for word, count in freqdist1.iteritems():
        pts = count / freqdist1.N()

        ptt = epsilon
        if word in freqdist2.keys():
            ptt = gamma * (freqdist2[word] / freqdist2.N())

        ckl = (pts - ptt) * np.log(pts / ptt)
        div +=  ckl

    return div

def main():
    filename = "arxiv.pickle"
    entries = fnunpickle(filename)
    
    ii = 0
    freqdists = dict()
    for id, entry in entries.items():
        freqdists[id] = nltk.FreqDist(parse_abstract(entry['abstract']))
        ii += 1
    
    items = freqdists.items()
    kl_matrix = np.zeros((len(freqdists.keys()), len(freqdists.keys())))
    for ii,(id1,freqdist1) in enumerate(items):
        for jj,(id2,freqdist2) in enumerate(items):
            kl_matrix[ii,jj] = kl_divergence(freqdist1, freqdist2)
    
    kl_avg = np.zeros_like(kl_matrix)
    for ii in range(kl_matrix.shape[0]):
        for jj in range(ii+1):
            kl_avg[ii,jj] = (kl_matrix[ii,jj] + kl_matrix[jj,ii]) / 2.
    
    np.save("arxiv_kl_matrix.npy", kl_avg)
    
    #plt.hist(np.ravel(kl_avg), bins=25)
    #plt.show()

if __name__ == "__main__":
    main()