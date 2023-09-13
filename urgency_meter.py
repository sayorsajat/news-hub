import re
import logging


def measureUrgency(article, keywords):
    mostUrgentKeyword = getMostImportantKeyword(article.lower(), keywords)
    urgency = 0

    for keyword, weight in mostUrgentKeyword.items():
        if article.lower().find(keyword.lower()) != -1:
            urgency += weight

    urgency += measureError(article.lower())
    urgency += calculateUrgencyOfTheRestKeywords(article.lower(), keywords, mostUrgentKeyword)


    return urgency


def getMostImportantKeyword(article, keywords):
    mostUrgentKeyword = keywords[0]

    for keyword_obj in keywords:
        for keyword, weight in keyword_obj.items():
            if article.find(keyword.lower()) == -1:
                continue
            if weight > list(mostUrgentKeyword.values())[0]:
                mostUrgentKeyword = keyword_obj
            # if urgency of newly proposed keyword is greater than previously picked one
            if weight > list(mostUrgentKeyword.values())[0]:
                mostUrgentKeyword = keyword_obj

    return mostUrgentKeyword


def calculateUrgencyOfTheRestKeywords(article, keywords, mostUrgentKeyword):
    auxiliaryUrgency = 0
    keywordToSkip = list(mostUrgentKeyword.keys())[0]

    for keyword_obj in keywords:
        for keyword, weight in keyword_obj.items():
            if keyword.lower() == keywordToSkip.lower():
                continue

            if article.find(keyword.lower()) != -1:
                auxiliaryUrgency += weight * 0.2

    return auxiliaryUrgency


def measureError(article):
    splittedArticle = article.split("~", 1)
    heading = splittedArticle[0]
    content = splittedArticle[1]


    if content.find("error while collecting") != -1:
        return -100

    # Convert the heading and content to lowercase
    heading_lower = heading.lower()
    content_lower = content.lower()

    # Tokenize the heading into words
    heading_words = set(re.findall(r'\b\w+\b', heading_lower))

    # Tokenize the content into words
    content_words = set(re.findall(r'\b\w+\b', content_lower))

    # Check if any word from the heading is in the content
    for word in heading_words:
        if word in content_words:
            return 0

    # If no common words were found, return -10
    return -10



