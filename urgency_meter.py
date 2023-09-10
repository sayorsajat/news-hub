def measureUrgency(article, keywords):
    mostUrgentKeyword = getMostImportantKeyword(article, keywords)
    urgency = 0

    for keyword, weight in mostUrgentKeyword.items():
        if article.find(keyword) != -1:
            urgency = weight

    urgency += calculateUrgencyOfTheRestKeywords(article, keywords, mostUrgentKeyword)

    return urgency


def getMostImportantKeyword(article, keywords):
    mostUrgentKeyword = keywords[0]

    for keyword_obj in keywords:
        for keyword, weight in keyword_obj.items():
            if article.find(keyword) == -1:
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
            if keyword == keywordToSkip:
                continue

            if article.find(keyword) != -1:
                auxiliaryUrgency += weight * 0.2

    return auxiliaryUrgency
