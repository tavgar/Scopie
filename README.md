# README
## Overview
This script is designed to update a list of subdomains to match a specified scope configuration. It filters the provided list of subdomains based on the hosts in the scope file and checks if the subdomains are alive by attempting to resolve the hostname to an IP address and connecting to the IP address on port 80 (HTTP) and 443 (HTTPS). The resulting list of alive subdomains is written to an output file.

## Prerequisites
- Python 3.5 or higher
- argparse library
- json library
- re library

## Usage
The script requires the following arguments to be passed:

--subs: path to a file containing a list of subdomains to check
--scope: path to a JSON file containing the scope configuration
--output: path to the output file to write the list of alive subdomains
--timeout: (optional) timeout for the response in seconds (default: 5)
Example usage:
`python scopie.py --subs subs.txt --scope scope.json --output alive_subs.txt --timeout 10`
## Inputs
## Subdomains File
The --subs argument is used to specify the path to a file containing a list of subdomains to check. Each subdomain should be on a separate line. For example:
```
subdomain1.example.com
subdomain2.example.com
subdomain3.example.com
```
## Scope File
The `--scope` argument is used to specify the path to a JSON file containing the scope configuration. The file should have the following format:
```
{
    "target": {
        "scope": {
            "include": [
                {
                    "host": "example.com"
                },
                {
                    "host": "subdomain1.example.com"
                }
            ]
        }
    }
}
```
The script will extract the hosts from the `include` section and use them to filter the subdomains.

## Output File
The `--output` argument is used to specify the path to the output file to write the list of alive subdomains. If the file already exists, the script will append the new subdomains to the end of the file.

## Outputs
The script will output a list of alive subdomains to the output file in the following format:
```
subdomain1.example.com
subdomain2.example.com
```
## Options
The `--timeout` option is used to specify the timeout for the response in seconds. If not specified, the default timeout of 5 seconds will be used.
