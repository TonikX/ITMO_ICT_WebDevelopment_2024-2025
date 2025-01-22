from collections import Counter

class Solution(object):
    def minWindow(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        if not s or not t:
            return ""

        t_count = Counter(t)
        current_count = {}

        required = len(t_count)
        formed = 0

        l, r = 0, 0
        min_len = float("inf")
        min_window = (0, 0)

        while r < len(s):
            char = s[r]
            current_count[char] = current_count.get(char, 0) + 1

            if char in t_count and current_count[char] == t_count[char]:
                formed += 1

            while l <= r and formed == required:
                char = s[l]

                if r - l + 1 < min_len:
                    min_len = r - l + 1
                    min_window = (l, r)

                current_count[char] -= 1
                if char in t_count and current_count[char] < t_count[char]:
                    formed -= 1

                l += 1

            r += 1

        l, r = min_window
        return s[l:r+1] if min_len != float("inf") else ""
