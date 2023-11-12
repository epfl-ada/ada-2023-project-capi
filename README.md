# ada-2023-project-capi


### Abstract: 
A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?

Goals:
- Recommend games based on difficulty?
- Infer ideas on how to write better, more understandable articles?
- Identify gaps in knowledge

### Research Questions: 
To this end, we want to explore the following questions, resp. hypotheses:
- Are unfinished paths inherently harder to finish, based on objective measures?
- Are there human factors that influence whether a path will be finished or not?
- Can we predict whether a path will be finished or not to a reasonable degree of accuracy?

### Proposed additional datasets (if any): 
None. Section to be deleted.
### Methods
Section to be expanded and clarified

The proposed methodology to answer the research questions asked above involves the in-depth analysis of finished and unfinished paths, and their comparison. In particular, we have looked at (or will in the future):
- Article metrics from the full wikipedia articles (such as stopword percentage, paragraph length, readability score, etc.)
- The length of the shortest path possible to complete a game
- Backclick rates
- The connectedness of the path target in the graph of wikipedia articles
- The categories that occur in the paths, and the source/target category pairs that occur in the two sets

We use graphical elements (appropriately interactive or not) as well as statistical tests to measure the importance of above factors. These analyses allow the characterisation of the paths based on human and non-human factors. These can then be used as regressors in a logistic regression to predict probabilities on whether a game will be finished or not. We can then use these results to infer the relative importance of the regressors to the completion of a game, which may then be used to make recommendations addressing the goals of this project.


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
