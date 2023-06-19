DigiKala Web Scraper for Mobile Phone Products
This script is a web scraper built specifically for extracting information about mobile phone products from the Digikala website. It utilizes the Digikala API to retrieve data and provides options for selecting brand, sort, and availability preferences. The extracted data is displayed in a table and can be downloaded as an Excel file.

Features
Select a specific brand of mobile phones to scrape data from.
Choose the sorting option for the scraped products (e.g., best-selling, most viewed, newest).
Option to include unavailable products in the scraped data.
Progress bar to track the progress of the scraping process.
Display the extracted data in a table.
Download the extracted data as an Excel file.
Dependencies
Python 3.x
requests
pandas
io
streamlit
PIL
jdatetime
concurrent.futures
Installation:
Install the required dependencies:
pip install -r requirements.txt
Run the script:
python scrape_digikala.py
Open the provided URL in your browser to access the Streamlit web interface.

Select the desired brand, sorting option, and availability preference.

Click on the "شروع استخراج" (Start Extraction) button to initiate the scraping process.

Wait for the scraping to complete and view the extracted data in the table.

Click on the "Download Excel 💾" button to download the extracted data as an Excel file.

Contributing
Contributions are welcome! If you find any issues or want to suggest enhancements, please open an issue or submit a pull request.

License
This project is licensed under the MIT License.

Acknowledgments
This script was developed by Hosssein Qashqaeii . email : qashqaeii.ps4@gmail.com
The script is based on the Digikala website and its API.
