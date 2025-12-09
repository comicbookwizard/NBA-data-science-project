import numpy as np
import pandas as pd
import os

def filter_stats_of_current_players(stats_csv, active_starters_csv, output_csv="FilteredPlayers.csv"):
    """
    Filters starters from the player statistics CSV based on active starters CSV.

    Args:
        stats_csv (str): Path to the player statistics CSV file.
        active_starters_csv (str): Path to the active starters CSV file.
        output_csv (str): Path to save the filtered CSV file.

    Returns:
        pd.DataFrame: DataFrame containing only the statstics of current players.
    """
    players_df = pd.read_csv(stats_csv) # Load player data 
    starters_df = pd.read_csv(active_starters_csv) # Load starter names

    players_df["playerName"] = (players_df["firstName"] + " " + players_df["lastName"]).str.replace(r"\s+", " ", regex=True).str.strip() # Creates full names column
    starters_df["playerName"] = (starters_df["firstName"] + " " + starters_df["lastName"]).str.replace(r"\s+", " ", regex=True).str.strip() 

    filtered_df = players_df[players_df["playerName"].isin(starters_df["playerName"].tolist())] # Filters players to only include starters

    folder = os.path.dirname(output_csv) # Create output directory if it doesn't exist
    if folder and not os.path.exists(folder): 
        os.makedirs(folder)

    filtered_df.to_csv(output_csv, index=False) # Save filtered CSV
    return filtered_df


if __name__ == "__main__":
    players_csv = 'PlayerStatistics.csv'
    active_starters_csv = 'ActivePlayers.csv'
    output_csv = 'FilteredPlayers.csv'

    filtered_players = filter_stats_of_current_players(players_csv, active_starters_csv)

    # Remove original first/last name columns
    for col in ["firstName", "lastName"]:
        if col in filtered_players.columns:
            filtered_players = filtered_players.drop(columns=[col])

    # Reorder columns to have playerName first
    cols = ["playerName"] + [c for c in filtered_players.columns if c != "playerName"]
    filtered_players = filtered_players[cols]

    # Save CSV
    filtered_players.to_csv(output_csv, index=False)

    print(f"\nSaved filtered CSV to: {output_csv}\n")
