import numpy as np
import stddraw
import stdrandom
import color
import math


class point2DMatrix:
    # 给定点阵中心坐标，区域宽、高，行列数定义一个点阵
    def __init__(self, cx=0.0, cy=0.0, w=100, h=100, m=10, n=10):
        # 点阵中心位置x坐标
        self._cx = cx
        # 点阵中心位置y坐标
        self._cy = cy
        # 点阵所在区域的宽度
        self._w = w
        # 点阵所在区域的高度
        self._h = h
        # 点阵的行数
        self._m = m
        # 点阵的列数
        self._n = n
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
        # 点阵中相邻点之间的所有的水平边
        self._HorizontalEdges = []
        # 点阵中相邻点之间的所有的垂直边
        self._VerticalEdges = []
        # 点阵中点的属性值矩阵,例如灰度值矩阵
        self._A = np.zeros([m, n], dtype=float)

        lbx = self._cx - w / 2
        lby = self._cy - h / 2
        delta_x = w / n
        delta_y = h / m
        self._dx = delta_x
        self._dy = delta_y
        lbcx = lbx + delta_x / 2
        lbcy = lby + delta_y / 2
        for i in range(n):
            self._X[:, [i]] = lbcx + delta_x * i
        for j in range(m):
            self._Y[[j], :] = lbcy + delta_y * j
        # 用X,Y矩阵初始化_poss矩阵
        self._update_poss_byXY()

        # 初始化水平边列表，垂直边列表
        for r in range(self._m):
            for c in range(self._n - 1):
                self._HorizontalEdges.append((r * self._n + c, r * self._n + c + 1))
        for r in range(self._m - 1):
            for c in range(self._n):
                self._VerticalEdges.append((r * self._n + c, r * self._n + c + self._n))

    # 用X,Y坐标值矩阵更新_poss位置坐标矩阵
    def _update_poss_byXY(self):
        tempX = self._X
        tempY = self._Y
        tempX = tempX.reshape(self._m * self._n, 1)
        tempY = tempY.reshape(self._m * self._n, 1)
        tempOne = np.ones([self._m * self._n, 1])
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

    # 设置点阵中点(r,c)的属性值为 a
    def set_value(self, r, c, a):
        self._A[r, c] = a

    # 将点阵属性值矩阵置为 A. 应确保A为m行,n列矩阵
    def set_values(self, A):
        self._A = A

    def get_value(self, r, c):
        return self._A[r, c]

    # # 根据点的序号取出其属性值
    # def get_value(self, ix):
    #     r = self._r_c(ix)[0]
    #     c = self._r_c(ix)[1]
    #     return self._A[r, c]
    #TODO
    def move(self,point,dic):
        if(dic=='d'):

            pos_value=self.get_value(point[0],point[1])
            pos_new_value=self.get_value(point[0],point[1]+1)
            print("pos",pos_value)
            print("pos_new",pos_new_value)
            self.set_value(point[0],point[1],pos_new_value)
            self.set_value(point[0], point[1]+1, pos_value)
        elif(dic=='a'):
            pos_value = self.get_value(point[0], point[1])
            pos_new_value = self.get_value(point[0], point[1] - 1)
            self.set_value(point[0], point[1], pos_new_value)
            self.set_value(point[0], point[1] - 1, pos_value)
        elif(dic=='s'):
            pos_value = self.get_value(point[0], point[1])
            pos_new_value = self.get_value(point[0]-1, point[1])
            self.set_value(point[0], point[1], pos_new_value)
            self.set_value(point[0]-1, point[1] , pos_value)
        else:
            pos_value = self.get_value(point[0], point[1])
            pos_new_value = self.get_value(point[0] + 1, point[1])
            self.set_value(point[0], point[1], pos_new_value)
            self.set_value(point[0]+1, point[1] , pos_value)
        self._update_XY_byposs()
    # 返回点阵中ix点的left、right、up、down四个邻居点的pix
    # 不存在的邻居点返回 -1
    def neighors_ixs(self, ix):
        r = self._r_c(ix)[0]
        c = self._r_c(ix)[1]
        left = right = up = down = -1
        if c - 1 >= 0:
            left = self._pix(r, c - 1)
        if c + 1 <= self._n - 1:
            right = self._pix(r, c + 1)
        if r - 1 >= 0:
            down = self._pix(r - 1, c)
        if r + 1 <= self._m - 1:
            up = self._pix(r + 1, c)
        return (left, right, up, down)

    # 返回点阵属性值矩阵置为 A
    def get_values(self):
        return self._A

    def m(self):
        return self._m

    def n(self):
        return self._n

    def cs(self):
        return (self._cx, self._cy)

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
    def row_pos(self, r):
        r_ps = []
        for j in range(self._n):
            r_ps.append((self._X[r, j], self._Y[r, j]))
        return r_ps

    # 返回点阵中指定列的所有点的坐标
    def col_pos(self, c):
        c_ps = []
        for i in range(self._m):
            c_ps.append((self._X[i, c], self._Y[i, c]))
        return c_ps

    # 返回点阵中指定行的所有点序号
    def row_ixs(self, r):
        if r < self.m():
            return list(range(r * self._n, (r + 1) * self._n, 1))

    # 返回点阵中指定列的所有点的序号
    def col_ixs(self, c):
        if c < self.n():
            return list(range(c, c + (self._m - 1) * self._n + 1, self._n))

    # 返回指定行、列的点
    def pos(self, r, c):
        return (self._X[r, c], self._Y[r, c])

    # 点阵中所有点以左下角点作为第0个点，按照从下到上，从左到右排序，
    # 此函数返回点阵中r,c位置的序号
    def _pix(self, r, c):
        return r * self._n + c

    # 点阵中所有点以左下角点作为第1个点，按照从下到上，从左到右排序，
    # 此函数返回点阵中第pix个点的行、列号
    def _r_c(self, pix):
        return (int(pix / self._n), pix % self._n)

        # 用变换矩阵 T 变换点阵中所有点的坐标位置, 实现平移点阵，旋转点阵等操作

    # 类似的变换矩阵有： T = np.array([[1,1/2],[0,1]])
    # T = np.array([[1/2, 0], [0, 2]])
    # T = np.array([[math.cos(math.pi / 6), -math.sin(math.pi / 6)], [math.sin(math.pi / 6), math.cos(math.pi / 6)]])
    def transform_by(self, T):
        self._poss = np.matmul(self._poss, T)
        self._update_XY_byposs()

    # 不改变当前的点矩阵内容，返回变换后的一个新的点矩阵
    def transform(self, T):
        t_m = self._m
        t_n = self._n
        new_poss = np.matmul(self._poss, T)
        first = new_poss[0]
        last = new_poss[t_m * t_n - 1]
        t_cs_x = (first[0] + last[0]) / 2
        t_cs_y = (first[1] + last[1]) / 2
        # print("new cs : " + str(t_cs_x) + " , " + str(t_cs_y) + "\n")
        # t_w = last[0] - first[0]
        # t_h = last[1] - first[1]
        # new_pmx = point2DMatrix(t_cs_x, t_cs_y, t_w, t_h, t_m, t_n)

        return new_poss

    def HorizontalEdges(self):
        return self._HorizontalEdges

    def VerticalEdges(self):
        return self._VerticalEdges


def main():
    # 设置stdDraw窗口尺寸
    stddraw.setCanvasSize(600, 600)
    # 设置stdDraw的坐标范围
    stddraw.setXscale(-5, 5)
    stddraw.setYscale(-5, 5)
    stddraw.clear(stddraw.WHITE)
    m, n = 5, 6
    pm = point2DMatrix(-2, -2, 4, 4, m, n)

    for r in range(m):
        for c in range(n):
            # 取出pm中c行，r列的点
            p = pm.pos(r, c)
            cc = 210
            stddraw.setPenColor(color.Color(cc, cc, cc))
            stddraw.filledCircle(p[0], p[1], 0.1)

    p1 = pm.pos(0, 2)
    stddraw.setPenColor(stddraw.BLUE)
    stddraw.filledSquare(p1[0], p1[1], 0.2)

    p2 = pm.pos(3, 4)
    stddraw.setPenColor(stddraw.BLUE)
    stddraw.filledSquare(p2[0], p2[1], 0.2)

    p3 = pm.pos_ix(12)
    stddraw.setPenColor(stddraw.RED)
    stddraw.filledSquare(p3[0], p3[1], 0.2)

    p4 = pm.pos_ix(14)
    stddraw.setPenColor(stddraw.RED)
    stddraw.filledSquare(p4[0], p4[1], 0.2)

    row = 1
    stddraw.setPenColor(stddraw.GREEN)
    # 取出pm中第row行的所有点，并绘制
    for p in pm.row_pos(row):
        stddraw.filledSquare(p[0], p[1], 0.1)
    col = 3
    stddraw.setPenColor(stddraw.CYAN)
    # 取出pm中第col列的所有点，并绘制
    for p in pm.col_pos(col):
        stddraw.filledSquare(p[0], p[1], 0.1)

    stddraw.show()


if __name__ == '__main__':
    main()
