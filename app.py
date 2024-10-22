import os
import random
import sys
from flask import Flask, render_template, request, send_from_directory, abort, redirect, url_for


class Main:
    def __init__(self):
        self.FileFolder = None
        self.main_folder = None
        self.app = Flask(__name__)

    def start(self):
        self.main_folder = sys.path[0]
        self.FileFolder = os.path.join(self.main_folder, "files")
        print(self.main_folder)
        print(self.FileFolder)

        if not os.path.isdir(self.FileFolder):
            os.mkdir(self.FileFolder)

        self.app.run(debug=True, host='0.0.0.0')

    @staticmethod
    def get_files(directory):
        return os.listdir(directory)

    def routes(self):
        # Главная страница
        @self.app.route('/')
        def home():
            files = self.get_files(self.FileFolder)
            return render_template("index.html", files=files)

        @self.app.route('/file/<path:filename>', methods=['GET'])
        def download_file(filename):
            file_path = os.path.join(self.FileFolder, filename)

            if os.path.isfile(file_path):
                return send_from_directory(self.FileFolder, filename, as_attachment=True)
            else:
                abort(404, description="Файл не найден")

        @self.app.route('/upload', methods=['POST'])
        def upload_file():
            if 'file' not in request.files:
                return "Нет файла для загрузки", 400
            file = request.files['file']
            if file.filename == '':
                return "Файл не выбран", 400
            file_path = os.path.join(self.FileFolder, file.filename)
            if os.path.isfile(file_path):
                file.save(str(random.randint(0,99999)) + file_path)
                return {"url": url_for('download_file', filename=file.filename, _external=True)}, 201
            else:
                file.save(file_path)
                return {"url": url_for('download_file', filename=file.filename, _external=True)}, 201

        @self.app.route("/files")
        def files():
            return {"files": self.get_files(self.FileFolder)}

        @self.app.errorhandler(404)
        def page_not_found(error):
            return f'Ошибка 404: {error.description}', 404


if __name__ == '__main__':
    app_instance = Main()
    app_instance.routes()
    app_instance.start()
