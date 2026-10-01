# Google Doc Message Decoder
A simple python script that extracts a hidden 2D textgraphic from a published Google Doc table containing character coordinates, and prints the decoded uppercase message to the console

## Feautures
* Fetches  document content live using 'requests'.
* Parses table cells using 'Beautifulsoup'.
* Automatically handles dynamic grid sizes and space buffering.

## Installation

Install the required depedencies using pip:
'''bash
pip install requests beautifulsoup
'''

## Usage
Import the function and passnit to the published Google Doc URL:
'''python
from decoder import decode_secret_message
url = "https://google.com"
decode_secret_message(url)
'''

## How it works
1. **Scrapes Table:** Downloads the HTML structure from the provided link.
2. **Maps Coordinates:** Loops through each data row to read '(x,y)' numeric layout and characters.
3. **Prints Grid:** Detaermines the maximum dimensions and draws the graphic row-by-row fro top to bottom.