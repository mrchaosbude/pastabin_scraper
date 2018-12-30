import sqlite3
import requests
import json
import re
import datetime
import time

def creat_db():
    """
    create the db if not exitst
    """
    create_pastebin_db ="""
    CREATE TABLE pastabin_meta (
    Id INTEGER PRIMARY KEY,
    scrape_url TEXT,
    full_url TEXT,
    date INTEGER,
    key TEXT,
    size INTEGER,
    expire INTEGER,
    title TEXT,
    syntax TEXT,
    user TEXT,
    content TEXT);
    """
    connection = sqlite3.connect('pastabin.db')
    cursor = connection.cursor()
    try:
        cursor.execute(create_pastebin_db)
        print('[+] Createt')
    except:
        print('[-] Alrady exists')
    connection.commit()
    connection.close()


def timePassed(oldtime):
    """Checks if time is past
    
    Arguments:
        oldtime {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    currenttime = time.time()
    if currenttime - oldtime > 35:
        print('[+] 35 sec gone')
        return True
    else:
        print('[-] wait', currenttime - oldtime)
        time.sleep(1)        
        return False
    
def get_contend():
    oldtime = time.time()
    r = requests.get('https://scrape.pastebin.com/api_scraping.php')
    try:
        r =json.loads(r.text)
    except:
        print(r.text)
    
    for entry in r:
        
        url_content = requests.get(entry['scrape_url']).text.encode("utf-8", "strict").decode("utf-8") # get the content
        format_str = """
            INSERT INTO pastabin_meta (Id, scrape_url, full_url, date, key, size, expire, title, syntax, user, content)
            VALUES (NULL, "{scrape_url}", "{full_url}", "{date}", "{key}", "{size}", "{expire}", "{title}", "{syntax}", "{user}", ?);"""



        sql_command = format_str.format(scrape_url=entry['scrape_url'],
                full_url= entry['full_url'],
                date= entry['date'],
                key= entry['key'],
                size= entry['size'],
                expire= entry['expire'],
                title= entry['title'],
                syntax= entry['syntax'],
                user= entry['user'],
                )

        connection = sqlite3.connect('pastabin.db')
        cursor = connection.cursor()
        cursor.execute("SELECT Id FROM pastabin_meta WHERE key = ?", (entry['key'],)) # check i for dubles
        data = cursor.fetchone()
        if data is None:
            try:
                cursor.execute(sql_command, (url_content,))
                print (f"[+] add {entry['full_url']} at {datetime.datetime.now()}")
            except:
                print("[-] cant  add", entry['full_url'])
                break
        else:
            print('[-] Kay = {} alrady exists at id = {}'.format(entry['key'], data[0]))
        connection.commit()
    connection.close()
    return oldtime


if __name__ == "__main__":
    creat_db()
    ran = False
    oldtime = time.time()
    while True:
        if timePassed(oldtime) or ran == False:
            oldtime = get_contend()
            ran = True