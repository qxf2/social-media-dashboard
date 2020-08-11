import sqlite3
import requests
import twitter
from mailchimp3 import MailChimp
from datetime import datetime
from conf import credentials_conf as conf


client = MailChimp(mc_api=conf.MC_API, mc_user=conf.MC_USER)

api = twitter.Api(consumer_key=conf.CONSUMER_KEY,
    consumer_secret=conf.CONSUMER_SECRET,
    access_token_key= conf.ACCESS_TOKEN_KEY,
    access_token_secret=conf.ACCESS_TOKEN_SECRET)

def get_docker_pulls():
    response = requests.get(conf.DOCKER_API_URL)
    jsonResponse = response.json()
    return jsonResponse['pull_count']

def get_github_stats():
    headers = {'Accept': 'application/vnd.github.scarlet-witch-preview+json'}
    response = requests.get(conf.GITHUB_API_URL)
    jsonResponse = response.json()
    forks = jsonResponse['forks']
    stars = jsonResponse['stargazers_count']
    subscribers = jsonResponse['subscribers_count']
    return forks,stars,subscribers

def get_blog_post_stats():
    response = requests.get(conf.BLOGPOST_API_URL)
    return response.headers['X-WP-Total']

def get_twitter_followers():
    try :
        followers = api.GetFollowers(screen_name=conf.SCREEN_NAME)
        following = api.GetFriends(screen_name=conf.SCREEN_NAME)
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
        if 'The Informed' in campaign['settings']['title']:
            campaigns_count +=1
    
    subscriber_dict = client.lists.members.all(conf.SUBSCRIBER_LIST_ID, get_all=True)
    subscriber_count = 0
    for subscriber in subscriber_dict['members']:
        if subscriber['status'] == 'subscribed':
            subscriber_count +=1
    return campaigns_count,subscriber_count

if __name__ == "__main__":
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    pull_count = get_docker_pulls()
    blog_post_count = get_blog_post_stats()
    github_forks,stars,subscribers = get_github_stats()
    twitter_stats = get_twitter_followers()
    campaigns_count,subscribers_count = get_all_campaigns()
    
    conn = sqlite3.connect(conf.DB_NAME)
    c = conn.cursor()    
    c.execute('''CREATE TABLE if not exists stats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recorddate text, 
        follower integer, 
        following integer,
        gforks integer,
        gsubscriber integer,
        gstars integer,
        newsletter integer,
        nsubscriber integer,
        blog integer,
        docker integer)''')

    sql = "insert into stats (recorddate,follower,following,gforks,gsubscriber,gstars,newsletter,nsubscriber,blog,docker) values (?,?,?,?,?,?,?,?,?,?);"
    data = (dt_string,twitter_stats['followers'],twitter_stats['following'],github_forks,subscribers,stars,campaigns_count,subscribers_count,blog_post_count,pull_count)
    c.execute(sql, data)
    
    #c.execute("INSERT into stats VALUES(?,?,?,?,?,?,?,?,?,?)",(dt_string,twitter_stats['followers'],twitter_stats['following'],github_forks,subscribers,stars,campaigns_count,subscribers_count,blog_post_count,pull_count))
    conn.commit()
    c.execute("SELECT * FROM stats ORDER BY id DESC LIMIT 1")
    result = c.fetchone()
    print(result)
    conn.close()