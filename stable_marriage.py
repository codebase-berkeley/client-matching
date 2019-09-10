from random import sample
import pprint
import csv
import random

## SET THESE VARIABLES
## Ideally, num_teams * max_team_size = num_devs
## Otherwise, num_teams * (max_team_size - 1) < num_devs <= num_teams * max_team_size, also works
num_teams = 4
num_devs = 22
max_team_size = 6

print("Number of teams: " + str(num_teams))
print("Number of devs: " + str(num_devs))
print("Max team size: " + str(max_team_size))

def stable_marriage(teams_rankings, devs_rankings):
    '''
    Performs stable matching algorithm where each team can propose to up to `num_teams` number of devs
    
    Parameters
    -----------
    teams_rankings: dictionary
        key is team name, value is list of devs where lower index is higher preference
    devs_rankings: dictionary
        key is dev name, value is list of teams where lower index is higher preference
    
    Returns
    -----------
    dev_matching: dictionary
        key is dev, value is the team dev is matched to
    '''
    
    teams = teams_rankings.keys()
    devs = devs_rankings.keys()
    
    matching = [{team: []} for team in teams]
    team_availability = dict(zip(teams, ["free"] * len(teams)))
    team_size = dict(zip(teams, [0] * len(teams)))
    dev_availability = dict(zip(devs, ["free"] * len(devs)))
    team_counter = dict(zip(teams, [0] * len(teams)))
    dev_matching = {}
    
    while not teams_full(team_size):
        if proposals_completed(team_counter):
            break
        
        for team in teams:
            if team_availability[team] != "free" or team_counter[team] >= num_devs:
                continue

            dev_index = team_counter[team]
            dev = teams_rankings[team][dev_index]

            if dev_availability[dev] == "free":
                dev_availability[dev] = "engaged"
                dev_matching[dev] = team
                team_size[team] += 1
                if team_size[team] >= max_team_size:
                    team_availability[team] = "engaged"

            elif dev_availability[dev] == "engaged":
                matched_team = dev_matching[dev]
                proposed_team = team
                dev_rankings = devs_rankings[dev]
                if dev_rankings.index(proposed_team) < dev_rankings.index(matched_team):
                    team_size[matched_team] -= 1
                    if team_availability[matched_team] == "engaged":
                        team_availability[matched_team] = "free"

                    team_size[proposed_team] += 1
                    if team_size[proposed_team] >= max_team_size:
                        team_availability[proposed_team] = "engaged"

                    dev_matching[dev] = proposed_team

            team_counter[team] += 1
    return dev_matching

def teams_full(team_size):
    '''
    Returns true if sum of all team sizes is num_devs
    
    Parameters
    -----------
    team_size: dictionary
        key is team, value is size of team

    Returns
    -----------
    boolean
    '''
    devs_matched = 0
    for _, size in team_size.items():
        devs_matched += size
    return devs_matched == num_devs

def proposals_completed(team_counter):
    '''
    Returns true if all teams have proposed to all devs
    
    Parameters
    -----------
    team_counter: dictionary
        key is team, value is number of devs team has proposed to

    Returns
    -----------
    boolean
    '''
    for _, count in team_counter.items():
        if count < num_devs - 1:
            return False
    return True

def dev_to_team_matching(dev_matching):
    '''
    Converts dev-to-team matching to team-to-dev matching
    
    Parameters
    -----------
    dev_matching: dictionary
        key is dev, value is the team dev is matched to

    Returns
    -----------
    team_matching: dictionary
        key is team, value is list containing devs matched to that team
    '''
    team_matching = {}
    for dev, team in dev_matching.items():
        if team in team_matching.keys():
            team_matching[team].append(dev)
        else:
            team_matching[team] = [dev]
    return team_matching

def get_team_names():
    '''
    Gets team names from team_ranking.csv
    
    Returns
    -----------
    teams: list
        list of team names
    '''
    with open("team_ranking.csv", "r") as f:
        reader = csv.reader(f, delimiter="\t")

        for i, line in enumerate(reader):
            return line[0].split(',')[1:]

print("Getting team names...")
team_names = get_team_names()
print("Team Names: " + str(team_names))

print("Getting rankings from devs...")
devs_ranking = {}
with open("dev_ranking.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        if i == 0:
            continue
        args = line[0].split(',')
        dev_name = args[0]
        dev_ranking = args[1:]
            
        devs_ranking[dev_name] = dev_ranking

print("Getting rankings from teams...")
dev_list = [[-1] * num_devs for i in range(num_teams)]
teams_ranking = dict(zip(team_names, dev_list))
with open("team_ranking.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        if i == 0:
            continue
        args = line[0].split(',')
        dev_name = args[0]
        dev_rankings = args[1:]
        for team, ranking in zip(team_names, dev_rankings):
            teams_ranking[team][int(ranking) - 1] = dev_name

print("Running matching algorithm...")
stable_matching = stable_marriage(teams_ranking, devs_ranking)
team_matching = dev_to_team_matching(stable_matching)

print("Writing match to stable_matching.txt")
with open("stable_matching.txt", 'w') as f:
    for key, value in team_matching.items():
        f.write('%s:%s\n' % (key, value))
print("Done!")
