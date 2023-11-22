import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QFileDialog, QSlider
from PyQt5 import uic
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class NiftiViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Charger l'interface depuis le fichier UI
        self.load_ui()

        # Connecter la fonction load_nifti à l'événement clic du bouton
        self.loadButton.clicked.connect(self.load_nifti)

        # Initialiser la figure et le canevas Matplotlib
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)

        # Ajouter le canevas à la mise en page
        self.verticalLayout.addWidget(self.canvas)

        # Ajouter des boutons de navigation
        self.prevImageButton = QPushButton("Previous Image")
        self.nextImageButton = QPushButton("Next Image")
        self.prevSliceButton = QPushButton("Previous Slice")
        self.nextSliceButton = QPushButton("Next Slice")

        self.prevImageButton.clicked.connect(self.prev_image)
        self.nextImageButton.clicked.connect(self.next_image)
        self.prevSliceButton.clicked.connect(self.prev_slice)
        self.nextSliceButton.clicked.connect(self.next_slice)

        self.verticalLayout.addWidget(self.prevImageButton)
        self.verticalLayout.addWidget(self.nextImageButton)
        self.verticalLayout.addWidget(self.prevSliceButton)
        self.verticalLayout.addWidget(self.nextSliceButton)

        # Ajouter des curseurs pour sélectionner l'image et la tranche
        self.imageSlider = QSlider()
        self.imageSlider.setOrientation(1)  # Set orientation to horizontal
        self.imageSlider.setMinimum(0)
        self.imageSlider.valueChanged.connect(self.display_nifti_image)

        self.sliceSlider = QSlider()
        self.sliceSlider.setOrientation(1)  # Set orientation to horizontal
        self.sliceSlider.setMinimum(0)
        self.sliceSlider.valueChanged.connect(self.display_nifti_image)

        self.verticalLayout.addWidget(self.imageSlider)
        self.verticalLayout.addWidget(self.sliceSlider)

    def load_ui(self):
        # Charger l'interface depuis le fichier UI
        uic.loadUi("nifti_viewer.ui", self)

        # Récupérer les widgets de l'interface
        self.label = self.findChild(QLabel, "label")
        self.loadButton = self.findChild(QPushButton, "loadButton")
        self.verticalLayout = self.findChild(QVBoxLayout, "verticalLayout")

    def load_nifti(self):
        # Ouvrir une boîte de dialogue pour choisir le fichier NIfTI
        filepath, _ = QFileDialog.getOpenFileName(self, "Open NIfTI File", "", "NIfTI Files (*.nii *.nii.gz)")

        if filepath:
            # Charger l'image NIfTI
            nifti_image = nib.load(filepath)
            self.image_data = nifti_image.get_fdata()

            # Initialiser les curseurs avec les valeurs maximales appropriées
            self.imageSlider.setMaximum(self.image_data.shape[2] - 1)
            self.sliceSlider.setMaximum(self.image_data.shape[3] - 1)

            # Afficher les informations sur l'image
            self.display_image_info(self.image_data)

            # Afficher l'image initiale dans Matplotlib
            self.display_nifti_image()

    def display_image_info(self, image_data):
        # Afficher les informations sur l'image dans le QLabel
        image_shape = image_data.shape
        self.label.setText(f"Image Shape: {image_shape}")

    def display_nifti_image(self):
        # Récupérer les indices sélectionnés par les curseurs
        image_index = self.imageSlider.value()
        slice_index = self.sliceSlider.value()

        # Afficher l'image sélectionnée dans Matplotlib
        image_to_display = self.image_data[:, :, image_index, slice_index]  # Modify the indices as needed
        self.ax.imshow(image_to_display, cmap='gray')
        self.canvas.draw()

    def prev_image(self):
        # Mettre à jour le curseur de l'image précédente
        current_value = self.imageSlider.value()
        if current_value > self.imageSlider.minimum():
            self.imageSlider.setValue(current_value - 1)

    def next_image(self):
        # Mettre à jour le curseur de l'image suivante
        current_value = self.imageSlider.value()
        if current_value < self.imageSlider.maximum():
            self.imageSlider.setValue(current_value + 1)

    def prev_slice(self):
        # Mettre à jour le curseur de la tranche précédente
        current_value = self.sliceSlider.value()
        if current_value > self.sliceSlider.minimum():
            self.sliceSlider.setValue(current_value - 1)

    def next_slice(self):
        # Mettre à jour le curseur de la tranche suivante
        current_value = self.sliceSlider.value()
        if current_value < self.sliceSlider.maximum():
            self.sliceSlider.setValue(current_value + 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NiftiViewer()
    window.show()
    sys.exit(app.exec_())