import sys
import argparse as ap
import matplotlib.pyplot as plt

def line_to_dict(line, keys):
    vals = line.split(',')
    if len(vals) != len(keys):
        TypeError("the line does not have the same amount of entries as keys")
    for i, val in enumerate(vals):
        vals[i] = int(val)
    return_dict = {}
    for key, val in zip(keys, vals):
        return_dict[key] = val
    return return_dict

def validate_peaks(peak):
    if peak['cycle'] == 0:
        return False
    if peak['timestamp'] == 0:
        return False
    return True

def get_keys_from_file(f):
    keys = f.readline().strip().split(',')
    return keys

def get_file(path):
    f = open(path, 'r')
    keys = get_keys_from_file(f)
    return f, keys

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Program to filter through the\
                               moessbauer Data and hopefully find the\
                               moessbauer dips.')
    parser.add_argument('datapath', help='Path to the file containing\
                        the csv file from the experiment')
    parser.add_argument('-b', '--bins', help='The amount of bins of the\
                        histogram', type=int, default=512)
    parser.add_argument('-lc', '--lowCut', help='define lower threshhold\
                        of the peak height. Used to suppress the noise events',
                        type=int, default=1000000)
    args = parser.parse_args()
    f, keys = get_file(args.datapath)
    preprocessing_pipeline = filter(validate_peaks,
                                    map(lambda p: line_to_dict(p, keys), f))
    main_pipleine = filter(lambda p: p > args.lowCut,
                           map(lambda p: p['peak_height'],
                               preprocessing_pipeline))
    fig, ax = plt.subplots()
    hist, bins, patches = ax.hist(list(main_pipleine), args.bins)
    ax.set_xlabel(r'Peak height $\propto$ Energy')
    ax.set_ylabel(r'Count')
    plt.show()
