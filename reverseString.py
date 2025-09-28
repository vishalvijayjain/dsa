"""
You are given an array of characters which represent a string s. Write a function which reverses a string.
In place.
"""

# def reverseString(s: list[str]) -> None:
#     s = s[::-1]
#     print(s)

#     return

# reverseString("neet")

# This approach is not right because strings are immutable, hence slicing doesn't do a in place reverse
# instead, a new obj is created in memory.
# either use s.reverse() [because s is a list here, hence that works], or two pointers, like below

def reverseString(s:list[str]) -> None:
    l,r = 0, len(s) - 1
    while l<r:
        s[l], s[r] = s[r], s[l]
        l += 1
        r -= 1
    
    return

