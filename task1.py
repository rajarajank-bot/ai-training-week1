#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_cell_magic('timeit', '', 'res = []\nfor i in range(10000):\n    res.append(i**2)\n')


# In[1]:


get_ipython().run_cell_magic('timeit', '', 'res = [i**2 for i in range(10000)]\n')


# In[ ]:





# ### When to use Notebook vs .py File:
# 1. Use Jupyter Notebooks for exploratory data analysis (EDA), data visualization, and step-by-step experimentation.
# 2. Notebooks are ideal for presentations, rapid prototyping, and sharing interactive data reports.
# 3. Use .py files for writing clean, reusable modular code and utility functions.
# 4. Python files (.py) are required for automated production pipelines, deployments, and CI/CD workflows.
# 
