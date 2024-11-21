import requests
import re
import argparse
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

failed_files = []

def process_file(file_path, email):
    file_name = os.path.basename(file_path)
    url = "https://www.ibge.gov.br/ppp/ppp_new.php"
    initial_url = "https://www.ibge.gov.br/geociencias/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=processar-os-dados"

    retries = 3
    while retries > 0:
        try:
            # Check file size before making the request
#            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
#            if file_size_mb <= 0 or file_size_mb >= 20:
#                print(f"File {file_name} does not meet size requirements (must be >0 and <20 MB).")
#                return

            # Create a new session for each file
            session = requests.Session()

            # Perform an initial GET request to grab the cookies
            initial_response = session.get(initial_url, timeout=30)
            if initial_response.status_code != 200:
                raise Exception(f"Failed to fetch initial page for {file_name}: {initial_response.status_code}")

            print(f"Session established for {file_name}")

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
            with open(file_path, "rb") as file_content:
                files = {
                    "arquivo": (file_name, file_content, "application/octet-stream"),
                }

                # Send the POST request
                response = session.post(url, headers=headers, data=data, files=files, timeout=120)

                if response.status_code != 200:
                    raise Exception(f"Failed to upload {file_name}: {response.status_code}")

                print(f"File {file_name} uploaded successfully.")

                # Check if the response contains the file size error
                if "O arquivo deve ter tamanho diferente de zero e ser menor que 20 MB." in response.text:
                    print(f"Error: File {file_name} does not meet size requirements on the server.")
                    return

                # Extract the download link from the response
                pattern = r"onclick=\"window\.open\('([^']+)'"
                match = re.search(pattern, response.text)

                if not match:
                    raise Exception(f"Failed to find download link for {file_name}.")

                download_link = match.group(1)

                # Download the processed file
                download_response = session.get(download_link, timeout=60)
                if download_response.status_code == 200:
                    output_file = f"{file_name}_ppp.zip"
                    with open(output_file, 'wb') as f:
                        f.write(download_response.content)
                    print(f"Processed file for {file_name} downloaded as {output_file}.")
                    return  # Exit the function on success
                else:
                    raise Exception(f"Failed to download the processed file for {file_name}: {download_response.status_code}")

        except Exception as e:
            retries -= 1
            print(f"Error processing {file_name}: {e}. Retries left: {retries}")
            time.sleep(5)  # Delay before retry

    print(f"Failed to process {file_name} after multiple retries.")
    failed_files.append(file_name)

def main(file_paths, email):
    # Check if email is valid (basic validation)
    if "@" not in email or "." not in email.split("@")[-1]:
        print("Invalid email address. Please provide a valid email.")
        return

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(process_file, file_path, email): file_path for file_path in file_paths}

        for future in as_completed(futures):
            file_path = futures[future]
            try:
                future.result()  # This will raise any exception encountered
            except Exception as e:
                print(f"Error with file {file_path}: {e}")

    if failed_files:
        print("\nThe following files could not be downloaded:")
        for failed_file in failed_files:
            print(f" - {failed_file}")
    else:
        print("\nAll files were processed successfully.")


if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Upload RINEX files for IBGE PPP processing.")
    parser.add_argument("file_paths", nargs='+', help="Paths to the files you want to upload (space-separated).")
    parser.add_argument("email", help="Your email address.")
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.file_paths, args.email)

