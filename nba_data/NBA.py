#!/home/jupyter/nba_data/venv_nba/bin/python
# coding: utf-8

#####################
#  Import Packages  #
#####################

import pandas as pd
import numpy as np
import re
import os
import datetime as dt
from bs4 import BeautifulSoup, Comment
import requests

###############
#  NBA Class  #
###############

class NBA:
    """
    NBA - Documentation goes here
    """
    
    def __init__(self, url, table_id, column_schema, row_schema, data_schema,
                 use_links=[], add_links={}, name_change={}, filter_rows = {}, ):
        self.url = url
        self.table_id = table_id
        self.use_links = use_links
        self.add_links = add_links
        self.column_schema = column_schema
        self.row_schema = row_schema
        self.data_schema = data_schema
        self.name_change = name_change
        self.filter_rows = filter_rows
        
        try:
            self.get_soup()
            self.get_columns()
            self.get_rows()               
            self.get_data()
            self.add_link()
            self.filter_by_value()
        except:
            self.df = pd.DataFrame()

    def get_soup(self):

        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'lxml')
        self.soup = soup.find('table', {"id": self.table_id})
        
    def get_columns(self):

        base="self.soup"
        add=".findAll('{}'){}"

        for i in range(len(self.column_schema['column_attrs'])):
            if self.column_schema['offset'][i] != None:
                base = f"{base}{add.format(self.column_schema['column_attrs'][i],'['+str(self.column_schema['offset'][i])+']')}"
            else:
                base = f"{base}{add.format(self.column_schema['column_attrs'][i],'')}"

        loop = f"[x.getText() for x in {base}][{self.column_schema['shift']}:]"

        self.columns = eval(loop)

        for k, v in self.name_change.items():
            self.columns[k] = v   
            
    def get_rows(self):

        base="self.soup"
        add=".findAll('{}'){}"

        for i in range(len(self.row_schema['row_attrs'])):
            if self.row_schema['row_offset'][i] != None:
                base = f"{base}{add.format(self.row_schema['row_attrs'][i], '['+str(self.row_schema['row_offset'][i])+']')}"
            else:
                base = f"{base}{add.format(self.row_schema['row_attrs'][i], '')}"

        self.rows = eval(base)

    def get_data(self):

        data = [[x.getText() if j not in self.use_links else x.a['href'] \
                 for j, x in enumerate(self.rows[i].findAll(self.data_schema['data_attrs']))][self.data_schema["data_offset"]:] \
                for i in range(len(self.rows))]

        max_list_len = max(list(map(lambda x: len(x), data)))
        self.data = [self.pad_list(sub,max_list_len) for sub in data if len(sub) > 0]

        self.df = pd.DataFrame(data=data, columns=self.columns)
        
    def add_link(self):

        for key, value in self.add_links.items():
            self.df[key] = [[x.a['href'] for j,x in enumerate(self.rows[i].findAll(self.data_schema['data_attrs']))                              if j == value][0] for i in range(len(self.data))]  
            
    def pad_list(self, l,n):
        while len(l) < n:
            l.append("")
        return l
    
    def filter_by_value(self):
        for key, value in self.filter_rows.items():
            self.df = self.df[self.df[key] != value].reset_index(drop=True)

###################
#  End of script  #
###################