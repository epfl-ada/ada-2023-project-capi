""" Module to store all functions related to data preprocessing """

import pandas as pd

# functions to get all links between articles
from itertools import tee

def pairwise(iterable):
  # from python docs - will be introduced in version 3.10
  # pairwise('ABCDEFG') --> AB BC CD DE EF FG
  a, b = tee(iterable)
  next(b, None)
  return zip(a, b)

def get_all_links(df, path_colname="path"):
  edge_counter = {}
  for _, row in df.iterrows():
    
    links = row['path']
    edges = list(pairwise(links))

    for edge in edges:
      if edge in edge_counter:
        edge_counter[edge] += 1
      else:
        edge_counter[edge] = 1

  out = pd.Series(edge_counter).reset_index()
  out.columns = ["source", "target", "weight"]
  return out

def merge_articles_categories(df, left_on, articles_categories):
  merged_df = df.copy()

  merged_df = merged_df.merge(articles_categories, how="left", left_on=left_on[0], right_on="article").rename(columns = {
    "category": "start_category",
    "broad_category": "start_broad_category",
  })

  merged_df = merged_df.merge(articles_categories, how="left", left_on=left_on[1], right_on="article").rename(columns = {
    "category": "end_category",
    "broad_category": "end_broad_category",
  })

  merged_df = merged_df.drop(['article_x', 'article_y'], axis=1)
  #display(merged_df.head())
  return merged_df