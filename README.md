# xoscraper

A simple web-scraping utility for extracting business information from xo.gr and exporting it to a CSV file.

## How It Works

1. Go to https://www.xo.gr and search for the topic you want (for example: doctors, plumbers, lawyers, etc.).

2. Open your browser's Developer Tools and inspect the search results page.

3. Locate the container with:

   <div class="row listResults">

4. Copy all elements inside this div and paste them into a file named:

   data.txt

5. Run the script:

   python app.py

6. The program will parse the data and generate a CSV file containing the extracted fields:

   - Clinic Name
   - Street Address
   - City
   - Postal Code
   - Phone 1
   - Phone 2
   - Website

## Output

A structured CSV file ready for use.
