#coding=utf-8
from  math import sqrt


"""
    Slope One算法：也是一个基于物品的协同过滤方法：
    最大优势是：简单，易于实现
    
    
    对于两个物品，我们只要计算出同时评价过两个物品的用户数目 就可以了
    
    1：计算差值
    2：使用加权的slope one算法 进行预测

"""

users = {"David": {"Imagine Dragons": 3, "Daft Punk": 5,
                    "Lorde": 4, "Fall Out Boy": 1},
          "Matt": {"Imagine Dragons": 3, "Daft Punk": 4,
                   "Lorde": 4, "Fall Out Boy": 1},
          "Ben": {"Kacey Musgraves": 4, "Imagine Dragons": 3,
                  "Lorde": 3, "Fall Out Boy": 1},
          "Chris": {"Kacey Musgraves": 4, "Imagine Dragons": 4,
                    "Daft Punk": 4, "Lorde": 3, "Fall Out Boy": 1},
          "Tori": {"Kacey Musgraves": 5, "Imagine Dragons": 4,
                   "Daft Punk": 5, "Fall Out Boy": 3}}

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

"""
    1:先找出 用户 没有听过的歌曲或者歌手
    2：对这些歌手进行 预测评分
"""
class Recommit:
    def __init__(self,username,users):
        self.username=username
        self.users=users

    """
         获取待推荐物品，即用户不曾见过的物品
     """

    def _getRecommits(self):
        recommits = []
        for user in self.users:
            if user != self.username:  # 不是该用户
                for item in self.users[user]:
                    if item not in self.users[self.username] and item not in recommits:
                        recommits.append(item)
        return recommits

    def __getDev(self,left,right):
        """
        :param left: 第一个参数
        :param right: 第二个参数
        :return: 平均差值和个数
        """
        dev=0.0
        n=0
        for user in self.users:
            if user != self.username:
                if left in self.users[user] and right in self.users[user]:
                    dev+=self.users[user][left]-self.users[user][right]
                    n+=1
        return dev/n,n

    def _computerScore(self,name):
        element=0.0
        length=0
        for item in self.users[self.username]:
            dev,n=self.__getDev(item,name)
            length+=n
            element+=(dev+self.users[self.username][item])*n
        return (element/length,name)

    def recommit(self):
        recommits=self._getRecommits()
        recommitlist=[]
        for item in recommits:
            recommitlist.append(self._computerScore(item))
        return recommitlist



for user in users:
    re= Recommit(user,users)
    print(re.recommit())