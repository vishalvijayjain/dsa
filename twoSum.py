class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        count = {}
        for i, num in enumerate(nums):
            count[num] = i
            if target - num in count:
                return [count[target - num], count[num]]
        return [0,0]
    
sol = Solution()
print(sol.twoSum([4,5,6], 10))
