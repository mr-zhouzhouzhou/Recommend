#coding=utf-8
from math import  sqrt
items = {"Dr Dog/Fate": [2.5, 4, 3.5, 3, 5, 4, 1],
         "Phoenix/Lisztomania": [2, 5, 5, 3, 2, 1, 1],
         "Heartless Bastards/Out": [1, 5, 4, 2, 4, 1, 1],
         "Todd Snider/Don't Tempt Me": [4, 5, 4, 4, 1, 5, 1],
         "The Black Keys/Magic Potion": [1, 4, 5, 3.5, 5, 1, 1],
         "Glee Cast/Jessie's Girl": [1, 5, 3.5, 3, 4, 5, 1],
         "La Roux/Bulletproof": [5, 5, 4, 2, 1, 1, 1],
         "Mike Posner": [2.5, 4, 4, 1, 1, 1, 1],
         "Black Eyed Peas/Rock That Body": [2, 5, 5, 1, 2, 2, 4],
         "Lady Gaga/Alejandro": [1, 5, 3, 2, 1, 2, 1]}


users = {"Angelica": {"Dr Dog/Fate": "L",
                      "Phoenix/Lisztomania": "L",
                      "Heartless Bastards/Out at Sea": "D",
                      "Todd Snider/Don't Tempt Me": "D",
                      "The Black Keys/Magic Potion": "D",
                      "Glee Cast/Jessie's Girl": "L",
                      "La Roux/Bulletproof": "D",
                      "Mike Posner": "D",
                      "Black Eyed Peas/Rock That Body": "D",
                      "Lady Gaga/Alejandro": "L"},
         "Bill": {"Dr Dog/Fate": "L",
                  "Phoenix/Lisztomania": "L",
                  "Heartless Bastards/Out at Sea": "L",
                  "Todd Snider/Don't Tempt Me": "D",
                  "The Black Keys/Magic Potion": "L",
                  "Glee Cast/Jessie's Girl": "D",
                  "La Roux/Bulletproof": "D",
                  "Mike Posner": "D",
                  "Black Eyed Peas/Rock That Body": "D",
                  "Lady Gaga/Alejandro": "D"}}
class Classify:
    def __init__(self,itemName,victor,user,users,items,distanceFunction='manhattan'):
        self.users=users
        self.user=user
        self.victor=victor
        self.itemName=itemName
        self.items=items
        if distanceFunction=='manhattan':
            self.distance=self._manhattan
        if distanceFunction=='euclid':
            self.distance=self._euclid
        if distanceFunction=='pearson':
            self.distance=self._pearson

    """
           数据格式：
               [2.5, 4, 3.5, 3, 5, 4, 1]
       """

    def _manhattan(self, victor1, victor2):
        distance = 0.0
        n=len(victor1)
        for item in range(n):
                distance += abs(victor1[item] - victor2[item])
        return distance

    def _euclid(self, victor1, victor2):
        distance = 0.0
        n=len(victor1)
        for item in range(n):
                distance += (victor1[item] - victor2[item]) ** 2
        return sqrt(distance)

    """
        皮尔逊相关系数: 又称皮尔逊积矩相关系数，是用于度量两个变量X和Y之间的相关（线性相关），其值介于-1与1之间。
            两个矩阵的协方差/（标准差的乘积）

        适用范围：当两个变量的标准差都不为零时，相关系数才有定义，皮尔逊相关系数适用于：
                    (1)、两个变量之间是线性关系，都是连续数据。
                    (2)、两个变量的总体是正态分布，或接近正态的单峰分布。
                    (3)、两个变量的观测值是成对的，每对观测值之间相互独立。

        作用：判断两组数的线性关系程度。
    """

    def _pearson(self, left, right):
        leftmean, rightmean, n = self._mean(left, right)
        element = 0.0
        leftdenominator = 0.0
        rightdenominator = 0.0

        for item in left:
            if item in right:
                element += (left[item] - leftmean) * (right[item] - rightmean)
                leftdenominator += (left[item] - leftmean) ** 2
                rightdenominator += (right[item] - rightmean) ** 2
        if leftdenominator == 0 or rightdenominator == 0 or element == 0:
            return 0.0
        return element / (sqrt(leftdenominator / n) * sqrt(rightdenominator / n))


    """
        计算最邻近的几个点
    """
    def _computerNearestNeighbor(self):

        disstances=[]
        for item in self.items:
            disstances.append(( self.distance(self.victor,self.items[item]),item))
        disstances.sort()
        return disstances


    def recommit(self):
        nearests=self._computerNearestNeighbor()
        return self.users[self.user][nearests[0][1]]






re=Classify('Chris Cagle/I Breathe In. I Breathe Out', [1, 5, 2.5, 1, 1, 5, 1], "Bill",users,items)
if re.recommit()=="D":
    print("Bill dont like Chris Cagle/I Breathe In. I Breathe Out !")
else:
    print("Bill like Chris Cagle/I Breathe In. I Breathe Out !")
