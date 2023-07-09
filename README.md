# Web Socket Fuzzer (wsfuzz)

wsfuzz is a command-line tool written in Python for carrying out various types of attacks, such as XSS, SQLi, LFI, and command injection, on WebSocket endpoints. It allows users to specify the target WebSocket URL, the payload to use, and the encoding scheme for the payloads.

## Prerequisites

- Python 3.x
- Dependencies: `base64`, `argparse`, `urllib`, `colorama`, `progressbar`

## Installation

1. Clone the wsfuzz repository:

```shell
$ git clone https://github.com/username/wsfuzz.git
$ cd wsfuzz
```

2. Install the required dependencies using pip:

```shell
$ pip install -r requirements.txt
```

## Usage

The general syntax to run wsfuzz is as follows:

```shell
$ python wsfuzz.py {attack_name} -t {target_url} -r {payload_example_string} -p {payload_file} -e {encoding_method}
```

Here's an example of running different attacks:

- XSS attack:

```shell
$ python wsfuzz.py xss -t ws://example.com/reflected-xss -r "*" -p payloads/xss.txt -e normal
```

- SQLi attack:

```shell
$ python wsfuzz.py sqli -t ws://example.com/authenticate-user -r '{"auth_user":"*","auth_pass":""}' -p payloads/custom_sqli.txt -e base64
```

- Command injection attack:

```shell
$ python wsfuzz.py cmdi -t ws://example.com/command-execution -r "127.0.0.1*" -p payloads/cmdi.txt -e normal
```

- LFI attack:

```shell
$ python wsfuzz.py lfi -t ws://example.com/file-inclusion -r "*" -p payloads/lfi.txt -e normal
```

Note: Replace the `{attack_name}`, `{target_url}`, and other parameters with the appropriate values.

## Command-line Arguments

- `-t`, `--target`: Specifies the target WebSocket URL.
- `-r`, `--request`: Specifies the format of an example request, e.g., `{'auth_user':'*','auth_pass':'*'}`.
- `-p`, `--payload`: Specifies the payload file to use.
- `-e`, `--encode`: Specifies the encoding scheme to use. Available options are `none`, `base64`, `hex`, and `url`.

## Response Analysis

wsfuzz performs checks on the response received from the server to determine the success or failure of an attack. The following criteria are evaluated:

- If the payload is found in the response, it's considered a success.
- If any predefined keywords are found in the response, it's considered a success.
- If the response is empty or contains only whitespace, it's considered a failure.
- If any error-related keywords are found in the response, it's considered a failure.


## Exiting

To terminate the execution of wsfuzz, press `Ctrl+C`. This will trigger a KeyboardInterrupt, and the program will exit gracefully. Otherwise, wsfuzz will exit at the end of its execution.

## Contributions

Contributions to wsfuzz are welcome! If you find any issues or have suggestions for improvements, please feel free to create a pull request or submit an issue on the [GitHub repository](https://github.com/username/wsfuzz).

## License

wsfuzz is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the [LICENSE](LICENSE) file for more details.
