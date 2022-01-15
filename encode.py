"""
This script is a command line utility which takes the folllowing arguments:
    -h, --help        show this help message and exit
    -f, --file        Specify a text file whose contents are to be encoded
    -m, --msg         The text to be encoded
    -s, --seed        The seed for encoding [default:random]
    -z, --size        The size_seed for encoding [default:2]
                          It determines how large to make the encoded string.
                          The encoded message is "roughly" 'size_seed' times the length of actual message
    -c, --char_range  The range of unicode characters to be used for encoded the message [default:256]
    -o, --output      Specify a text file where the output code will be saved
    -g, --garbage     Seed for garbage values
It encodes a given message (or contents of a given file) and provides a python code to extract the original message
It uses python random module and XOR (^) operator to encode the message
"""


from random import Random
from typing import Any


def encode(
    message: str = "",
    seed: Any = 0,
    size_seed: int = 2,
    char_range: int = 256,
    garbage_seed: Any = None,
) -> tuple[str, Any, int, int]:
    """\
    This function encodes the given message
    The feild 'seed' is the seed for randomisation.
    The feild 'size_seed' determines how large to make the encoded string
        The encoded message is "roughly" 'size_seed' times the length of actual message
    The feild 'char_range' determines the range of unicode characters to be used for encoded the message
        NOTE: The same 'seed', 'size_seed' and 'char_range' has to be used while decoding
        P.S. Yes I do take care of that by default
    The feild 'garbage_seed' is the seed for garbage values.
        If you intend to get the same encoded message again pass same value to this feild.
    """
    if seed is None:
        seed = 0
    temp = Random(garbage_seed)
    determined = Random(seed)
    result = ""
    i = 0
    n = len(message)
    if size_seed < 2:
        size_seed = 2
    while i < n:
        char = message[i]
        if not determined.randrange(size_seed):
            i += 1
            result += chr(determined.randrange(char_range) ^ ord(char))
        else:
            result += chr(temp.randrange(char_range))
    return result.encode().hex().upper(), seed, size_seed, char_range


def decode(
    encoded: str = "",
    seed: Any = 0,
    size_seed: int = 2,
    char_range: int = 256,
) -> str:
    """\
    Decodes the encoded message based on the given parameters
    """
    determined = Random(seed)
    # return "".join((chr(determined.randrange(char_range) ^ ord(char)) for char in bytes.fromhex(encoded).decode() if not determined.randrange(size_seed)))
    message = ""
    for char in bytes.fromhex(encoded).decode():
        if not determined.randrange(size_seed):
            message += chr(determined.randrange(char_range) ^ ord(char))
    return message


def give_code(
    code: str = "",
    seed: Any = 0,
    size_seed: int = 2,
    char_range: int = 256,
) -> str:
    """\
    This function gives the python code that can be used to decode the message based on given parameters
    """
    return f"""\
import random
random.seed({seed!r})
m = {code!r}
print(''.join((chr(random.randrange({char_range})^ord(c))for c in bytes.fromhex(m).decode()if not random.randrange({size_seed}))))
"""


def get_input():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        default="",
        help="Specify a text file whose contents are to be encoded",
    )
    parser.add_argument(
        "--msg",
        "-m",
        type=str,
        default="",
        help="The text to be encoded",
    )
    parser.add_argument(
        "--seed",
        "-s",
        default=f"{Random().random()}"[3:],
        help="The seed for encoding [default:random]",
    )
    parser.add_argument(
        "--size",
        "-z",
        default=2,
        type=int,
        help="The size_seed for encoding [default:2]\nIt determines how large to make the encoded string.\n\tThe encoded message is \"roughly\" 'size_seed' times the length of actual message",
    )
    parser.add_argument(
        "--char_range",
        "-c",
        type=int,
        default="256",
        help="The range of unicode characters to be used for encoded the message [default:256]",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="",
        help="Specify a text file where the output code will be saved",
    )
    parser.add_argument(
        "--garbage",
        "-g",
        default=None,
        help="Seed for garbage values",
    )
    return parser.parse_args()


def main(args):
    message = ""
    if args.msg:
        message = args.msg
    else:
        if args.file:
            try:
                with open(args.file) as f:
                    message = f.read()
            except FileNotFoundError:
                print("File does not exist")
                exit()
        else:
            print("No Arguments Given")
            exit()

    temp = give_code(
        *encode(
            message=message,
            seed=args.seed,
            size_seed=args.size_seed,
            char_range=args.char_range,
            garbage_seed=args.garbage_seed,
        )
    )
    if args.output:
        with open(args.output, "w") as f:
            f.write(temp)
    else:
        print("\n\n", temp, sep="\n")


if __name__ == "__main__":
    main(get_input())
