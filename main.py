import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
import dash_table
import pandas as pd

# Create a Dash app
app = dash.Dash(__name__,suppress_callback_exceptions=True)
app.title = 'Reverse DCF'

# Define the layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.A(html.H1('REVERSE DCF', style={'text-align': 'left', 'margin': '0px', 'padding': '50px', 'font-size': '20px', 'color': 'white', 'font-family': 'Nunito Sans'}),
               href='/home'),
        dcc.Dropdown(
            id='dropdown',
            placeholder="PAGES",
            value='/home',  
            style={'margin-top': '20px', 'width': '120px','background-color': '#343a40','color':'black' }  
        )
    ], className='header', style={'background-color': '#343a40', 'display': 'flex', 'flex-direction': 'row','width' : '100%'}),
    html.Div([
        html.P(id='page-content', children="This site provides interactive tools to valuate and analyze stocks through Reverse DCF model. Check the navigation bar for more.",
               style={'text-align': 'left', 'font-size': '1.5em', 'margin-top': '20px'}),
    ], className='subheading'),
], style={'font-family': 'Nunito Sans','padding': '0px','margin-top':'-10px','margin-left':'-10px','margin-right':'-10px','display':'border-box'})  # Apply style to the whole webpage


valuation_layout = html.Div([
    html.H3('VALUING CONSISTENT COMPOUNDERS'),
    html.P('Hi there!'),
    html.P('This page will help you calculate intrinsic PE of consistent compounders through growth-RoCE DCF model.'),
    html.P('We then compare this with current PE of the stock to calculate degree of overvaluation.'),
    html.Label('NSE/BSE symbol'), html.Br(),
    dcc.Input(id='symbol-input', type='text', value='NESTLEIND'),
    html.Br(),  
    # html.Label('Cost of Capital (CoC): %', className='form-label'),  # Fixed the label syntax
    html.Br(),
    html.Div(id='stock-pe-output')  # Output div for stock P/E
])

# Define callback to fetch and display stock P/E
@app.callback(
    Output('stock-pe-output', 'children'),
    [Input('symbol-input', 'value')]
)
def update_stock_pe(symbol):
    url = f"https://www.screener.in/company/{symbol}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize variables to store values
    stock_pe = ""
    market_cap = ""
    roce_values = []

    # Find all list items containing information
    list_items = soup.find_all('li', class_='flex flex-space-between')
    for li in list_items:
        name_span = li.find('span', class_='name')
        if name_span:
            name = name_span.get_text(strip=True)
            value_span = li.find('span', class_='number')
            if value_span:
                value = value_span.get_text(strip=True)
                if "Stock P/E" in name:
                    stock_pe = value
                elif "Current Price" in name:
                    current_price = value
                elif "Market Cap" in name:
                    market_cap = value

    # Convert market_cap and current_price to numeric values
    try:
        market_cap = float(market_cap.replace('₹', '').replace(',', '')) if market_cap else None
        current_price = float(current_price.replace('₹', '').replace(',', '')) if current_price else None
    except ValueError:
        market_cap = None
        current_price = None

    FY23PE = round(market_cap / current_price, 1) if market_cap and current_price != 0 else None

    # Find the table containing the RoCE values
    section_ratios = soup.find('section', id='ratios')
    if section_ratios:
        table = section_ratios.find('table', class_='data-table')
        for row in table.find_all('tr'):
            if "ROCE %" in row.text:
                cells = row.find_all('td')
                roce_values.extend([float(cell.text.strip('%')) for cell in cells[1:6] if cell.text.strip('%')])

    # Calculate the median RoCE
    median_roce = round(sorted(roce_values)[len(roce_values) // 2]) if roce_values else None

    # Find the tables with class 'ranges-table' and create table components
    sales_growth_data = []
    profit_growth_data = []
    years = [10, 5, 3, 'TTM']  # List of years extracted from the table

    tables = soup.find_all('table', class_='ranges-table')
    for table in tables:
        title = table.find('th').text.strip()
        if title in ["Compounded Sales Growth", "Compounded Profit Growth"]:
            rows = table.find_all('tr')
            # Create heading row with years
            # years_row = rows[0]
            # years = [cell.text.strip() for cell in years_row.find_all('td')]
            # Iterate through remaining rows and extract growth data
            for row in rows[1:]:
                cells = row.find_all('td')
                if len(cells) == 2:
                    growth_values = [cell.text.strip() for cell in cells]
                    if '%' in growth_values[1]:  # Check if the value contains '%'
                        growth_value = growth_values[1].replace('%', '')  # Remove '%' sign
                    else:
                        growth_value = growth_values[1]
                    if title == "Compounded Sales Growth":
                        sales_growth_data.append(growth_value)
                    elif title == "Compounded Profit Growth":
                        profit_growth_data.append(growth_value)

    # Convert growth data to appropriate numeric format if needed
    sales_growth_data = [float(value) for value in sales_growth_data]
    profit_growth_data = [float(value) for value in profit_growth_data]

    # Ensure the length of years matches the length of growth data
    # years = years[:len(sales_growth_data)]  # or years[:len(profit_growth_data)] (assuming both have the same length)

    # Printing extracted data for verification
    print("Years:", years)
    print("Sales Growth Data:", sales_growth_data)
    print("Profit Growth Data:", profit_growth_data)


    # sales_growth_data = [...]  # Sales growth data for each year
    # profit_growth_data = [...]  # Profit growth data for each year
    years = [10,5,3,'TTM']  # List of years
    df = pd.DataFrame({'Year': years, 'Sales Growth': sales_growth_data, 'Profit Growth': profit_growth_data})

    # Create bar chart for sales growth
    fig_sales_growth = go.Figure()
    fig_sales_growth.add_trace(go.Bar(x=df['Sales Growth'], y=df['Year'], orientation='h'))
    fig_sales_growth.update_layout(title='Sales Growth Over Years', xaxis_title='Sales Growth', yaxis_title='Year')

    # Create bar chart for profit growth
    fig_profit_growth = go.Figure()
    fig_profit_growth.add_trace(go.Bar(x=df['Profit Growth'], y=df['Year'], orientation='h'))
    fig_profit_growth.update_layout(title='Profit Growth Over Years', xaxis_title='Profit Growth', yaxis_title='Year')

    # Define table data
    data = {'Year': years, 'Sales Growth': sales_growth_data, 'Profit Growth': profit_growth_data}

    # Build the output HTML
    output_html = html.Div([
        html.Span(f'Stock Symbol: {symbol}'), html.Br(),
        html.Span(f'Current PE: {stock_pe if stock_pe else "N/A"}'), html.Br(),
        html.Span(f'FY23PE: {FY23PE if FY23PE else "N/A"}'), html.Br(),
        html.Span(f'5-year median RoCE (excluding FY23): {median_roce if median_roce else "N/A"}%'), html.Br(),
        html.Div([
            dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in data.keys()],
        data=[{col: data[col][i] for col in data.keys()} for i in range(len(years))],
        style_table={'height': '300px', 'overflowY': 'auto'})]), 
        html.Div([
            html.Div(dcc.Graph(figure=fig_sales_growth), style={'flex': '50%'}),
            html.Div(dcc.Graph(figure=fig_profit_growth), style={'flex': '50%'}),
        ], style={'display': 'flex'}),
    ], id='stock-pe-output')

    return output_html
            
def update_output(value):
    return f'Value: {value}'

# Define callback to update page content based on URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def update_page_content(pathname):
    if pathname == '/home':
        return "This site provides interactive tools to valuate and analyze stocks through Reverse DCF model. Check the navigation bar for more."
    elif pathname == '/val':
        return valuation_layout
    else:
        return "Page not found"

# Define callback to update dropdown options based on selection
@app.callback(
    Output('dropdown', 'options'),
    [Input('dropdown', 'value')]
)
def update_dropdown_options(selected_value):
    options = [
        {'label': 'Home', 'value': '/home'},
        {'label': 'DCF Valuation', 'value': '/val'}
    ]
    if selected_value in [option['value'] for option in options]:
        options = [option for option in options if option['value'] != selected_value]
    return options

# Define callback to update URL based on dropdown selection
@app.callback(
    Output('url', 'pathname'),
    [Input('dropdown', 'value')]
)
def update_url(value):
    return value

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
