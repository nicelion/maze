# get_high_scores.py
#
# By Ian Thompson
# Computer Programming


def get_high_scores():
    with open('high_scores.txt', 'r') as f:
        words = f.read().splitlines()
        first = words[0]
        second = words[1]
        third = words[2]

    return [first, second, third]
def formatted_scores():
    with open('high_scores.txt', 'r') as f:
        words = f.read().splitlines()
        first = words[0]
        second = words[1]
        third = words[2]

        first = first[4:]
        second = second[4:]
        third = third[4:]

    return [first, second, third]

scores = get_high_scores()
formatted_scores = formatted_scores()



print(formatted_scores)


