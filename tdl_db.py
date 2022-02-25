import sqlite3

filedir="D://get_tweets//"
filenames=["mutilated_catal_tweet_date_links_modified","ultramarine471_tweet_date_links_modified"]

for filename in filenames:
    filepath=filedir+filename+".txt"
    username=filename.replace("_tweet_date_links_modified","")
    db_path=filedir+"tweet"+".db"
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
    if len(cursor.execute("select name from sqlite_master where type='table' and name='user'").fetchall())!=1:
        cursor.execute("create table user (id varchar(20), username varchar(20), content varchar(20), date varchar(20), link varchar(20))")
    cursor.executemany("insert into user (username,content,date,link) values (?,?,?,?)",tdl_tups)
    # cursor.execute("insert into user(username) values ({})".format(username))
    print(cursor.rowcount)
    cursor.close()
    conn.commit()
    conn.close()
    print("one done.")
