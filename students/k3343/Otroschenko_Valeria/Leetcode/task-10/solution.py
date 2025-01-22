class Solution(object):
    def totalNQueens(self, n):
        """
        :type n: int
        :rtype: int
        """
        def backtrack(row, diagonals, anti_diagonals, cols):
            if row == n:
                return 1

            count = 0
            for col in range(n):
                curr_diag = row - col
                curr_anti_diag = row + col

                if col in cols or curr_diag in diagonals or curr_anti_diag in anti_diagonals:
                    continue

                cols.add(col)
                diagonals.add(curr_diag)
                anti_diagonals.add(curr_anti_diag)

                count += backtrack(row + 1, diagonals, anti_diagonals, cols)

                cols.remove(col)
                diagonals.remove(curr_diag)
                anti_diagonals.remove(curr_anti_diag)

            return count

        return backtrack(0, set(), set(), set())
