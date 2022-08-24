import argparse
import sys

VERSION_FILE = 'version'


def load_version() -> list[int]:
    v = load_version_string().split('.')
    return list(map(lambda x: int(x), v))


def load_version_string() -> str:
    with open(VERSION_FILE, 'r') as file:
        v = file.read()
    return v


def save_version(v: list[int]):
    with open(VERSION_FILE, 'w') as file:
        file.write('.'.join(list(map(lambda x: str(x), v))))


def increase(v: list[int], level: int) -> list[int]:
    v[level] += 1
    return v


def main(args: list[str]):
    parser = argparse.ArgumentParser(prog='Version Increaser')
    parser.add_argument('-l', '--level', type=int, help='Level to upgrade (0 for major, etc.)', default=None)
    parser.add_argument('-i', '--initialize', type=int, help='Depth of the version size.', default=None)
    parser.add_argument('--build', action='store_true', help='Automatically increase the last number of the version')
    args = parser.parse_args(args)

    if args.initialize is not None:
        save_version([0 for _ in range(args.initialize)])

    if args.level is not None:
        version = load_version()
        save_version(increase(version, args.level))

    if args.build:
        version = load_version()
        save_version(increase(version, len(version) - 1))


if __name__ == '__main__':
    main(sys.argv[1:])
