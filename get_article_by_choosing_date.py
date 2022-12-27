import sqlite3
from datetime import datetime,timedelta
import os

dir_path="D://get_tweets"
db_path=dir_path+"//twitter.db"
conn=sqlite3.connect(db_path)
cursor=conn.cursor()

search_name="ultramarine471"

date_ask=input("which date(enter for default)\n(month-date like 0629):")
if date_ask == "":
    # tweets_dates=[each for each in cursor.execute("select t,d from tw where u='{}'".format(search_name)).fetchall()]
    last_date=[each[0] for each in cursor.execute("select d from tw where u='{}'".format(search_name)).fetchall() if ":" in each[0]][-1]
    last_date=last_date.split(" ")[0]
else:
    assert len(date_ask) == 4
    date_ask_str="{}-{}".format(date_ask[0:2],date_ask[2:4])
    last_date=[each[0] for each in cursor.execute("select d from tw where u='{}' and d like '%{}%'".format(search_name,date_ask_str)).fetchall() if ":" in each[0]][-1]
    last_date=last_date.split(" ")[0]  
print("当前日期：",last_date)

# os._exit(0)

query_str="select t,d,l from tw where u='ultramarine471' and d like '%{}%'"
# sql_date_patt="%{}%"

article_head_patt="---\ntitle: {}\ndate: {}\ntags:\n---\n"
archive_head_patt="原帖：\n{}\n"

date_fmt="%Y-%m-%d"

def get_article_str(tweets,date,title,archive_links):
    article_head=article_head_patt.format(title,date)
    archive_links=["{}".format(each) for each in archive_links if not "`" in each]
    archive_links_s="\n".join(archive_links)
    archive_head=archive_head_patt.format(archive_links_s)
    tweets_s="\n\n".join(tweets)
    article_str=article_head+"\n"+archive_head+"\n"+tweets_s+"\n"
    return article_str

def date_forward(date_str,time_spent):
    next_date=datetime.strptime(date_str, date_fmt)+timedelta(days=time_spent)
    return next_date.strftime(date_fmt)

def date_backward(date_str,time_spent):
    prev_date=datetime.strptime(date_str, date_fmt)-timedelta(days=time_spent)
    return prev_date.strftime(date_fmt)

# def show_tweets()

def make_article():
    global last_date
    while True:
        ask=input("go on press enter or n (go 2 for 2n), go back press b(back 2 for 2b), for sure press y:\t")
        print("（注意：选择到文章开头的那天）")
        if ask == "n":
            cur_date=date_forward(last_date, 1)
        elif ask == "b":
            cur_date=date_backward(last_date, 1)
        elif "n" in ask:
            time_spent=int(ask[:-1])
            cur_date=date_forward(last_date,time_spent)
        elif "b" in ask:
            time_spent=int(ask[:-1])
            cur_date=date_backward(last_date,time_spent)
        elif ask == "":
            cur_date=date_forward(last_date,1)
        print("当前日期：",cur_date)
        print(query_str.format(cur_date))
        # print(sql_date_patt.format(cur_date))
        # print(query_str,(sql_date_patt.format(cur_date),))
        # print(query_str,"%"+cur_date+"%")
        cur_packs=cursor.execute(query_str.format(cur_date)).fetchall()

        os.system("cls")

        if cur_packs == []:
            print("此日无任何推文")
        
        for num,pack in enumerate(cur_packs,1):
            print("\n=== 第{}条 ===\n".format(num))
            tweet,date,link=pack
            print(tweet,date,sep="\n")
            print("\n*** *** *** ***\n")
        if ask == "y":
            cur_date2=date_forward(cur_date, 1)
            cur_packs2=cursor.execute(query_str.format(cur_date2)).fetchall()
            twoday_pack=cur_packs+cur_packs2
            print("\n"*8)
            break
        last_date=cur_date

    article_pack=[]
    archive_links=[]

    cnt=0
    while cnt<=len(twoday_pack)-1:
        print("\n=== 第{}条 ===\n".format(cnt+1))
        pack=twoday_pack[cnt]
        tweet,date,link=pack
        print(tweet,date,sep="\n")
        print("\n*** *** *** ***\n")
        ask=input("go on press enter, go back press b, for sure press y:\t")
        os.system("cls")
        if "y"  == ask:
            article_pack.append(pack)
            if "https://twitter.com/ultramarine471/status/" in tweet:
                archive_links.append(link)
        if "b" == ask:
            cnt-=1
            continue
        if "f" == ask:
            break
        cnt+=1

    # for num,pack in enumerate(twoday_pack,1):
    #     print("\n=== 第{}条 ===\n".format(num))
    #     tweet,date,link=pack
    #     print(tweet,date,sep="\n")
    #     print("\n*** *** *** ***\n")
    #     ask=input("for sure press y, go back press b:\t")
    #     if "y"  == ask:
    #         article_pack.append(pack)
    #         if "https://twitter.com/ultramarine471/status/" in tweet:
    #             archive_links.append(link)
    #     if "b" == ask:


    dir_path_patt="D:\Blogs\{}\source\_posts"
    
    while True:
        project=input("tm or cl:\t")
        if project == "tm":
            article_dir=dir_path_patt.format("Linkeer365TinyMoment2")
            break
        elif project == "cl":
            article_dir=dir_path_patt.format("Linkeer365ColorfulLife3")
            break

    tweets=[each[0] for each in article_pack]
    atc_date=article_pack[0][1]+":00"

    while True:
        title=input("文章标题：")
        if title == "":
            continue
        article_path=article_dir+os.sep+title+".md"
        if os.path.exists(article_path):
            print("标题起重名了，重新起一个！")
            continue
        break

    archive_link=article_pack[0][2]
    if archive_links == []:
        archive_links=[archive_link]
    else:
        archive_links.insert(0, archive_link)


    article_str=get_article_str(tweets, atc_date, title, archive_links)

    with open(article_dir+os.sep+title+".md","w",encoding="utf-8") as f:
        f.write(article_str)

    print("one done.")

if __name__ == "__main__":
    flag=1
    while flag:
        make_article()
        wantmore=input("want more?[n for not]")
        if wantmore == "n":
            break
    print("all done.")
