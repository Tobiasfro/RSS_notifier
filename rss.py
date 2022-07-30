import sqlite3
import smtplib
from email.mime.text import MIMEText

import feedparser

db_connection = sqlite3.connect('rss.sqlite')
db = db_connection.cursor()
db.execute('CREATE TABLE IF NOT EXISTS magazine (title TEXT, date TEXT)')

def article_is_not_db(article_title, article_date):
    db.execute('SELECT * from magazine WHERE title=? AND date=?', (article_title, article_date))
    if not db.fetchall():
        return True
    else:
        return False

def add_article_to_db(article_title, article_date):
    db.execute('INSERT INTO magazine VALUES (?,?)', (article_title, article_date))
    db_connection.commit()

def read_article_feed():
    feed = feedparser.parse('https://fedoramagazine.org/feed/')
    for article in feed['entries']:
        title = article['title']
        date_published = article['published']
        if article_is_not_db(title, date_published):
            print('Title: ' + title)
            print('Published ' + date_published)
            print('Link: ' + article['link'] + '\n')
            add_article_to_db(title, date_published)
    db.execute('SELECT * from magazine')
    print('All entries: ', db.fetchall())
    db.execute('SELECT COUNT(1) from magazine')
    print('Number of entries in database: ', db.fetchall())

if __name__ == '__main__':
    read_article_feed()
    db_connection.close()