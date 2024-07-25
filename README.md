# Cancer Models FTP Uploader

This Python script fetches, processes, and uploads cancer model data to an FTP server. The data is retrieved from an API endpoint, processed into a specific format, and then uploaded as a compressed JSON file to a specified folder on the FTP server.
The resulting JSON file has an structure that allows the EBI Search to index it and show cancer models data in https://www.ebi.ac.uk/ebisearch/.

## Features

- Fetches data from the Cancer Models API.
- Processes and formats the data.
- Compresses the data into a gzip file.
- Uploads the compressed file to a specified directory on an FTP server.

## Requirements

- Python 3.x
- `requests`
- `argparse`
- `gzip`
- `ftplib`

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/cancer-models-ftp-uploader.git
   cd cancer-models-ftp-uploader
   ```

2. Install the required Python packages:
```sh
pip install requests
```

## Usage
```sh
python script_name.py --ftp_host your_ftp_host --ftp_user your_ftp_user --ftp_pass your_ftp_pass --ftp_folder upload/test
```
## Command-Line Arguments
- `--ftp_host`: The FTP host address.
- `--ftp_user`: The FTP username.
- `--ftp_pass`: The FTP password.
- `--ftp_folder`: The FTP folder where the file will be uploaded.