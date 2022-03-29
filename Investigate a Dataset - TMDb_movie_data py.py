#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Dataset - TMDb_movie_data
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# > TMDb_movie_data is a dataset of 10000 movie from the year 1960 to 2015 
# > This dataset was generated from The Movie Database API. This product uses the TMDb API but is not endorsed or certified by TMDb.
# 
# 
# ### Question(s) for Analysis
# > Which Year was the most succesful year in Holywood in Terms of Revenues, Budget and Popularity ? and what are the changes of Revenues, budget , profit and poupularity over the years ?
# 
# > Which actors,Genres,directors and movie duration that will help movie profits to exceed 100 million dollars ? and the correlation between movie duration and profits ?

# In[1]:


# import all of the packages that I will use.
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
from matplotlib import rcParams


# In[2]:


# Loaded my Data and Checked if It's Correctely loaded.
df = pd.read_csv('Database_TMDb_movie_data/tmdb-movies.csv')
df.head()


# <a id='wrangling'></a>
# ## Data Wrangling

# In[3]:


# to check for the number of columns and rows 
df.shape


# In[4]:


# to check for the data types and any problem
df.info()


# In[5]:


# to check for the values in the Table and make sure there is no wrong values like zero 
df.describe()


# In[6]:


# After Checking the Data we will start by droping all the columns that we don't need
df.drop(['id' , 'imdb_id' , 'budget' , 'revenue', 'production_companies' , 'homepage' , 'tagline' , 'keywords','overview','release_date','vote_count','vote_average'],axis=1,inplace= True)
df.info()


# 
# ### Data Cleaning
# > **Tip**: Make sure that you keep your reader informed on the steps that you are taking in your investigation. Follow every code cell, or every set of related code cells, with a markdown cell to describe to the reader what was found in the preceding cell(s). Try to make it so that the reader can then understand what they will be seeing in the following cell(s).
#  

# In[7]:


#after That we have to remove zero values in the Budget, Revenue and runtime
df = df[df.budget_adj != 0]
df = df[df.revenue_adj != 0]
df = df[df.runtime != 0]
df.info()


# In[8]:


# Checking for NAN values 
df.isnull().any().sum()


# In[9]:


# Deleting the row with NAN values 
df.dropna(axis=0 , inplace=True)


# In[10]:


# Checking again for NAN values 
df.isnull().any().sum()


# In[ ]:


# Creating a new column to Calculate the profit 
df['profit'] = df['revenue_adj'] - df['budget_adj']


# In[ ]:


# Creating a heat map to identify the correltion between the Variables 
d = sns.heatmap(df.corr(), annot = True);

d.set(xlabel='Movies Data', ylabel='Movies Data', title = "Correlation matrix of Movies data\n");


# #### We can figure the following : 
# > - We Can figrue out that there is a medium correlation between revenues and popularity
# > - Another correlation between release year and cost
# > - While negative correlation between release year and profits
# > - Also a correlation between runtime and poularity and runtime and profits 

# In[ ]:


# Final check for our data before starting .. 
df.head()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# 
# 
# ### Which Year was the most succesful year in Holywood in Terms of Revenues, Budget and Popularity ? and what are the changes of Revenues, budget , profit and poupularity over the years ?  

# In[ ]:


# First We need to Group by the mean of the Years 
df_ry = df.groupby('release_year').mean()
df_ry.head(5)


# In[ ]:


# Now we will create a function to identify the max year in terms of columns   
def max_data(column):
    max_year_data = df_ry[df_ry[column] == df_ry[column].max()]
    return max_year_data
max_data('popularity')


# > Seems that the highest year in terms of popularity is 2015 with average 2.85

# In[ ]:


# in terms of revenue
max_data('revenue_adj')


# > It seems That 1965 was the highest year with average revenue six hundred thirty-four million thirty-six thousand nine hundred dollars

# In[ ]:


# in terms of cost
max_data('budget_adj')


# > It seems That also 1965 was the highest year with average cost eighty-one million three hundred eighty-five thousand eight hundred thirty dollars 

# In[ ]:


#in terms of profit
max_data('profit')


# > It seems That also 1965 was the highest year in terms of profit with average profit five hundred fifty-two million six hundred fifty-one thousand one hundred dollars 

# In[ ]:


#Now we will do it in terms of revenue 
plt.plot(df_ry['revenue_adj']);


# > A graph That shows the change of revenues from 1960 to 2015 

# In[ ]:


# Now we will Draw A Chart for the progress of years in terms of Popularity 
df_ry.plot(y='popularity');


# > A graph That shows the change of popularity from 1960 to 2015 

# In[ ]:


# Now in terms of Cost 
df_ry.plot(y='budget_adj');


# > > A graph That shows the change of cost from 1960 to 2015 

# In[ ]:


#now in terms of profit
df_ry.plot(y='profit');


# > A graph That shows the change of profits from 1960 to 2015 

#    ### Which actors,Genres,director and movie duration that will help movie profits to exceed 100 million dollars ? and the correlation between movie duration and both profits and popularity ?

# In[ ]:


#First we will Start with movies with profits more than 100 millions 
df = df[df['profit'] > 100000000]
# Creating a function that get count of participation of each element in the movies   
def clean(column):
    df_data = df[column]
    # spliting Data by '|'
    df_data = df_data.apply(lambda x: x.split('|'))
    # Creating a new dataframe with each value in a column 
    split_data = pd.DataFrame(df_data.tolist())
    # Creating a list to add all the values of the 5 columns to it 
    df_count = []
    # Creating a for loop to add all the items to the list 
    for i in split_data.columns:
        split_data[i].apply(lambda x: df_count.append(x))
    # Transforming the list to data frame to get the counts of elements    
    df_count = pd.DataFrame(df_count)
    return df_count[0].value_counts()


# In[ ]:


# First we will start with the Actors by identifing the Top 10 Actors that particpate in
# a movie with more than 100 million dollars 
def final(column):
    #getting the top 10 actors 
    top_10 = pd.DataFrame(clean(column).head(10))
    #Changing Actors from index to a column 
    top_10.reset_index(inplace=True)
    return top_10
#Changing Actors from index to a column 
top_10 = final('cast')
top_10.rename(columns = {'index':'Actor'}, inplace = True)
#Drawing a graph to represent the number of apperance that actors 
rcParams['figure.figsize'] = 15,5
C = sns.barplot(x = 'Actor',y = top_10[0],data = top_10, palette="Blues_d" );
C.set( xlabel = "Actors", ylabel = "Frequency");


# > A graph that shows the frequency of Top 10 Actors apperance , You have to hire one of these actors to your film [Tom Cruise , Tom Hanks , Brad Pitt , Sylvester Stallone , Cameron Diaz , Adam Sandler , Eddie Murphy , Robert De Niro , Bruce Willis , Jim Carrey]

# In[ ]:


# we will do the same with genres 
top_10 = final('genres')
top_10.rename(columns = {'index':'genres'}, inplace = True)
# now we will show the genres in graph 
rcParams['figure.figsize'] = 15,5
G = sns.barplot(y = 'genres',x = top_10[0],data = top_10, palette="rocket" );
G.set( xlabel = "genres", ylabel = "Frequency");


# > A Graph that represents the Frequency of each Genres , Make your movie with Genre Action , drama and a little bit Comedy for the 100 Million dollars :) 

# In[ ]:


# one more time for the director 
top_10 = final('director')
top_10.rename(columns = {'index':'director'}, inplace = True)
# now we will show the director in a graph 
rcParams['figure.figsize'] = 18,5
D = sns.barplot(x = 'director',y = top_10[0],data = top_10, palette="vlag" );
D.set( xlabel = "genres", ylabel = "Frequency");


# >A graph that shows Top 10 directors participation on movies with profit 100 million dollars, and we will choose one of these two [Steven Spielbreg , Robert Zemeckis] 

# In[ ]:


# now we will calculate the correltion between Profits and run time
df['profit'].corr(df['runtime'])


# > The correltion between profits and runtime is 0.2306 

# In[ ]:


# Now we will graph it 
sns.regplot(x=df["profit"], y=df["runtime"]);


# > A graph to Show the Correlation between profit and runtime 

# In[ ]:


# we can also calculate the correltion between Popularity and run time
df['popularity'].corr(df['runtime'])


# In[ ]:


# Now we will graph it 
sns.regplot(x=df["popularity"], y=df["runtime"]);


# >A graph to Show the Correlation between profit and runtime 

# In[ ]:


# finaly we are going to see the average run time of the movie 
print('Your Movie should be {} min'.format(df['runtime'].mean().astype(int)))


# >Finally Your Movie should be around 116 min 

# <a id='conclusions'></a>
# ## Conclusions
# 
# #### First Question : Which Year was the most succesful year in Holywood in Terms of Revenues, Budget and Popularity ? and what are the changes of Revenues, budget , profit and poupularity over the years ? 
# > - Seems that the highest year in terms of popularity is 2015 with average 2.85
# > - It seems That 1965 was the highest year in terms of revenue with average revenue six hundred thirty-four million thirty-six thousand nine hundred dollars
# > - It seems That also 1965 was the highest year with average cost eighty-one million three hundred eighty-five thousand eight hundred thirty dollars 
# > - It seems That also 1965 was the highest year in terms of profit with average profit five hundred fifty-two million six hundred fifty-one thousand one hundred dollars 
# > - And finally the Graghs illustrate the change over years 
# #### Second Question : Which actors,Genres,director and movie duration that will help movie profits to exceed 100 million dollars ? and the correlation between movie duration and profits ?
# > - You have to hire one of these actors to your film [Tom Cruise , Tom Hanks , Brad Pitt , Sylvester Stallone , Cameron Diaz , Adam Sandler , Eddie Murphy , Robert De Niro , Bruce Willis , Jim Carrey] 
# > - Make your movie with Genre Action , drama and a little bit Comedy 
# > - Directed by one of these two [Steven Spielbreg , Robert Zemeckis] 
# > - Finally Your Movie should be around 116 min 
# ## Limitations 
# >- The dataset is for movies from the year 1960 to 2015
# >- In the second question there are sevral factors that affect the profit I just listed some of them

# In[ ]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




