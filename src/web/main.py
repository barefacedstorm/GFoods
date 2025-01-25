from monitor.monitor import FoodMonitor
from providers.provider_manager import ProviderManager
from providers.bloomberg_provider import BloombergAgProvider
from processors.processor import DataProcessor
from flask import Flask, render_template, jsonify
import logging
import os
from dotenv import load_dotenv
import threading

# Flask app setup with correct template path
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web', 'templates')
app = Flask(__name__, template_folder=template_dir)

def setup_logging():
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/gfoods.log'),
            logging.StreamHandler()
        ]
    )

def run_flask():
    print(f"Starting Flask server with template directory: {template_dir}")
    print(f"Dashboard template exists: {os.path.exists(os.path.join(template_dir, 'dashboard.html'))}")
    app.run(host='127.0.0.1', port=6000, debug=True, use_reloader=False)

@app.route('/')
async def dashboard():
    try:
        data = await ag_provider.fetch_data()
        print(f"Route '/' accessed, data fetched: {bool(data)}")
        return render_template('dashboard.html', data=data)
    except Exception as e:
        print(f"Route error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/test')
def test():
    return "Flask server is running!"

def main():
    load_dotenv()
    setup_logging()
    logger = logging.getLogger(__name__)

    # Initialize with Bloomberg provider
    global ag_provider
    provider_manager = ProviderManager()
    ag_provider = BloombergAgProvider()
    provider_manager.add_provider(ag_provider)

    data_processor = DataProcessor()
    monitor = FoodMonitor(provider_manager, data_processor)

    # Start web server thread
    web_thread = threading.Thread(target=run_flask)
    web_thread.start()

    logger.info("Starting GFoods monitoring system with Bloomberg data")
    monitor.start()

if __name__ == "__main__":
    main()
