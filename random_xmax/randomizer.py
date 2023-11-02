from random import shuffle


def has_self_mapping(mapping: list[int]) -> bool:
    for i in range(len(mapping)):
        if mapping[i] == i:
            return True
    return False


def create_random_mapping(N: int) -> list[int]:
    if N == 1:
        return None
    if N == 2:
        return [1, 0]

    x = list(range(N))
    shuffle(x)
    while has_self_mapping(x):
        shuffle(x)

    return x
