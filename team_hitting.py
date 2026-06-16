import json


#Take player hitting stats and make genereate team wide stats

with open('team_data_with_stats.json', 'r') as g:
    team_stats=json.load(g)


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

for team in team_stats:
    # running totals
    team_games_played = 0
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
    team_plate_appearances = 0
    team_total_bases = 0
    team_rbi = 0
    team_left_on_base = 0
    team_sac_bunts = 0
    team_sac_flies = 0
    team_catchers_interference = 0


    # team rate stats
    team_avg = 0
    team_obp = 0
    team_slg = 0
    team_ops = 0
    team_stolen_base_percentage = 0
    team_caught_stealing_percentage = 0
    team_babip = 0
    team_ground_to_air_outs = 0
    team_at_bats_per_home_run = 0


    #weighted stats
    weighted_avg = 0
    weighted_obp = 0
    weighted_slg = 0
    weighted_ops = 0
    weighted_stolen_base_percentage = 0
    weighted_caught_stealing_percentage = 0
    weighted_babip = 0
    weighted_ground_to_air_outs = 0
    weighted_at_bats_per_home_run = 0


    for player in team_stats[team]['players']:
        print(player['name'])

        stats = player.get('stats',{})

        if not stats:
            continue

        if 'plateAppearances' not in stats:
            print(f"Skipping {player['name']} on {team} not a a hitter")
            continue

        print(player.get('stats', {}))
        print('-----')


        pa = int(stats['plateAppearances'])

        if pa == 0:
            continue



        # Count stats
        team_games_played += int(stats['gamesPlayed'])
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
        team_plate_appearances += int(stats['plateAppearances'])
        team_total_bases += int(stats['totalBases'])
        team_rbi += int(stats['rbi'])
        team_left_on_base += int(stats['leftOnBase'])
        team_sac_bunts += int(stats['sacBunts'])
        team_sac_flies += int(stats['sacFlies'])
        team_catchers_interference += int(stats['catchersInterference'])

        # Weighted rate stats
        weighted_avg += safe_float(stats['avg']) * pa
        weighted_obp += safe_float(stats['obp']) * pa
        weighted_slg += safe_float(stats['slg']) * pa
        weighted_ops += safe_float(stats['ops']) * pa
        weighted_stolen_base_percentage += safe_float(stats['stolenBasePercentage']) * pa
        weighted_caught_stealing_percentage += safe_float(stats['caughtStealingPercentage']) * pa
        weighted_babip += safe_float(stats['babip']) * pa
        weighted_ground_to_air_outs += safe_float(stats['groundOutsToAirouts']) * pa
        weighted_at_bats_per_home_run += safe_float(stats['atBatsPerHomeRun']) * pa



         

           
    # after player loop get final team rate stats


    print(f"{team}: total PA = {team_plate_appearances}")

    team_avg = weighted_avg / team_plate_appearances
    team_obp = weighted_obp / team_plate_appearances
    team_slg = weighted_slg / team_plate_appearances
    team_ops = weighted_ops / team_plate_appearances
    team_stolen_base_percentage = (
        weighted_stolen_base_percentage / team_plate_appearances
    )
    team_caught_stealing_percentage = (
        weighted_caught_stealing_percentage / team_plate_appearances
    )
    team_babip = weighted_babip / team_plate_appearances
    team_ground_to_air_outs = (
        weighted_ground_to_air_outs / team_plate_appearances
    )
    team_at_bats_per_home_run = (
        weighted_at_bats_per_home_run / team_plate_appearances
    )



    # store aggregated team batting stats
    team_stats[team]['team_batting'] = {

    # counting stats
    'gamesPlayed': team_games_played,
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
    'plateAppearances': team_plate_appearances,
    'totalBases': team_total_bases,
    'rbi': team_rbi,
    'leftOnBase': team_left_on_base,
    'sacBunts': team_sac_bunts,
    'sacFlies': team_sac_flies,
    'catchersInterference': team_catchers_interference,

    # rate stats
    'avg': team_avg,
    'obp': team_obp,
    'slg': team_slg,
    'ops': team_ops,
    'stolenBasePercentage': team_stolen_base_percentage,
    'caughtStealingPercentage': team_caught_stealing_percentage,
    'babip': team_babip,
    'groundOutsToAirouts': team_ground_to_air_outs,
    'atBatsPerHomeRun': team_at_bats_per_home_run
}

with open('team_data_with_batting.json', 'w') as f:
    json.dump(team_stats, f)