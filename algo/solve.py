from collections import defaultdict


def solve(wordList, target):
    word_list = defaultdict(int)
    for word in wordList:
        word_list[word] += 1

    for idx in range(len(target)):
        first, second = (target[:idx], target[idx:])
        if word_list[first] > 0:
            word_list[first] -= 1
            if word_list[second] > 0:
                return (first, second)
            word_list[first] += 1
    else:
        return None

# * edit test case here


wordList = ["ab", "ab"]
target = "abab"

if __name__ == "__main__":
    print(solve(wordList, target))
