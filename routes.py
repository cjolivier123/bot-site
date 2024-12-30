import logging
import os
import zipfile
from flask import render_template, send_file
from flask import current_app as app
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of files to include in the download
INCLUDE_FILES = [
    './main.py',
    './app_init.py',
    './routes.py',
    './models.py',
    './requirements.txt',
    './templates/home.html',
    './templates/download.html',
    './templates/partials/_header.html',
    './templates/partials/_desktop_header.html',
    './templates/partials/_mobile_header.html',
    './static/css/styles.css',
    './static/css/download.css',
    './static/js/header.js',
    './static/js/home.js',
    './migrations/000_example.sql'
]

def register_routes(app):
    @app.route("/")
    def home_route():
        return render_template("home.html")

    @app.route("/download")
    def download_route():
        return render_template("download.html")

    @app.route("/download/source")
    def download_source():
        try:
            # Create a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, 'website_source.zip')
                
                # Create a ZIP file
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # Add specific files to the ZIP
                    for file_path in INCLUDE_FILES:
                        if os.path.exists(file_path):
                            logger.info(f"Adding file to ZIP: {file_path}")
                            zipf.write(file_path, file_path)
                        else:
                            logger.warning(f"File not found: {file_path}")

                # Send the zip file
                logger.info("ZIP file created successfully")
                return send_file(
                    zip_path,
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='website_source.zip'
                )
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return "An error occurred while creating the ZIP file.", 500