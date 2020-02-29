import get_data
import urllib.request
import os

URL = "https://toyokeizai.net/sp/visual/tko/covid19/csv/data.csv"
FILE_NAME = "data.csv"


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


def gen_msg(url=URL, filename=FILE_NAME):
    data = get_data.patiant_data(url, filename)
    res = get_data.extract_info_from_data(data)
    msg = ""

    # create message
    msg += "新型コロナウイルス国内感染の状況\n"
    msg += "{0} 現在\n".format(res["last_date"])
    msg += "総計: {0}名\n".format(res["num_ppl"])
    msg += "男性: {0}名\n".format(res["num_male"])
    msg += "女性: {0}名\n".format(res["num_female"])
    msg += "前日から {0}名増加しました\n".format(res["diff"])
    msg += "詳しくはこちら↓\n" + "https://t.co/uxsL1MQICb?amp=1\n"
    msg += "#新型コロナ"
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


def main():
    msg = gen_msg(url=URL, filename=FILE_NAME)
    print(msg)
    msg = compare_cache(msg)
    if msg is not None:
        send_tweet(msg)
        print(len(msg))


if __name__ == "__main__":
    main()
