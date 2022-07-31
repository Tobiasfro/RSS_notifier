'''rss.py: RSS notifier created with the help of the tutorial found here
           https://fedoramagazine.org/never-miss-magazines-article-build-rss-notification-system/

           All credit goes to the author of that article'''

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
    print('New entries:')
    for article in feed['entries']:
        title = article['title']
        date_published = article['published']
        link = article['link']
        if article_is_not_db(title, date_published):
            print('Title: ' + title)
            print('Published ' + date_published)
            print('Link: ' + link + '\n')
            #send_notification(title, link)
            add_article_to_db(title, date_published)
    db.execute('SELECT * from magazine')
    print('Existing entries:')
    for entry in db.fetchall():
        print(str(entry) + '\n')
    db.execute('SELECT COUNT(1) from magazine')
    print('Number of entries in database:', db.fetchall()[0][0])

def send_notification(article_title, article_url):
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login('my@gmail.com', 'my_password')
    msg = MIMEText(f'\nHi there is a new Fedora Magazine article : {article_title}.\nYou can read it here {article_url}')
    msg['Subject'] = 'New Article Available'
    msg['From'] = 'my@gmail.com'
    msg['To'] = 'my_main@mail.com'
    smtp_server.send_message(msg)
    smtp_server.quit() 

if __name__ == '__main__':
    read_article_feed()
    db_connection.close()