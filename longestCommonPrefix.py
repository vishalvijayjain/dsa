"""
You are given an array of strings strs. Return the longest common prefix of all the strings.

If there is no longest common prefix, return an empty string "".
Input: strs = ["bat","bag","bank","band"]

Output: "ba"

"""
class Solution:
    def lcp(self, strs: list[str])-> list[str]:
        res = ""
        for i in range(len(strs[0])):
            for s in strs:
                if i == len(s) or s[i] != strs[0][i]:
                    return res
            res += strs[0][i]
        return res
    
sol = Solution()
print(sol.lcp(["bat","bag","bank","band"]))
        