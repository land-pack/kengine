import random


def custom(seq, scale=100):
    checking_seq = sum(seq)
    assert checking_seq == 1
    seq = [int(i * scale) for i in seq]
    seq_hash = {i: seq[i] for i in range(len(seq))}
    seq_list = [[k] * v for k, v in seq_hash.items()]
    all_seq = sum(seq_list, [])
    ret = random.choice(all_seq)
    return ret


if __name__ == '__main__':
    d = [1, 0, 0, 0]
    print custom(d)
    d = [0.7, 0.3, 0, 0]
    print custom(d)
