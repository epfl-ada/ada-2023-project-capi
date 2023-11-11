""" Module to store all functions related to data analysis tasks """

import networkx as nx
import matplotlib.pyplot as plt

def visualize_article_connections_per_category(connections, description):
  graph = nx.DiGraph()
  for _, row in connections.iterrows():
    start_category = row['start_broad_category']
    end_category = row['end_broad_category']
    if graph.has_edge(start_category, end_category):
      graph[start_category][end_category]['weight'] += 1
    else:
      graph.add_edge(start_category, end_category, weight=1)

  edge_weights = [graph[u][v]['weight'] for u, v in graph.edges()]
  max_edge_weight = max(edge_weights)
  min_edge_weight = min(edge_weights)
  normalized_edge_weights = [(weight - min_edge_weight) / (max_edge_weight - min_edge_weight) for weight in edge_weights]
  edge_widths = [weight * 4 for weight in normalized_edge_weights]

  figure = nx.shell_layout(graph)
  plt.figure(figsize=(8, 8))
  nx.draw(graph, figure, with_labels=True, width=edge_widths, edge_color='gray', arrows=True)
  plt.title(description)
  plt.show()