import hashlib

from PySide6.QtCharts import QLineSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


def hash_to_color(input_number):
    # Generate a hash value using MD5 (you can use other hash functions as well)
    hash_object = hashlib.md5(str(input_number).encode())
    hash_hex = hash_object.hexdigest()

    # Take the first 6 characters of the hash as RGB values
    r = int(hash_hex[:2], 16)
    g = int(hash_hex[2:4], 16)
    b = int(hash_hex[4:6], 16)

    return QColor(r, g, b)


def draw_vertical_line(x, y_min=-2, y_max=2):
    # Create a vertical line series
    line_series = QLineSeries()
    line_series.append(x, y_min)
    line_series.append(x, y_max)

    # Set pen properties for the line (you can customize as needed)
    pen = line_series.pen()
    pen.setColor(Qt.black)
    pen.setWidth(5)
    line_series.setPen(pen)

    return line_series
