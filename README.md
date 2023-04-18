# ci_cd project

## Merging strategy
Given the project info provided (not a big team, technologies and release frequency), the "Git Feature Branch Workflow" was chosen as a suitable merging strategy. 

Justification:
1) Independent development: using feature branches allows each developer to work on their assigned tasks independently. This minimizes the chances of conflicts and keeps the main branch stable.

2) Code reviews: by using merge requests (or pull requests), the team can perform code reviews before merging the changes into the main branch. 

3) Agile development: the strategy aligns with the Agile development approach. Developers can create branches for each sprint or user story, making it easy to track the progress of individual tasks.

## Automation Testing Framework
Framework to run data-related tests on MS SQL SERVER. Tests are based on pytest framework.There are basic SQL-based tests.
