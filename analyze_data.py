import pandas as pd 

INPUT_FILE = './modified_data/kickoff_plays.csv'
OUTPUT_FILE = './results/kickoff_returners_1999.csv'
GROUPED_OUTPUT_FILE = './results/grouped_kickoff_returners_1999.csv'

def calculate_avg_epa():
    data = pd.read_csv(INPUT_FILE, dtype={"lateral_kickoff_returner_player_id": str, "lateral_kickoff_returner_player_name": str, "own_kickoff_recovery_player_id": str, "own_kickoff_recovery_player_name": str})
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
    result.to_csv(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    calculate_avg_epa()
    print(f"Average EPA and EP for each kickoff returner saved to {OUTPUT_FILE}")