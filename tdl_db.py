import sqlite3

filedir="D://get_tweets//"
filenames=["mutilated_catal_tweet_date_links_modified","ultramarine471_tweet_date_links_modified"]

for filename in filenames:
    filepath=filedir+filename+".txt"
    username=filename.replace("_tweet_date_links_modified","")
    db_path=filedir+"twitter"+".db"
    tdl_tups=[]
    with open(filepath,"r",encoding="utf-8") as f:
        lines=[each.strip("\n") for each in f.readlines()]
        for line in lines:
            tdls=line.split("\t")
            tdls=[username]+tdls
            if len(tdls)!=4:
                print(len(tdls))
                print(tdls)
                print("fuck")
            else:
                tdl_tup=tuple(tdls)
                tdl_tups.append(tdl_tup)
                print(tdl_tup)
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    if len(cursor.execute("select name from sqlite_master where type='table' and name='tw'").fetchall())!=1:
        cursor.execute("create table tw (u varchar(20), t varchar(20), d varchar(20), l varchar(20))")
    cursor.executemany("insert into tw (u,t,d,l) values (?,?,?,?)",tdl_tups)
    # cursor.execute("insert into user(username) values ({})".format(username))
    print(cursor.rowcount)
    cursor.close()
    conn.commit()
    conn.close()
    print("one done.")
