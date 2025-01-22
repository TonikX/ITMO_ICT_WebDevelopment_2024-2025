class Solution(object):
    def fullJustify(self, words, maxWidth):
        """
        :type words: List[str]
        :type maxWidth: int
        :rtype: List[str]
        """
        result = []
        line = []
        line_length = 0

        for word in words:
            if line_length + len(word) + len(line) > maxWidth:
                for i in range(maxWidth - line_length):
                    line[i % (len(line) - 1 or 1)] += ' '
                result.append(''.join(line))
                line, line_length = [], 0

            line.append(word)
            line_length += len(word)

        result.append(' '.join(line).ljust(maxWidth))
        return result
