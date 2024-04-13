"""
`python main.py -h` for help message
Uses python random module and XOR operation to encrypt/decrypt
The script is modular and each function can be used independently
"""

from argparse import ArgumentParser
from random import Random

defaults = {
    "seed": 0,
    "size_multiplier": 2,
    "char_range": 128,
    "garbage_seed": None,
    "hex": False,  # When hex is True, encrypted message is outputted longer than multiplier because multiple hex characters correspond to a single character
}


help_messages = {
    "arg": "The text to be encrypted, or the path of the file if -f flag is set.",
    "file": "[default:False] Indicate that the given argument is a file path insead of string.",
    "decrypt": "[default:False] Indicate that the message is to be decrypted, not encrypted.",
    "output": "[default:stdout] Specify a text file where the output code/values will be saved.",
    "hex": "[default:False] Indicates that the encrypted message is to be hex encoded. (or the message is to be decoded from hex, if -d is set)",
    "seed": "[default:random] The seed for encrypting/decrypting. Passed to random library as seed.",
    "size": "[default:2] Approximately equal to len(encrypted) / len(original).",
    "char range": "[default:128] Unicode character range of the encrypted message (Does not limit the original message).",
    "garbage seed": "[default:random] Seed for garbage values which randomize encrypted text.",
    "values only": "[default:False] Give key values and encrypted message only, not the entire code (Ignored if -d flag is set).",
}


def _load_defaults(params: dict, *args: str) -> None:
    """\
    Load default values of given args into params

    Args:
        params (dict): The dictionary to load defaults into
        args (str): The arguments to load defaults of

    Returns:
        None: makes changes in params itself
    """
    for arg in args:
        params[arg] = params.get(arg, defaults[arg])


def _validate(params: dict) -> None:
    """
    Validate the values passed by the user (as params)

    Args:
        seed (Any): If value is None, the system fails
        size_multiplier (int): Min value is 1
        char_range (int): Min value is 1

    Returns:
        None: makes changes in params itself
    """
    args = ("seed", "size_multiplier", "char_range")
    _load_defaults(params, *args)

    if params["seed"] is None:
        params["seed"] = defaults["seed"]
    if params["size_multiplier"] < 1:
        params["size_multiplier"] = defaults["size_multiplier"]
    if params["char_range"] < 1:
        params["char_range"] = defaults["char_range"]


def encrypt(message: str, **params) -> str:
    """\
    Encrypts the given message based on given parameters

    Args:
        message (str): The string to encrypt
        seed (Any): Main key for encryption, passed to random library as seed
        size_multiplier (int): Factor of how large the encrypted message should be
        char_range (int): Unicode character range of the encrypted message, does not limit the input message
        garbage_seed (Any): Seed for randomizing the output, to replicate an output, use the same value
        hex (bool): If the output should be hex encoded

    Returns:
        str: The encrypted message

    NOTE: Ensure to use the same 'seed', 'size_multiplier', and 'char_range' values as used for decoding
    """

    args = ("seed", "size_multiplier", "char_range", "garbage_seed", "hex")
    _load_defaults(params, *args)

    temp = Random(params["garbage_seed"])
    determined = Random(params["seed"])
    result = ""
    size_multiplier = params["size_multiplier"]
    char_range = params["char_range"]
    i = 0
    n = len(message)
    while i < n:
        char = message[i]
        if not determined.randrange(size_multiplier):
            i += 1
            result += chr(determined.randrange(char_range) ^ ord(char))
        else:
            result += chr(temp.randrange(char_range))
    if params.get("hex"):
        result = result.encode().hex().upper()
    return result


def decrypt(encrypted_message: str, **params) -> str:
    """\
    Decrypts the encrypted message based on the given parameters

    Args:
        encrypted_message (str): The encrypted message to be decrypted
        seed (Any): Main key for decryption, passed to random library as seed
        size_multiplier (int): Factor of how small the original message is
        char_range (int): Unicode character range of the encrypted message

    Returns:
        str: The decrypted message

    NOTE: Ensure to use the same 'seed', 'size_multiplier', and 'char_range' values as used while encoding.
    """

    args = ("seed", "size_multiplier", "char_range")
    _load_defaults(params, *args)

    determined = Random(params["seed"])

    size_multiplier = params["size_multiplier"]
    char_range = params["char_range"]
    message = ""
    for char in encrypted_message:
        if not determined.randrange(size_multiplier):
            message += chr(determined.randrange(char_range) ^ char)

    return message


def give_code(encrypted_message: str, **params) -> str:
    """\
    Generates Python code to decrypt the message based on given parameters

    Args:
        encrypted_message (str): The encrypted message
        seed (Any): Main key for decryption, passed to random library as seed
        size_multiplier (int): Factor of how small the original message is
        char_range (int): Unicode character range of the encrypted message
        hex (bool): If the encrypted message is hex encoded

    Returns:
        str: 2 lines of Python code for decoding the message

    NOTE: Ensure to use the same 'seed', 'size_multiplier', and 'char_range' values as used while encoding.
    """
    args = ("seed", "size_multiplier", "char_range", "hex")
    _load_defaults(params, *args)

    m = "bytes.fromhex(m).decode()" if params["hex"] else "m"
    return f"""from random import randrange, seed; seed({params["seed"]!r}); m = {encrypted_message!r}
print(''.join((chr(randrange({params.get("char_range")})^ord(c))for c in {m} if not randrange({params.get("size_multiplier")}))),end='')"""


def give_values(encrypted_message: str, **params) -> str:
    """\
    Generates a formatted string containing encrypted message and key values for decryption

    Args:
        encrypted_message (str): The encrypted message
        seed (Any): Main key for decryption, passed to random library as seed
        size_multiplier (int): Factor of how small the original message is
        char_range (int): Unicode character range of the encrypted message
        hex (bool): Indicates weather the output message is hex encoded 

    Returns:
        str: The formatted string containing key values

    NOTE: Ensure to use the same 'seed', 'size_multiplier', and 'char_range' values as used while encoding.
    """
    args = ("seed", "size_multiplier", "char_range", "hex")
    _load_defaults(params, *args)

    return f"message:\t{encrypted_message!r}\nseed:\t\t{params['seed']!r}\nsize seed:\t{params['size_multiplier']}\nchar range:\t{params['char_range']}\nhex encoded:\t{params['hex']}"


def get_input() -> dict:
    """\
    Set up argument parser and return it

    Returns:
        dict: The parsed arguments in a dictionary form
    """
    parser = ArgumentParser("Pseudo-Random Encryptor")
    parser.add_argument("arg", type=str, help=help_messages["arg"])
    parser.add_argument("--hex", "-x", action="store_true", default=False, help=help_messages["hex"])
    parser.add_argument("--file", "-f", action="store_true", default=False, help=help_messages["file"])
    parser.add_argument("--decrypt", "-d", action="store_true", default=False, help=help_messages["decrypt"])
    parser.add_argument("--values-only", "-vo", action="store_true", default=False, help=help_messages["values only"])
    parser.add_argument("--seed", "-s", default=f"{Random().random()}"[2:], help=help_messages["seed"])
    parser.add_argument("--size", "-z", default=2, type=int, help=help_messages["size"])
    parser.add_argument("--char-range", "-r", type=int, default="128", help=help_messages["char range"])
    parser.add_argument("--output", "-o", type=str, default="", help=help_messages["output"])
    parser.add_argument("--garbage", "-g", default=None, help=help_messages["garbage seed"])
    args = parser.parse_args()
    params = {k:v for k, v in args._get_kwargs()}
    params["size_multiplier"] = args.size
    del params["size"]
    return params


def _extract_message(params: dict) -> str | int:
    """\
    Extracts the original message to be encrypted/decrypted.
    Reads the file if specified.

    Args:
        params (dict): a dictionary of arguments

    Returns:
        str|int: message (str) if it exists, otherwise -1 (int)
    """
    if params["file"]:
        try:
            with open(params["arg"], "r") as f:
                message = f.read()
        except FileNotFoundError:
            print("File does not exist")
            return -1
    else:
        message = params["arg"]
    return message if message else -1


def run(params: dict) -> None:
    """\
    Main function

    Args:
        params (dict): all the arguments passed to the program

    Returns:
        None: Prints or writes output to the file
    """
    message = _extract_message(params)
    if message == -1:  # file does not exist or empty file
        print("No message to encrypt")
        return
    _validate(params)

    if params["decrypt"]:
        message = message.encode().decode("unicode-escape").encode()
        if params["hex"]:
            message = bytes.fromhex(message.decode())
        output = decrypt(message, **params)
    else:
        params["encrypted_message"] = encrypt(message, **params)

        output = give_values(**params) if params["values_only"] else give_code(**params)
    if params["output"]:
        try:
            with open(params["output"], "w") as f:
                f.write(output)
        except Exception as err:
            print(f"Error occured while writing to file: {err}")
    else:
        print(output)


if __name__ == "__main__":
    run(get_input())
