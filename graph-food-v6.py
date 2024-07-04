import sys
import random
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QSplitter, QFrame, QLabel, QPushButton, QToolBox
from PyQt5.QtCore import Qt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from bson.json_util import dumps, loads
from flask import Flask, send_file
from flask_cors import CORS
from io import BytesIO
import threading

class MainWindow(QMainWindow):
    def __init__(self, sub_category, scores, food_category):
        self.sub_category = sub_category
        self.scores = scores
        self.food_category = food_category
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Food Acceptance')
        self.setGeometry(100, 100, 1000, 600)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e3440;
            }
            QFrame {
                background-color: #3b4252;
                color: #d8dee9;
            }
            QLabel, QPushButton {
                color: #d8dee9;
                font-size: 16px;
            }

            QScrollArea {
                background-color: #434c5e;
            }

            QToolBox::tab {
                background-color: #4c566a;
                border: none;
                padding: 10px;
                color: #d8dee9;
            }

            QToolBox::tab:selected {
                background-color: #81a1c1;
            }

            QToolBox::tab:hover {
                background-color: #5e81ac;
            }

            QPushButton {
                background-color: #81a1c1;
                border: none;
                padding: 10px;
                border-radius: 17px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #5e81ac;
            }
        """)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        splitter = QSplitter(Qt.Horizontal, centralWidget)
        layout = QVBoxLayout(centralWidget)

        layout.addWidget(splitter)
        leftFrame = QFrame(splitter)
        leftFrame.setFrameShape(QFrame.StyledPanel)
        leftLayout = QVBoxLayout(leftFrame)
        toolbox = QToolBox(leftFrame)
        leftLayout.addWidget(toolbox)

        settingsWidget = QWidget()
        settingsLayout = QVBoxLayout(settingsWidget)
        table = QPushButton("Tables", settingsWidget)
        new_date = QPushButton("Add new date", settingsWidget)
        another_setting = QPushButton("Setting", settingsWidget)

        settingsLayout.addWidget(table)
        settingsLayout.addWidget(new_date)
        settingsLayout.addWidget(another_setting)
        toolbox.addItem(settingsWidget, "Settings")

        rightFrame = QFrame(splitter)
        rightFrame.setFrameShape(QFrame.StyledPanel)
        rightLayout = QVBoxLayout(rightFrame)

        scrollArea = QScrollArea(rightFrame)
        rightLayout.addWidget(scrollArea)

        scrollContent = QWidget()
        scrollArea.setWidget(scrollContent)
        scrollArea.setWidgetResizable(True)

        scrollLayout = QVBoxLayout(scrollContent)

        food_items = self.sub_category

        for i, food in enumerate(food_items):
            plotWidget = pg.PlotWidget()
            scrollLayout.addWidget(plotWidget)

            y = self.scores[food]
            x = list(range(len(y)))

            for j in range(len(x) - 1):
                value1 = y[j]
                value2 = y[j + 1]

                pen = pg.mkPen(color=self.get_color(value1), width=2)
                plotWidget.plot(x=[x[j], x[j + 1]], y=[value1, value2], pen=pen)

            plotWidget.setTitle(food)

        self.show()

    def get_color(self, value):
        """Return color based on value."""
        if value < 4:
            return (0, 255, 0)
        elif 4 <= value <= 6:
            return (255, 255, 0)
        else:
            return (255, 0, 0)


def run_flask(app):
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Use example data if database connection fails
    try:
        uri = 'mongodb://admin:4XHoLm6jWVk0W7Dm@SG-Report-Graphics-2-64046.servers.mongodirector.com:27017/admin'
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("Your code is connected to the database")

        mydatabase = client.database
        mycollection = mydatabase.reports
        cursor = mycollection.find({'type': 'Enhanced'})
        list_cur = list(cursor)
    except Exception as e:
        print(f"Database connection failed: {e}")
        list_cur = [
            {
                "type": "Enhanced",
                "allergies": [
                    {
                        "Category": "Fruits",
                        "Sub-Category": "Apple",
                        "Scan Test - Current": 7
                    },
                    {
                        "Category": "Vegetables",
                        "Sub-Category": "Carrot",
                        "Scan Test - Current": 5
                    },
                    {
                        "Category": "Dairy",
                        "Sub-Category": "Milk",
                        "Scan Test - Current": 3
                    }
                ]
            },
            {
                "type": "Enhanced",
                "allergies": [
                    {
                        "Category": "Fruits",
                        "Sub-Category": "Apple",
                        "Scan Test - Current": 6
                    },
                    {
                        "Category": "Vegetables",
                        "Sub-Category": "Carrot",
                        "Scan Test - Current": 4
                    },
                    {
                        "Category": "Dairy",
                        "Sub-Category": "Milk",
                        "Scan Test - Current": 8
                    }
                ]
            },
            {
                "type": "Enhanced",
                "allergies": [
                    {
                        "Category": "Fruits",
                        "Sub-Category": "Apple",
                        "Scan Test - Current": 5
                    },
                    {
                        "Category": "Vegetables",
                        "Sub-Category": "Carrot",
                        "Scan Test - Current": 7
                    },
                    {
                        "Category": "Dairy",
                        "Sub-Category": "Milk",
                        "Scan Test - Current": 2
                    }
                ]
            }
        ]

    # Ensure list_cur is not empty
    if not list_cur:
        raise ValueError("No data available to display.")

    food_category = []
    food_list2 = list_cur
    scores = {}

    # for z in range(len(food_list2)):
    sub_category = [value['Sub-Category'] for value in food_list2[0]['allergies']]
    for category in sub_category:
        scores[category] = []
    for value in food_list2:
        allergies = value['allergies']
        for j in allergies:
            food_category.append(j['Category'])
            # scores.append(int(j['Scan Test - Current']))
            scores[j['Sub-Category']].append(int(j['Scan Test - Current']))
        # break

    app = QApplication(sys.argv)
    mainWin = MainWindow(sub_category, scores, food_category)

    flask_app = Flask(__name__)
    CORS(flask_app)

    @flask_app.route('/chart/<string:food>', methods=['GET'])
    def get_chart(food):
        if food not in scores:
            return "Food not found", 404

        y = scores[food]
        x = list(range(len(y)))

        plotWidget = pg.PlotWidget()
        for j in range(len(x) - 1):
            value1 = y[j]
            value2 = y[j + 1]
            pen = pg.mkPen(color=mainWin.get_color(value1), width=2)
            plotWidget.plot(x=[x[j], x[j + 1]], y=[value1, value2], pen=pen)

        img = BytesIO()
        exporter = pg.exporters.ImageExporter(plotWidget.plotItem)
        exporter.parameters()['width'] = 640
        exporter.export(img)
        img.seek(0)

        return send_file(img, mimetype='image/png')

    flask_thread = threading.Thread(target=run_flask, args=(flask_app,))
    flask_thread.setDaemon(True)
    flask_thread.start()

    sys.exit(app.exec_())
