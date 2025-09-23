"""
Given an array nums of size n, return the majority element. 

Input: nums = [5,5,1,1,1,5,5]

Output: 5
"""
from collections import defaultdict
class solution:
    def me (self, nums: list[int])-> int:
        # res ,maxCount = 0, 0
        # count = defaultdict(int)
        # for num in nums:
        #     count[num] += 1
        #     if maxCount < count[num]:
        #         res = num
        #         maxCount = count[num]
        count = defaultdict(int)
        res = maxCount = 0

        for num in nums:
            count[num] += 1
            if maxCount < count[num]:
                res = num
                maxCount = count[num]
        return res
sol = solution()
print(sol.me([2,2,2]))
