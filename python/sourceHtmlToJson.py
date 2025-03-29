import re
from bs4 import BeautifulSoup

def getFirstText(soupText):
    return re.split(r'\n *\n', soupText)[0]

def getBookIndex(books, bookStr):
    bookInd = 0
    for book in books:
        if book['numStr'] == bookStr:
            return bookInd
        bookInd += 1

def getQuestionIndex(questions, questionNum):
    questionIndex = 0
    for question in questions:
        if question['questionNum'] == questionNum:
            return questionIndex
        questionIndex += 1

def generateQuestionJsonFromSourceHtmlBooks1and2(sourceHtmlSoup):
    questions = []
    questionNum = 1
    for questionSoup in sourceHtmlSoup.body.find_all('table')[1:]:
        allTds = questionSoup.find_all('td')
        content = ''
        for tdAddress in range(5, len(allTds), 2):
            content = content + getFirstText(allTds[tdAddress].text) + '\n'
        try:
            questions.append(
                {
                    'questionNum': questionNum,
                    'chapter': getFirstText(questionSoup.td.td.text),#.find_all('b')[1].text,
                    'title': re.sub(r'\n *', ' ', getFirstText(allTds[3].text)),
                    'content': content.strip(' \n')
                }
            )
        except IndexError:
            print(f'IndexError on {questionNum}')
        questionNum += 1
    return questions

def generateQuestionJsonFromSourceHtmlBooks3and4(sourceHtmlSoup):
    questions = []
    questionNum = 1
    for questionSoup in sourceHtmlSoup.body.find_all('table')[1:]:
        allTds = questionSoup.find_all('td')
        content = ''
        for tdAddress in range(3, len(allTds), 2):
            content = content + getFirstText(allTds[tdAddress].text) + '\n'
        try:
            questions.append(
                {
                    'questionNum': questionNum,
                    'chapter': re.split(r'\n +', getFirstText(questionSoup.td.td.text))[0],
                    'title': re.split(r'\n +', getFirstText(questionSoup.td.td.text))[1],
                    'content': content.strip(' \n')
                }
            )
        except IndexError:
            print(f'IndexError on {questionNum}')
        questionNum += 1
    return questions

def generateBooksJson(booksHtmlFolder='C:/Users/jackk/Projects/scg/data/'):
    books = []
    bookTitles = {
        '1': 'God',
        '2': 'Creation',
        '3.1': 'Providence',
        '3.2': 'Providence (Cont)',
        '4': 'Salvation'
    }
    for numStr in ['1','2','3.1','3.2','4']:
        print(f"Book {numStr}")
        with open(f"{booksHtmlFolder}/scgBook{numStr}.html", 'r', encoding='utf8') as file:
            bookHtmlSoup = BeautifulSoup(
                file,
                'html.parser'
            )
        if numStr == '1' or numStr == '2':
            questions = generateQuestionJsonFromSourceHtmlBooks1and2(sourceHtmlSoup=bookHtmlSoup)
        else:
            questions = generateQuestionJsonFromSourceHtmlBooks3and4(sourceHtmlSoup=bookHtmlSoup)
        books.append(
            {
                'numStr': numStr,
                'title': bookTitles[numStr],
                'questions': questions
            }
        )
    return books

def overwriteQuestions(books, hardCodeQuestions):
    for hardCodeQuestion in hardCodeQuestions:
        bookIndex = getBookIndex(books, hardCodeQuestion['bookStr'])
        questions = books[bookIndex]['questions']
        if hardCodeQuestion['insertAfter'] == -1:
            questionIndex = getQuestionIndex(questions, hardCodeQuestion['questionNum'])
            questions[questionIndex] = hardCodeQuestion['newQuestion']
        else:
            questionIndex = getQuestionIndex(questions, hardCodeQuestion['insertAfter'])
            questions.insert(questionIndex+1, hardCodeQuestion['newQuestion'])

    return books

if __name__ == '__main__':
    import json
    from vars import hardCodeQuestions

    books = generateBooksJson('C:/Users/jackk/Projects/scg/data/')
    books = overwriteQuestions(books, hardCodeQuestions)

    with open('C:/Users/jackk/Projects/scg/outputs/books.json', 'w') as file:
        file.write(json.dumps(books))