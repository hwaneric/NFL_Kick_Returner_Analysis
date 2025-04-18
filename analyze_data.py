import pandas as pd 
import os

INPUT_FILE = './modified_data/kickoff_plays.csv'
OUTPUT_FILE = './results/kickoff_returners_1999.csv'
GROUPED_OUTPUT_FILE = './results/grouped_kickoff_returners.csv'

def calculate_avg_epa(input_files):

    data_frames = []
    for input_file in input_files:
        df = pd.read_csv(input_file, dtype={"lateral_kickoff_returner_player_id": str, "lateral_kickoff_returner_player_name": str, "own_kickoff_recovery_player_id": str, "own_kickoff_recovery_player_name": str})
        data_frames.append(df)
    
    data = pd.concat(data_frames, ignore_index=True)
    data = data.sort_values(by="kickoff_returner_player_id")
    data.to_csv(GROUPED_OUTPUT_FILE, index=False)
        
    result = data.groupby("kickoff_returner_player_id").agg(
        avg_ep=("ep", "mean"),
        avg_epa=("epa", "mean"),
        return_count=("kickoff_returner_player_id", "size")
    ).reset_index()

    result = result.merge(
        data[["kickoff_returner_player_id", "kickoff_returner_player_name"]].drop_duplicates(),
        on="kickoff_returner_player_id",
        how="left"
    )
    filtered_result = result[result["return_count"] >= 20]
    print(filtered_result.nlargest(5, "avg_epa"))
    return result



if __name__ == "__main__":
    cleaned_data_dir = './modified_data'
    eras = {"1999_to_2010": [], "2011_to_2015": [], "2016_to_2023": [], "2024": []}
    
    for file_name in os.listdir(cleaned_data_dir):
        if file_name.endswith('.csv'):
            input_file = os.path.join(cleaned_data_dir, file_name)

            print(f"Processing file: {input_file}")

            year = int(file_name.split('_')[-1].split('.')[0])
            if year <= 2010:
                eras["1999_to_2010"].append(input_file)
            elif year <= 2015:
                eras["2011_to_2015"].append(input_file)
            elif year <= 2023:
                eras["2016_to_2023"].append(input_file)
            else:
                eras["2024"].append(input_file)

    for era, input_files in eras.items():
        print(f"Processing era: {era}")
        result = calculate_avg_epa(input_files)
        output_file = os.path.join('./results', f'kickoff_returners_{era}.csv')
        result.to_csv(output_file, index=False)
        print(f"Average EPA and EP for each kickoff returner saved to {output_file}")
    
