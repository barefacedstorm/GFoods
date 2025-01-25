from flask import Flask, render_template, jsonify
from providers.bloomberg_provider import BloombergAgProvider
from providers.provider_manager import ProviderManager
import asyncio
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

provider_manager = ProviderManager()
ag_provider = BloombergAgProvider()
provider_manager.add_provider(ag_provider)

@app.route('/')
async def dashboard():
    try:
        data = await ag_provider.fetch_data()
        print(f"Data received: {data}")
        response = render_template('dashboard.html', data=data, datetime=datetime)
        print(f"Response length: {len(response)}")
        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"Server starting at http://localhost:6001")
    app.run(host='0.0.0.0', port=6001, debug=True)
