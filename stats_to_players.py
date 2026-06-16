import json
import statsapi
import time


#load player stats

with open('team_data.json', 'r') as f:
    team_ids=json.load(f)

for team in team_ids:
    print(f"processing {team}...")
    for player in team_ids[team]['players']:
        player_id=player['id']
        
        stats= {}
        for group in ['hitting', 'pitching', 'fielding']:
            try:
                result = statsapi.player_stats(player_id, group = group, type = 'season')
            
            #get cleaned stats from api, we only want the stat value
                if result:
                    lines = result.split ('\n')
                    for line in lines:
                        if ':' in line:
                            parts = line.split(': ')
                            cat=parts[0].strip()
                            stat=parts[1].strip()
                            stats[cat]=stat

            except Exception as e:
                print (f"failed {player['name']} - {group}: {e}")

            time.sleep(.5)
        
        player['stats']= stats

with open('team_data_with_stats.json', 'w') as f:
    json.dump(team_ids, f)

print("Done!")