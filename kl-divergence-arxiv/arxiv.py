# coding: utf-8

""" Download abstracts from the arXiv """

from __future__ import division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os, sys
import string
import re
import time

# Third-party
from astropy.io.misc import fnpickle, fnunpickle
import numpy as np
import requests
import feedparser

default_api_url = "http://export.arxiv.org/api/query?"

def retrieve_abstracts(api_url=default_api_url, **kwargs):
    """ Retrieve abstracts from the arXiv 
    
        Parameters
        ----------
        api_url : str (optional)
        kwargs : 
            Any valid key-value pair for an arXiv API search. See:
                http://arxiv.org/help/api/user-manual
    
    """
    
    # Container for all returned results. Keys will be arXiv ID's 
    #   (e.g., 1305.2160), values contain title, authors, abstract
    parsed_entries = dict()
    
    # Default search parameters
    params = dict(search_query='cat:astro-ph',
                  max_results=10,
                  sortBy='submittedDate',
                  sortOrder='descending',
                  start=0)
    
    # update API query parameters with kwargs
    for k,v in kwargs.items():
        params[k] = v
    
    # send request, use feedparser to parse the ATOM feed response
    resp = requests.get(url=api_url, params=params)
    feed = feedparser.parse(resp.content)
    
    # for each entry, extract ID, abstract, title, authors
    for entry in feed['entries']:
        id = os.path.basename(entry.id) # http://arxiv.org/abs/1305.1919v1
        abstract = entry.summary_detail['value']
        parsed_entries[id] = dict(title=entry.title, 
                                  authors=entry.authors,
                                  abstract=abstract)
    
    return parsed_entries

num = 10000
max_results = 1000

parsed_entries = dict()
for start in range(0, num+max_results, max_results):
    entries = retrieve_abstracts(search_query="abs:galaxy",
                                 start=start, 
                                 max_results=max_results)
    parsed_entries = dict(parsed_entries.items() + entries.items())
    time.sleep(3)
    
fnpickle(parsed_entries, "arxiv.pickle")

