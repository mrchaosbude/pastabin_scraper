import sqlite3 # for the db
import requests # to get the data 
import json # the api is json
import re # regular expresion
import datetime
import time
#from tkinter import Tk # to put the ip in the clipbord
import subprocess
import webbrowser # to open the browser
import os 

def creat_db():
    """
    create the db if not exitst
    """
    create_pastebin_db ="""
    CREATE TABLE pastabin_meta (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    scrape_url TEXT,
    full_url TEXT,
    date INTEGER,
    key TEXT,
    size INTEGER,
    expire INTEGER,
    title TEXT,
    syntax TEXT,
    user TEXT,
    content TEXT,
    unseen INTEGER DEFAULT '1');
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

def put_clipbord(txt):
    """puts the text in windows to the clipbord
    
    Arguments:
        txt {str} -- is the content youd licke to put to the clipbord
    """

    subprocess.run(['clip.exe'], input=txt.strip().encode('utf-16'), check=True)

def find_ip(text):
    """finds an ip in a given text
    
    Arguments:
        text {str} -- the text to serch for an ip adress
    
    Returns:
        {str} -- return ip
    """

    regex = r'(::|(([a-fA-F0-9]{1,4}):){7}(([a-fA-F0-9]{1,4}))|(:(:([a-fA-F0-9]{1,4})){1,6})|((([a-fA-F0-9]{1,4}):){1,6}:)|((([a-fA-F0-9]{1,4}):)(:([a-fA-F0-9]{1,4})){1,6})|((([a-fA-F0-9]{1,4}):){2}(:([a-fA-F0-9]{1,4})){1,5})|((([a-fA-F0-9]{1,4}):){3}(:([a-fA-F0-9]{1,4})){1,4})|((([a-fA-F0-9]{1,4}):){4}(:([a-fA-F0-9]{1,4})){1,3})|((([a-fA-F0-9]{1,4}):){5}(:([a-fA-F0-9]{1,4})){1,2}))'
    r = re.findall(regex, text)
    return r[0][0]

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
        print('[-] wait', int(currenttime - oldtime))
        time.sleep(1)        
        return False
    
def get_contend():
    oldtime = time.time()
    r = requests.get('https://scrape.pastebin.com/api_scraping.php')
    try:
        r =json.loads(r.text)
    except:
        ip = find_ip(r.text)
        put_clipbord(ip)
        webbrowser.open_new_tab('https://pastebin.com/doc_scraping_api')
        print(r.text)
        quit()
    
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
    oldtime = time.time() + 35
    while True:
        if timePassed(oldtime) or ran == False:
            oldtime = get_contend()
            ran = True
