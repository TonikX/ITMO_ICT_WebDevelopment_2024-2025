class Solution(object):
    def findSubstring(self, s, words):
        """
        :type s: str
        :type words: List[str]
        :rtype: List[int]
        """
        from collections import Counter

        if not s or not words:
            return []

        word_len = len(words[0])
        total_words = len(words)
        word_count = Counter(words)
        n = len(s)

        result = []

        for i in range(word_len):
            left = i
            right = i
            current_count = Counter()
            count = 0

            while right + word_len <= n:
                word = s[right:right + word_len]
                right += word_len

                if word in word_count:
                    current_count[word] += 1
                    count += 1

                    while current_count[word] > word_count[word]:
                        current_count[s[left:left + word_len]] -= 1
                        count -= 1
                        left += word_len

                    if count == total_words:
                        result.append(left)
                else:
                    current_count.clear()
                    count = 0
                    left = right

        return result
