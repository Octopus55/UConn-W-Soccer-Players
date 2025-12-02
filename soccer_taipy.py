from taipy.gui import Gui, Icon
import taipy.gui.builder as tgb
import plotly.graph_objects as go
import pandas as pd
import warnings
from soccer_tp_funcs import get_all_players

warnings.filterwarnings('ignore')

all_players = get_all_players()

all_players[['home_team', 'rest']] = all_players['Match'].str.split(' - ', expand=True)
all_players[['away_team', 'score']] = all_players['rest'].str.extract(r'(.+?) (\d+:\d+)$')
all_players[['home_score', 'away_score']] = all_players['score'].str.split(':', expand=True)
all_players.drop(columns='rest', inplace=True)

# Create percentage columns and insert them in the correct spot in the df
# Potentially change category_list later
# fix cumulative and per 90 buttons for the percentage case
all_players['Save Opps'] = all_players['Total Saves'] + all_players['Conceded goals']

divisors = {'Successful actions': 'Total actions', 'Shots on target': 'Shots', 'Accurate Passes': 'Passes Attempted', 'Long passes accurate': 'Total Long passes',
            'Crosses accurate': 'Total Crosses', 'Successful Dribbles': 'Total Dribbles', 'Duels Won': 'Total Duels', 'Aerial duels won': 'Total Aerial duels', 'Defensive duels won': 'Total Defensive duels',
            'Loose ball duels won': 'Total Loose ball duels', 'Offensive duels won': 'Total Offensive duels', 'Through passes accurate': 'Total Through passes', 'Passes to final third accurate': 'Total Passes to final third',
            'Passes to penalty area accurate': 'Total Passes to penalty area', 'Forward passes accurate': 'Total Forward passes', 'Back passes accurate': 'Total Back passes', 'Passes to GK accurate': 'Total Passes to GK',
            'Total Saves': 'Save Opps', 'Saves with reflexes': 'Total Saves'}

def percentage(df, divisors:dict):
    for dividend, divisor in divisors.items():
        #df[dividend + ' %'] = 100*df[dividend]/df[divisor]
        percentage_col = 100*df[dividend]/df[divisor]
        dividend_index = df.columns.get_loc(dividend)
        df.insert(dividend_index + 1, dividend + ' percentage', percentage_col)
        df[dividend + ' percentage'] = df[dividend + ' percentage'].fillna(0).round(2)

percentage(all_players, divisors)

# if undefined, just set as 0
# round to 2 decimal places

#all_players['']

#print(all_players['player'].unique())

# State variables
selected_player = "null"
player_list = sorted(all_players["player"].unique().tolist())
selected_player_df = all_players[all_players["player"] == "null"]

selected_category = "null"
category_list = all_players.columns[6:-6]
plot_variable = "Minutes played"

# Initializing modes
mode_options = ["Per 90", "Cumulative"]
selected_modes = []

# Callback to update filtered data and column selection
def update_player(state):
    if 'null' in state.selected_player:
        state.selected_player.remove('null')
    #print(state.selected_player)
    state.selected_player_df = all_players[all_players["player"].isin(state.selected_player)]

    #if 'null' in state.selected_category:
    #    state.selected_category.remove('null')
    
    plot_variable = state.selected_category

    # Handle Modes
    if 'Cumulative' in state.selected_modes:
        state.selected_player_df = state.selected_player_df.sort_values(['player', 'Date'])

        if 'percentage' in plot_variable:
            variable_dividend = plot_variable.rsplit(" ", 1)[0]
            variable_divisor = divisors[variable_dividend]
            state.selected_player_df['Cumulative ' + variable_dividend] = state.selected_player_df.groupby("player")[variable_dividend].cumsum()
            state.selected_player_df['Cumulative ' + variable_divisor] = state.selected_player_df.groupby("player")[variable_divisor].cumsum()
            state.selected_player_df['Cumulative ' + plot_variable] = 100*state.selected_player_df['Cumulative ' + variable_dividend]/state.selected_player_df['Cumulative ' + variable_divisor]
            state.selected_player_df['Cumulative ' + plot_variable] = state.selected_player_df['Cumulative ' + plot_variable].fillna(0).round(2)
        else:
            state.selected_player_df['Cumulative Minutes'] = state.selected_player_df.groupby("player")['Minutes played'].cumsum()
            state.selected_player_df['Cumulative ' + plot_variable] = state.selected_player_df.groupby("player")[plot_variable].cumsum()
        
        state.selected_player_df = state.selected_player_df.sort_values(['player', 'Date'], ascending=False)
        plot_variable = 'Cumulative ' + plot_variable

        if 'Per 90' in state.selected_modes:
            if 'percentage' in plot_variable:
                pass
            else:
                state.selected_player_df[plot_variable + ' Per 90'] = round(state.selected_player_df.loc[:, plot_variable] / (state.selected_player_df.loc[:, 'Cumulative Minutes']/90), 2)
                plot_variable = plot_variable + ' Per 90'
    elif 'Per 90' in state.selected_modes:
        if 'percentage' in plot_variable:
                pass
        else:
            state.selected_player_df[plot_variable + ' Per 90'] = round(state.selected_player_df.loc[:, plot_variable] / (state.selected_player_df.loc[:, 'Minutes played']/90), 2)
            plot_variable = plot_variable + ' Per 90'


    pivoted = state.selected_player_df.pivot(index="Date", columns="player", values=plot_variable).reset_index()

    # Create tooltip text
    #season_comp['tooltip_text'] = season_comp.apply(
    #    lambda row: f"{row['Home Team']} {str(row['Score'])[0]} - {row['Away Team']} {str(row['Score'])[2]}",
    #    axis=1
    #)
    #print(pivoted)
    def get_tooltip_text(player):
        text = list(state.selected_player_df.loc[state.selected_player_df['player'] == player, 'Match'])
        return text
    
    #print(get_tooltip_text('C. Okafor'))
    #print(type(get_tooltip_text('C. Okafor')))

    fig = go.Figure()
    for p in state.selected_player:

        specific_player_df = state.selected_player_df[state.selected_player_df['player'] == p]
        specific_player_pivoted = pivoted[['Date', p]].dropna()

        fig.add_trace(go.Scatter(x=specific_player_pivoted["Date"], y=specific_player_pivoted[p], mode="lines+markers", name=p, marker=dict(size=8),
                                 customdata=specific_player_df[['home_team', 'away_team', 'home_score', 'away_score']].values[::-1],
                                 hovertemplate=("<b>%{customdata[0]} %{customdata[2]} - %{customdata[1]} %{customdata[3]}</b><br>" +
                                                p + ' ' + plot_variable + " = %{y}")
                                 #hovertext=get_tooltip_text(p)
                                 ))
        #print(specific_player_df[['player', 'home_team', 'away_team', 'home_score', 'away_score']])
        #print(specific_player_pivoted)
    
    # Add axis titles
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=plot_variable
    )
    
    state.chart_figure = fig

with tgb.Page() as page:
    #tgb.text('Player Comparison Tool', class_name='heading')
    tgb.html("h2", "Player Comparison Tool")
    tgb.selector(
        value="{selected_player}",
        lov="{player_list}",
        multiple=True,
        on_change=update_player,
        label="Select Player",
        dropdown=True
    )
    tgb.selector(
        value="{selected_category}",
        lov="{category_list}",
        multiple=False,
        on_change=update_player,
        label="Select Stat Category",
        dropdown=True
    )
    tgb.selector(
        value="{selected_modes}",
        lov="{mode_options}",
        mode="check",
        multiple=True,
        on_change=update_player,
        label="Options"
    )
    tgb.chart(figure="{chart_figure}")

    '''tgb.chart(data="{selected_player_df}",
              x='Date',
              y='Minutes played',
              type='line')'''

# runs well for editing with the command ls soccer_taipy.py | entr -r python3 soccer_taipy.py

if __name__ == "__main__":
    chart_figure = None
    Gui(page=page, css_file='soccer_taipy.css').run(title="UConn Women's Soccer | Player Comparison Tool", favicon='logo.ico', host="0.0.0.0", port=10000)