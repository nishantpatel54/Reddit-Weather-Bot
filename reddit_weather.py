import requests
import json
import praw
import dataset
import sqlalchemy
from time import sleep


def main():
    reddit = praw.Reddit(client_id='WzRggI52vI-jow',
                         client_secret='7npjkP3LtP5FEO-FzFjGANJW5GI',
                         username='TchallaIsMySon',
                         password='nishu5499',
                         user_agent='weather bot at your service')

    subreddit = reddit.subreddit('testingground4bots+ryerson+UofT+uwo+McMaster')
    bot_invoke = '!weatherreport'
    db = dataset.connect('sqlite:///comments.db')

    for comment in subreddit.stream.comments(skip_existing=True):
        if bot_invoke in comment.body:
            if db['replied'].find_one(comment_id=comment.id) == None:
                city = comment.body.replace(bot_invoke, '')
                city.strip()
                comment.reply(weather(city))
                print('posted')
                db['replied'].insert(dict(comment_id=str(comment.id)))
                break


def weather(city):
    api_address = 'http://api.openweathermap.org/data/2.5/weather?'
    api_key = '8e9d852b737762298689ece1c9d5e135'
    uri = api_address + 'units=metric' + "&appid=" + api_key + "&q=" + city
    response = requests.get(uri).json()
    output = ''
    if response['cod'] != '404':
        data = response['main']
        temp = data['temp']
        pressure = data['pressure']
        humidity = data['humidity']
        text = response['weather'][0]['description']
        output += "Hello, today's weather report is, Temperature: " + str(temp) + ' °C, Humidity: ' + str(humidity) + "'%'" + ' forecast: ' + text

    return output


if __name__ == '__main__':
    print('running....')
    while(not sleep(5)):
        try:
            main()
        except:
            continue
