def solve(nums):
    if len(nums) == 0:
        return 0
    if len(nums) == 1:
        return nums[0]
    max_sum = min(nums)
    # make a window, and move it
    for window_length in range(1, len(nums) + 1):
        for start in range(len(nums) - window_length + 1):
            new_sum = sum(nums[start : window_length + start])
            max_sum = max(new_sum, max_sum)

    return max_sum


assert solve([1]) == 1
assert solve([5, 4, -1, 7, 8]) == 23, solve([5, 4, -1, 7, 8])
assert solve([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6, solve(
    [-2, 1, -3, 4, -1, 2, 1, -5, 4]
)


def solve(nums):
    best_sum = nums[0]
    current_sum = 0
    for num in nums:
        current_sum = max(num, current_sum + num)
        best_sum = max(current_sum, best_sum)
    return best_sum


assert solve([1]) == 1
assert solve([5, 4, -1, 7, 8]) == 23, solve([5, 4, -1, 7, 8])
assert solve([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6, solve(
    [-2, 1, -3, 4, -1, 2, 1, -5, 4]
)


def solve(s):
    opening_parens = {"(", "{", "["}
    closing_parens = {")": "(", "}": "{", "]": "["}
    open_parens = []
    for c in s:
        if c in opening_parens:
            open_parens.append(c)
        if c in closing_parens:
            try:
                last_open = open_parens.pop()
            except IndexError:
                return False
            if last_open == closing_parens[c]:
                continue
            else:
                return False
    if open_parens:
        return False
    return True


assert solve("()[]{}")
assert not solve("((")
assert solve("(foo{bar[baz]})[]{}")
assert solve("(foo({bar[baz]})[]{})")
assert not solve("(foo{bar[baz})[]{}")
assert not solve(")kda")


# 8
def solve(nums, target):
    current_sum = 0
    for i in range(len(nums)):
        for j in range(1, len(nums)):
            if i == j:
                continue
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


assert solve([2, 7, 11, 15], target=9) == [0, 1]
assert solve([3, 9, -1, 5], target=14) == [1, 3]
assert solve([1, 2, 3, 4], 8) == []


# 8
def solve(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return []


assert solve([2, 7, 11, 15], target=9) == [0, 1]
assert solve([3, 9, -1, 5], target=14) == [1, 3]
assert solve([1, 2, 3, 4], 8) == []


# 9 sliding window maximum
def solve(nums, k):
    max_nums = []
    for i in range(len(nums) - k + 1):
        max_nums.append(max(nums[i : i + k]))
    return max_nums


assert solve([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7], solve(
    [1, 3, -1, -3, 5, 3, 6, 7], 3
)


# 9 According to Won, there's an O(n) solution...
# (This one is O(kn))
def solve(nums, k):
    from collections import deque

    window = deque()
    window_max = nums[0]
    window_max_idx = 0  # the index in the window that has the current maximum
    for i in range(k):
        # compute the max in the first window, don't use `max` so we can get the index
        window.append(nums[i])
        if nums[i] > window_max:
            window_max = nums[i]
            window_max_idx = i

    max_nums = [window_max]

    for i in range(k, len(nums)):
        current_num = nums[i]
        window.popleft()
        window.append(current_num)
        window_max_idx -= 1
        if window_max_idx < 0:
            # we popped off the maximum number in the window, we need to find the new max:
            window_max = window[0]
            window_max_idx = 0
            for i in range(1, k):
                if window[i] >= window_max:
                    window_max = window[i]
                    window_max_idx = i
        if current_num >= window_max:
            window_max = current_num
            window_max_idx = k - 1
        max_nums.append(window_max)
    return max_nums


assert solve([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7], solve(
    [1, 3, -1, -3, 5, 3, 6, 7], 3
)
assert solve([9, 8, 7, 6, 5, 4, 3], 3) == [9, 8, 7, 6, 5], solve(
    [9, 8, 7, 6, 5, 4, 3], 3
)


# 10
def solve(nums):
    snums = sorted(set(num for num in nums if num > 0))
    for i, num in enumerate(snums):
        if i + 1 != num:
            return i + 1
    return len(snums) + 1


assert solve([3, 4, -1, 1]) == 2, solve([3, 4, -1, 1])
