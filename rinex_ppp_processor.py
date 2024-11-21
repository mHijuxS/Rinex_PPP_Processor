import requests
import re
import argparse
import os

def main(file_path,email):
# Replace these values with your file path and email
    file_name = os.path.basename(file_path)

    # URL and headers
    url = "https://www.ibge.gov.br/ppp/ppp_new.php"
    initial_url = "https://www.ibge.gov.br/geociencias/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=processar-os-dados"

    # Create a session to manage cookies
    session = requests.Session()

    # Perform an initial GET request to grab the cookies
    initial_response = session.get(initial_url)
    if initial_response.status_code != 200:
        print(f"Failed to fetch initial page: {initial_response.status_code}")
        return

    # Debug: Print the cookies set by the site
    print(f"Getting Session Data")

    headers = {
        "Host": "www.ibge.gov.br",
    }

    # Form data
    data = {
        "MAX_FILE_SIZE": "31457280",
        "chapa": "",
        "processo": "estatico",
        "ant": "Nao alterar RINEX",
        "hant": "0.000",
        "email": email,
        "dlib": "Sim",
    }

    # File payload
    files = {
        "arquivo": (file_name, open(file_path, "rb"), "application/octet-stream"),
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=data, files=files)

    # Print the response
    print(f"Status code: {response.status_code}")

    pattern = r"onclick=\"window\.open\('([^']+)'"
    match = re.search(pattern, response.text)
    download_link=match.group(1)

    response = requests.get(download_link)
    if response.status_code == 200:
        with open(f"{file_name}_ppp.zip", 'wb') as f:
            f.write(response.content)
        print(f"File downloaded and saved as {file_name}_ppp.zip")
    else:
        print(f"Failed to download the file: {response.status_code}")
 


if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Upload a rinex file for IBGE processing.")
    parser.add_argument("file_path", help="The path to the file you want to upload.")
    parser.add_argument("email", help="Your email address.")
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.file_path, args.email)
