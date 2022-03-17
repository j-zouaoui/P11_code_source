from datetime import datetime
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
    return render_template('index.html', club=clubs)

@app.route('/showSummary',methods=['POST'])
def showSummary():

    email = request.form['email']
    # if condition has been integrate to fix issue 1 by checking if club email exist
    # creating a club email list
    club_email = []
    for club in clubs:
        club_email.append(club["email"])
    # check if email exist in club email list otherwise display message error
    if email not in club_email:
        flash("unknown mail")
        return render_template('index.html')
    else:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

@app.route('/book/<competition>/<club>')
def book(competition,club):

    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    #solving porblem relative to booking past compete date
    to_day_date = datetime.today()
    competition_date = foundCompetition["date"]
    competition_date_obj = datetime.strptime(competition_date, "%Y-%m-%d %H:%M:%S")
    if foundClub and foundCompetition:
        if competition_date_obj < to_day_date:
            flash("date de competition expirer")
            #redirect to showsummary
            return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)
            #during test the url end point n ete pas le bon
        else:
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    club_points = int(club['points'])  # club points
    placesRequired = int(request.form['places'])


    # club point sold is less than requested place (we assume 1 place needed 1 point)
    if placesRequired > club_points:
        flash('Solde des points insuffisants')
        return render_template('booking.html', club=club, competition=competition)

    # Requested places greater than what it is available
    elif placesRequired > int(competition['numberOfPlaces']):
        flash('Nembre de places demander superieur au place disponible')
        return render_template('booking.html', club=club, competition=competition)

    # Fixing issue 3 which define the maximum place to reserve = 12
    elif placesRequired > 12:
        flash('Vous pouvez reserver 12 place maximum')
        return render_template('booking.html', club=club, competition=competition)

    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        updated_club_points = int(club['points']) - placesRequired
        club_name = club['name']
        updating_club_score(club_name, updated_club_points)
        updated_clubs_list = loadClubs()
        club = [c for c in updated_clubs_list if c['name'] == request.form['club']][0]
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions, clubs=updated_clubs_list)



# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))