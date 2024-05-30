import typing
from pathlib import Path

import fiona
from PyQt6.QtWidgets import QGridLayout, QPushButton, QMainWindow, QWidget, QFileDialog, QComboBox, QLabel, QHBoxLayout, \
    QStatusBar, QLineEdit
from geopandas import GeoDataFrame
from pyqttoast import Toast, ToastPreset, ToastPosition

from src import GeoUtils
from src.gui.Table import Table


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # === Data ===
        self._last_open_dir = None
        self._last_save_dir = None
        self._filepath = None
        self.gdf = None

        # === Layout ===
        self.layout = QGridLayout()
        self.central_widget = QWidget()

        # === Widgets ===
        self.open_button = QPushButton('Open')
        self.save_button = QPushButton('Save')
        self.saveas_button = QPushButton('Save As')
        self.feature_combo_box = QComboBox()
        self.filter_line_edit = QLineEdit()
        self.table = Table()
        self.status_bar = QStatusBar()

        self._initialize()
        self._signals()

    def _initialize(self):
        self.setWindowTitle('GeoFileEditor - Edit Shape and MapInfo files')
        self.resize(500, 600)

        self.layout.setSpacing(10)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.setStatusBar(self.status_bar)

        # === Layouts ===
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.saveas_button)
        self.layout.addLayout(button_layout, 0, 0, 1, 2)
        combo_box_layout = QHBoxLayout()
        combo_box_layout.addWidget(QLabel('Feature'))
        combo_box_layout.addWidget(self.feature_combo_box, 1)
        self.layout.addLayout(combo_box_layout, 1, 0, 1, 2)
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel('Filter'))
        filter_layout.addWidget(self.filter_line_edit)
        self.layout.addLayout(filter_layout, 2, 0, 1, 2)
        self.layout.addWidget(self.table, 3, 0, 1, 2)

    def _signals(self):
        self.open_button.clicked.connect(self._on_open_button_clicked)
        self.save_button.clicked.connect(self._on_save_button_clicked)
        self.saveas_button.clicked.connect(self._on_saveas_button_clicked)
        self.filter_line_edit.textChanged.connect(self._on_filter_line_edit_changed)
        self.feature_combo_box.currentIndexChanged.connect(self._on_feature_combo_box_change)

    def _on_open_button_clicked(self):
        self._filepath, _ = QFileDialog.getOpenFileName(self, 'Open File', str(self._last_open_dir), 'Zip files (*.zip)')

        if self._filepath:
            self._last_open_dir = Path(self._filepath).parent
            self._last_save_dir = self._last_open_dir if not self._last_save_dir else self._last_save_dir

            self.gdf = GeoUtils.read_geo_zip(self._filepath)

            with fiona.open(f'zip://{self._filepath}') as f:
                schema = f.schema
            print(f'Read {self._filepath} with {len(self.gdf)} features')

            self.status_bar.showMessage(self._filepath)

            self.feature_combo_box.blockSignals(True)
            self.feature_combo_box.clear()
            for i in range(len(self.gdf)):
                feature = f'Feature {i}'
                self.feature_combo_box.insertItem(i, feature)
            self.feature_combo_box.blockSignals(False)

            self.table.setData(self.gdf, schema)
            self.feature_combo_box.setCurrentIndex(0)

    def _on_save_button_clicked(self):
        if self.gdf is not None:
            try:
                GeoUtils.overwrite_zip(self.gdf, self._filepath)
                toast = Toast()
                toast.setDuration(6000)
                toast.setTitle('Save complete!')
                toast.setText(f'File <strong>{self._filepath}</strong> has been successfully updated.')
                toast.applyPreset(ToastPreset.SUCCESS)
                toast.setPosition(ToastPosition.TOP_MIDDLE)
                toast.show()
                self.table.resetOriginalValues()
            except Exception as e:
                print(e)

    def _on_saveas_button_clicked(self):
        if self.gdf is not None:
            filepath, _ = QFileDialog.getSaveFileName(self, 'Save File', str(self._last_save_dir))
            self._last_save_dir = Path(self._filepath).parent
            GeoUtils.write_new_zip(self.gdf, filepath)

    def _on_feature_combo_box_change(self, index: int):
        self.table.setFeatureIndex(index)

    def _on_filter_line_edit_changed(self):
        text = self.filter_line_edit.text()
        self.table.filter(text)
