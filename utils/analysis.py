""" Module to store all functions related to data analysis tasks """

import networkx as nx
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter
import numpy as np
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, f1_score, precision_score, recall_score
import matplotlib.colors as colors

def visualize_article_connections_per_category(connections, nodes, description, edge_widths=None):
    """
    Function to plot a network (vertices: article categories, edges: strength of connection)
    :param connections: Edges.
    :param nodes: Vertices.
    """
    graph = nx.DiGraph()

    for _, node in nodes.iterrows():
        graph.add_node(node["broad_category"])

    for _, row in connections.iterrows():
        start_category = row["start_broad_category"]
        end_category = row["end_broad_category"]
        if graph.has_edge(start_category, end_category):
            graph[start_category][end_category]["size"] += 1
        else:
            graph.add_edge(start_category, end_category, size=1)

    if edge_widths is None:
        edge_weights = [graph[u][v]["size"] for u, v in graph.edges()]
        max_edge_weight = max(edge_weights)
        min_edge_weight = min(edge_weights)
        normalized_edge_weights = [
            (weight - min_edge_weight) / (max_edge_weight - min_edge_weight)
            for weight in edge_weights
        ]
        edge_widths = [weight * 5 for weight in normalized_edge_weights]

    plt.figure(figsize=(10, 10))
    nx.draw(
        graph,
        pos=nx.shell_layout(graph),
        with_labels=True,
        width=edge_widths,
        edge_color="gray",
        arrows=True,
    )
    plt.title(description)
    plt.show()

    return graph, edge_widths


def t_test_article_metrics(metrics, dist1, dist2):
    """
    Function to perform a simple t-test on article metrics and print out the results in a readable format.
    :param metrics: Article metric on which the t-test will be performed.
    :param dist1: First of the two distributions going into the t-test.
    :param dist2: Second of the two distributions going into the t-test.
    """
    for metric in metrics:
        statistic, pvalue = stats.ttest_ind(
            dist1[metric], dist2[metric], nan_policy="omit", equal_var=False
        )
        print(
            "\t - {} - t-statistic: {:.3f}, p-value: {:.3f}".format(
                metric, statistic, pvalue
            )
        )


def simple_t_test(dist1, dist2):
    """
    Function to perform a simple t-test and print out the results in a readable format.
    :param dist1: First of the two distributions going into the t-test.
    :param dist2: Second of the two distributions going into the t-test.
    """
    statistic, pvalue = stats.ttest_ind(
        dist1, dist2, nan_policy="omit", equal_var=False
    )
    print("t-statistic: {:.3f}, p-value: {:.3f}".format(statistic, pvalue))


def sorted_category_counts(df, category_dict, part="target"):
    """
    Function to create a dictionary of the counts of the categories present in the targets in a dataframe,
    and sort this dictionary alphabetically.
    :param df: Dataframe in which the targets in question are found.
    :param category_dict: Dictionary for mapping article names to categories.
    :param part: Part of the path, can be start/target.
    :return sorted_cats: Dictionary of the counts of the categories sorted alphabetically by category.
    """
    all_target_categories = [
        category_dict[target] for target in df[part] if target in category_dict
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
    """
    Function to manually find the shortest possible path length in a game.
    :param df: Dataframe containg the games in question.
    :param articles: Dataframe of the article names.
    :param shortest_paths: Square matrix containg the length of the shortest paths between articles.
    :return shortest_unfinished: List of the shortest possible path lengths of the games in df.
    :return not_found: Integer of the number of shortest paths that could not be found in 'shortest_paths'.
    """
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

def bootstrap_CI_prob_cat(data_f, data_u, cat, category_dict, iterations=1000):
    """
    Function to bootstrap the 95% confidence interval of the empirical likelihood that a target 
    belonging to a certain category not being reached.
    :param data_f: A Pandas Series of articles from the finished paths.
    :param data_u: A Pandas Series of articles from the unfinished paths.
    :param cat: Category name.
    :param category_dict: Dictionary for mapping article names to categories.
    :param iterations: The number of bootstrap samples to generate.
    :return: A tuple representing the lower and upper bounds of the 95% confidence interval
    """
    finished_target_categories = [
        category_dict[artic] for artic in data_f if artic in category_dict
    ]
    finished_target_categories = [
        item for sublist in finished_target_categories for item in sublist
    ]

    unfinished_target_categories = [
        category_dict[artic] for artic in data_u if artic in category_dict
    ]
    unfinished_target_categories = [
        item for sublist in unfinished_target_categories for item in sublist
    ]

    means = np.zeros(iterations)

    for i in range(iterations):
        bootstrap_sample_f = np.random.choice(finished_target_categories, size=len(finished_target_categories), replace=True)
        bootstrap_sample_u = np.random.choice(unfinished_target_categories, size=len(unfinished_target_categories), replace=True)
        count_cats_sample_f = Counter(bootstrap_sample_f)
        count_cats_sample_u = Counter(bootstrap_sample_u)
        means[i] = count_cats_sample_u[cat] / (count_cats_sample_u[cat] + count_cats_sample_f[cat])
        
    lower_bound = np.percentile(means, 2.5)
    upper_bound = np.percentile(means, 97.5)
    
    return (lower_bound, upper_bound)

def create_coefplot(model_summary, figsize=(14, 18), height_ratios=[0.7, 2.0, 2.5, 2.5]):
    """
    Function to plot the coefficient of a statsmodel regression summary, including confidence intervals in the defined variable groups.
    :param model_summary: a statsmodel summary object
    :return: A tuple of plt figure and axes
    """
    err_series = model_summary.params - model_summary.conf_int()[0]
    temp_df = pd.DataFrame({"coef": model_summary.params.values[1:],
                            "error": err_series.values[1:], 
                            "variable": err_series.index.values[1:]})
    

    CATEGORIES = {'Start Category: Business_Studies': 'Start Categories',
    'Start Category: Citizenship': 'Start Categories',
    'Start Category: Countries': 'Start Categories',
    'Start Category: Design_and_Technology': 'Start Categories',
    'Start Category: Everyday_life': 'Start Categories',
    'Start Category: Geography': 'Start Categories',
    'Start Category: History': 'Start Categories',
    'Start Category: IT': 'Start Categories',
    'Start Category: Language_and_literature': 'Start Categories',
    'Start Category: Mathematics': 'Start Categories',
    'Start Category: Music': 'Start Categories',
    'Start Category: People': 'Start Categories',
    'Start Category: Religion': 'Start Categories',
    'Start Category: Science': 'Start Categories',
    'Target Category: Business_Studies': 'Target Categories',
    'Target Category: Citizenship': 'Target Categories',
    'Target Category: Countries': 'Target Categories',
    'Target Category: Design_and_Technology': 'Target Categories',
    'Target Category: Everyday_life': 'Target Categories',
    'Target Category: Geography': 'Target Categories',
    'Target Category: History': 'Target Categories',
    'Target Category: IT': 'Target Categories',
    'Target Category: Language_and_literature': 'Target Categories',
    'Target Category: Mathematics': 'Target Categories',
    'Target Category: Music': 'Target Categories',
    'Target Category: People': 'Target Categories',
    'Target Category: Religion': 'Target Categories',
    'Target Category: Science': 'Target Categories',
    'Start Article: Avg. Sentence Length': 'Article Metrics',
    'Start Article: Avg. Word Length': 'Article Metrics',
    'Start Article: Paragraph Count': 'Article Metrics',
    'Start Article: Readability Score': 'Article Metrics',
    'Start Article: Stopword Percentage': 'Article Metrics',
    'Target Article: Avg. Sentence Length': 'Article Metrics',
    'Target Article: Avg. Word Length': 'Article Metrics',
    'Target Article: Paragraph Count': 'Article Metrics',
    'Target Article: Readability Score': 'Article Metrics',
    'Target Article: Stopword Percentage': 'Article Metrics',
    'Links from Source': 'Game Difficulty',
    'Links to Target': 'Game Difficulty',
    'Shortest Possible Path': 'Game Difficulty',
    'Semantic Similarity Start Target': 'Game Difficulty'}
    MAPPING = {
    # Starting Categories    
    'start_broad_category[T.Business_Studies]': 'Start Category: Business_Studies',
    'start_broad_category[T.Citizenship]': 'Start Category: Citizenship',
    'start_broad_category[T.Countries]': 'Start Category: Countries',
    'start_broad_category[T.Design_and_Technology]': 'Start Category: Design_and_Technology',
    'start_broad_category[T.Everyday_life]': 'Start Category: Everyday_life',
    'start_broad_category[T.Geography]': 'Start Category: Geography',
    'start_broad_category[T.History]': 'Start Category: History',
    'start_broad_category[T.IT]': 'Start Category: IT',
    'start_broad_category[T.Language_and_literature]': 'Start Category: Language_and_literature',
    'start_broad_category[T.Mathematics]': 'Start Category: Mathematics',
    'start_broad_category[T.Music]': 'Start Category: Music',
    'start_broad_category[T.People]': 'Start Category: People',
    'start_broad_category[T.Religion]': 'Start Category: Religion',
    'start_broad_category[T.Science]': 'Start Category: Science',

    # Ending Categories
    'target_broad_category[T.Business_Studies]': 'Target Category: Business_Studies',
    'target_broad_category[T.Citizenship]': 'Target Category: Citizenship',
    'target_broad_category[T.Countries]': 'Target Category: Countries',
    'target_broad_category[T.Design_and_Technology]': 'Target Category: Design_and_Technology',
    'target_broad_category[T.Everyday_life]': 'Target Category: Everyday_life',
    'target_broad_category[T.Geography]': 'Target Category: Geography',
    'target_broad_category[T.History]': 'Target Category: History',
    'target_broad_category[T.IT]': 'Target Category: IT',
    'target_broad_category[T.Language_and_literature]': 'Target Category: Language_and_literature',
    'target_broad_category[T.Mathematics]': 'Target Category: Mathematics',
    'target_broad_category[T.Music]': 'Target Category: Music',
    'target_broad_category[T.People]': 'Target Category: People',
    'target_broad_category[T.Religion]': 'Target Category: Religion',
    'target_broad_category[T.Science]': 'Target Category: Science',

    # article metrics
    'start_avg_sent_length': 'Start Article: Avg. Sentence Length',
    'start_avg_word_length': 'Start Article: Avg. Word Length',
    'start_paragraph_count': 'Start Article: Paragraph Count',
    'start_readability_score': 'Start Article: Readability Score',
    'start_stopword_percentage': 'Start Article: Stopword Percentage',

    'target_avg_sent_length': 'Target Article: Avg. Sentence Length',
    'target_avg_word_length': 'Target Article: Avg. Word Length',
    'target_paragraph_count': 'Target Article: Paragraph Count',
    'target_readability_score': 'Target Article: Readability Score',
    'target_stopword_percentage': 'Target Article: Stopword Percentage',

    # game difficulty
    'links_from_source': 'Links from Source',
    'links_to_target': 'Links to Target',
    'shortest_path_length': 'Shortest Possible Path',
    'sims_start_target': 'Semantic Similarity Start Target'}
    TITLE_SIZE = 14
    AXIS_SIZE = 12

    temp_df["clean_name"] = temp_df.variable.map(MAPPING)
    temp_df["group"] = temp_df.clean_name.map(CATEGORIES)

    # sort by coefficent
    temp_df = temp_df.sort_values(by="coef")

    # make individual dfs for plotting
    diff = temp_df[temp_df.group == "Game Difficulty"]
    start = temp_df[temp_df.group == "Start Categories"]
    target = temp_df[temp_df.group == "Target Categories"]
    metrics = temp_df[temp_df.group == "Article Metrics"]

    fig, ax = plt.subplots(4, 1, figsize=figsize, gridspec_kw={'height_ratios': height_ratios}, sharex=True)

    ax[0].axvline(0, c="darkgrey", linestyle="--")
    ax[0].scatter(y="clean_name", x="coef", data=diff, s=120, marker="s", c="coef", norm=colors.CenteredNorm(), cmap="RdYlGn_r")
    ax[0].errorbar(y="clean_name", x="coef", xerr="error", c="white", data=diff, ecolor="grey", fmt="none" )
    ax[0].xaxis.set_tick_params(which='both', labelbottom=True)
    ax[0].set_title("Game Difficulty", fontsize=TITLE_SIZE, fontweight="bold")
    ax[0].tick_params(axis='both', which='major', labelsize=AXIS_SIZE)

    ax[1].axvline(0, c="darkgrey", linestyle="--")
    ax[1].errorbar(y="clean_name", x="coef", xerr="error", c="white", data=metrics, ecolor="grey", fmt="none" )
    ax[1].scatter(y="clean_name", x="coef", data=metrics, s=120, marker="s", c="coef", norm=colors.CenteredNorm(), cmap="RdYlGn_r")
    ax[1].xaxis.set_tick_params(which='both', labelbottom=True)
    ax[1].set_title("Article Metrics", fontsize=TITLE_SIZE, fontweight="bold")
    ax[1].tick_params(axis='both', which='major', labelsize=AXIS_SIZE)

    ax[2].axvline(0, c="darkgrey", linestyle="--")
    ax[2].errorbar(y="clean_name", x="coef", xerr="error", c="white", data=start, ecolor="grey", fmt="none" )
    ax[2].scatter(y="clean_name", x="coef", data=start, s=120, marker="s", c="coef", norm=colors.CenteredNorm(), cmap="RdYlGn_r")
    ax[2].xaxis.set_tick_params(which='both', labelbottom=True)
    ax[2].set_title("Starting Categories", fontsize=TITLE_SIZE, fontweight="bold")
    ax[2].tick_params(axis='both', which='major', labelsize=AXIS_SIZE)

    ax[3].axvline(0, c="darkgrey", linestyle="--")
    ax[3].scatter(y="clean_name", x="coef", data=target, s=120, marker="s", c="coef", norm=colors.CenteredNorm(), cmap="RdYlGn_r")
    ax[3].errorbar(y="clean_name", x="coef", xerr="error", c="white", data=target, ecolor="grey", fmt="none" )
    ax[3].xaxis.set_tick_params(which='both', labelbottom=True)
    ax[3].set_title("Target Categories", fontsize=TITLE_SIZE, fontweight="bold")
    ax[3].tick_params(axis='both', which='major', labelsize=AXIS_SIZE)

    plt.tight_layout()

    return fig, ax

def evaluate_predictions(y_test, y_pred):
    """
    Function to print out classification metrics and display confusion matrices.
    :param y_test: array of predicted class labels
    :param y_test: array of ground truths
    :return: None (printouts and plots)
    """
    print(" Accuracy: {:.4f} \n F1-Score: {:.4f} \n Precision: {:.4f}\n Recall: {:.4f}".format(
            accuracy_score(y_test, y_pred),
            f1_score(y_test, y_pred),
            precision_score(y_test, y_pred),
            recall_score(y_test, y_pred),
        )  
    )

    # Plot Confusion Matrices
    fig, axes = plt.subplots(1, 3, figsize=(14, 8))
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=axes[0])
    axes[0].set_title("Raw Counts")
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, normalize="true", ax=axes[1])
    axes[1].set_title("Normalized by True Values (Per Class Recall)")
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, normalize="pred", ax=axes[2])
    axes[2].set_title("Normalized by True Values (Per Class Recall)")
    fig.show()