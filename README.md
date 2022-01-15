# Python_MessageEncoder
This simple script creates an encoded message that can be decoded with a code sample the script provides
## Usage
```
usage: encode.py [-h] [--file FILE] [--msg MSG] [--seed SEED] [--size SIZE] [--char_range CHAR_RANGE] [--output OUTPUT] [--garbage GARBAGE]

options:
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
```
##Example
```
python encode.py -m message -c 256 -g garbage_seed
python encode.py -f file -s seed -c 256 -z 3 -o out.py
```
