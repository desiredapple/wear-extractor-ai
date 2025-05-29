from urllib.request import urlopen

url = "https://github.com/SimbiozizV/kino"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

print(html)