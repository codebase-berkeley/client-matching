# Stable Marriage for Teams and Devs

This is a jupyter notebook for matching teams and developers for CodeBase.

### Instructions

1. Add team rankings to `team_ranking.csv`, where 1 is most preferred
2. Add dev rankings to `dev_ranking.csv`, where 1 is most preferred
3. In `stable_marriage.ipynb`
	- edit `num_teams`
	- edit `num_devs`
	- edit `max_team_size`
	- in `cell 6`, replace team name keys. (`ATLASSIAN` should be replaced with the name of the team in leftmost ranking column in `team_ranking.csv`).
4. Run all cells in `stable_marriage.ipynb`
5. Open `stable_matching.txt` to check results.

All of the data in the rankings of this example repo is fake.
