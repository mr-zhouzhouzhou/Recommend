#coding=utf-8
from math import  sqrt
"""
    基于商品的推荐系统：论文发表于2001年
    论文亮点在于：修正后的余弦相似度，加入了 每个用户的评分标准
    第二个就是 预测方式
            p (u i ) = ∑ （S i,n* R u,n）/ ∑ |S i,n|

            S i,n  表示商品i和n 的相似度
            R u,n  表示用户u 对商品N的评分


    为了让计算效果更佳，需要把评分转换为-1到1 之间
"""


users2 = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
                      "Norah Jones": 4.5, "Phoenix": 5.0,
                      "Slightly Stoopid": 1.5, "The Strokes": 2.5,
                      "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5,
                 "Deadmau5": 4.0, "Phoenix": 2.0,
                 "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0,
                  "Deadmau5": 1.0, "Norah Jones": 3.0,
                  "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0,
                 "Deadmau5": 4.5, "Phoenix": 3.0,
                 "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                 "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0,
                    "Norah Jones": 4.0, "The Strokes": 4.0,
                    "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0,
                     "Norah Jones": 5.0, "Phoenix": 5.0,
                     "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                     "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0,
                 "Norah Jones": 3.0, "Phoenix": 5.0,
                 "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0,
                      "Phoenix": 4.0, "Slightly Stoopid": 2.5,
                      "The Strokes": 3.0}
        }

class Recommit:
    def __init__(self,username,userScores):
        self.username=username
        self.userScores=userScores


    """
        计算两个物品之间的相似度
    """
    def _computer_cos_similar(self,bandname1, bandname2):
        meanscore = self._meanScore(self.userScores)
        leftDe = 0.0
        righDe = 0.0
        element = 0.0
        for user in self.userScores:
            if bandname1 in self.userScores[user] and bandname2 in self.userScores[user]:
                element += (self.userScores[user][bandname1] - meanscore[user]) * (
                            self.userScores[user][bandname2] - meanscore[user])
                leftDe += (self.userScores[user][bandname1] - meanscore[user]) ** 2
                righDe += (self.userScores[user][bandname2] - meanscore[user]) ** 2
        return element / (sqrt(leftDe) * sqrt(righDe))

    def _meanScore(self,userScores):
        meanscore = {}
        for user in userScores:
            scoresum = 0.0
            l = 0
            for item in userScores[user]:
                l += 1
                scoresum += userScores[user][item]
            meanscore[user] = scoresum / l
        return meanscore

    """
        获取待推荐物品，即用户不曾见过的物品
    """
    def _getRecommits(self):
        recommits=[]
        for user in self.userScores:
            if user!=self.username:#不是该用户
                for item in self.userScores[user]:
                    if item not in self.userScores[self.username] and item not in recommits:
                        recommits.append(item)
        return recommits


    def recommit(self):
        recommits=self._getRecommits()
        recommitList=[]
        for re in recommits:
            mlist=[]
            for item in self.userScores[self.username]:
                mlist.append([self._computer_cos_similar(re,item),self.userScores[self.username][item]])
            recommitList.append([mlist,re])
        print(len(recommitList))
        results=[]
        for items in  recommitList:
            element=0.0
            totalSimile=0.0
            for item in items[0]:
                if item[0]>0:
                    element+=item[0]*item[1]
                    totalSimile+=abs(item[0])
            results.append((element/totalSimile,items[1]))
        results.sort(reverse=True)
        return results,




re=Recommit("Hailey",users)
results=re.recommit()
print(results)
