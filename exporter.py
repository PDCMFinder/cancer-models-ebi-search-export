import requests
import json
import gzip
from ftplib import FTP
from datetime import datetime
import argparse

# Define the endpoint and query parameters
COLUMNS_TO_READ = [
    "external_model_id",
    "project_name",
    "provider_name",
    "model_type",
    "histology",
    "search_terms",
    "cancer_system",
    "primary_site",
    "tumour_type",
    "patient_age",
    "patient_sex",
    "markers_with_cna_data",
    "markers_with_mutation_data",
    "markers_with_expression_data",
    "markers_with_biomarker_data",
    "breast_cancer_biomarkers",
    "treatment_list",
]
# Uncomment to export a reduced version to test
# COLUMNS_TO_READ = [
#     "external_model_id",
#     "project_name",
#     "provider_name",
#     "model_type",
#     "histology"
# ]
ENDPOINT = "https://dev.cancermodels.org/api/search_index"
PARAMS = {
    "select": ",".join(COLUMNS_TO_READ),
    "limit": 100,  # Set a limit for pagination
    "offset": 0,
}

# Define the function to process each model
def format_model(model):
    # Convert each model's key-value pairs to the desired format
    fields = []
    for key, value in model.items():
        fields.append({"name": key, "value": value})

    processed_model = {
        "cross_references": [],  # Empty array for now
        "fields": fields,
    }
    return processed_model

# Fetch and process data with pagination
def fetch_and_process_data():
    processed_data = []
    total_count = 0
    while True:
        response = requests.get(ENDPOINT, params=PARAMS)
        response.raise_for_status()
        data = response.json()

        # Process each model in the current batch
        for model in data:
            processed_data.append(format_model(model))

        # Update metadata
        total_count += len(data)

        # Check if there are more results to fetch
        if len(data) < PARAMS["limit"]:
            break
        else:
            PARAMS["offset"] += PARAMS["limit"]

    return processed_data, total_count

# Function to upload the file to FTP
def upload_to_ftp(filename, ftp_host, ftp_user, ftp_pass, ftp_folder):
    with FTP(ftp_host, ftp_user, ftp_pass) as ftp:
        ftp.cwd(ftp_folder)  # Change to the target directory
        with open(filename, 'rb') as file:
            ftp.storbinary(f'STOR {filename}', file)
        print(f"Uploaded {filename} to FTP server in {ftp_folder} directory")

# Main function
def main(ftp_host, ftp_user, ftp_pass, ftp_folder):
    processed_data, total_count = fetch_and_process_data()

    # Add metadata
    result = {
        "entry_count": total_count,
        "name": "CancerModels.Org",
        "release": "v6.4",  # Hardcoded for now
        "release_date": "18-07-2024",  # Hardcoded for now
        "entries": processed_data,
    }

    # Write the result to a JSON file and compress it
    json_filename = "cancerModels_EBISearch.json"
    gz_filename = f"{json_filename}.gz"
    with open(json_filename, "w") as json_file:
        json.dump(result, json_file, indent=4)

    with open(json_filename, "rb") as f_in:
        with gzip.open(gz_filename, "wb") as f_out:
            f_out.writelines(f_in)

    print(f"Processed {total_count} models and saved to {gz_filename}")

    # Upload the compressed file to FTP
    upload_to_ftp(gz_filename, ftp_host, ftp_user, ftp_pass, ftp_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch, process, and upload cancer model data to an FTP server.")
    parser.add_argument("--ftp_host", required=True, help="FTP host")
    parser.add_argument("--ftp_user", required=True, help="FTP user")
    parser.add_argument("--ftp_pass", required=True, help="FTP password")
    parser.add_argument("--ftp_folder", required=True, help="FTP folder to upload files")

    args = parser.parse_args()

    main(args.ftp_host, args.ftp_user, args.ftp_pass, args.ftp_folder)
