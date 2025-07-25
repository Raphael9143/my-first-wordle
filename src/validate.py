def validate(word, answer):
    if (word == answer):
        return [1] * 5
    res = [-1, -1, -1, -1, -1]
    for i in range(5):
        if answer[i] == word[i]:
            res[i] = 1
        else:
            for j in range(5):
                if word[j] == answer[i] and j != i and res[j] == -1:
                    res[j] = 0
                    break
          
    return res

