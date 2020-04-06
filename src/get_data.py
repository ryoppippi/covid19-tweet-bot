import urllib.request
import io
import pandas as pd


def download(url, **args):
    res = urllib.request.urlopen(url).read().decode("utf-8")
    df = pd.read_csv(io.StringIO(res), **args)
    return df


def patiant_data(url):
    df = download(url, parse_dates=True)

    # change datetime
    df["公表日"] = df["公表日"] = pd.to_datetime(
        df["公表年"].astype(str)
        + "-"
        + df["公表月"].astype(str)
        + "-"
        + df["公表日"].astype(str),
        errors="coerce",
    )

    # remove unjudged patient
    # df = df.dropna()

    return df


def extract_info_from_data(df):
    res = {}
    res["num_ppl"] = len(df)
    res["num_male"] = (df == "男")["性別"].sum()
    res["num_female"] = (df == "女")["性別"].sum()
    res["diff"] = (df.iloc[-1]["確定日"] == df["確定日"]).sum()
    res["last_date"] = df.iloc[-1]["確定日"].strftime("%m/%d")
    return res


if __name__ == "__main__":
    URL = "https://toyokeizai.net/sp/visual/tko/covid19/csv/data.csv"
    FILE_NAME = "data.csv"
    data = patiant_data(URL)
    res = extract_info_from_data(data)

    pd.set_option("display.max_rows", data.shape[0] + 1)
    print(data)
    print(res)
