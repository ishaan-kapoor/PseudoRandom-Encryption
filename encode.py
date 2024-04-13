"""
`python encode.py -h` for help message
It encodes a given message (or contents of a given file) and provides a python code to extract the original message
It uses python random module and XOR (^) operator to encode the message
"""

from random import Random
from typing import Any


def encode(
    message: str,
    seed: Any = 0,
    size_seed: int = 2,
    char_range: int = 256,
    garbage_seed: Any = None,
) -> str:
    """\
    Encodes the given message
    The feild 'seed' is the seed for randomisation.
    The feild 'size_seed' determines how large to make the encoded string
        The encoded message is "roughly" 'size_seed' times the length of actual message
    The feild 'char_range' determines the range of unicode characters to be used for encoded the message
    The feild 'garbage_seed' is the seed for garbage values.
        If you intend to get the same encoded message again pass same value to this feild.
    NOTE: The same 'seed', 'size_seed' and 'char_range' values are required for decoding
    """
    temp = Random(garbage_seed)
    determined = Random(seed)
    result = ""
    i = 0
    n = len(message)
    while i < n:
        char = message[i]
        if not determined.randrange(size_seed):
            i += 1
            result += chr(determined.randrange(char_range) ^ ord(char))
        else:
            result += chr(temp.randrange(char_range))
    return result.encode().hex().upper()


def validate(
    seed: Any = 0,
    size_seed: int = 2,
    char_range: int = 256,
) -> tuple[Any, int, int]:
    """
    Validate the values passed by the user
    If seed is None, then the encryption will not be consistent and the algorithm will fail
    """
    if seed is None: seed = 0
    size_seed = max(size_seed, 1)
    if char_range < 1: char_range = 256
    return seed, size_seed, char_range


def decode(
    encoded: str,
    seed: Any = 0,
    size_seed: int = 2,
    char_range: int = 256,
) -> str:
    """\
    Decodes the encoded message based on the given parameters
    Please use the same values of 'seed', 'size_seed' and 'char_range' as used while encoding
    """
    determined = Random(seed)
    # return "".join((chr(determined.randrange(char_range) ^ ord(char)) for char in bytes.fromhex(encoded).decode() if not determined.randrange(size_seed)))
    message = ""
    for char in bytes.fromhex(encoded).decode():
        if not determined.randrange(size_seed):
            message += chr(determined.randrange(char_range) ^ ord(char))
    return message


def give_code(encoded_message: str, seed: Any, size_seed: int, char_range: int) -> str:
    """\
    This function gives the python code that can be used to decode the message based on given parameters
    """
    return f"""import random; random.seed({seed!r}); m = {encoded_message!r}
print(''.join((chr(random.randrange({char_range})^ord(c))for c in bytes.fromhex(m).decode()if not random.randrange({size_seed}))))
"""


def give_values(encoded_message: str, seed: Any, size_seed: int, char_range: int) -> str:
    return f"message:\t{encoded_message}\nseed:\t\t{seed}\nsize seed:\t{size_seed}\nchar range:\t{char_range}"


def get_input():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "arg",
        type=str,
        default="",
        help="The text to be encoded, or the path of the file if -f flag is set",
    )
    parser.add_argument(
        "--file",
        "-f",
        action="store_true",
        default=False,
        help="If the argument is a file",
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
        "-r",
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
    parser.add_argument(
        "--values-only",
        "-vo",
        default=False,
        action="store_true",
        help="Give values only, not the entire code",
    )
    return parser.parse_args()


def _extract_message(args) -> str | int:
    if args.file:
        try:
            with open(args.arg) as f:
                message = f.read()
        except FileNotFoundError:
            print("File does not exist")
            return -1
    else:
        message = args.arg
    return message if message else -1


def _extract_keys(args):
    seed, size_seed, char_range = validate(args.seed, args.size, args.char_range)
    try: garbage_seed = args.garbage
    except: garbage_seed = None
    return seed, size_seed, char_range, garbage_seed


def run(args):
    message = _extract_message(args)
    if message == -1:  # file does not exist or empty file
        print("No message to encode")
        return

    # keys = (seed, size_seed, char_range)
    *keys, garbage_seed = _extract_keys(args)
    encoded_message = encode(message, *keys, garbage_seed)

    output_tuple = (encoded_message, *keys)
    output = (
        give_values(*output_tuple) if args.values_only else give_code(*output_tuple)
    )
    if args.output:
        try:
            with open(args.output, "w") as f:
                f.write(output)
        except Exception as err:
            print(f"Error occured while writing to file: {err}")
    else:
        print(f"\n{output}")


if __name__ == "__main__":
    run(get_input())
