# WebSocket Fuzzer

WebSocket Fuzzer is a Python script that enables you to perform various types of attacks, such as XSS, SQL injection, command injection, and file inclusion, on WebSocket-based web applications. The script allows you to customize the target URL, payload, encoding scheme, and other parameters.

## Installation

1. Clone the repository or download the `wsfuzz.py` script.
2. Install the required dependencies by running the following command:

```shell
pip install -r requirements.txt
```

## Usage

The script can be executed using the following command:

```shell
python wsfuzz.py <attack> [options]
```

Replace `<attack>` with the type of attack you want to carry out (`xss`, `sqli`, `cmdi`, or `lfi`).

### Attack Options

The available options depend on the attack type. Here are the common options:

- `-t`, `--target`: Specify the target WebSocket URL. Default values are provided for each attack, but you can customize it as needed.
- `-r`, `--request`: Specify the format of an example request. Use curly braces `{}` to represent dynamic parts that will be replaced by payloads. Default values are provided for each attack, but you can customize it as needed.
- `-p`, `--payload`: Specify the payload file to use. Default payload files are provided for each attack, but you can provide your own.
- `-e`, `--encode`: Specify the encoding scheme to use for payloads. Choose from `none`, `base64`, `hex`, or `url`. Default is `none`.

### Examples

Here are some examples of how to use the script:

1. XSS attack:

```shell
python wsfuzz.py xss -t ws://example.com/xss -r "*" -p payloads/default/xss.txt -e none
```

2. SQL injection attack:

```shell
python wsfuzz.py sqli -t ws://example.com/authenticate-user -r '{"auth_user":"*","auth_pass":""}' -p payloads/default/sqli.txt -e base64
```

3. Command injection attack:

```shell
python wsfuzz.py cmdi -t ws://example.com/command-execution -r "127.0.0.1*" -p payloads/default/cmdi.txt -e none
```

4. File inclusion attack:

```shell
python wsfuzz.py lfi -t ws://example.com/file-inclusion -r "*" -p payloads/default/lfi.txt -e none
```

## Customization

You can customize the target URL and payloads by modifying the default values provided in the script. Refer to the respective attack sections in the script to make the necessary changes.

## Credits

This script utilizes the `wsHandler` module for WebSocket communication and the `progressbar` module for progress visualization.

## Disclaimer

Use this script responsibly and only on web applications for which you have proper authorization. Do not misuse or perform illegal activities with this script.
If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request on the GitHub repository.
