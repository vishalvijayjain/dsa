"""
Concatenation of Array:
You are given an integer array nums of length n. 
Create an array ans of length 2n where ans[i]== nums[i] and ans[i+n] == nums[i] for 0<=i<n (0-indexed).

"""
class Solution:
    def concat(self, nums: list[int]) -> list[int]:
        ans = []

        for i in range(2):
            for num in nums:
                ans.append(num)
        return ans

sol = Solution()
print(sol.concat([1,2,3,4]))
