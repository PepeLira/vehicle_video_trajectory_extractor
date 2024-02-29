from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QRectF

def array_to_pixmap(array):
        if array is None:
            return None

        height, width, channel = array.shape
        bytes_per_line = 3 * width
        q_image = QImage(array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_image)

        return pixmap


class GPSReferenceDialog(QDialog):

    def __init__(self, image_array=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set the Reference GPS Coordinates")

        self.image_array = image_array
        self.selected_points = []
        self.gps_entries = []
        self.color_names = {
            Qt.red: "Red",
            Qt.green: "Green",
            Qt.blue: "Blue",
            Qt.yellow: "Yellow",
            Qt.magenta: "Magenta",
            Qt.cyan: "Cyan",
            Qt.white: "White",
            Qt.gray: "Gray"
        }
        self.marker_colors = [
            Qt.red, 
            Qt.green,
            Qt.blue, 
            Qt.yellow, 
            Qt.magenta, 
            Qt.cyan, 
            Qt.white, 
            Qt.gray
            ]
        self.current_color_index = 0

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.pixmap_item = QGraphicsPixmapItem(array_to_pixmap(self.image_array))
        self.scene.addItem(self.pixmap_item)
      
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)

        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setOptimizationFlags(QGraphicsView.DontAdjustForAntialiasing | QGraphicsView.DontSavePainterState)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
      
        self.coords_label = QLabel(self)
        self.layout.addWidget(self.coords_label)

        self.set_coords_button = QPushButton("Set Coordinates", self)
        self.set_coords_button.clicked.connect(self.prepare_and_accept)
        self.layout.addWidget(self.set_coords_button)
      
        self.setLayout(self.layout)
        self.view.mousePressEvent = self.image_clicked

    def accept(self):
        super().accept()

    def get_coordinates_mapping(self):
        return self.coordinates_mapping
    
    def coordinates_mapping_is_empty(self):
        return len(self.coordinates_mapping) == 0 

    def prepare_and_accept(self):
        self.coordinates_mapping = {}
        for point, entry in zip(self.selected_points, self.gps_entries):
            x, y, color = point
            gps_coords = list(map(float,entry.text().split(",")))
            self.coordinates_mapping[(x, y)] = gps_coords
        self.accept()

    def image_clicked(self, event):
        scene_point = self.view.mapToScene(event.pos())
        img_coords = self.pixmap_item.mapFromScene(scene_point).toPoint()
        
        point_color = self.marker_colors[self.current_color_index]
        self.selected_points.append((img_coords.x(), img_coords.y(), point_color))
        
        coords_text = ", ".join([f"({x}, {y}, {self.color_names[color]})" for x, y, color in self.selected_points])
        self.coords_label.setText(f"Selected points: {coords_text}")

        marker_size = 6  # The size of the ellipse (circle) to mark the point
        marker_rect = QRectF(img_coords.x() - marker_size/2, img_coords.y() - marker_size/2, marker_size, marker_size)
        marker = QGraphicsEllipseItem(marker_rect)
        
        marker.setBrush(point_color)
        self.current_color_index = (self.current_color_index + 1) % len(self.marker_colors)
        self.scene.addItem(marker)
        
        gps_entry = QLineEdit(self)
        gps_entry.setPlaceholderText(
            f"Enter GPS for point ({self.selected_points[-1][0]}, "
            f"{self.selected_points[-1][1]}, "
            f"{self.color_names[self.selected_points[-1][2]]})"
        )        
        self.layout.addWidget(gps_entry)
        self.gps_entries.append(gps_entry)
