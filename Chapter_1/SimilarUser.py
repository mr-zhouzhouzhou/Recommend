#coding=utf-8

"""
采用相似用户的方式，进行推荐：
    即：寻找最相似的一个或者几个用户，推荐用户没有关注过并且高分的歌曲

距离公式：   曼哈顿距离
            欧几里得距离
            皮尔逊相似度
            余弦相似度

            特点：曼哈顿距离和欧几里得距离 在没有缺失值的时候 效果 比较好
                 当“分数爆炸” 的时候 ，采用皮尔逊相似度 比较好，因为，每个用户的评分标准可能不一样，有的人习惯性地打高分，打分的标准是4-5分之间
                 有的人，打分偏低，2-3分，那么这时可以采用 皮尔逊相似度 计算它们的一致性
                 余弦相似度：
"""


from math import sqrt
import numpy as np
"""
    数据集：用户对7个乐队的评价分数
"""
users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

"""
 def __init__(self,recommitUser,usersList,is_normalization=False,distanceFunction='')
           recommitUser ： 需要推荐的用户
            usersList   ：  和该用户 评价过同样商品的一些用户
            is_normalization： 是否对数据采用正规化
            distanceFunction：距离函数
            
"""
class Recommit:

     def __init__(self,user,users,k):
         self.user=user
         self.users=users
         self.k=k


     def _manhattanDistance(self,username):
            distance=0
            for item in self.users[self.user]:
                if item in self.users[username]:
                    distance+=abs(self.users[username][item]-self.users[self.user][item])
            return distance


    #计算出最近的几个用户
     def _computerNeighbor(self):
        distances=[]
        for item  in self.users:
          if self.user!=item:
              distances.append((self._manhattanDistance(item),item))
        distances.sort()
        if len(distances)<self.k :
            return distances
        else:
            return distances[0:self.k]
     #推荐
     def recommit(self):
        recommituser=self._computerNeighbor()
        recommitList=[]
        userList=self.users[self.user]
        for item in recommituser:
            values=self.users[item[1]]
            for value in values:
                if values[value]> 3 and value not in userList and value not in recommitList:
                    recommitList.append(value)
        return recommitList

     def normalization(self):
         """
         正则化
         :return:
         """
         pass






re=Recommit("Hailey",users,3)
print(re.recommit())
