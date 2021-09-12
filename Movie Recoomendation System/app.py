

import numpy as np
import pandas as pd
import flask
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = flask.Flask(__name__, template_folder='Templates')

df = pd.read_csv('Recommend_Movies.csv')            
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df['soup'])

df = df.reset_index()
indices = pd.Series(df.index, index=df['Title'])
all_titles = [df['Title'][i] for i in range(len(df['Title']))]

def get_recommendations(title):
  cosine_sim = cosine_similarity(count_matrix, count_matrix)
  idx = indices[title]
  sim_scores = list(enumerate(cosine_sim[idx]))
  sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
  sim_scores = sim_scores[1:11]
  movie_indices = [i[0] for i in sim_scores]
  movies = df.iloc[movie_indices][['Title', 'Year', 'Score','Language']].sort_values('Score', ascending = False)
  return movies



@app.route('/', methods=['GET', 'POST'])

def main():
  if flask.request.method == 'GET':
    return(flask.render_template('index.html'))

  if flask.request.method == 'POST':
    m_name = flask.request.form['movie_name']
    m_name = m_name.title()
    if m_name not in all_titles:
      return(flask.render_template('negative.html', name=m_name))
    else:
      result = get_recommendations(m_name)
      names = []
      year = []
      score = []
      lang = []
      for i in range(len(result)):
        names.append(result.iloc[i][0])
        year.append(result.iloc[i][1])
        score.append(result.iloc[i][2])
        lang.append(result.iloc[i][3])

      return flask.render_template('positive.html', movie_names=names, movie_years=year, movie_scores=score, movie_languages=lang, search_name=m_name)

if __name__ == '__main__':
  app.run(debug=True)
