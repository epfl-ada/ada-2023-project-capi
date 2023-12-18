# Success or Failure? A comparative analysis of finished and unfinished Wikispeedia games
*CAPI: Antonio Mari, Arda Civelekoğlu, Juan Garcia Giraldo, Luca Sbicego, Matteo Santelmo*

## Datastory
You can view our datastory here: [Success or Failure?](https://antoniomari.github.io/ADA-CAPI-DataStory/)

## Abstract

Humans tend to not be very persistent. Faced with difficult tasks, many opt to give up and pursue easier endeavours, instead of persevering through initial difficulties. In this context, we want to analyse the Wikispeedia dataset to study what makes people give up prematurely. Might it be that unfamiliar starting categories or seemingly far-away target articles make people give up? To study such factors, we conduct statistical analyses, honing in on a range of influential factors, before building a model for the likelihood of a game being abandoned prematurely. Our findings could help game-style environments (e.g., online educational platforms) enhance player retention and satisfaction (e.g., by adjusting levels/tasks). Moreover, this analysis can also reveal valuable insights into the human psyche, determining potential deterring factors of completing a task.

## Research Questions
To achieve these aims, our overarching research question is the following:

****What makes players give up a game of Wikispeedia?****

We want to further explore the following topics (“research” subquestions) to see if they affect the likelihood of a player quitting a game:
1. Categories of starting (“source”) and ending (“target”) articles
2. Article language characteristics
3. Objective game difficulty and graph structure
4. Individual player behaviour 

## Methods
### 1. Data Processing and Exploration

To answer our research questions, we use the finished paths (n=51,318) and unfinished paths (n=24,875) datasets, but also the categories and links datasets, the network graph and the shortest path matrix. We initially conduct data cleaning (e.g., removing URL encoding from path and article names). To answer research subquestion 2, we also process the plaintext Wikipedia articles and extract article metrics (e.g., readability score, word count; using NLTK and textstat packages).

In a preliminary data exploration, we noticed the following:
* 11 finished and 5214 unfinished paths have length 1 (max. path length=435).
* 6 articles lack an assigned category.
* 9 games had no shortest path possible according to the provided matrix, and 31 games had a target article with 0 in-degree. 
* Unfinished paths have data from 2011, while finished paths are available from 2008.

### 2. Individual analyses

To prepare our data for the overall statistical analysis, we calculate and analyse a range of metrics regarding each of our four research subquestions. Please refer to our notebook for details.

  1. ***Research Subquestion 1: Categories***

      Some categories may be more difficult for people to engage with. We extract the broadest possible category label for each article to avoid an unnecessarily large number of classes, giving 15 distinct categories. We then use the empirical likelihood of a target belonging to a certain category not being reached successfully in a game. We further explore the connections between different source and target categories, to see which pairings lead to easier or more difficult games in a similar fashion.

      <!-- This is the probability of a game being unfinished ($u$) for a given category $i$, and is calculated as:
      $\Bbb{P}(u|i) = \frac{\text{num category i in unfinished paths target}}{\text{num category i in target}}$. -->

  2. ***Research Subquestion 2: Article Metrics***
  
      With article metrics calculated in Step 1, we analyse differences between finished and unfinished games across categories. We visualise differences in the distribution of article metrics through violin plots (aiding distribution assessment). We supplement this visual assessment through t-tests to compare group means between all combinations of source/target articles across finished/unfinished paths.

  3. ***Research Subquestion 3: Path difficulty***

      We wish to see if some games are inherently more difficult. First, we look at the out-degrees and in-degrees of the source and target articles respectively, hypothesising that starts with a lower out-degree or targets with a lower in-degree make a game more difficult. Similarly, we look up the shortest possible path for each game. We compare these metrics between finished and unfinished paths using plots, as well as an appropriate t-test to compare the two groups (depending on the distributions). 

  4. ***Research Subquestion 4: Individual Player Behaviour***
  
      We analyse in-game behavioural aspects like back-click usage (computing player’s aggregated back-click frequency), including the use of back-clicks across different categories. Through statistical tests (like point-biserial correlation) we assess such factors’ correlations with quitting. We further explore the semantic closeness of articles in paths, in particular focusing on how semantically close the player gets to the target article throughout their games in finished and unfinished paths.
      

### 3. Putting everything together: Logistic Regression

To reach a conclusion for our datastory, we build a logistic regression model. This allows us to synthesise the above analysis output a probability to predict if a game will be finished or abandoned. This allows us to control for all factors and measure the relative strength of the effects (after standardisation). From the output, we can discuss statistically significant predictors and derive implications.

### 4. Expanding upon the model: Machine Learning

We expand upon the logistic regression model by training a Random Forest model which considers non-linearities and interaction effects. This model allows us to reach a level of predictive performance with an F1-score of 0.56 and an accuracy 0f 0.70. More importantly, it allows us to use Shapley values to better understand the real contributions of different factors to the probability of completion of a game according to the model.

## Proposed timeline and internal milestones
Our timeline and planned milestone are split across the two work streams on *Analysis* and *Data Story*:

| Week #                   | Code / Analysis                                                                         | Data Story                                                              |
|--------------------------|-----------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| 24.11.2023 / Week 1 | << Work on homework 2 >>                    | Created website setup for data story.                    |
| 01.12.2023 / Week 2  | Executed proposed remaining individual analyses; implemented P2 Feedback. | Structured and planned out data story.                              |
| 8.12.2023 / Week 3  | Created relevant (interactive) plots for data story; finalised logistic regression, and implemented random forest model.                   | Integrated plots in data story; started writing data story. |
| 15.12.2023 / Week 4 | Documented and cleaned code; expanded supporting analysis.                                                 | Finalised draft of data story.                                            |
| 22.12.2023 / Week 5 | Implemented last details and minor fixes.                      | **Hand in:** proof-read data story.                          |


### Organization within the team:
* **[Antonio](https://github.com/antoniomari):** Data exploration, website for data story, data story
* **[Arda](https://github.com/arcivelekoglu):** Data exploration and analysis (objective difficulty, categories), data story
* **[Juan](https://github.com/d23845jg):** Data exploration and analysis (article metrics, categories), visualizations, master of the repo
* **[Luca](https://github.com/lsbicego):** Data exploration and analysis (logistic regression, machine learning), data story
* **[Matteo](https://github.com/matsant01)**: Data exploration and analysis (individual player behaviour), visualizations


<!-- ### Questions for TAs (optional):  -->
<!-- Add here any questions you have for us related to the proposed project.  -->
