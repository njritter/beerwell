from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


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
