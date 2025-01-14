from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 0
        for x in nums:
            if k < 2 or x != nums[k - 2]:
                nums[k] = x
                k += 1
        return k


solution = Solution()

my_list = [1, 1, 1, 2, 2, 3]

new_length = solution.removeDuplicates(my_list)
print(new_length)