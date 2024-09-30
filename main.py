import os
import shutil
import sys
import glob
from pathlib import Path
from itertools import islice, chain


def tree(root_paths, level: int = -1, length_limit: int = 1000):
    files = 0
    directories = 0
    space = '    '
    branch = '│   '
    tee = '├── '
    last = '└── '

    def file_gen(root: Path, prefix: str = '', level=-1):
        nonlocal files
        if not level:
            return
        remove_prefix = "\033[1;31mRemove\033[0m F: "
        if prefix == '':
            yield remove_prefix + str(root)
        else:
            yield remove_prefix + prefix + root.name
        files += 1

    def link_gen(root: Path, prefix: str = '', level=-1):
        nonlocal files
        if not level:
            return
        remove_prefix = "\033[1;31mRemove\033[0m L: "
        if prefix == '':
            yield remove_prefix + str(root)
        else:
            yield remove_prefix + prefix + root.name
        files += 1

    def mount_gen(root: Path, prefix: str = '', level=-1):
        nonlocal files
        if not level:
            return
        remove_prefix = "\033[1;31mRemove\033[0m M: "
        if prefix == '':
            yield remove_prefix + str(root)
        else:
            yield remove_prefix + prefix + root.name
        files += 1

    def dir_gen(root: Path, prefix: str = '', level=-1):
        nonlocal directories
        if not level:
            return
        remove_prefix = "\033[1;31mRemove\033[0m \033[1;34mD\033[0m: "
        if prefix == '':
            yield remove_prefix + "\033[1;34m{}\033[0m/".format(str(root))
        else:
            yield remove_prefix + prefix + "\033[1;34m{}\033[0m/".format(root.name)
        directories += 1

    def iter_dir(root: Path, prefix: str = '', level=-1):
        nonlocal files, directories
        if not level:
            return  # 0, stop iterating
        contents = list(root.iterdir())
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_mount():
                yield from mount_gen(path, prefix=prefix + pointer, level=level)
            elif path.is_symlink():
                yield from link_gen(path, prefix=prefix + pointer, level=level)
            elif path.is_dir():
                yield from dir_gen(path, prefix=prefix + pointer, level=level)
                extension = branch if pointer == tee else space
                yield from iter_dir(path, prefix=prefix + extension, level=level - 1)
            else:
                yield from file_gen(path, prefix=prefix + pointer, level=level)

    iterator = None
    for root_path in root_paths:
        if root_path.is_mount():
            temp_iter = mount_gen(root_path, level=level)
        elif root_path.is_symlink():
            temp_iter = link_gen(root_path, level=level)
        elif root_path.is_dir():
            temp_iter = dir_gen(root_path, level=level)
            temp_iter = chain(temp_iter, iter_dir(root_path, level=level))
        else:
            temp_iter = file_gen(root_path, level=level)
        iterator = chain(iterator, temp_iter) if iterator else temp_iter

    for line in islice(iterator, length_limit):
        print(line)
    if next(iterator, None):
        print(f'... length_limit, {length_limit}, reached, counted:')
    print(f'\n{directories} directories' + (f', {files} files' if files else ''))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py [path1] [path2] ...")
        sys.exit(1)

    all_paths = []
    for i in range(1, len(sys.argv)):
        # parse regex
        paths = glob.glob(sys.argv[i])
        paths = [Path(p) for p in paths]
        all_paths.extend(paths)

    if not all_paths:
        print("No file or directory found.")
        sys.exit(1)

    # print(all_paths)

    tree(all_paths, level=-1, length_limit=1000)

    # prompt user to confirm, and auto enter
    while True:
        try:
            s = input("Are you sure to remove these files and dirs? (y/n): ")
        except KeyboardInterrupt:
            print()
            sys.exit(0)
        if s == "y" or s == "Y" or s == "":
            break
        elif s == "n" or s == "N":
            sys.exit(0)
        else:
            pass
    # remove
    for path in all_paths:
        if os.path.ismount(path):
            try:
                os.system("umount {}".format(path))
            except:
                print("Failed to unmount", path)
        elif os.path.islink(path):
            try:
                os.unlink(path)
            except:
                print("Failed to remove link", path)
        elif os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except:
                print("Failed to remove dir", path)
        else:
            try:
                os.remove(path)
            except:
                print("Failed to remove file", path)
