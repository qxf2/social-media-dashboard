from flask import Flask, render_template
import requests,json
#import twitter
#from mailchimp3 import MailChimp
import sqlite3


"""
client = MailChimp(mc_api='03281ad59bc173990352760cb8970643-us3', mc_user='rohan.j@qxf2.com')

api = twitter.Api(consumer_key='ipUWYOeJexFpviIzjqC5jBuBx',
    consumer_secret='ewXUeJbfst1AbGIu2rBY3M64fIuh9NPCS45CDuVcRoLc5KKBS6',
    access_token_key='155219549-4RmRcfHsaU1hjPpKp0531N9kBCUow4FvY9sbPt6q',
    access_token_secret='xnXmcKtkMKnnO3IfZgRQmNSFgJpjIiTqXj7nE9JZvzIvA')
"""

app = Flask(__name__)
"""
def get_docker_pulls():
    response = requests.get('https://hub.docker.com/v2/repositories/qxf2rohand/qxf2_pom_essentials/')
    jsonResponse = response.json()
    return jsonResponse['pull_count']

def get_github_stats():
    headers = {'Accept': 'application/vnd.github.scarlet-witch-preview+json'}
    response = requests.get('https://api.github.com/repos/qxf2/qxf2-page-object-model')
    jsonResponse = response.json()
    forks = jsonResponse['forks']
    stars = jsonResponse['stargazers_count']
    subscribers = jsonResponse['subscribers_count']
    return forks,stars,subscribers

def get_blog_post_stats():
    response = requests.get('https://qxf2.com/blog/wp-json/wp/v2/posts')
    return response.headers['X-WP-Total']

def get_twitter_followers():
    try :
        followers = api.GetFollowers(screen_name='Qxf21')
        following = api.GetFriends(screen_name='Qxf21')
        return {'followers':len(followers),'following':len(following)}
    except:
        followers = 500
        following = 300
        return {'followers':followers,'following':following}
    

def get_all_campaigns():
    campaigns_dict = client.campaigns.all(get_all=True)
    campaigns_list = campaigns_dict['campaigns']
    campaigns_count = 1
    for campaign in campaigns_list:
        if 'The Informed Tester’s Newsletter' in campaign['settings']['title']:
            campaigns_count +=1
    
    subscriber_dict = client.lists.members.all('3562d1c87b', get_all=True)
    subscriber_count = 0
    for subscriber in subscriber_dict['members']:
        if subscriber['status'] == 'subscribed':
            subscriber_count +=1
    return campaigns_count,subscriber_count

@app.route('/')
def home():
    pull_count = get_docker_pulls()
    blog_post_count = get_blog_post_stats()
    github_forks,stars,subscribers = get_github_stats()
    twitter_stats = get_twitter_followers()
    campaigns_count,subscribers_count = get_all_campaigns()
    #return render_template('index.html',docker_pull=pull_count,blog_post_count=blog_post_count,github_forks=github_forks,followers=twitter_stats['followers'],following=twitter_stats['following'])
    return render_template('index.html',docker_pull=pull_count,blog_post_count=blog_post_count,github_forks=github_forks,github_stars=stars,github_subscribers=subscribers,followers=twitter_stats['followers'],following=twitter_stats['following'],campaigns_count=campaigns_count,subscribers_count=subscribers_count)
"""

@app.route('/')
def home():
    conn = sqlite3.connect('social-media-dashboard.db')
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