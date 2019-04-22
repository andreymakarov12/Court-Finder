from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user

from CourtFinder import db
from CourtFinder.models.courts import Court, CourtReview
from CourtFinder.models.users import User

from CourtFinder.endpoints.courts.forms import CourtSearch

import json

courts = Blueprint('courts', __name__)


@courts.route('/courts', methods=['GET', 'POST'])
def list_courts():
    form = CourtSearch()

    if request.method == 'GET':
        court = Court.query.all()
        return render_template('courts/courts.html', Courts=court, form=form)

    else:
        tpe = form.type.data
        dist = form.distance.data
        lght = form.lights.data

        court = Court.query.filter((Court.lights == lght) & (Court.membership_required == tpe)).all()
        return render_template('courts/courts.html', Courts=court, form=form)


@courts.route('/court/<id>', methods=['GET', 'POST'])
def list_court(id):
    if request.method == 'GET':
        court = Court.query.filter_by(id=id).first()
        reviews = CourtReview.query.filter_by(court_id=id)

        return render_template('courts/courtProfile.html', Court=court, Reviews=reviews)

    elif request.method == 'POST':
        court = Court.query.filter_by(id=id).first()
        reviews = CourtReview.query.filter_by(court_id=id)

        # Check if user is logged in before allowing to post to DB
        if not current_user.is_authenticated:
            return redirect(url_for("users.login"))

        # Make sure theres a review typed in
        if request.form.get('court_review') == '':
            flash("Please enter a review!", "danger")
            return render_template('courts/courtProfile.html', Court=court, Reviews=reviews)

        add_review = request.form.get('court_review')

        court_review = CourtReview.query.filter_by(court_id=id).first()
        user = User.query.filter_by(id=current_user.get_id()).first()

        # If a review doesnt exsist already make a new one
        if not court_review:
            court_review = CourtReview(
                court_id=id,
                user_id=user.id,
                username=user.username,
                review=add_review)
        else:
            court_review.review = add_review

        db.session.add(court_review)
        db.session.commit()

        return render_template('courts/courtProfile.html', Court=court, Reviews=reviews)


@courts.route("/map")
def map_view():
    courts_query = Court.query.all()
    # This is a list comprehension - it works exactly the same as the for loop below. I went with the for loop for a better readability

    # courts = {court.id :{"name" : court.name, "latlng":{ "lat": float(court.latitude), "lng":float(court.longitude)}} for court in courts}

    courts = {}
    for court in courts_query:
        courts[court.id] = {
            "name": court.name,
            "latlng": {
                "lat": float(court.latitude),
                "lng": float(court.longitude)
            }
        }

    return render_template('courts/map.html', courts=courts)


@courts.route('/CreateCourt', methods=['GET', 'POST'])
def createCourt():
    if request.method == 'GET':
        return render_template('courts/CreateCourt.html')

    elif request.method == 'POST':
        court = Court(
            address=request.form.get('inputCourtAddress'),
            name=request.form.get('inputCourtName'),
            total_courts=request.form.get('inputNumCourts'),
            total_visits=0,
            lights=int(request.form.get('lightsRadios')),
            membership_required=int(request.form.get('publicprivateRadios')),
            description=request.form.get('inputCourtDescription'),
            latitude=request.form.get('xCoordCourt'),
            longitude=request.form.get('yCoordCourt'))
        db.session.add(court)
        db.session.commit()

        flash('Court Created!', 'success')
        return redirect(url_for('courts.list_courts'))


@courts.route('/UpdateCourt/<id>', methods=['GET', 'POST'])
def updateCourt(id):
    if request.method == 'POST':
        court = Court.query.filter_by(id=id).first()

        court.adress = request.form.get('inputCourtAddress')
        court.name = request.form.get('inputCourtName')
        court.total_courts = request.form.get('inputNumCourts')
        court.total_visits = 0
        court.lights = int(request.form.get('lightsRadios'))
        court.membership_required = int(request.form.get('publicprivateRadios'))
        court.description = request.form.get('inputCourtDescription')
        court.latitude = request.form.get('xCoordCourt')
        court.longitude = request.form.get('yCoordCourt')

        db.session.commit()
        flash('Your court has been updated!', 'success')
        return redirect(url_for('courts.list_courts'))

    elif request.method == 'GET':

        court = Court.query.filter_by(id=id).first()
        return render_template('courts/UpdateCourt.html', court=court)


@courts.route('/DeleteCourt/<id>', methods=['GET'])
def deleteCourt(id):
    if request.method == 'GET':
        court = Court.query.filter_by(id=id).first()

        db.session.delete(court)
        db.session.commit()

        flash('Court has been deleted', 'success')
        return redirect(url_for('courts.list_courts'))
