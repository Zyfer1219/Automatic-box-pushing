import numpy as np
import random

class PointGrid(object):
    # 给定行、列数定义一个点阵
    def __init__(self, m=10, n=10):
        # 点阵的行数
        self._m = m
        # 点阵的列数
        self._n = n
        # 点阵中相邻点之间的所有的水平边
        self.HorizontalEdges = []
        # 点阵中相邻点之间的所有的垂直边
        self.VerticalEdges = []

        # 点阵中点的属性字典，其格式为key->value
        # 其中key是节点编号，value是该编号节点的属性值
        # value类型可由用户决定，因此可以支持各种不同类型的属性值
        # 例如，value可以是布尔状态，可以是灰度值，...
        self._A = {}

        # 初始化水平边列表，垂直边列表
        for r in range(self.m()):
            for c in range(self.n() - 1):
                self.HorizontalEdges.append((r * self.n() + c, r * self.n() + c + 1))
        for r in range(self.m() - 1):
            for c in range(self.n()):
                self.VerticalEdges.append((r * self.n() + c, r * self.n() + c + self.n()))

    # 设置点阵中点(r,c)的属性值为 a
    def set_attr(self, r, c, a):
        key = r * self.n() + c
        self._A[key] = a

    # 设置点阵中第ix个点的属性值为a
    def set_attr_bykey(self, key, a):
        self._A[key] = a

    # 将点阵属性值矩阵置为 A. 应确保A为m行,n列矩阵
    def set_attrs(self, dict):
        self._A = dict

    def get_attr(self, r, c):
        key = r * self.n() + c
        return self._A[key]

    # 根据点的序号取出其属性值
    def get_attr_bykey(self, key):
        return self._A[key]

    # 返回点阵中ix点的left、right、up、down四个邻居点的pix
    # 不存在的邻居点返回 -1
    def neighors_keys(self, key):
        r = self._r_c(key)[0]
        c = self._r_c(key)[1]
        left = right = up = down = -1
        if c - 1 >= 0:
            left = self._key(r, c - 1)
        if c + 1 <= self.n - 1:
            right = self._key(r, c + 1)
        if r - 1 >= 0:
            down = self._key(r - 1, c)
        if r + 1 <= self.m - 1:
            up = self._key(r + 1, c)
        return (left, right, up, down)

    # 返回点阵属性值矩阵置为 A
    def get_attrs(self):
        return self._A

    # 返回点阵中指定行的所有点序号
    def row_keys(self, r):
        if r < self.m:
            return list(range(r * self.n, (r + 1) * self.n, 1))

    # 返回点阵中指定列的所有点的序号
    def col_keys(self, c):
        if c < self.n:
            return list(range(c, c + (self.m - 1) * self.n + 1, self.n))

    # 返回点阵中指定行的所有属性值
    def row_attrs(self, r):
        r_attrs = []
        if r < self.m:
            for k in self.row_keys(r):
                r_attrs.append(self.get_attr_bykey(k))
            return r_attrs

    # 返回点阵中指定列的所有点的序号
    def col_attrs(self, c):
        c_attrs = []
        if c < self.n:
            for k in self.col_keys(c):
                c_attrs.append(self.get_attr_bykey(k))
            return c_attrs


    # 点阵中所有点以左下角点作为第0个点，按照从下到上，从左到右排序，
    # 此函数返回点阵中r,c位置的序号,注意 key即为点阵中节点的编号
    def _key(self, r, c):
        return r * self.n + c

    # 点阵中所有点以左下角点作为第1个点，按照从下到上，从左到右排序，
    # 此函数返回点阵中第pix个点的行、列号
    def _r_c(self, key):
        return (int(key / self.n), key % self.n)

    def getHorizontalEdges(self):
        return self.HorizontalEdges

    def getVerticalEdges(self):
        return self.VerticalEdges

    def m(self):
        return self._m

    def n(self):
        return self._n

    # PointGrid按照从下到上，从左到右对边进行编号
    # 返回第ix条水平边，注意边的编号从0开始
    def hedge(self, heix):
        left = int(heix / (self.n() - 1)) * self.n() + heix % (self.n() - 1)
        right = left + 1
        return (left, right)

    # PointGrid按照从下到上，从左到右对边进行编号
    # 返回第ix条垂直边，注意边的编号从0开始
    def vedge(self, veix):
        return (veix, veix + self.n())


# PointGrid类型的单元测试
def main():
    m1, n1 = 4, 4
    pg1 = PointGrid(m1, n1)
    keys1 = list(range(0, m1 * n1, 1))
    # 生成属性值随机0-1向量
    attrs1 = np.random.randint(0, 2, (1, m1 * n1))[0]
    dicts1 = dict(zip(keys1, attrs1))
    pg1.set_attrs(dicts1)
    print(pg1.get_attrs())

    m2, n2 = 5, 5
    pg2 = PointGrid(m2, n2)
    keys2 = list(range(0, m2 * n2, 1))
    attrs2 = []
    for i in range(m2 * n2):
        c = random.choice('abcdefghijklmnopqrstuvwxyz')
        attrs2.append(c)
    dicts2 = dict(zip(keys2, attrs2))
    pg2.set_attrs(dicts2)
    print(pg2.get_attrs())


if __name__ == '__main__':
    main()
