class Solution(object):
    def solveNQueens(self, n):
        """
        :type n: int
        :rtype: List[List[str]]
        """
        def backtrack(row, diagonals, anti_diagonals, cols, board, solutions):
            if row == n:
                solutions.append(["".join(r) for r in board])
                return

            for col in range(n):
                curr_diag = row - col
                curr_anti_diag = row + col

                if col in cols or curr_diag in diagonals or curr_anti_diag in anti_diagonals:
                    continue

                board[row][col] = 'Q'
                cols.add(col)
                diagonals.add(curr_diag)
                anti_diagonals.add(curr_anti_diag)

                backtrack(row + 1, diagonals, anti_diagonals, cols, board, solutions)

                board[row][col] = '.'
                cols.remove(col)
                diagonals.remove(curr_diag)
                anti_diagonals.remove(curr_anti_diag)

        solutions = []
        board = [["." for _ in range(n)] for _ in range(n)]
        backtrack(0, set(), set(), set(), board, solutions)
        return solutions