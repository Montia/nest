import os

def test_lab(lab, filename):
    score = 8
    log = 'lab{}: {}'.format(lab, os.path.join(os.getcwd(), filename))
    return score, log
