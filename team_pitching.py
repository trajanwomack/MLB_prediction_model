import json

#here we create a team level pitching stats that can be used if needed 

with open('team_data_with_stats.json', 'r') as g:
    team_stats=json.load(g)

    

    #ensure that flot values, if empty, are replaced with 0 not an error
def safe_float(value, default = 0.0): 
    try:
        return float(value)
    except(ValueError, TypeError):
        return default
    
    #convert innings pitched to 3 out format ex: 1.2 ip = 1.2/3 
def ip_conversion(value, default=0.0):
    try:
        value = float(value)

        whole_innings = int(value)
        outs = round((value - whole_innings) * 10)

        if outs == 0:
            return whole_innings
        elif outs == 1:
            return whole_innings + (1 / 3)
        elif outs == 2:
            return whole_innings + (2 / 3)
        else:
            return default

    except (ValueError, TypeError):
        return default
    

for team in team_stats:
    # pitching counting stats
    team_games_played = 0
    team_games_started = 0
    team_ground_outs = 0
    team_air_outs = 0
    team_runs = 0
    team_doubles = 0
    team_triples = 0
    team_home_runs = 0
    team_strike_outs = 0
    team_base_on_balls = 0
    team_intentional_walks = 0
    team_hits = 0
    team_hit_by_pitch = 0
    team_at_bats = 0
    team_caught_stealing = 0
    team_stolen_bases = 0
    team_ground_into_double_play = 0
    team_number_of_pitches = 0
    team_wins = 0
    team_losses = 0
    team_saves = 0
    team_save_opportunities = 0
    team_holds = 0
    team_blown_saves = 0
    team_earned_runs = 0
    team_batters_faced = 0
    team_outs = 0
    team_games_pitched = 0
    team_complete_games = 0
    team_shutouts = 0
    team_strikes = 0
    team_hit_batsmen = 0
    team_balks = 0
    team_wild_pitches = 0
    team_pickoffs = 0
    team_total_bases = 0
    team_games_finished = 0
    team_inherited_runners = 0
    team_inherited_runners_scored = 0
    team_catchers_interference = 0
    team_sac_bunts = 0
    team_sac_flies = 0

    # inning-based counting stat
    team_innings_pitched = 0.0

    # final team rate stats
    team_avg = 0
    team_obp = 0
    team_slg = 0
    team_ops = 0
    team_stolen_base_percentage = 0
    team_caught_stealing_percentage = 0
    team_era = 0
    team_whip = 0
    team_strike_percentage = 0
    team_ground_outs_to_airouts = 0
    team_win_percentage = 0
    team_pitches_per_inning = 0
    team_strikeout_walk_ratio = 0
    team_strikeouts_per_9_inn = 0
    team_walks_per_9_inn = 0
    team_hits_per_9_inn = 0
    team_runs_scored_per_9 = 0
    team_home_runs_per_9 = 0

    # weighted rate stat accumulators
    weighted_avg = 0
    weighted_obp = 0
    weighted_slg = 0
    weighted_ops = 0
    weighted_stolen_base_percentage = 0
    weighted_caught_stealing_percentage = 0
    weighted_era = 0
    weighted_whip = 0
    weighted_strike_percentage = 0
    weighted_ground_outs_to_airouts = 0
    weighted_win_percentage = 0
    weighted_pitches_per_inning = 0
    weighted_strikeout_walk_ratio = 0
    weighted_strikeouts_per_9_inn = 0
    weighted_walks_per_9_inn = 0
    weighted_hits_per_9_inn = 0
    weighted_runs_scored_per_9 = 0
    weighted_home_runs_per_9 = 0


    for player in team_stats [team]['players']:
   

        stats = player.get('stats',{})

        if not stats:
            continue


          
        print (player['name'])
        if 'inningsPitched' not in stats:

            print(f"skipping {player['name']} not a pitcher")
            
            continue
      
        print (player.get('stats', {}))
        print('-----')


        bf = int(stats['battersFaced'])
        ab = int(stats['atBats'])
        pitch_count = int(stats['numberOfPitches'])
        outs_recorded = int(stats['outs'])


        if bf == 0:
            continue
        if ab == 0:
            continue
        if pitch_count == 0:
            continue
        
        if outs_recorded == 0: continue



        #countable pitcher stats 
         
        team_games_played += int(stats['gamesPlayed'])
        team_games_started += int(stats['gamesStarted'])
        team_ground_outs += int(stats['groundOuts'])
        team_air_outs += int(stats['airOuts'])
        team_runs += int(stats['runs'])
        team_doubles += int(stats['doubles'])
        team_triples += int(stats['triples'])
        team_home_runs += int(stats['homeRuns'])
        team_strike_outs += int(stats['strikeOuts'])
        team_base_on_balls += int(stats['baseOnBalls'])
        team_intentional_walks += int(stats['intentionalWalks'])
        team_hits += int(stats['hits'])
        team_hit_by_pitch += int(stats['hitByPitch'])
        team_at_bats += int(stats['atBats'])
        team_caught_stealing += int(stats['caughtStealing'])
        team_stolen_bases += int(stats['stolenBases'])
        team_ground_into_double_play += int(stats['groundIntoDoublePlay'])
        team_number_of_pitches += int(stats['numberOfPitches'])
        team_wins += int(stats['wins'])
        team_losses += int(stats['losses'])
        team_saves += int(stats['saves'])
        team_save_opportunities += int(stats['saveOpportunities'])
        team_holds += int(stats['holds'])
        team_blown_saves += int(stats['blownSaves'])
        team_earned_runs += int(stats['earnedRuns'])
        team_batters_faced += int(stats['battersFaced'])
        team_outs += int(stats['outs'])
        team_games_pitched += int(stats['gamesPitched'])
        team_complete_games += int(stats['completeGames'])
        team_shutouts += int(stats['shutouts'])
        team_strikes += int(stats['strikes'])
        team_hit_batsmen += int(stats['hitBatsmen'])
        team_balks += int(stats['balks'])
        team_wild_pitches += int(stats['wildPitches'])
        team_pickoffs += int(stats['pickoffs'])
        team_total_bases += int(stats['totalBases'])
        team_games_finished += int(stats['gamesFinished'])
        team_inherited_runners += int(stats['inheritedRunners'])
        team_inherited_runners_scored += int(stats['inheritedRunnersScored'])
        team_catchers_interference += int(stats['catchersInterference'])
        team_sac_bunts += int(stats['sacBunts'])
        team_sac_flies += int(stats['sacFlies'])

        # innings pitched is a decimal value
        team_innings_pitched += safe_float(stats['inningsPitched'])
        ip = ip_conversion(stats['inningsPitched'])


        #weighted rate stats
        weighted_avg += safe_float(stats['avg']) * ab
        weighted_obp +=safe_float(stats['obp']) * bf
        weighted_slg +=safe_float(stats['slg']) * ab
        weighted_ops +=safe_float(stats['ops']) * bf
        
        #stolen bases
        stolen_base_attempts= team_caught_stealing + team_stolen_bases
        if stolen_base_attempts > 0:
            weighted_stolen_base_percentage += safe_float(stats['stolenBasePercentage'])*stolen_base_attempts
            weighted_caught_stealing_percentage += safe_float(stats['caughtStealingPercentage'])* stolen_base_attempts 
           
        
        weighted_era += safe_float(stats['era']) *ip
        weighted_whip += safe_float(stats['whip'])*ip
        weighted_strike_percentage += safe_float(stats['strikePercentage']) * pitch_count
        weighted_ground_outs_to_airouts += safe_float(stats['groundOutsToAirouts']) * outs_recorded
        weighted_win_percentage += safe_float(stats['winPercentage'])
        weighted_pitches_per_inning += safe_float(stats['pitchesPerInning']) * ip

        #strikeout to walk ratio
        total_strikeouts_walks= team_strikes +team_base_on_balls
        if total_strikeouts_walks > 0:
            weighted_strikeout_walk_ratio += safe_float(stats['strikeoutWalkRatio']) * total_strikeouts_walks

        weighted_strikeouts_per_9 +=(safe_float(stats['strikeoutsPer9Inn'])) *ip

        weighted_walks_per_9 += (safe_float(stats['walksPer9Inn']) * ip)

        weighted_hits_per_9 += (safe_float(stats['hitsPer9Inn']) * ip)

        weighted_runs_scored_per_9 += (safe_float(stats['runsScoredPer9']) * ip)

        weighted_home_runs_per_9 += (safe_float(stats['homeRunsPer9']) * ip)

    #get team rate stats
    team_era = weighted_era / team_innings_pitched
    team_whip = weighted_whip / team_innings_pitched
    team_strikeouts_per_9_inn = weighted_strikeouts_per_9_inn / team_innings_pitched
    team_walks_per_9_inn = weighted_walks_per_9_inn / team_innings_pitched
    team_hits_per_9_inn = weighted_hits_per_9_inn / team_innings_pitched
    team_runs_scored_per_9 = weighted_runs_scored_per_9 / team_innings_pitched
    team_home_runs_per_9 = weighted_home_runs_per_9 / team_innings_pitched

    team_avg = weighted_avg / team_at_bats
    team_obp = weighted_obp / team_batters_faced
    team_ops = weighted_ops / team_batters_faced
    team_strike_percentage = weighted_strike_percentage / team_number_of_pitches
    team_slg = weighted_slg / team_at_bats
    team_win_percentage = weighted_win_percentage / (team_wins + team_losses)

    
    if team_air_outs > 0:
   
        team_ground_outs_to_airouts = (
        weighted_ground_outs_to_airouts / team_outs
        )


    team_pitches_per_inning = (
    weighted_pitches_per_inning / team_innings_pitched
    )

    if team_base_on_balls > 0:
        team_strikeout_walk_ratio = (
        weighted_strikeout_walk_ratio /
        (team_strikes + team_base_on_balls))

    # stolen base percentages
    stolen_base_attempts = (
        team_stolen_bases + team_caught_stealing
    )

    if stolen_base_attempts > 0:
        team_stolen_base_percentage = (
            team_stolen_bases / stolen_base_attempts
        )

        team_caught_stealing_percentage = (
            team_caught_stealing / stolen_base_attempts
        )



    team_stats[team]['team_pitching'] = {

    # counting stats
    'gamesPlayed': team_games_played,
    'gamesStarted': team_games_started,
    'groundOuts': team_ground_outs,
    'airOuts': team_air_outs,
    'runs': team_runs,
    'doubles': team_doubles,
    'triples': team_triples,
    'homeRuns': team_home_runs,
    'strikeOuts': team_strike_outs,
    'baseOnBalls': team_base_on_balls,
    'intentionalWalks': team_intentional_walks,
    'hits': team_hits,
    'hitByPitch': team_hit_by_pitch,
    'atBats': team_at_bats,
    'caughtStealing': team_caught_stealing,
    'stolenBases': team_stolen_bases,
    'groundIntoDoublePlay': team_ground_into_double_play,
    'numberOfPitches': team_number_of_pitches,
    'inningsPitched': team_innings_pitched,
    'wins': team_wins,
    'losses': team_losses,
    'saves': team_saves,
    'saveOpportunities': team_save_opportunities,
    'holds': team_holds,
    'blownSaves': team_blown_saves,
    'earnedRuns': team_earned_runs,
    'battersFaced': team_batters_faced,
    'outs': team_outs,
    'gamesPitched': team_games_pitched,
    'completeGames': team_complete_games,
    'shutouts': team_shutouts,
    'strikes': team_strikes,
    'hitBatsmen': team_hit_batsmen,
    'balks': team_balks,
    'wildPitches': team_wild_pitches,
    'pickoffs': team_pickoffs,
    'totalBases': team_total_bases,
    'gamesFinished': team_games_finished,
    'inheritedRunners': team_inherited_runners,
    'inheritedRunnersScored': team_inherited_runners_scored,
    'catchersInterference': team_catchers_interference,
    'sacBunts': team_sac_bunts,
    'sacFlies': team_sac_flies,

    # rate stats
    'avg': team_avg,
    'obp': team_obp,
    'slg': team_slg,
    'ops': team_ops,
    'stolenBasePercentage': team_stolen_base_percentage,
    'caughtStealingPercentage': team_caught_stealing_percentage,
    'era': team_era,
    'whip': team_whip,
    'strikePercentage': team_strike_percentage,
    'groundOutsToAirouts': team_ground_outs_to_airouts,
    'winPercentage': team_win_percentage,
    'pitchesPerInning': team_pitches_per_inning,
    'strikeoutWalkRatio': team_strikeout_walk_ratio,
    'strikeoutsPer9Inn': team_strikeouts_per_9_inn,
    'walksPer9Inn': team_walks_per_9_inn,
    'hitsPer9Inn': team_hits_per_9_inn,
    'runsScoredPer9': team_runs_scored_per_9,
    'homeRunsPer9': team_home_runs_per_9
}

with open('team_data_with_pitching.json', 'w') as f:
    json.dump(team_stats, f)


