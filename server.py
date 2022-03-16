import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

def updating_club_score(club_name, updated_club_points):
    """
    this function allows to update the club points value by rewriting club json file
    :param club_name:
    :param updated_point:
    :return: clubs.json file updated withe the new value of point
    """
    with open('clubs.json', "r+") as c:
        listOfClubs = json.load(c)['clubs']

        for club in listOfClubs:
            if club['name'] == club_name:
                club['points'] = updated_club_points
                break
        data = {"clubs": listOfClubs}

        c.seek(0)  # rewind
        json.dump(data, c)
        c.truncate()

def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    updated_club_points = int(club['points']) - placesRequired
    club_name = club['name']
    updating_club_score(club_name, updated_club_points)
    updated_clubs_list = loadClubs()
    club = [c for c in updated_clubs_list if c['name'] == request.form['club']][0]
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))