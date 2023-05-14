import numpy as np
import pandas as pd


# CustomMatrix class, represented by a numpy 2D array (matrix)
class CustomMatrix(object):
    # constructor from a numpy 2D array
    def __init__(self, matrix: np.ndarray | np.matrix):
        matrix = matrix.copy()
        self.check_matrix(matrix)
        self.matrix = self.invariant(matrix)

    # check if the input is a numpy 2D array
    def check_matrix(self, matrix):
        if not isinstance(matrix, np.ndarray) and not isinstance(matrix, np.matrix):
            raise TypeError(
                f"Input matrix is not a numpy array or matrix, but {type(matrix)}"
            )
        if matrix.ndim != 2:
            raise TypeError(f"Input matrix is not a 2D array, but {matrix.ndim}D")

    # initialize from a pandas DataFrame
    # require all numeric
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Input is not a pandas DataFrame, but {type(df)}")
        if not df.select_dtypes(include=np.number).columns.equals(df.columns):
            raise TypeError("Not all columns are numeric")

        # convert to numpy array
        matrix = df.to_numpy()
        return cls(matrix)

    # copy
    def copy(self):
        return self.__class__(self.matrix)

    # clean the input matrix
    #   fill all sorts of nan, NA, None with 0
    #   convert to float
    def invariant(self, matrix):
        matrix = np.nan_to_num(matrix)
        matrix = matrix.astype(float)
        return matrix

    # display the matrix
    #  use the __str__ method
    def __repr__(self):
        return self.__str__()

    # display the matrix
    #   "CustomMatrix"
    #   dimensions
    #   top 5 rows and columns if the matrix is large
    #   the whole matrix if the matrix is small
    def __str__(self):
        payload = f"CustomMatrix: {self.matrix.shape}"
        if self.matrix.size > 25:
            payload += ", Top 5 rows and columns:"
            payload += f"\n{self.matrix[:5, :5]}"
        else:
            payload += f"\n{self.matrix}"
        return payload

    # some magical methods
    def __getitem__(self, key):
        return self.matrix[key]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __len__(self):
        return len(self.matrix)

    def __and__(self, other):
        return self._dispatch_to_numpy(other, np.logical_and)

    def __or__(self, other):
        return self._dispatch_to_numpy(other, np.logical_or)

    def __le__(self, other):
        return self._dispatch_to_numpy(other, np.less_equal)

    def __lt__(self, other):
        return self._dispatch_to_numpy(other, np.less)

    def __ge__(self, other):
        return self._dispatch_to_numpy(other, np.greater_equal)

    def __gt__(self, other):
        return self._dispatch_to_numpy(other, np.greater)

    def __eq__(self, other):
        return self._dispatch_to_numpy(other, np.equal)

    # some numpy methods

    def sum(self, axis=None):
        return self.matrix.sum(axis=axis)

    def flatten(self):
        return self.matrix.flatten()

    @property
    def shape(self):
        return self.matrix.shape

    def mean(self, axis=None):
        return self.matrix.mean(axis=axis)

    def std(self, axis=None):
        return self.matrix.std(axis=axis)

    def min(self, axis=None):
        return self.matrix.min(axis=axis)

    def max(self, axis=None):
        return self.matrix.max(axis=axis)

    def median(self, axis=None):
        return np.median(self.matrix, axis=axis)

    def count_nonzero(self, axis=None):
        return np.count_nonzero(self.matrix == 0, axis=axis)

    # some numpy methods that return a CustomMatrix: todo

    # allow adding and subtracting
    def __add__(self, other):
        # return self._dispatch_to_add(other)
        return self._dispatch_to_numpy(other, np.add)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self._dispatch_to_numpy(other, np.subtract)

    def __rsub__(self, other):
        # other - self
        return (-self).__add__(other)

    # unary minus
    def __neg__(self):
        return self._dispatch_to_numpy(-1, np.multiply)

    # despatch various arithmetic operations to numpy
    def _dispatch_to_numpy(self, other, method):
        if isinstance(other, CustomMatrix):
            return self.__class__(method(self.matrix, other.matrix))
        elif isinstance(other, np.ndarray):
            res = method(self.matrix, other)
            return self.__class__(res)
        elif isinstance(other, (int, float)):
            return self.__class__(method(self.matrix, other))
        else:
            raise TypeError(
                f"Cannot operate on a CustomMatrix and a {type(other)} object. "
                "Try converting it to a CustomMatrix first."
            )

    # allow multiplying to a scalar
    def __mul__(self, other):
        return self._dispatch_to_numpy(other, np.multiply)

    def __rmul__(self, other):
        return self.__mul__(other)

    # allow dividing by a scalar
    def __truediv__(self, other):
        return self._dispatch_to_numpy(other, np.divide)


if __name__ == "__main__":
    # if run interactively
    """
    ::

        python3.11
        from custom_matrix import CustomMatrix
        import numpy as np
        import pandas as pd
    """

    # dirty one
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, np.nan]])
    print(CustomMatrix(m))

    # small one
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(CustomMatrix(m))

    # large one
    m = np.random.rand(100, 100)
    print(CustomMatrix(m))

    # initialisation from matrix
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, np.nan]])
    cm2 = CustomMatrix(m)
    assert cm2[0, 0] == 1
    cm2

    # initialisation from dataframe
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, np.nan]])
    df = pd.DataFrame(m)
    cm3 = CustomMatrix.from_dataframe(df)
    assert cm3[0, 0] == 1
    cm3

    # snippet to go from stack of dataframe matrixes to list of CustomMatrix
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, np.nan]])
    df = pd.DataFrame(m)
    df = pd.concat([df, df * 2, df * 3], axis=0)
    dates = pd.date_range("2021-01-01", periods=3)
    # expand the dates by size of the matrixes
    dates_expanded = np.repeat(dates, df.shape[0] / len(dates))
    df["date"] = dates_expanded
    # input
    df
    # list of unique dates
    dates = np.sort(df["date"].unique())
    # list of dataframes, one per date, with date column removed
    df_list = [df[df["date"] == d].copy() for d in dates]
    for d in df_list:
        d.drop("date", axis=1, inplace=True)
    # list of CustomMatrix
    cm_list = [CustomMatrix.from_dataframe(d) for d in df_list]
    for date, cm in zip(dates, cm_list):
        cm.info = date
    # results
    cm_list[0]
    cm_list[1]
    cm_list[2]

    # clean one
    # also as invariant for testing
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    cm = CustomMatrix(m)
    print(cm)
    cm

    # indexing
    assert cm[0, 0] == 1

    # setting and copying
    cm2 = cm.copy()
    cm2[0, 0] = 10

    assert cm2[0, 0] == 10

    # adding and subtracting
    cm2 = cm * 2

    assert (cm + cm2)[0, 0] == 3
    assert (cm - cm2)[0, 0] == -1

    # adding a scalar
    assert (cm + 1)[0, 0] == 2
    assert (2 + cm)[0, 0] == 3

    # multiplying by a scalar
    assert (cm * 2)[0, 0] == 2
    assert (-3 * cm)[0, 0] == -3

    # dividing by a scalar
    assert (cm / 2)[0, 0] == 0.5

    # unary minus
    assert (-cm)[0, 0] == -1

    # average of 3 matrices
    cm2 = CustomMatrix(m) * 2
    cm3 = CustomMatrix(m) - 1
    cm_avg = (cm + cm2 + cm3) / 3

    assert cm_avg[0, 1] == (2 + 4 + 1) / 3

    # sum from a list of matrices
    cm_sum = sum([cm, cm2, cm3])

    assert cm_sum[0, 1] == 2 + 4 + 1

    # adding a numpy array
    m2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) * 2

    assert (cm + m2)[0, 0] == 3

    # type mismatch
    try:
        cm + "a"
    except TypeError as e:
        msg_part = "Cannot operate on a CustomMatrix and a <class 'str'> object."
        if msg_part not in str(e):
            raise e

    # magic methods: len and or le lt etc
    assert len(cm) == 3
    assert cm < 10
    assert cm <= 10
    assert cm > 0
    assert cm >= 0
    assert cm == cm

    # numpy methods: min, max, mean, sum, median
    assert cm.min() == 1
    assert cm.max() == 9
    assert cm.mean() == 5
    assert cm.sum() == 45
    assert cm.median() == 5

    # subclassing
    class CustomMatrix2(CustomMatrix):
        def __init__(self, matrix, info=None):
            super().__init__(matrix)
            self.info = info

        def __str__(self):
            parent_str = super().__str__()
            # replace the class name
            res = parent_str.replace("CustomMatrix", "CustomMatrix2")
            # add the info
            res += f"\n{self.info}"
            return res

        def _combine_potential_infos(self, other):
            # if both are CustomMatrix2 and both have info not none
            if isinstance(other, CustomMatrix2) and (
                self.info is not None
                and hasattr(other, "info")
                and other.info is not None
            ):
                if self.info != other.info:
                    info = None
                else:
                    info = self.info
            else:
                info = self.info
            return info

        # override copy and dispatch
        def __copy__(self):
            return self.__class__(self.matrix, info=self.info)

        def _dispatch_to_numpy(self, other, func):
            info = self._combine_potential_infos(other)
            res = super()._dispatch_to_numpy(other, func)
            return self.__class__(res.matrix, info=info)

        def calculate(self):
            res = self * 2
            return self.__class__(res.matrix, info=self.info)

        def calculate2(self, other):
            if not isinstance(other, CustomMatrix):
                raise TypeError(
                    f"cannot calculate2 with a {type(other)} object. "
                    "Try converting it to a CustomMatrix first."
                )
            res = self * 2 - other
            return self.__class__(res.matrix, info=self.info)

        def calculate3(self, other):
            if not isinstance(other, CustomMatrix):
                raise TypeError(
                    f"cannot calculate3 with a {type(other)} object. "
                    "Try converting it to a CustomMatrix first."
                )
            res = self.matrix * 2 - other.matrix
            return self.__class__(res, info=self.info)

    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    prnt = CustomMatrix(m)
    cm = CustomMatrix2(m, info="cm")
    cm2 = CustomMatrix2(m * 2, info="cm2")
    cm_noinfo = CustomMatrix2(m * 3)

    # print
    print(cm)
    print(cm2)
    print(cm_noinfo)

    # overriding method
    cm + cm2
    cm + cm_noinfo
    cm + prnt
    cm * 2
    cm == 3

    # overriding method with right info
    assert (cm + cm2).info is None
    assert (cm + cm_noinfo).info == "cm"

    # new method
    cm.calculate()

    # new method with binary operator
    cm.calculate2(cm2)
    cm.calculate2(cm_noinfo)
    cm_noinfo.calculate2(prnt)

    # another new mthod with binary operator
    cm.calculate3(cm2)