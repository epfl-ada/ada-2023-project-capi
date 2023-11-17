# Success or Failure? A comparative analysis of finished and unfinished Wikispeedia games

### Abstract: 
Humans tend to not be very persistent. Faced with difficult tasks, many opt to give up and pursue easier endeavours, instead of persevering through initial difficulties. In this context, we want to analyse the Wikispeedia dataset to study what makes people give up prematurely. Might it be that unfamiliar starting categories or seemingly far-away target articles make people give up? To study such factors, we conduct statistical analyses, honing in on a range of influential factors, before building a model for the likelihood of a game being abandoned prematurely. Our findings could help game-style environments (e.g., online educational platforms) enhance player retention and satisfaction (e.g., by adjusting levels/tasks). Moreover, this analysis can also reveal valuable insights into the human psyche, determining potential deterring factors of completing a task.

### Research Questions: 
To achieve these aims, our overarching research question is the following:
**What makes players give up a game of Wikispeedia?**
We want to further explore the following topics (“research” subquestions) to see if they affect the likelihood of a player quitting a game:
1. Categories of starting (“source”) and ending (“target”) articles
2. Article language characteristics
3. Objective game difficulty and graph structure
4. Individual player behaviour 

### Methods
1. **Data Processing and Exploration**
To answer our research questions, we are mainly relying on the finished paths (n=51,318) and unfinished paths (n=24,875) datasets, but also the categories and links datasets, the network graph and the shortest path matrix. We initially conduct data cleaning (e.g., removing URL encoding from path and article names). To answer research subquestion 2, we also process the plaintext Wikipedia articles and extract article metrics (e.g., readability score, word count; using NLTK and textstat packages, see the notebook for details).

In a preliminary data exploration, we noticed the following:
* 11 finished and 5214 unfinished paths have length 1 (max. path length=435).
* 6 articles lack an assigned category.
* 9 games had no shortest path possible according to the provided matrix, and 31 games had a target article with 0 in-degree. 
* Unfinished paths have data from 2011, while finished paths are available from 2008.

For P3, we will think about whether we need to exclude certain games from the analysis.

2. **Individual analyses**
To prepare our data for the overall statistical analysis, we calculate and analyse a range of metrics regarding each of our four research subquestions. Please refer to our notebook for a discussion of initial results and more details.
  1. Research Subquestion 1: Categories
     Some categories may be more difficult for people to engage with (e.g., geography is in general more accessible than mathematics). We first extract the broadest possible category label for each article to avoid an unnecessarily large number of classes, giving 15 distinct categories. We use the empirical likelihood of a target belonging to a certain category not being reached successfully in a game. This is the probability of a game being unfinished ($u$) for a given category $i$, and is calculated as:
$ P(u|i) = \frac{\text{# category i in unfinished paths target}}{\text{# category i in target}} $

  3. Research Subquestion 2: Article Metrics
    With article metrics calculated in Step 1, we analyse differences between finished and unfinished games across categories. We visualise differences in the distribution of article metrics through violin plots (aiding distribution assessment). We supplement this visual assessment through t-tests to compare group means between all combinations of source/target articles across finished/unfinished paths.
  4. Research Subquestion 3: Path difficulty
  5. Research Subquestion 4: Individual Player Behaviour
     We analyse in-game behavioural aspects like back-click usage (computing player’s aggregated back-click frequency), quitting tendencies (looking at the prior probability to quit), and category choice (how commonly articles of each category are used by the same player). Through statistical tests (like point-biserial correlation) we assess these factors’ correlations with quitting. 

3. **Putting everything together: Logistic Regression**
To reach a conclusion for our datastory, we build a logistic regression model. This allows us to output a probability to predict if a game will be finished or abandoned (based on starting and ending categories, article metrics, objective difficulties of games, etc). This allows us to control for all factors and measure the relative strength of the effects (after standardisation). From the output, we can discuss statistically significant predictors and derive implications (e.g., which categories have a negative influence, are more readable start articles better etc.). 

### Proposed timeline
Our timeline split across the workstreams on Code / Analysis and Data Story is represented in the following table. The week numbers start after the P2 Milestone (i.e. Week 1 is the first week after the P2 deadline).
| Week #                   | Code / Analysis                                                                         | Data Story                                                              |
|--------------------------|-----------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| Week 1 (starting Nov 20) | Execute proposed analysis and implemented Feedback from Milestone P2                    | Explore options to create website to host data story                    |
| Week 2 (starting Nov 27) | Create relevant (interactive) plots and statistics to illustrate findings in data story | Create website and structure of data story                              |
| Week 3 (starting Dec 4)  | Document code, expand supporting analysis and clean up the repository                   | Integrate plots in data story and get started on writing the commentary |
| Week 4 (starting Dec 11) | Implement last details and minor fixes                                                  | Finalize draft of data story                                            |
| Week 5 (starting Dec 18) | -                                                                                       | Proof read data story and work on last details                          |


### Organization within the team:
A list of internal milestones up until project Milestone P3.
### Questions for TAs (optional): 
Add here any questions you have for us related to the proposed project.
