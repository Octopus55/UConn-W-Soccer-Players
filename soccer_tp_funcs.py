import pandas as pd
import os

def clean_col_names_player(data):
    clean_cols = data.rename(columns={'Total actions / successful': 'Total actions',
                                      'Unnamed: 6': 'Successful actions',
                                      'Shots / on target': 'Shots',
                                      'Unnamed: 10': 'Shots on target',
                                      'Passes / accurate': 'Passes Attempted',
                                      'Unnamed: 13': 'Accurate Passes',
                                      'Long passes / accurate': 'Total Long passes',
                                      'Unnamed: 15': 'Long passes accurate',
                                      'Crosses / accurate': 'Total Crosses',
                                      'Unnamed: 17': 'Crosses accurate',
                                      'Dribbles / successful': 'Total Dribbles',
                                      'Unnamed: 19': 'Successful Dribbles',
                                      'Duels / won': 'Total Duels',
                                      'Unnamed: 21': 'Duels Won',
                                      'Aerial duels / won': 'Total Aerial duels',
                                      'Unnamed: 23': 'Aerial duels won',
                                      'Losses / own half': 'Total Losses',
                                      'Unnamed: 26': 'Losses in own half',
                                      'Recoveries / opp. half': 'Total Recoveries',
                                      'Unnamed: 28': 'Recoveries in opponent half',
                                      'Defensive duels / won': 'Total Defensive duels',
                                      'Unnamed: 32': 'Defensive duels won',
                                      'Loose ball duels / won': 'Total Loose ball duels',
                                      'Unnamed: 34': 'Loose ball duels won',
                                      'Sliding tackles / successful': 'Total Sliding tackles',
                                      'Unnamed: 36': 'Sliding tackles successful',
                                      'Offensive duels / won': 'Total Offensive duels',
                                      'Unnamed: 43': 'Offensive duels won',
                                      'Through passes / accurate': 'Total Through passes',
                                      'Unnamed: 49': 'Through passes accurate',
                                      'Passes to final third / accurate': 'Total Passes to final third',
                                      'Unnamed: 53': 'Passes to final third accurate',
                                      'Passes to penalty area / accurate': 'Total Passes to penalty area',
                                      'Unnamed: 55': 'Passes to penalty area accurate',
                                      'Forward passes / accurate': 'Total Forward passes',
                                      'Unnamed: 58': 'Forward passes accurate',
                                      'Back passes / accurate': 'Total Back passes',
                                      'Unnamed: 60': 'Back passes accurate',
                                      'Saves / with reflexes': 'Total Saves',
                                      'Unnamed: 65': 'Saves with reflexes',
                                      'Passes to GK / accurate': 'Total Passes to GK',
                                      'Unnamed: 68': 'Passes to GK accurate'
    })
    return clean_cols

def get_all_players():
    players_list = ['A_Yamas', 'S_Parker', 'E_DiBlasi',
                'L_Dantes', 'A_Carson', 'M_Mooney', 'R_Prozzo', 'I_Nourani',
                'A_Johnson', 'L_LeBlanc', 'A_Merchant', 'T_Jenkins', 'R_Lifrieri', 'B_Brown', 'T_Righetti', 'G_Miller','M_van Doesburg', 'J_Carr', 'K_Richins',
                'N_Ocio', 'K_Monaco', 'C_Okafor', 'Ala_Taylor', 'K_Gorman', 'I_Meadows', 'Ale_Taylor', 'K_Fraser', 'S_Mars', 'F_Stephens-Martin']
    
    positions_list = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']

    all_players = pd.DataFrame()

    for player in players_list:
        for position in positions_list:
        
            #file_path = f'../data/players/2025_season/{position}/Player stats {player.replace('_', '. ')}.csv'
            file_path = f"player_data/Player stats {player.replace('_', '. ')}.csv"
            if os.path.exists(file_path):
                player_df = pd.read_csv(file_path)
                player_df = clean_col_names_player(player_df)
                player_df.insert(0, 'player', player.replace('_', '. '))
                player_df['Date'] = pd.to_datetime(player_df['Date'])
                player_df.insert(4, 'Year', player_df['Date'].dt.year)
                all_players = pd.concat([all_players, player_df])
                break

    return all_players