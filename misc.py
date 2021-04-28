from shutil import get_terminal_size as get_size

FREE = 2

# terminal's width = shutil.get_terminal_size.columns

def print_align_space(first, last):
    width = get_size().columns
    hangul_count = 0
    for c in first:
        c = c.encode()
        if not c.isascii():
            hangul_count += 1
    space = width - (len(first) + len(last))
    print(' ' * (space - hangul_count - FREE), end='', flush=True)
