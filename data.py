import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import seaborn as sns
import io
import base64
from nba_api.stats.static import players
from PIL import Image
import os.path


# Method to draw a halfcourt and populate it with the players data
# Takes the players name as input and returns an image
def populate_chart(player, season, maptype, filter_paint_shots, width=2):

    ### Create the halfcourt ###
    fig, ax = plt.subplots(1, figsize=(10, 10))

    hoop = plt.Circle((0, 0), radius=7.5, linewidth=width, color='black', fill=False)

    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=width, color='black', fill=False)

    paint = Rectangle((-60, -47.5), 120, 190, linewidth=width, color='black', fill=False)

    outer_rectangle = Rectangle((-80, -47.5), 160, 190, linewidth=width, color='black', fill=False)

    ft_arc = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=width, color='black', fill=False)

    ft_arc_bottom = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=width, color='black', linestyle="dashed", fill=False)

    corner_3_left = Rectangle((220, -47.5), -1, 140, linewidth=width, color='black', fill=False)

    corner_3_right = Rectangle((-220, -47.5), -1, 140, linewidth=width, color='black', fill=False)

    three_pt_arc = Arc((0, 88), 440, 280, theta1=0, theta2=180, linewidth=width, color='black', fill=False)

    out_of_bounds = Rectangle((-250, -47.5), 500, 470, linewidth=width, color='black', fill=False)

    court_elements = [hoop, backboard, paint, outer_rectangle, ft_arc, ft_arc_bottom, corner_3_left, corner_3_right, three_pt_arc, out_of_bounds]
    for element in court_elements:
        ax.add_patch(element)


    ### Populate the court with the specific players data ###

    player = player.lower()
    playerID = players.find_players_by_full_name(player)[0]["id"]

    url = "https://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=&LeagueID=00&LastNGames=0&TeamID=0&PlayerPosition=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season=%s&AheadBehind=&PlayerID=%d&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=Regular+Season&SeasonSegment=&GameID=" % (season, playerID)

    # Get request headers User Agent
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    response = requests.get(url, headers=headers)
    # Grab the headers to be used as column headers for our DataFrame
    column_headers = response.json()['resultSets'][0]['headers']
    # Grab the shot chart data
    shots = response.json()['resultSets'][0]['rowSet']
    shot_df = pd.DataFrame(data=shots, columns=column_headers)


    if maptype == "heatmap":
        if filter_paint_shots == "no":
            sns.kdeplot(-1*shot_df.LOC_X, shot_df.LOC_Y, shade = "True", color = "red", n_levels = 1000)
        else:
            paint_shots = shot_df[shot_df.SHOT_ZONE_RANGE != "Less Than 8 ft."]
            sns.kdeplot(-1*paint_shots.LOC_X, paint_shots.LOC_Y, shade = "True", color = "red", n_levels = 1000)
    else:
        plt.scatter((-1*shot_df.LOC_X), shot_df.LOC_Y)


    ### Set graph limits and convert to png ###

    ax.set_xlim(-300, 300)
    ax.set_ylim(-100, 500)
    plt.axis("off")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    bball_court = 'data:image/png;base64,{}'.format(graph_url)

    return bball_court


# Method to get a players image
# Takes the players name as input and returns an image
def getPlayerImage(player):

    player = player.lower()
    fullname = player.split()
    firstname = fullname[0]
    lastname = fullname[1]

    if os.path.exists("%s_%s.png" % (lastname, firstname)) == False:

        # If the players image file doesn't exist, create it


        url = "https://nba-players.herokuapp.com/players/%s/%s" % (lastname, firstname)

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

        response = requests.get(url, headers=headers)

        with open("%s_%s.png" % (lastname, firstname),'wb') as f: 
      
            # Saving received content as a png file in 
            # binary format 
          
            # write the contents of the response (r.content) 
            # to a new file in binary mode. 
            f.write(response.content)


    # load the image into a displayable format
    playerImgIO = io.BytesIO()
    player_img = Image.open("%s_%s.png" % (lastname, firstname))
    player_img.save(playerImgIO, "PNG")
    playerImgIO.seek(0)

    url = base64.b64encode(playerImgIO.getvalue()).decode()

    player_img = 'data:image/png;base64,{}'.format(url)

    return player_img