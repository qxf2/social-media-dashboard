from flask import Flask, render_template
import requests,json
import sqlite3
from conf import credentials_conf as conf

app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect(conf.DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM stats ORDER BY recorddate DESC LIMIT 1")
    result = c.fetchone()
    recorddate = result[0]
    followers = result[1]
    following = result[2]
    github_forks = result[3]
    github_subscribers = result[4]
    github_stars = result[5]
    campaigns_count = result[6]
    subscriber_count = result[7]
    blog_post_count = result[8]
    docker_pull = result[9] 
    conn.close()
    return render_template('index.html',recorddate=recorddate,docker_pull=docker_pull,blog_post_count=blog_post_count,github_forks=github_forks,github_stars=github_stars,github_subscribers=github_subscribers,followers=followers,following=following,campaigns_count=campaigns_count,subscribers_count=subscriber_count)

if __name__ == '__main__':
    app.run(debug=True)