# Reverse DCF Dashboard

This project is a Dash application that provides interactive tools to valuate and analyze stocks through the Reverse DCF model. It allows users to fetch and display stock data, calculate intrinsic PE ratios, and visualize sales and profit growth over the years.

## Features

- **Interactive Dashboard:** A user-friendly interface to navigate and interact with the tool.
- **Stock Data Fetching:** Automatically fetches stock data such as P/E ratios, market cap, and RoCE values.
- **Growth Visualization:** Displays sales and profit growth over different periods using interactive charts.
- **DCF Valuation:** Helps users calculate the intrinsic value of consistent compounders through a growth-RoCE DCF model.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/reverse-dcf.git
   cd reverse-dcf
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Dash app:**
   ```bash
   python app.py
   ```

4. **Open your web browser and navigate to:**
   ```
   http://127.0.0.1:8050/
   ```

## File Structure

- `app.py`: Main application file that contains the Dash app and its callbacks.
- `requirements.txt`: A file listing the necessary Python packages.

## Usage

The application has the following main components:

### Header

- **Title:** Displays the title "REVERSE DCF".
- **Navigation Dropdown:** Allows users to navigate between different pages.

### Pages

#### Home Page

Displays a brief introduction to the site and its functionality.

#### DCF Valuation Page

- **Input Field:** Users can enter the NSE/BSE stock symbol to fetch the stock data.
- **Stock Data Display:** Shows the current P/E, FY23 P/E, and 5-year median RoCE.
- **Growth Charts:** Visualizes sales and profit growth over different periods.
- **Data Table:** Displays the sales and profit growth data in a tabular format.

## Callback Functions

### `update_stock_pe(symbol)`

Fetches stock data from Screener.in, parses the HTML to extract necessary values such as P/E, market cap, RoCE, sales growth, and profit growth. It then calculates the FY23 P/E and median RoCE and returns a structured HTML output.

### `update_page_content(pathname)`

Updates the page content based on the current URL pathname. Returns the layout for the home page or the DCF valuation page.

### `update_dropdown_options(selected_value)`

Updates the dropdown options based on the current selection to avoid displaying the currently selected page in the dropdown.

### `update_url(value)`

Updates the URL pathname based on the dropdown selection.

## Dependencies

- Dash
- Plotly
- Requests
- BeautifulSoup4
- Pandas

## License

This project is licensed under the MIT License.

## Author

- **Your Name**
- [Your Email](mailto:preet2828chandak@gmail.com)
- [GitHub Profile](https://github.com/Preet-Chandak)

Feel free to contribute to this project by opening issues or submitting pull requests. Your feedback and contributions are welcome!
