from flask import Flask, render_template, request, redirect
from data import populate_chart

app = Flask(__name__)

# Hoemepage, search for a single player or navigate to comparison page
@app.route('/', methods=["GET", "POST"])
def player_search():

    if request.method == "POST":
        
        # If the user wants to compare two players
        if request.form["go"] == "compare_players":
            return redirect("/compare")


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
                return redirect("/error")


            if maptype == "heatmap":
                try:
                    filter_paint_shots = request.form["filter"]
                except:
                    return redirect("/error")
            else:
                filter_paint_shots = "no"


            if (player != "" and season != "" and maptype != ""):
                return redirect("/%s/%s/%s/%s" %(player, season, maptype, filter_paint_shots))
            else:
                # If invalid strings are input, redirect to a standard error page
                return redirect("/error")

    else:

        return render_template("player_search.html")


# URL at which the heatmap/shotchart shows up for a single player
@app.route('/<playerName>/<seasonName>/<maptype>/<filter_paint_shots>')
def singlePlayerData(playerName, seasonName, maptype, filter_paint_shots):

    bball_court = populate_chart(playerName, seasonName, maptype, filter_paint_shots)
    return render_template('graphs.html', graph1=bball_court, player=playerName, season=seasonName)


# URL where you can look at two players side by side
@app.route('/compare', methods=["GET", "POST"])
def compare():

    if request.method == "POST":
        
        p1 = ""
        s1 = ""
        p2 = ""
        s2 = ""

        p1 = request.form["p1"].strip()
        s1 = request.form["s1"].strip()
        p2 = request.form["p2"].strip()
        s2 = request.form["s2"].strip()
        
        try:
            maptype = request.form["map_type"]
        except:
            return redirect("/error")


        if maptype == "heatmap":
            try:
                filter_paint_shots = request.form["filter"]
            except:
                return redirect("/error")
        else:
            filter_paint_shots = "no"


        if (p1 != "" and p2 != "" and s1 != "" and s2 != "" and maptype != ""):
            return redirect("/compare/%s/%s/%s/%s/%s/%s" %(p1, s1, p2, s2, maptype, filter_paint_shots))
        else:
            # If invalid strings are input, redirect to a standard error page
            return redirect("/error")

    else:

        return render_template("player_compare.html")



@app.route('/compare/<p1>/<s1>/<p2>/<s2>/<maptype>/<filter_paint_shots>')
def multiPlayerData(p1, s1, p2, s2, maptype, filter_paint_shots):

    p1_data = populate_chart(p1, s1, maptype, filter_paint_shots)
    p2_data = populate_chart(p2, s2, maptype, filter_paint_shots)
    return render_template('player_compare_graphs.html', graph1=p1_data, graph2= p2_data, p1=p1, s1=s1, p2=p2, s2=s2)


@app.route('/error')
def error():
    return "<h1> Error! Check your player name and the format of the season and the map type</h1>"

if __name__ == '__main__':
   app.run(debug = True)