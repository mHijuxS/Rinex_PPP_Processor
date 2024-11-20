# Rinex-PPP-Processor
A Python script that automates the submission of RINEX files to the IBGE (Instituto Brasileiro de Geografia e Estatística) online platform for Precise Point Positioning (PPP) processing. The script handles file upload, processing, and downloading of the processed results.

## Features
- Uploads RINEX files to the IBGE PPP processing service.
- Automatically downloads the processed file once available.
- User-friendly and efficient script for geodetic data processing.

## Requirements
Python 3.7 or later
### Required Python libraries:
- requests
- os
- re
- argparse

You can install the required libraries using pip:

```bash
pip install requests os re argparse
```

# Usage
Clone the repository to your local machine:
```bash
git clone https://github.com/your-username/rinex-ppp-processor.git
cd rinex-ppp-processor
```
Run the script with the following command:

```bash
python rinex_ppp_processor.py <rinex_file>
```
Replace <rinex_file> with the name of your RINEX file.

## The script will:
- Upload the file to the IBGE PPP service.
- Wait for the processing to complete.
- Download the processed result to your directory.

## Example
```bash
python rinex_ppp_processor.py example.21o test@example.com
```
