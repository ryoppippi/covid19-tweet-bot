import get_data
import urllib.request
import urllib.parse
import os


P_URL = "https://data.corona.go.jp/converted-json/covid19japan-npatients.json"
D_URL = "https://data.corona.go.jp/converted-json/covid19japan-ndeaths.json"

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


def domestic_gen_msg():
    df_p = get_data.download(P_URL)
    df_d = get_data.download(D_URL)
    msg = ""
    # create message
    msg += "新型コロナウイルス国内感染の状況\n"
    msg += "{0} 現在\n".format(df_p[-1].get("date"))
    msg += "感染者: {0}名\n".format(df_p[-1].get("npatients"))
    msg += "死者: {0}名\n".format(df_d[-1].get("ndeaths"))
    msg += "感染者は前日から {0}名増加しました\n".format(df_p[-1].get("adpatients"))
    msg += "死者は前日から {0}名増加しました\n".format(int(df_d[-1].get("ndeaths"))-int(df_d[-2].get("ndeaths")))
    msg += "詳しくはこちら↓\n" + "corona.go.jp/dashboard\n"
    msg += "#新型コロナ #Covid_19"
    return msg



def send_tweet(msg):
    # params for IFTTT
    webhook_access_key = os.environ.get("webhook_access_key") 
    ifttt_event = "create_tweet"

    url = f"https://maker.ifttt.com/trigger/{ifttt_event}/with/key/{webhook_access_key}"
    messgae = {"value1": msg}
    req = urllib.request.Request("{}?{}".format(url, urllib.parse.urlencode(messgae)))
    with urllib.request.urlopen(req) as res:
        body = res.read().decode("utf-8")
        print(body)


def main():
    msg = domestic_gen_msg()
    print(msg)
    msg = compare_cache(msg, filename="./tweet/DTWEET.txt")
    print(msg)
    if msg is not None:
        send_tweet(msg)
        print(len(msg))


if __name__ == "__main__":
    main()
