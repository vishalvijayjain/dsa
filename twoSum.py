class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        count = {}
        for i, num in enumerate(nums):
            if target - num in count:
                return [count[target - num], i]
            count[num] = i
    
sol = Solution()
print(sol.twoSum([4,5,6], 10))
