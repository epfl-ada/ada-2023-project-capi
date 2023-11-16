""" Module to store all functions related to data analysis tasks """

import networkx as nx
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter


def visualize_article_connections_per_category(
    connections, nodes, description
):
    graph = nx.DiGraph()

    for _, node in nodes.iterrows():
        graph.add_node(node["broad_category"])

    for _, row in connections.iterrows():
        start_category = row["start_broad_category"]
        end_category = row["end_broad_category"]
        if graph.has_edge(start_category, end_category):
            graph[start_category][end_category]["weight"] += 1
        else:
            graph.add_edge(start_category, end_category, weight=1)

    edge_weights = [graph[u][v]["weight"] for u, v in graph.edges()]
    max_edge_weight = max(edge_weights)
    min_edge_weight = min(edge_weights)
    normalized_edge_weights = [
        (weight - min_edge_weight) / (max_edge_weight - min_edge_weight)
        for weight in edge_weights
    ]
    edge_widths = [weight * 5 for weight in normalized_edge_weights]

    figure = nx.shell_layout(graph)
    plt.figure(figsize=(10, 10))
    nx.draw(
        graph,
        figure,
        with_labels=True,
        width=edge_widths,
        edge_color="gray",
        arrows=True,
    )
    plt.title(description)
    plt.show()


def t_test_article_metrics(metrics, df_1, df_2):
    for metric in metrics:
        statistic, pvalue = stats.ttest_ind(
            df_1[metric], df_2[metric], nan_policy="omit", equal_var=False
        )
        print(
            "\t - {} - t-statistic: {:.3f}, p-value: {:.3f}".format(
                metric, statistic, pvalue
            )
        )


def simple_t_test(dist1, dist2):
    '''
    Function to perform a simple t-test and print out the results in a readable format.
    :param dist1: First of the two distributions going into the t-test.
    :param dist2: Second of the two distributions going into the t-test.
    '''
    statistic, pvalue = stats.ttest_ind(
        dist1, dist2, nan_policy="omit", equal_var=False
    )
    print("t-statistic: {:.3f}, p-value: {:.3f}".format(statistic, pvalue))


def sorted_category_counts(df, category_dict):
    '''
    Function to create a dictionary of the counts of the categories present in the targets in a dataframe, 
    and sort this dictionary alphabetically.
    :param df: Dataframe in which the targets in question are found.
    :param category_dict: Dictionary for mapping article names to categories.
    :return sorted_cats: Dictionary of the counts of the categories sorted alphabetically by category.
    '''
    all_target_categories = [
        category_dict[target] for target in df["target"] if target in category_dict
    ]
    all_target_categories = [
        item for sublist in all_target_categories for item in sublist
    ]
    count_cats_finished_target = Counter(all_target_categories)
    keys_finished = list(count_cats_finished_target.keys())
    keys_finished.sort()
    sorted_cats = {i: count_cats_finished_target[i] for i in keys_finished}
    return sorted_cats


def shortest_path_find(df, articles, shortest_paths):
    '''
    Function to manually find the shortest possible path length in a game.
    :param df: Dataframe containg the games in question.
    :param articles: Dataframe of the article names.
    :param shortest_paths: Square matrix containg the length of the shortest paths between articles.
    :return shortest_unfinished: List of the shortest possible path lengths of the games in df.
    :return not_found: Integer of the number of shortest paths that could not be found in 'shortest_paths'.
    '''
    shortest_unfinished = []
    not_found = 0
    for i in range(len(df)):
        source = articles.loc[articles["article"] == df.iloc[i]["path"][0]]
        target = articles.loc[articles["article"] == df.iloc[i]["target"]]
        if len(source) != 0 and len(target) != 0:
            index_source = source.index[0]
            index_target = target.index[0]
            shortest_unfinished.append(int(shortest_paths[index_source][index_target]))
        else:
            shortest_unfinished.append(None)
            not_found += 1
    return shortest_unfinished, not_found
