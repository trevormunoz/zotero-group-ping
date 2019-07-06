#!/usr/bin/env python
# coding: utf-8

# # Poll Zotero Group Library
# 
# Created on: 2019-06-28
# 
# Revised on: 2019-07-06

# In[1]:


import os
import datetime
import markdown
from pyzotero import zotero


# Set up the zotero connection …

# In[2]:


get_ipython().run_line_magic('load_ext', 'dotenv')
get_ipython().run_line_magic('dotenv', '')

zot = zotero.Zotero(os.environ.get('ZOTERO_GROUP_ID'), 'group', os.environ.get('ZOTERO_API_KEY'))


# Grab the whole contents of the library at once

# In[3]:


lib_contents = zot.everything(zot.top())


# Setup some datetimes:

# In[4]:


runtime = datetime.datetime.now()


# For this we will look at a two-week window …

# In[5]:


window = runtime - datetime.timedelta(weeks=2)


# In[6]:


window


# In[7]:


def grab_dates(dict):
    """
    Pull the added and modified dates out of the metadata returned by the zotero client (a dictionary)
    Give back a tuple with just the date values as datetime objects
    """
    format_str = '%Y-%m-%dT%H:%M:%SZ'
    add_date = datetime.datetime.strptime(dict['data']['dateAdded'], format_str)
    mod_date = datetime.datetime.strptime(dict['data']['dateModified'], format_str)
    
    return (add_date, mod_date)


# In[8]:


from collections import defaultdict

entries = defaultdict(list)

for i in lib_contents:
    added,modified = grab_dates(i)
    if modified > window:
            zot_url = f"https://www.zotero.org/groups/{os.environ.get('ZOTERO_GROUP_ID')}/community-centered_collections/items/itemKey/{i['data']['key']}"
            item_data = i['data']
            
            # Add extra code for collection-level notes
            if item_data['itemType'] == 'note':
                info_string = f"*[Note: {item_data['note'].strip()}]({zot_url})*"
            else:
                info_string = f"[{item_data['title']}]({zot_url})"
                                                       
            entries[datetime.datetime.strftime(modified, '%B %-d, %Y')].append(info_string)                                       


# In[9]:


from IPython.core.display import HTML

email_contents = []
email_contents.append("###Latest Updates")

for k in entries.keys():
    email_contents.append(f"####Modified on: {k}")
    for v in entries[k]:
        email_contents.append(f"* {v}")
        
HTML(markdown.markdown("\n".join(email_contents)))

