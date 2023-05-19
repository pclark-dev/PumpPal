# PumpPal

PumpPal is a web application that uses machine learning alongside the U.S. Energy Information Administration's API to predict gas prices up to a year in advance on a weekly basis.

## Features

- Select a city and gas type to get the current gas price and predicted prices.
- View the gas price data on a map with corresponding pins.
- Explore the predicted gas prices for different dates.
- Get insights into the project and its dependencies.

## Technologies Used

- Python
- Flask
- Pandas
- Prophet
- HTML
- CSS
- JavaScript
- Leaflet

## Installation

1. Clone the repository:

git clone https://github.com/pclark-dev/PumpPal.git


2. Install the required dependencies:

pip install -r requirements.txt

3. Run the Flask application:

python app.py

4. Open a web browser and navigate to `http://localhost:5000` to access PumpPal.

## Usage

- Select a city from the dropdown menu to choose the location.
- Select a gas type from the dropdown menu to choose the gasoline type.
- Click the "Go" button to retrieve the current gas price and predicted prices.
- The current gas price, predicted prices, and map will be displayed on the right side of the page.
- Scroll down to see the predicted gas prices for different dates.

## Contributing

Contributions to PumpPal are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
