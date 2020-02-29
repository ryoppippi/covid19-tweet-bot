import config
import get_data
from twitter import Twitter, OAuth

URL = "https://toyokeizai.net/sp/visual/tko/covid19/csv/data.csv"
FILE_NAME = "data.csv"


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


def main():
    t = Twitter(
        auth=OAuth(
            config.TW_TOKEN,
            config.TW_TOKEN_SECRET,
            config.TW_CONSUMER_KEY,
            config.TW_CONSUMER_SECRET,
        )
    )
    msg = gen_msg(URL, FILE_NAME)
    t.statuses.update(status=msg)


if __name__ == "__main__":
    res = gen_msg()
    print(res)
    print(len(res))
    # main()
