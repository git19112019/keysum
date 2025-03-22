# keysum

A Python script for processing and summarizing text from PDF files or URLs. This script extracts keywords, Subject-Verb-Object (SVO) structures, and creates a keyword map to help understand the main topics.

## Features

- Extracts text from PDF files and HTML URLs.
- Preprocesses text to remove stop words.
- Extracts Subject-Verb-Object (SVO) structures from the text.
- Extracts keywords based on frequency.
- Creates a keyword map showing relationships between keywords and SVOs.
- Summarizes the main topics of the text.

## Installation

To install and set up this project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/git19112019/keysum.git
    ```

2. Navigate to the project directory:
    ```bash
    cd keysum
    ```

3. Install the required dependencies:
    ```bash
    pip install spacy PyPDF2 requests beautifulsoup4
    ```

4. Download the SpaCy language model:
    ```bash
    python -m spacy download en_core_web_sm
    ```

## Usage

To use this project, follow these instructions:

1. Run the Python script `keysum.py` with the path to a PDF file or a URL as an argument:
    ```bash
    python keysum.py <file_path_or_url>
    ```

2. The script will process the text and display:
    - The prominent keywords and their frequencies.
    - The Subject-Verb-Object (SVO) structures found in the text.
    - A summary of the main topics discussed in the text.
    - A keyword map showing the relationships between keywords and SVOs.

### Examples

1. Process a local PDF file:
    ```bash
    python keysum.py /path/to/your/file.pdf
    ```

2. Process a PDF file from a URL:
    ```bash
    python keysum.py http://example.com/yourfile.pdf
    ```

3. Process an HTML URL:
    ```bash
    python keysum.py http://example.com/yourpage.html
    ```

## Dependencies

This project requires the following dependencies:
- `spacy`
- `PyPDF2`
- `requests`
- `beautifulsoup4`

Make sure to install these dependencies using `pip`.

## Example Output

Here is an example of the output you might get when running the script:
