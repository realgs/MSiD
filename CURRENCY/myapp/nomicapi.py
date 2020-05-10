import urllib.request
url = "https://api.nomics.com/v1/markets?key=d89640265d015f1144316d4702afded7"
print(urllib.request.urlopen(url).read())