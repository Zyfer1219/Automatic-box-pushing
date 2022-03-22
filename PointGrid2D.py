import numpy as np
import stddraw
import stdrandom
import color
import math
from PointGrid import PointGrid

# PointGrid2D是PointGrid的继承类，具有平面坐标位置
class PointGrid2D(PointGrid):
    # 给定点阵中心坐标，区域宽、高，行列数定义一个点阵
    def __init__(self, cx=0.0, cy=0.0, w=100, h=100, m=10, n=10):
        PointGrid.__init__(self, m, n)
        # 点阵中心位置x坐标
        self._cx = cx
        # 点阵中心位置y坐标
        self._cy = cy
        # 点阵所在区域的宽度
        self._w = w
        # 点阵所在区域的高度
        self._h = h
        # 点阵中x方向上点之间的距离
        self._dx = 0.0
        # 点阵中y方向上点之间的距离
        self._dy = 0.0
        # 点阵中所有点的x坐标矩阵
        self._X = np.empty([m, n], dtype=float)
        # 点阵中所有点的y坐标矩阵
        self._Y = np.empty([m, n], dtype=float)
        # 点阵中所有点的位置坐标矩阵, m*n行 3列
        self._poss = np.empty([m * n, 3], dtype=float)
        #初始化
        for i in range(n*m):
            self._A[i]=1

        lbx = self._cx - w / 2
        lby = self._cy - h / 2
        self._dx = w / m
        self._dy = h / n
        lbcx = lbx + self._dx / 2
        lbcy = lby + self._dy / 2
        for i in range(n):
            self._X[:, [i]] = lbcx + self._dx * i
        for j in range(m):
            self._Y[[j], :] = lbcy + self._dy * j
        # 用X,Y矩阵初始化_poss矩阵
        self._update_poss_byXY()

    # 用X,Y坐标值矩阵更新_poss位置坐标矩阵
    def _update_poss_byXY(self):
        tempX = self._X
        tempY = self._Y
        tempX = tempX.reshape(self.m() * self.n(), 1)
        tempY = tempY.reshape(self.m() * self.n(), 1)
        tempOne = np.ones([self.m() * self.n(), 1])
        # 点阵中所有点的位置坐标矩阵, m*n行, 3列的矩阵
        self._poss = np.c_[tempX, tempY, tempOne]

    # 用_poss更新X,Y坐标值矩阵
    def _update_XY_byposs(self):
        # 取得_poss的左列,即 所有点的x坐标值构成的向量
        temp_left = self._poss[:, 0]
        # 取得_poss的右列,即 所有点的y坐标值构成的向量
        temp_right = self._poss[:, 1]
        self._X = temp_left.reshape(self._m, self._n)
        self._Y = temp_right.reshape(self._m, self._n)

    def dx(self):
        return self._dx

    def dy(self):
        return self._dy

    # 返回点阵中所有点的位置坐标矩阵
    def poss(self):
        return self._poss

    # 返回_poss中第ix个点的坐标元组
    def pos_ix(self, ix):
        return self._poss[ix, :]

    # 返回点阵中指定行的所有点的坐标
    def row_poss(self, r):
        r_ps = []
        for j in range(self._n):
            r_ps.append((self._X[r, j], self._Y[r, j]))
        return r_ps

    # 返回点阵中指定列的所有点的坐标
    def col_poss(self, c):
        c_ps = []
        for i in range(self._m):
            c_ps.append((self._X[i, c], self._Y[i, c]))
        return c_ps

    # 返回指定行、列的点的坐标
    def pos(self, r, c):
        return (self._X[r, c], self._Y[r, c])

    def get_attr_byvalue(self, val):
        for key,value in self.get_attrs().items():
            if value==val:
                return key

    # #箱子到人，箱子到目的地的曼哈顿距离
    # def Manhattan(self,op):
    #     box=self._r_c(self.get_attr_byvalue(3))
    #     if op=='me':
    #         me = self._r_c(self.get_attr_byvalue(2))
    #         manhattan = abs(me[0] - box[0]) + abs(me[1] - box[1])
    #     elif op=='des':
    #         des = self._r_c(self.get_attr_byvalue(4))
    #         manhattan = abs(des[0] - box[0]) + abs(des[1] - box[1])
    #     return manhattan
    #
    # def __lt__(self, other):
    #     # return self.Manhattan() +self.move < other.Manhattan()+other.move
    #     return self.Manhattan() < other.Manhattan()
# PointGrid2D类型的单元测试
def main():
    # 设置stdDraw窗口尺寸
    stddraw.setCanvasSize(600, 600)
    # 设置stdDraw的坐标范围
    stddraw.setXscale(-5, 5)
    stddraw.setYscale(-5, 5)
    stddraw.clear(stddraw.WHITE)

    m, n = 7, 9
    pg = PointGrid2D(0, 0, 6, 6, m, n)

    for p in pg.poss():
        x = p[0]
        y = p[1]
        stddraw.filledCircle(x, y, 0.2)

    stddraw.setPenRadius(0.1)
    ix = 12
    left_ix, right_ix = pg.hedge(ix)[0], pg.hedge(ix)[1]
    leftx, lefty = pg.pos_ix(left_ix)[0], pg.pos_ix(left_ix)[1]
    rightx, righty = pg.pos_ix(right_ix)[0], pg.pos_ix(right_ix)[1]
    stddraw.line(leftx, lefty, rightx, righty)

    cix = 7
    (down, up) = pg.vedge(cix)
    downx, downy = pg.pos_ix(down)[0],pg.pos_ix(down)[1]
    upx, upy = pg.pos_ix(up)[0], pg.pos_ix(up)[1]
    stddraw.setPenColor(stddraw.BLUE)
    stddraw.line(upx, upy, downx, downy)

    stddraw.show()

if __name__ == '__main__':
    main()
