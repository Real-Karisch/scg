from airium import Airium
import json
import re
from titlecase import titlecase

def generateScgIndexHtml(booksJson):
    scgIndexHtmlBuilder = Airium()
    with scgIndexHtmlBuilder.head():
        scgIndexHtmlBuilder.title(_t=f"Summa Contra Gentiles - Contents")
        scgIndexHtmlBuilder.link(href="./styles.css", rel="stylesheet")
        scgIndexHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with scgIndexHtmlBuilder.div(id='mainwrap'):
        with scgIndexHtmlBuilder.div(style="text-align: center"):
            scgIndexHtmlBuilder.h1(_t=f"Summa Contra Gentiles - Contents")
            scgIndexHtmlBuilder.br()
            scgIndexHtmlBuilder.a(href='./../index.html', _t=f"Return to Documents Home Page", style="text-decoration: underline")
            scgIndexHtmlBuilder.br()
            scgIndexHtmlBuilder.br()

            for book in booksJson:
                scgIndexHtmlBuilder.a(_t=f"Book {book['numStr']} - {book['title']}", href=f"./scgBook{book['numStr']}.html", style="text-decoration: underline")
                scgIndexHtmlBuilder.br()
            scgIndexHtmlBuilder.br()
    return scgIndexHtmlBuilder

def generateScgBookHtml(bookJson):
    scgBookHtmlBuilder = Airium()
    with scgBookHtmlBuilder.head():
        scgBookHtmlBuilder.title(_t=f"Summa Contra Gentiles, Book {bookJson['numStr']}")
        scgBookHtmlBuilder.link(href="./styles.css", rel="stylesheet")
        scgBookHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with scgBookHtmlBuilder.div(id='mainwrap'):
        with scgBookHtmlBuilder.div(style="text-align: center"):
            scgBookHtmlBuilder.h1(_t=f"Summa Contra Gentiles, Book {bookJson['numStr']} - {bookJson['title']}")
            scgBookHtmlBuilder.br()
           
            scgBookHtmlBuilder.a(href='./../index.html', _t=f"Return to Documents Home Page", style="text-decoration: underline")
            scgBookHtmlBuilder(" | ")
            scgBookHtmlBuilder.a(href='./scg.html', _t=f"Return to Summa Contra Gentiles Contents", style="text-decoration: underline")
            scgBookHtmlBuilder.br()

    with scgBookHtmlBuilder.div(id='tightwrap'):
        for question in bookJson['questions']:
            with scgBookHtmlBuilder.details():
                scgBookHtmlBuilder.summary(_t=f"{question['chapter']} - {titlecase(question['title'])}", style="font-weight:bold")
                with scgBookHtmlBuilder.div(id='expansionwrap'):
                    with scgBookHtmlBuilder.span():
                        scgBookHtmlBuilder(
                            re.sub(r'\n', '<br><br>', question['content'])
                        )
                scgBookHtmlBuilder.br()
                scgBookHtmlBuilder.br()
            scgBookHtmlBuilder.hr()

    return scgBookHtmlBuilder


def saveAllScgBooksHtml(jsonAddress='C:/Users/jackk/Projects/scg/outputs/books.json', saveFolder='C:/Users/jackk/Projects/website/scg/'):
    with open('C:/Users/jackk/Projects/scg/outputs/books.json', 'r') as file:
        booksJson = json.loads(file.read())

    scgIndexHtml = generateScgIndexHtml(booksJson)
    with open(f"{saveFolder}/scg.html", 'wb') as file:
        file.write(bytes(scgIndexHtml))

    for bookJson in booksJson:
        scgBookHtml = generateScgBookHtml(bookJson)
        with open(f"{saveFolder}/scgBook{bookJson['numStr']}.html", 'wb') as file:
            file.write(bytes(scgBookHtml))


if __name__ == '__main__':
    saveAllScgBooksHtml()