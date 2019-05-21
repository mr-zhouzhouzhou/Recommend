#coding==utf-8


"""
    余弦相似度：
        在文本挖掘中应用的比较多，在协同过滤中用的也比较多
    之所以这么做：例如网易云音乐上，可能很多歌曲 你都没有听过。所以说单个用户的数据
    是稀疏的，因为非零值较总体来说，要小得多


    余弦相似度的计算 会忽略这些非零值。
      cos （x,y）= x . y /（||x||*||y||）
      .代表数量积  ||x|| 代表的是 x的 模
      计算公式  平方和的开根号



    如果 数据存在 分数膨胀 问题 ： 就使用皮尔逊相关系数
    如果数据比较密集， 变量之间基本都存在公有值，且这些距离非常重要，那么采用欧几里得或者曼哈顿距离

    如果数据是稀疏的，就使用余弦相似度
"""


"""
        K最近邻算法：
            在协同过滤中可以使用K最邻近算法来 找出K个最相似的用户 ，以此作为推荐的基础
            在不同的应用中，有不同的K值，需要做一些实验得出
            采用余弦相似度的比重 来计算 最后 对某一个需要推荐商品的评分
"""

from math import sqrt

"""
        当不同特征的评分尺度不一致的时候，为了的得更准确的距离结果时，就需要将这些特征进行标准化，使得他们在同一个尺度内波动；
        正规化：就是将值得范围缩小到0-1之间；
        标准化：就是将特征值转化为均值为0的一组数

        例子1：（value - min）/(max -min)
        例子2：(value-mean）/(max -min)
"""
users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0,
                      "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5,
                  "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5,
                  "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5,
                 "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0,
                    "Vampire Weekend": 1.0},
         "Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5,
                    "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0,
                 "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5,
                      "The Strokes": 3.0}
         }


class Recommit:

    def __init__(self, user, users, k, functionname='manhattan', is_normalization=False):
        self.user = user
        self.k = k
        if is_normalization:
            self.users = self._normal_batch(users)
        else:
            self.users = users
        if functionname == "manhattan":
            self.distance = self._manhattan
        if functionname == "euclid":
            self.distance = self._euclid
        if functionname == "pearson":
            self.distance = self._pearson
        if functionname == "cosSimilar":
            self.distance = self._cosSimilar

    def _getMaxMin(self, items):
        maxValue = 0.0
        minValue = 0.0
        for item in items:
            if items[item] > maxValue:
                maxValue = items[item]
            if items[item] < minValue:
                minValue = items[item]
        return maxValue, minValue

    def _normal_batch(self, users):
        for item in users:
            users[item] = self._normalization(users[item])
        return users

    def _normalization(self, items):
        maxValue, minValue = self._getMaxMin(items)
        for item in items:
            items[item] = (items[item] - minValue) / (maxValue - minValue)
        return items

    """
        数据格式：
            {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    """

    def _manhattan(self, left, right):
        distance = 0.0
        for item in left:
            if item in right:
                distance += abs(left[item] - right[item])
        return distance

    def _euclid(self, left, right):
        distance = 0.0
        for item in left:
            if item in right:
                distance += (left[item] - right[item]) ** 2
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
        余弦相似度：用于稀疏矩阵
    """
    def _cosSimilar(self,left,right):
        element=0.0
        leftdenominator=0.0
        rightdenominator=0.0
        for item in left:
            if item in right:
                element+=left[item]*right[item]
                leftdenominator+=left[item]**2
                rightdenominator+=right[item]**2
        return element/(sqrt(leftdenominator)*sqrt(rightdenominator))



    def _mean(self, left, right):
        leftSum = 0.0
        rightSum = 0.0
        n = 0
        for item in left:
            if item in right:
                n += 1
                leftSum += left[item]
                rightSum += right[item]
        return leftSum / n, rightSum / n, n

    # 计算出最近的几个用户
    def _computerNeighbor(self):
        distances = []
        for item in self.users:
            if self.user != item:
                distances.append(((self.distance(users[self.user], self.users[item])), item))
        distances.sort()
        if len(distances) < self.k:
            print("distances :", distances)
            return distances
        else:
            print("distances[0:self.k] :", distances[0:self.k])
            return distances[0:self.k]

            # 推荐

    def recommit(self):
        recommituser = self._computerNeighbor()
        # print(recommituser)
        recommitList = []
        userList = self.users[self.user]
        for item in recommituser:
            values = self.users[item[1]]
            for value in values:
                if values[value] > 0.5 and value not in userList and value not in recommitList:
                    recommitList.append(value)
        return recommitList


# re = Recommit("Bill", users, 3)
# print(re.recommit())
#
# re = Recommit("Bill", users, 3, functionname='euclid',is_normalization=False)
# print(re.users)


def getMaxMin(items):
    maxValue = 0.0
    minValue = 0.0
    for item in items:
        if items[item] > maxValue:
            maxValue = items[item]
        if items[item] < minValue:
            minValue = items[item]
    return maxValue, minValue


def normal_batch(users):
    for item in users:
        users[item] = normalization(users[item])
    return users


def normalization(items):
    maxValue, minValue = getMaxMin(items)
    for item in items:
        items[item] = (items[item] - minValue) / (maxValue - minValue)
    return items


re = Recommit("Bill", users, 3, functionname='euclid', is_normalization=True)
print(re.recommit())