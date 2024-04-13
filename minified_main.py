from argparse import ArgumentParser
from random import Random

defaults = {
    "seed": 0,
    "size_multiplier": 2,
    "char_range": 128,
    "garbage_seed": None,
    "hex": False
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
    for arg in args: params[arg] = params.get(arg, defaults[arg])


def _validate(params: dict) -> None:
    args = ("seed", "size_multiplier", "char_range")
    _load_defaults(params, *args)
    if params["seed"] is None: params["seed"] = defaults["seed"]
    if params["size_multiplier"] < 1: params["size_multiplier"] = defaults["size_multiplier"]
    if params["char_range"] < 1: params["char_range"] = defaults["char_range"]


def encrypt(message: str, **params) -> str:
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
    args = ("seed", "size_multiplier", "char_range")
    _load_defaults(params, *args)
    size_multiplier = params["size_multiplier"]
    char_range = params["char_range"]
    determined = Random(params["seed"])
    message = ""
    for char in encrypted_message:
        if not determined.randrange(size_multiplier):
            message += chr(determined.randrange(char_range) ^ char)
    return message


def give_code(encrypted_message: str, **params) -> str:
    args = ("seed", "size_multiplier", "char_range", "hex")
    _load_defaults(params, *args)
    m = "bytes.fromhex(m).decode()" if params["hex"] else "m"
    return f"""from random import randrange, seed; seed({params["seed"]!r}); m = {encrypted_message!r}
print(''.join((chr(randrange({params.get("char_range")})^ord(c))for c in {m} if not randrange({params.get("size_multiplier")}))),end='')"""


def give_values(encrypted_message: str, **params) -> str:
    args = ("seed", "size_multiplier", "char_range", "hex")
    _load_defaults(params, *args)
    return f"message:\t{encrypted_message!r}\nseed:\t\t{params['seed']!r}\nsize seed:\t{params['size_multiplier']}\nchar range:\t{params['char_range']}\nhex encoded:\t{params['hex']}"


def get_input() -> dict:
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
    if params["file"]:
        try:
            with open(params["arg"], "r") as f:
                message = f.read()
        except FileNotFoundError:
            print("File does not exist")
            return -1
    else: message = params["arg"]
    return message if message else -1


def run(params: dict) -> None:
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
