"""
You are given an integer array nums and an integer val. 
Your task is to remove all occurrences of val from nums in place
Input: nums = [1,1,2,3,4], val = 1

Output: [2,3,4]
"""

class Solution:
    def re(self, nums: list[int], k: int) -> list[int]:
        res = []
        for num in nums:
            if num != k:
                res.append(num)
        for i in range(len(res)):
            nums[i] = res[i]
        return res
sol = Solution()
print(sol.re([1,1,2,3,4], 1))
