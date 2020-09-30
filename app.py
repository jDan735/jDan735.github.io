from flask import Flask
from wikipedia import Wikipedia
import os
app = Flask(__name__, static_url_path="/")


def page(file_name):
    with open(file_name, encoding="utf-8") as file:
        return file.read()


pages = {
    "index": page("index.html"),
    "kanobu": page("kanobu.html"),
    "timer": page("timer.html"),
    "404": page("404.html"),
    "lorem": page("lorem.html"),
    "ftp": page("ftp.html")
}


@app.route("/")
def index():
    return pages["index"]


@app.route("/kanobu/server")
def kanobu_server():
    return {
        "game": "kanobu",
        "users": ["ban", "obama", "3nr3"],
        "time": 1,
        "ban": True
    }


@app.route("/kanobu/server/<user>")
def kanobu_server_user(user):
    return {
        "user": user
    }


@app.route('/obama')
def sosat():
    return "sosat"


@app.route('/kanobu')
def kanobu():
    return pages["kanobu"]


@app.route('/timer')
def timer():
    return pages["timer"]


def makeBelarus(text):
    namelist = [
        ["Белоруссия", "Беларусь"],
        ["Белоруссии", "Беларуси"],
        ["Беларуссию", "Беларусь"],
        ["Белоруссией", "Беларусью"],
        ["Белоруссиею", "Беларусью"],


        ["Белору́ссия", "Белару́сь"],
        ["Белору́ссии", "Белару́си"],
        ["Белору́ссию", "Белару́сь"],
        ["Белору́ссией", "Белару́сью"],
        ["Белору́ссиею", "Белару́сью"]
    ]

    for name in namelist:
        text = text.replace(*name)

    return text


@app.route('/wiki/<page_name>')
def wiki(page_name):
    wiki = Wikipedia("ru")
    search = wiki.search(page_name)

    if search == -1:
        with open("404.html", encoding="utf-8") as index:
            return index.read()

    head = '<link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16" /><link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32" /><link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" /><link rel="stylesheet" href="/css/style.css?v=1.5.7" /><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />'

    h1 = f'<h1 class=wiki>{makeBelarus(search[0][0])}</h1>'
    page = makeBelarus(str(wiki.getPage(search[0][0], -1)))
    title = f'<title>{makeBelarus(search[0][0])}</title>'
    style = '<link rel="stylesheet" href="/css/style.css?v=1.4.0"/><link rel="stylesheet" href="/css/wiki.css?v=1.9.2"/>'

    image_url = wiki.getImageByPageName(search[0][0], 400)

    page_open = "<div class=page>"

    if image_url == "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Flag_of_Belarus.svg/400px-Flag_of_Belarus.svg.png":
        image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg/400px-Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg.png"

    if image_url == -1:
        img = ""

    else:
        full_image_url = wiki.getImageByPageName(search[0][0])

        if full_image_url == "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Flag_of_Belarus.svg/1000px-Flag_of_Belarus.svg.png":
            full_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg/1000px-Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg.png"

        img = f'<a href="{full_image_url}"><img src="{image_url}"></a>'

    result = head + style + title + img + page_open + h1 + page + "</div>"

    return result


@app.route('/ftp/<path:path>')
@app.route('/ftp/')
@app.route('/ftp')
def ftp(path=""):
    file_path = os.path.abspath(os.path.dirname(__file__))
    s = "/" if os.name == "posix" or os.name == "macos" else "\\"
    a = ""
    this = None

    fp = f"{s}static{s}ftp{s}{path}"

    for i in os.walk(file_path + fp):
        this = i[1:]

        break

    else:
        return pages["404"]

    went = fp.replace(s + 'static', '')
    went = s.join(went.split(s)[:-1])

    if path != "":
        a += f"<li><h3><a href='{went}'>📁 ..<a></h3></li>"

    icons = [
        [["jpeg", "jpg", "png", "webp", "svg"], "🖼"],
        [["license"], "📖"],
        [["procfile"], "🤖"],
        [["css"], "💅"],
        [["py"], "🐍"],
        [["js"], "☕️"]
    ]

    for b in this[0]:
        a += f"<li><h3><a href='{fp.replace(s + 'static', '')}{b}'>📁 /{b}<a></h3></li>"

    for b in this[1]:
        file_icon = "📄"

        for icon in icons:
            file_type = b.split(".")[-1].lower()
            for type_ in icon[0]:
                if file_type == type_:
                    file_icon = icon[1]

        a += f"<li><h3><a href='{fp}{s}{b}'>{file_icon} {b}<a></h3></li>"

    if path == "":
        h1 = "/ftp"

    else:
        h1 = fp.replace(f"{s}static", "").replace(s, "/")

    return f'<!DOCTYPE html><html><head><link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16"><link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32"><link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96"><link rel="stylesheet" href="/css/style.css?v=2.4.8"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>FTP</title></head><body><h1>{h1}</h1><ul class=projects>' + a + "</ul></body></html>"


@app.errorhandler(404)
def not_found(error):
    return pages["404"]


@app.errorhandler(505)
def not_found_shizha(error):
    return "Не сюда)"


@app.route('/lorem')
def lorem():
    return pages["lorem"]


if __name__ == '__main__':
    app.run(port=5050)
