import copy


class Matrix:
    def __init__(self, r: int = 0, c: int = 0, mat: list[list] = None):
        if mat is None:
            mat = [[]]
        self.__r = r
        self.__c = c
        self.__mat = mat
        self.__determinant = 0

    # user functions
    def determinant(self):
        if self.__c == self.__r:
            i, j = 0, 0
            if self.__c == 2:
                return (self.__mat[0][0] * self.__mat[1][1]) - (self.__mat[0][1] * self.__mat[1][0])
            if self.__c == 3:
                return ((self.__mat[0][0] * self.__mat[1][1] * self.__mat[2][2]) + (
                        self.__mat[1][0] * self.__mat[2][1] * self.__mat[0][2]) + (
                                self.__mat[0][1] * self.__mat[1][2] * self.__mat[2][0])) - (
                        (self.__mat[0][2] * self.__mat[1][1] * self.__mat[2][0]) + (
                        self.__mat[0][1] * self.__mat[1][0] * self.__mat[2][2]) + (
                                self.__mat[1][2] * self.__mat[2][1] * self.__mat[0][0]))
            else:
                while j < self.__c:
                    if self.__mat[i][j] != 0:
                        temp = self.__delete_deter(i, j)
                        self.__determinant += (((-1) ** (i + j)) * self.__mat[i][j] * temp.determinant())
                    j += 1
                return self.__determinant
        else:
            raise Exception("Matrix Dimension should be square")

    def transpose(self):
        self.__r, self.__c = self.__c, self.__r
        tmp = [[] for _ in range(self.__r)]
        for i in self.__mat:
            pos = 0
            for j in i:
                tmp[pos].append(j)
                pos += 1
        self.__mat = tmp

    def rref(self):  # Reduced Row Echelon form
        temp, row, no_nonzero_row, limit = copy.deepcopy(self), 0, 0, min(self.__r, self.__c)
        while row < limit:
            pivot = row
            if temp[row] == [0] * temp.__c:  # detect zero row and move it to bottom
                for i in range(row + 1, temp.__r):
                    if temp[i] != [0] * temp.__c:
                        temp.__chr(row, i)
                        break
                else:
                    no_nonzero_row = 1
            if not no_nonzero_row:
                if temp[row][pivot] == 0:  # make pivot element for each row nonzero
                    for i in range(pivot + 1, temp.__c):
                        if temp[row][i] != 0:
                            # temp.__chr(pivot, i, 1) for changing two column (use when u want change columns)
                            pivot = i
                            break
                temp.__mulnum(1 / temp[row][pivot], row)  # check the argument if it doesn't work good
                for i in range(temp.__r):
                    if i == row:
                        continue
                    if temp[i][pivot] != 0:
                        temp.__mulnum(-1 * temp[i][pivot], row, addind=i)
            else:
                break
            row += 1
        return temp

    # Operator overloading
    def __getitem__(self, item):
        return self.__mat[item]

    def __add__(self, other: "Matrix"):
        if self.__c != other.__c or self.__r != other.__r:
            raise Exception("Matrix Dimensions have to equal")
        res = []
        for i in range(self.__r):
            res.append([sum(item) for item in zip(self.__mat[i], other.__mat[i])])
        return Matrix(self.__r, self.__c, res)

    def __mul__(self, inp: "int | Matrix"):
        temp, clm = [], self.__c
        if type(inp) == int:
            for i in self.__mat:
                new = []
                for j in i:
                    new.append(j * inp)
                temp.append(new.copy())
        else:
            if self.__c != inp.__r:
                raise Exception("Matrices can't multiply to each other")
            else:
                inp.transpose()
                for i in self.__mat:
                    new = []
                    for j in inp.__mat:
                        new.append(sum([x * y for x, y in zip(i, j)]))
                    temp.append(new)
                clm = inp.__c
                inp.transpose()
        return Matrix(self.__r, clm, temp)

    def __str__(self):
        res = ""
        for i in self.__mat:
            for j in i:
                res += f'{str(j)} '
            res += '\n'
        return res

    # private functions
    def __delete_deter(self, r, c):
        i, result = 0, []
        while i < self.__r:
            tmp, j = [], 0
            if i != r:
                while j < self.__c:
                    if j != c:
                        tmp.append(self.__mat[i][j])
                    j += 1
                result.append(tmp.copy())
            i += 1
        return Matrix(self.__r - 1, self.__c - 1, result)

    def __chr(self, org, des, column=0):  # change rows and column
        if column:
            self.transpose()
        self.__mat[org], self.__mat[des] = self.__mat[des], self.__mat[org]
        if column:
            self.transpose()

    def __mulnum(self, num, ind, row=0,
                 addind: int = None):  # multiply a number into one row/column and add to another row/column
        if not row:
            tmp = [num * i for i in self.__mat[ind]]
            if addind is not None:
                self.__mat[addind] = [x + y for x, y in zip(tmp, self.__mat[addind])]
            else:
                self.__mat[ind] = tmp
            return
        else:
            self.transpose()
            self.__mulnum(num, ind, addind=addind)
            self.transpose()


m, n = 4, 4
a = Matrix(3, 4, [[1, 0, 1, 5], [1, 2, 0, 6], [4, 6, 2, 7]])
b = Matrix(m, n, [[1, 0, 1, 8], [1, 2, 0, 3], [4, 6, 2, 6], [0, 3, 6, 4]])
c = Matrix(6, 6, [[1, 0, 0, 0, 0, 2], [0, 1, 0, 0, 2, 0], [0, 0, 1, 2, 0, 0], [0, 0, 2, 1, 0, 0], [0, 2, 0, 0, 1, 0],
                  [2, 0, 0, 0, 0, 1]])
e = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
f = Matrix(3, 2, [[7, 8], [9, 10], [11, 12]])
g = Matrix(4, 5, [[1, 2, 3, 4, 5], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [6, 7, 8, 9, 10]])
l = Matrix(3, 5, [[1, 2, 3, 4, 5], [0, 0, 2, 3, 4], [0, 0, 0, 1, 3]])

print(l.rref())
# c = a + b
# print(c)
