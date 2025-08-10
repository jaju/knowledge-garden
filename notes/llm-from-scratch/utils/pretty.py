from tabulate import tabulate

def print_kv_table(kv_pairs):
    print(tabulate(kv_pairs, tablefmt='fancy_grid', maxcolwidths=[None, 80]))
