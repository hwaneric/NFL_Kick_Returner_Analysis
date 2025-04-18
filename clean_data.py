import pandas as pd
import os

INPUT_FILE = './raw_data/play_by_play_1999.csv'
OUTPUT_FILE = './modified_data/kickoff_plays_1999.csv'

def remove_unecessary_data(input_file):
    # Load the data
    columns_to_read = [
        'play_id', 'game_id', 'old_game_id', 'home_team', 'away_team', 'season_type', 'week', 
        'posteam', 'posteam_type', 'defteam', 'side_of_field', 'yardline_100', 'game_date', 
        'quarter_seconds_remaining', 'half_seconds_remaining', 'game_half', 'time', 'yrdln', 
        'play_type', 'desc', 'ep', 'epa', 'kick_distance', 'touchback', 'kickoff_in_endzone', 
        'kickoff_out_of_bounds', 'kickoff_downed', 'kickoff_fair_catch', 'fumble_forced', 
        'fumble_not_forced', 'own_kickoff_recovery', 'own_kickoff_recovery_td', 'kickoff_attempt', 
        'kickoff_returner_player_name', 'kickoff_returner_player_id', 
        'lateral_kickoff_returner_player_id', 'lateral_kickoff_returner_player_name', 
        'kicker_player_name', 'kicker_player_id', 'own_kickoff_recovery_player_id', 
        'own_kickoff_recovery_player_name', 'return_team', 'return_yards', 'penalty_team', 
        'penalty_player_id', 'penalty_player_name', 'penalty_yards', 'penalty_type', 'location'
    ]
    data = pd.read_csv(input_file, usecols=columns_to_read, dtype={"lateral_kickoff_returner_player_id": str, "lateral_kickoff_returner_player_name": str, "own_kickoff_recovery_player_id": str, "own_kickoff_recovery_player_name": str})

    # Filter rows where play_type is "kickoff"
    kickoff_data = data[data['play_type'] == 'kickoff']
    return kickoff_data 
   

if __name__ == "__main__":
    raw_data_dir = './raw_data'

    for file_name in os.listdir(raw_data_dir):
        if file_name.endswith('.csv'):
            input_file = os.path.join(raw_data_dir, file_name)
            year = file_name.split('_')[-1].split('.')[0]

            print(f"Processing file: {input_file}")
            data = remove_unecessary_data(input_file)

            output_file = os.path.join('./modified_data', f'kickoff_plays_{year}.csv')
            data.to_csv(output_file, index=False)
            print(f"Filtered data saved to {output_file}")
    
    
    


    # kickoff_data = remove_unecessary_data()
    # print(kickoff_data.head())
    # # Save the filtered data to 
    # # a new CSV
    # kickoff_data.to_csv(OUTPUT_FILE, index=False)
    # print(f"Kickoff data saved to {OUTPUT_FILE}")