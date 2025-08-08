# Stock-Dashboard-250702
# Stock Dashboard

This project retrieves Taiwan Stock Exchange (TWSE) data via API, stores it as JSON, and visualizes market performance in an interactive treemap.

## Features
- **Data downloader** – `stockData_load.ipynb` calls the TWSE API and writes timestamped `twse_data_*.json` files using APScheduler.
- **Treemap dashboard** – `stockTWtreemap.ipynb` reads the generated JSON file and serves a Dash web app (default port `8051`) displaying a Plotly treemap colored by price changes.

## Project Structure
```
README.md                Project overview and usage guide
stockData_load.ipynb     Fetches TWSE data and saves JSON
stockTWtreemap.ipynb     Builds Dash treemap from saved JSON
stock_data.csv           (Optional) sample CSV created by the downloader
.gitignore               Ignores generated JSON data
```

## Requirements
- Python 3.8+
- `requests`
- `pandas`
- `apscheduler`
- `plotly`
- `dash`

Install packages with:
```bash
pip install requests pandas apscheduler plotly dash
```

## Usage
1. **Download data**
   - Launch Jupyter Notebook and open `stockData_load.ipynb`.
   - Run all cells to fetch the latest TWSE data.
   - A timestamped JSON file (`twse_data_*.json`) will be created. A CSV file (`stock_data.csv`) may also be exported for reference.

2. **Visualize data**
   - Open `stockTWtreemap.ipynb` in Jupyter Notebook.
   - Run all cells. The notebook loads the newest JSON file and starts a Dash server.
   - Visit `http://127.0.0.1:8051` in a browser to interact with the treemap.

## Notes
- JSON files are ignored by Git (see `.gitignore`). Remove the pattern if you wish to version data files.
- Notebooks are ideal for experimentation. For production use, consider refactoring into Python modules with a proper dependency file and documentation.

## License
This repository is provided as-is without any specific license. Use at your own discretion.
