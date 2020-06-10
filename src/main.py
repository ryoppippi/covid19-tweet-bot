import get_data
import urllib.request
import os
import argparse


URL = "https://raw.githubusercontent.com/kaz-ogiwara/covid19/master/data/summary.csv"
D_URL = "https://oku.edu.mie-u.ac.jp/~okumura/python/data/COVID-19.csv"


def compare_cache(msg, filename="TWEET.txt", cache_dir="."):
    file_path = os.path.join(cache_dir, filename)
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    try:
        with open(file_path) as f:
            old_msg = f.read()
    except FileNotFoundError:
        with open(file_path, "w") as f:
            f.write(msg)
        return msg
    if msg == old_msg:
        return None
    else:
        with open(os.path.join(cache_dir, filename), "w") as f:
            f.write(msg)
        return msg


def domestic_gen_msg(url=URL):
    df = get_data.patiant_data(url)
    msg = ""
    # create message
    msg += "新型コロナウイルス国内感染の状況\n"
    msg += "{0} 現在\n".format(df.iloc[-1]["date"])
    msg += "感染者: {0}名\n".format(df.iloc[-1]["pcr_tested_positive"])
    msg += "死者: {0}名\n".format(df.iloc[-1]["death"])
    msg += "感染者は前日から {0}名増加しました\n".format(
        abs(df.iloc[-1]["pcr_tested_positive"] - df.iloc[-2]["pcr_tested_positive"])
    )
    msg += "死者は前日から {0}名増加しました\n".format(
        abs(df.iloc[-1]["death"] - df.iloc[-2]["death"])
    )
    msg += "詳しくはこちら↓\n" + "https://t.co/uxsL1MQICb?amp=1\n"
    msg += "#新型コロナ #Covid_19"
    return msg


def global_gen_msg(url=URL):
    df = get_data.download(url)

    msg = ""
    # create message
    msg += "新型コロナウイルス世界的感染の状況\n"
    msg += "{0} 現在\n".format(df.iloc[-1]["Date"])
    msg += "感染者: {0}名\n".format(df.iloc[-1]["Global Confirmed"])
    msg += "死者: {0}名\n".format(df.iloc[-1]["Global Deaths"])
    msg += "感染者は前日から {0}名増加しました\n".format(
        abs(df.iloc[-1]["Global Confirmed"] - df.iloc[-2]["Global Confirmed"])
    )
    msg += "死者は前日から {0}名増加しました\n".format(
        abs(df.iloc[-1]["Global Deaths"] - df.iloc[-2]["Global Deaths"])
    )
    msg += "詳しくはこちら↓\n" + "ift.tt/38ukisZ\n"
    msg += "#新型コロナ #Covid_19"
    return msg


def send_tweet(msg):
    # params for IFTTT
    print(os.environ.get("webhook_access_key"))
    ifttt_api_key = "/with/key/" + os.environ.get("webhook_access_key")
    url_base = "https://maker.ifttt.com/trigger/"
    # EVENT name for IFTTT
    ifttt_event = "create_tweet"

    url = url_base + ifttt_event + ifttt_api_key
    messgae = {"value1": msg}
    req = urllib.request.Request("{}?{}".format(url, urllib.parse.urlencode(messgae)))
    with urllib.request.urlopen(req) as res:
        body = res.read().decode("utf-8")
        print(body)


def main(t="d"):
    if t == "d":
        msg = domestic_gen_msg(url=URL)
        print(msg)
        msg = compare_cache(msg, filename="./tweet/DTWEET.txt")
        if msg is not None:
            send_tweet(msg)
            print(len(msg))
    elif t == "g":
        msg = global_gen_msg(url=D_URL)
        print(msg)
        msg = compare_cache(msg, filename="./tweet/GTWEET.txt")
        if msg is not None:
            send_tweet(msg)
            print(len(msg))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", "-t", default="d")
    _type = parser.parse_args().type
    main(_type)
