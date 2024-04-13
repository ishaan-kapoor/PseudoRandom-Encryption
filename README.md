# Pseudo-Random Encryption
This script provides Python functions for symmetric encryption and decryption using pseudo-random number generation.

By default, the script takes in a message to encrypt and prints 2 lines of python code to `stdout`,
which when executed will give back the original message. e.g. `python main.py ishaan` outputs the following
```python
from random import randrange, seed; seed('5822100138856949'); m = 'b\x04v\x1b\x16\x05\x03\x00a\x00\x0e@4P'
print(''.join((chr(randrange(128)^ord(c))for c in m if not randrange(2))),end='')
```
The script also offers modularity, allowing each function to be used independently as needed.

The key in this encryption system is a tuple of 3 values: `seed`, `size_multiplier` and `char_range`.
They are interpreted as:
- `seed`: main `seed` value for encryption, passed to python's random library as is.
- `size_multiplier`: size multiplier for encrypted message. i.e. $\frac{\text{length of encrypted message}}{\text{length of original message}} \approx \text{size multiplier}$
- `char_range`: unicode character range for each `char` of encrypted message. Does not impose any limitation on character range of original message.

## Usage
<details>
<summary>Try: <code>python main.py -h</code> for help message and usage instructions.</summary>
<pre>
usage: Pseudo-Random Encryptor [-h] [--hex] [--file] [--decrypt] [--values-only] [--seed SEED] [--size SIZE] [--char-range CHAR_RANGE]
                               [--output OUTPUT] [--garbage GARBAGE]
                               arg

positional arguments:
  arg                   The text to be encrypted, or the path of the file if -f flag is set.

options:
  -h, --help            show this help message and exit
  --hex, -x             [default:False] Indicates that the encrypted message is to be hex encoded. (or the message is to be decoded from
                        hex, if -d is set)
  --file, -f            [default:False] Indicate that the given argument is a file path insead of string.
  --decrypt, -d         [default:False] Indicate that the message is to be decrypted, not encrypted.
  --values-only, -vo    [default:False] Give key values and encrypted message only, not the entire code (Ignored if -d flag is set).
  --seed SEED, -s SEED  [default:random] The seed for encrypting/decrypting. Passed to random library as seed.
  --size SIZE, -z SIZE  [default:2] Approximately equal to len(encrypted) / len(original).
  --char-range CHAR_RANGE, -r CHAR_RANGE
                        [default:128] Unicode character range of the encrypted message (Does not limit the original message).
  --output OUTPUT, -o OUTPUT
                        [default:stdout] Specify a text file where the output code/values will be saved.
  --garbage GARBAGE, -g GARBAGE
                        [default:random] Seed for garbage values which randomize encrypted text.
</pre>
</summary>
</details>

## Functionality
### Encrypting a Message
The `encrypt` function takes a message and encrypts it based on specified parameters, including:
- Seed: Main key for encryption, passed to the random library as a seed.
- Size Multiplier: Factor determining the size of the encrypted message.
- Character Range: Unicode character range of the encrypted message.
- Garbage Seed: Seed for randomizing the output.
- Hex Encoding: Indicates whether the output should be hex encoded.

### Decrypting an Encrypted Message
The `decrypt` function decrypts an encrypted message based on given parameters, including:
- Seed: Main key for decryption, passed to the random library as a seed.
- Size Multiplier: Factor determining the size of the original message.
- Character Range: Unicode character range of the encrypted message.

### Generating Python Code for Decryption
The `give_code` function generates Python code to decrypt a message based on specified parameters, including:
- Seed: Main key for decryption, passed to the random library as a seed.
- Size Multiplier: Factor determining the size of the original message.
- Character Range: Unicode character range of the encrypted message.
- Hex Encoding: Indicates whether the encrypted message is hex encoded.

### Generating Key Values for Decryption
The `give_values` function generates a formatted string containing encrypted message and key values for decryption, including:

- Seed: Main key for decryption, passed to the random library as a seed.
- Size Multiplier: Factor determining the size of the original message.
- Character Range: Unicode character range of the encrypted message.
- Hex Encoding: Indicates whether the output message is hex encoded.

### Input Handling
The `get_input` function sets up an argument parser and returns parsed arguments in dictionary form.

### Main Functionality
The `run` function serves as the main entry point, handling the encryption, decryption, and output functionalities based on user inputs and parameters.

## Examples

1. With no flags
```sh
$ python main.py message
```
```python
from random import randrange, seed; seed('13234983975254888'); m = '2LA2\x01D\x1e\x0eQ8y\x1eB\x1d+r>\x16'
print(''.join((chr(randrange(128)^ord(c))for c in m if not randrange(2))),end='')
```
2. Get only the encoded message and key values
```sh
$ python main.py message --values-only
```
```text
message:        "\x17\rk#\\/\r\x1b\x01$)\x1fC='("
seed:           '5008982697256702'
size seed:      2
char range:     128
hex encoded:    False
```
3. Write to an output file
```sh
$ python main.py "secret message" -o output.py
$ python output.py
```
```text
secret message
```
4. Read from file
```sh
$ python main.py -f input.txt -o output.py
$ python output.py > decoded.txt
$ diff decoded.txt input.txt
```
```sh
# no diff
```
5. Specify a size multiplier
```sh
$ python main.py "secret" --seed 0 --size 5 -vo -g 0
```
```text
message:        'U2N5|^0\x0e>\x1cO\x03\x1cjM@\x1d|ddf+\\'
seed:           '0'
size seed:      5
char range:     128
hex encoded:    False
```
```sh
$ python main.py "secret" --seed 0 --size 1 -vo -g 0
```
```text
message:        'g9su\x057'
seed:           '0'
size seed:      1
char range:     128
hex encoded:    False
```
6. Specifying garbage seed
```sh
$ python main.py "secret" --seed 0 -vo -g 0
```
```text
message:        '-2$ud\x12&\x1a'
seed:           '0'
size seed:      2
char range:     128
hex encoded:    False
```
```sh
$ python main.py "secret" --seed 0 -vo -g 1
```
```text
message:        '\x1e2Bud\x12&\x1a'
seed:           '0'
size seed:      2
char range:     128
hex encoded:    False
```
7. Decrypting an Encrypted Message
```text
message:        '}/xf\x01-'
seed:           '0'
size seed:      1
char range:     128
hex encoded:    False
```
```sh
$ python main.py -d '}/xf\x01-' -s 0 -z 1
```
```text
ishaan
```
8. Using hex values
```sh
$ python main.py 'ishaan' -vo -s 0 -z 1 -x
```
```text
message:        '7D2F7866012D'
seed:           '0'
size seed:      1
char range:     128
hex encoded:    True
```
```sh
$ python main.py -d '7D2F7866012D' -vo -s 0 -z 1 -x
```
```text
ishaan
```
9. Customizing character range
```sh
$ python main.py "secret" --seed 0 --char-range 1024 -vo
```
```text
message:        'ͱɾϧâ]ͱɿ̃'
seed:           '0'
size seed:      2
char range:     1024
hex encoded:    False
```
10. Decrypting a file
```sh
$ python main.py -d /path/to/file.enc -vo -s 0 -z 1 -o /path/to/file.dec
$ cat /path/to/file.dec
```
```text
super secret text in file
```
