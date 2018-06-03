import matplotlib.pyplot as plt
import numpy as np

'''
Naive implementation of BWT taken from Wikipedia
https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform#Sample_implementation
'''
def bwt(s):
    """Apply Burrows-Wheeler transform to input string."""
    assert "\002" not in s and "\003" not in s, "Input string cannot contain STX and ETX characters"
    s = "\002" + s + "\003"  # Add start and end of text marker
    table = sorted(s[i:] + s[:i] for i in range(len(s)))  # Table of rotations of string
    last_column = [row[-1:] for row in table]  # Last characters of each row
    return "".join(last_column)  # Convert list of characters into string

def loadText(filename):
    with open(filename, 'r') as myfile:
        data = myfile.read()
    return data

def countConsecutive(s, graphname, imgname):
    counts = [0]*2
    count = 1
    for i in range(1,len(s)):
        if s[i-1] == s[i]:
            count += 1
            while len(counts) <= count:
                counts.append(0)
        else:
            counts[count] += 1
            count = 1
    plt.bar(range(len(counts)), counts, log=True)
    plt.xlabel('Length of run of consecutive characters')
    plt.ylabel('Number of (log) occurences')
    plt.title(graphname)
    plt.savefig(imgname + '.png')
    plt.clf()


def moveToFront(s):
    Y = sorted(list(set(s)))
    Y_sort = Y
    codedText = list()
    rank = 0
    for c in s:
        rank = Y.index(str(c))
        codedText += [rank]
        Y.pop(rank)
        Y.insert(0, c)

    Y = Y_sort
    return codedText, Y

def normOfMoveToFront(s):
    code, Y = moveToFront(s)
    code = np.array(code)
    norm = np.linalg.norm(code)
    num_zeros = code.size - np.count_nonzero(code)
    percent_zero = 1.0 * num_zeros / code.size
    return norm, percent_zero

def main():
    for title, text in [('Green Eggs and Ham', 'green_eggs_and_ham'), ('Constitution', 'const')]:
        filename = './sample_texts/' + text + '.txt'
        S = loadText(filename)
        countConsecutive(S, '%s pre-transform' % title, '%s_pre' % text)
        pre_norm, pre_percent_zero = normOfMoveToFront(S)
        L = bwt(S)
        countConsecutive(L, '%s post-transform' % title, '%s_post' % text)
        post_norm, post_percent_zero = normOfMoveToFront(L)
        print '%s stats:' % title
        print 'Norm differences:'
        print '%f to %f, ratio of %f' % (pre_norm, post_norm, 1.0*pre_norm / post_norm)
        print 'Percent Zero differences:'
        print '%f to %f' % (pre_percent_zero, post_percent_zero)
        print '\n'


if __name__ == '__main__':
    main()
