""" Module to store all functions related to data preprocessing """

import pandas as pd


def merge_articles_categories(df, left_on, articles_categories):
    """
    Function to merge article categories.
    :param df: Dataframe to be merged on.
    :param left_on: Specifying the column containing article names (used for merging).
    :return merged_df: Merged dataframe.
    """
    merged_df = df.copy()

    merged_df = merged_df.merge(
        articles_categories, how="left", left_on=left_on[0], right_on="article"
    ).rename(
        columns={
            "category": "start_category",
            "broad_category": "start_broad_category",
        }
    )

    merged_df = merged_df.merge(
        articles_categories, how="left", left_on=left_on[1], right_on="article"
    ).rename(
        columns={
            "category": "end_category",
            "broad_category": "end_broad_category",
        }
    )

    merged_df = merged_df.drop(["article_x", "article_y"], axis=1)
    merged_df = merged_df.dropna(subset=["start_broad_category", "end_broad_category"])
    merged_df = merged_df.sort_values(by=["start"], ascending=True)
    # display(merged_df.head())
    return merged_df


def create_category_dictionaries(categories):
    """
    Function to create dictionaries of categories & broad categories of articles.
    :param categories: Dataframe containing the categories & broad categories of articles.
    :return article_to_category: Dictionary mapping article names to categories.
    :return article_to_broad_category: Dictionary mapping article names to broad categories.
    """
    article_to_category = {}
    article_to_broad_category = {}
    for i in range(len(categories)):
        if categories.iloc[i]["article"] in article_to_category:
            article_to_category[categories.iloc[i]["article"]].append(
                categories.iloc[i]["category"]
            )
            article_to_broad_category[categories.iloc[i]["article"]].append(
                categories.iloc[i]["broad_category"]
            )
        else:
            article_to_category[categories.iloc[i]["article"]] = [
                categories.iloc[i]["category"]
            ]
            article_to_broad_category[categories.iloc[i]["article"]] = [
                categories.iloc[i]["broad_category"]
            ]
    return article_to_category, article_to_broad_category


def get_backclicked_pages(path):
    """Returns a list of all the pages that were backclicked on in a path l."""
    if "<" in path:
        s = []
        res = []
        for i in range(len(path)):
            if path[i] == "<":
                res.append(s.pop())
            else:
                s.append(path[i])
        return res
    else:
        return []


def get_quitted_page(path):
    """Return the page on which the user quit the path."""
    if path is None:
        return pd.NA
    else:
        if path[-1] != "<":
            return path[-1]
        else:
            clean_path = []
            for page in path:
                if page != "<":
                    clean_path.append(page)
                else:
                    clean_path.pop()
            return clean_path[-1]


def filter_games(
    df_finished: pd.DataFrame,
    df_unfinished: pd.DataFrame,
    min_length: int = 2,
    min_games: int = 10,
    type: str = "restart",
):
    """
    Filter out games and players that do not match the following criteria:
    - Players that played at least min_games games
    - Games that are at least min_length pages long
    - Games that are of type type (restart or timeout)
    """

    if min_length < 0 or min_games < 0:
        raise ValueError("min_length and min_games must be positive integers.")

    # Copy data since we're gonna filter out some games and players
    bck_an_finished = df_finished.copy(deep=True)
    bck_an_unfinished = df_unfinished.copy(deep=True)

    # For the moment we'll be considering all data. The following, comment line will keep only data matching
    # the same period (unfinished path were not recorded before 2011-02-07)
    # bck_an_finished = bck_an_finished[bck_an_finished["datetime"] >= bck_an_unfinished.sort_values(by="datetime").datetime[0]]

    # Keep only unfinished games where the reason is "restart"
    if type == "restart" or type == "timeout":
        bck_an_unfinished = bck_an_unfinished[bck_an_unfinished["type"] == type]
    elif type != "all":
        raise ValueError("type must be either 'restart', 'timeout' or 'all'.")

    # Keep only games referring to path longer than l
    bck_an_unfinished = bck_an_unfinished[
        bck_an_unfinished["path"].apply(lambda x: len(x) >= min_length)
    ]
    bck_an_finished = bck_an_finished[
        bck_an_finished["path"].apply(lambda x: len(x) >= min_length)
    ]

    # Keep only players that played overall at least n games
    considered_players = pd.concat(
        [
            bck_an_finished[["hashedIpAddress", "datetime"]],
            bck_an_unfinished[["hashedIpAddress", "datetime"]],
        ]
    )
    considered_players = (
        considered_players.groupby(by="hashedIpAddress")
        .size()
        .reset_index(name="num_games")
    )
    considered_players = considered_players[
        considered_players["num_games"] >= min_games
    ]

    bck_an_finished = pd.merge(
        left=bck_an_finished,
        right=considered_players,
        how="inner",
        on="hashedIpAddress",
    )
    bck_an_unfinished = pd.merge(
        left=bck_an_unfinished,
        right=considered_players,
        how="inner",
        on="hashedIpAddress",
    )

    print(
        "{} players played at least {} games longer than {} clicks.".format(
            len(considered_players), min_games, min_length
        )
    )

    return bck_an_finished, bck_an_unfinished
