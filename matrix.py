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

    # *********** do not forget to write RREF function ********

    # Operator overloading
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

    def __chr(self, org, des):  # change rows
        self.__mat[org], self.__mat[des] = self.__mat[des], self.__mat[org]

    def __mulnum(self, num, ind, row=0,
                 addind: int = None):  # multiply a number into one row/column and add to another row/column
        if not row:
            tmp = [num * i for i in self.__mat[ind]]
            if addind is not None:
                self.__mat[ind] = [x + y for x, y in zip(tmp, self.__mat[addind])]
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

print(e * f)
print(e)
print(f)
# c = a + b
# print(c)
