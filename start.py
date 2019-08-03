from flask import Flask, render_template, request, redirect
from data import populate_chart

app = Flask(__name__)
base_url = "http://127.0.0.1:5000"
# Hoemepage, search for a single player or navigate to comparison page
@app.route('/', methods=["GET", "POST"])
def player_search():

    if request.method == "POST":
        
        # If the user wants to compare two players
        if request.form["go"] == "compare_players":
            return "<h1> Hello </h1>"


        # User chooses to look at a single player's map
        else:

            player = ""
            season = ""
            maptype = ""

            player = request.form["player"].strip()
            season = request.form["season"].strip()
            
            try:
                maptype = request.form["map_type"]
            except:
                return redirect("%s/error" %base_url)


            if maptype == "heatmap":
                try:
                    filter_paint_shots = request.form["filter"]
                except:
                    return redirect("%s/error" %base_url)
            else:
                filter_paint_shots = "no"


            if (player != "" and season != "" and maptype != ""):
                return redirect("%s/%s/%s/%s/%s" %(base_url, player, season, maptype, filter_paint_shots))
            else:
                # If invalid strings are input, redirect to a standard error page
                return redirect("%s/error" %base_url)

    else:

        return render_template('player_search.html')



# URL at which the heatmap/shotchart shows up for a single player
@app.route('/<playerName>/<seasonName>/<maptype>/<filter_paint_shots>')
def playerName(playerName, seasonName, maptype, filter_paint_shots):

    bball_court = populate_chart(playerName, seasonName, maptype, filter_paint_shots)
    return render_template('graphs.html', graph1=bball_court, player=playerName, season=seasonName)


@app.route('/error')
def error():
    return "<h1> Error! Check your player name and the format of the season and the map type</h1>"

if __name__ == '__main__':
   app.run(debug = True)