#coding=utf-8

from math import sqrt

users3 = {"David": {"Imagine Dragons": 3, "Daft Punk": 5,
                    "Lorde": 4, "Fall Out Boy": 1},
          "Matt": {"Imagine Dragons": 3, "Daft Punk": 4,
                   "Lorde": 4, "Fall Out Boy": 1},
          "Ben": {"Kacey Musgraves": 4, "Imagine Dragons": 3,
                  "Lorde": 3, "Fall Out Boy": 1},
          "Chris": {"Kacey Musgraves": 4, "Imagine Dragons": 4,
                    "Daft Punk": 4, "Lorde": 3, "Fall Out Boy": 1},
          "Tori": {"Kacey Musgraves": 5, "Imagine Dragons": 4,
                   "Daft Punk": 5, "Fall Out Boy": 3}}
"""
    修正后的相似度：
        每个人评分标准是不一样的。  后效果更好了  ，好像还可以修正；
"""
def computer_cos_similar(bandname1,bandname2,userScores):
    meanscore=meanScore(userScores)
    leftDe=0.0
    righDe=0.0
    element=0.0
    for user in userScores:
        if bandname1 in userScores[user] and bandname2 in userScores[user]:
            element+=(userScores[user][bandname1]-meanscore[user])*(userScores[user][bandname2]-meanscore[user])
            leftDe+=(userScores[user][bandname1]-meanscore[user])**2
            righDe+=(userScores[user][bandname2]-meanscore[user])**2
    return element/(sqrt(leftDe)*sqrt(righDe))


def meanScore(userScores):
    meanscore={}
    for user in userScores:
        scoresum=0.0
        l=0
        for item in userScores[user]:
            l+=1
            scoresum+=userScores[user][item]
        meanscore[user]=scoresum/l
    return meanscore


print(computer_cos_similar('Kacey Musgraves', 'Lorde', users3))
print(computer_cos_similar('Imagine Dragons', 'Lorde', users3))
print(computer_cos_similar('Daft Punk', 'Lorde', users3))