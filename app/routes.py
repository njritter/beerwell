from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

import pandas as pd
import json
import plotly
import plotly.graph_objs as go

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Drazi'}
    posts = [
    {
        'author': {'username': 'Drazi'},
        'body': 'Hai there'
    },
    {
        'author': {'username': 'Draziwamai'},
        'body': 'Hai there to you'
    }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test 1'},
        {'author': user, 'body': 'Test 2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/recommendations')
@login_required
def recommendations():
    return render_template('recommendations.html')

@app.route('/explore/')
@app.route('/explore/<ind>')
def explore(ind=0):
    panda = pd.read_pickle('/Users/Drazi/beerwell/app/data/beerpanda.pkd')

    def trace_factory(pandas):
        styles = list(set(pandas['Style']))
        list_of_traces = [] # List of lists of tuples
        for s in styles:
            beers = pandas[pandas['Style'] == s]
            trace = go.Scatter(x = beers['X'],
                            y = beers['Y'],
                            mode = 'markers',
                            marker = {'line': {'width': 1, 'color': '#000000'}},
                            text = beers['Name'],
                            name = s)
            list_of_traces.append(trace)
        return list_of_traces

    list_of_traces = trace_factory(panda)

    myGraph = {
    "data": list_of_traces,
    "layout": go.Layout(
        xaxis = {'showticklabels': False,
                 'showgrid': False,
                 'zeroline': False},
        yaxis = {'showticklabels': False,
                 'showgrid': False,
                 'zeroline': False},
        plot_bgcolor='#C0C0C0')
              }

    myGraphJSON = json.dumps(myGraph, cls=plotly.utils.PlotlyJSONEncoder)

    beers = zip(list(range(250)), panda['Name'].tolist())
    current_beer = panda['Name'].tolist()[int(ind)]
    beer_wordcloud = 'wordclouds/Beer_' + str(ind)
    beer_stats = panda.iloc[int(ind)].tolist() # row from beerPanda

    return render_template('explore.html',
                            myGraphJSON=myGraphJSON,
                            beers=beers,
                            current_beer=current_beer,
                            beer_stats=beer_stats,
                            beer_wordcloud=beer_wordcloud)
