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
    df["date"] = df["date"] = pd.to_datetime(
        df["year"].astype(str)
        + "-"
        + df["month"].astype(str)
        + "-"
        + df["date"].astype(str),
        errors="coerce",
    )
    return df


if __name__ == "__main__":
    URL = (
        "https://raw.githubusercontent.com/kaz-ogiwara/covid19/master/data/summary.csv"
    )
    data = patiant_data(URL)

    pd.set_option("display.max_rows", data.shape[0] + 1)
    print(data)
