import urllib.request
import io
import json


def download(url):
    res = urllib.request.urlopen(url)
    data = json.loads(res.read().decode('utf8'))
    return data

if __name__ == "__main__":
    URL = "https://data.corona.go.jp/converted-json/covid19japan-npatients.json"
    data = download(URL)

    print(data[-1])
