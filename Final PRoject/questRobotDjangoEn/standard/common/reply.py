import math
from math import isnan
from sklearn.feature_extraction.text import TfidfVectorizer
from data import QUESTION


def jieba_function(sent):
    import jieba
    sent1 = jieba.cut(sent)
    s = []
    for each in sent1:
        s.append(each)
    return ' '.join(str(i) for i in s)


def count_cos_similarity(vec_1, vec_2):
    if len(vec_1) != len(vec_2):
        return 0

    s = sum(vec_1[i] * vec_2[i] for i in range(len(vec_2)))
    den1 = math.sqrt(sum([pow(number, 2) for number in vec_1]))
    den2 = math.sqrt(sum([pow(number, 2) for number in vec_2]))
    return s / (den1 * den2)


def tfidf(sent1, sent2):
    sent1 = jieba_function(sent1)
    sent2 = jieba_function(sent2)
    tfidf_vec = TfidfVectorizer()
    sentences = [sent1, sent2]
    vec_1 = tfidf_vec.fit_transform(sentences).toarray()[0]
    vec_2 = tfidf_vec.fit_transform(sentences).toarray()[1]
    similarity = count_cos_similarity(vec_1, vec_2)
    if isnan(similarity):
        similarity = 0.0
    return similarity


def returAnswer(word):
    # Text similarity algorithm
    maxScore = 0.010
    maxFaq = []

    # Data cleaning
    word = word.strip()

    for row in QUESTION:
        # Then compare each question in the database to the current question
        score = tfidf(row["title"], word)  # Computes the similarity and returns the similarity value
        if score > maxScore:
            print(score)
            maxScore = score
            maxFaq = row["content"]
    return maxFaq  # Returns the answer to the question with the highest similarity


if __name__ == '__main__':
    data = returAnswer("pep")
    print(data)
