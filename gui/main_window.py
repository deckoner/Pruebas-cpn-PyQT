from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QStackedWidget, QPushButton
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from gui.theme import THEME
from gui.components.sidebar_button import SidebarButton
import platform


class MainWindow(QMainWindow):
    """
    Ventana principal con menú lateral moderno y soporte de tema dinámico.

    La ventana contiene un menú lateral con botones interactivos que
    cambian la página visible en el contenedor principal. Permite alternar
    entre tema claro y oscuro mediante un botón con icono de sol/luna.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplicación PyQt - Menú moderno")
        self.setGeometry(100, 100, 900, 600)

        # --- Layout principal ---
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # --- Menú lateral ---
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)
        self.sidebar.setLayout(self.sidebar_layout)
        self.sidebar.setFixedWidth(200)
        main_layout.addWidget(self.sidebar)

        # --- Botones del menú ---
        self.btn_inicio = SidebarButton("Inicio")
        self.btn_config = SidebarButton("Configuración")
        self.btn_about = SidebarButton("Acerca de")

        # Agregar botones al layout lateral
        for btn in [self.btn_inicio, self.btn_config, self.btn_about]:
            self.sidebar_layout.addWidget(btn)
            if isinstance(btn, SidebarButton):
                btn.clicked.connect(self.handle_button_click)

        self.btn_inicio.setChecked(True)
        self.sidebar_layout.addStretch()

        # --- Contenedor de páginas ---
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # --- Páginas ---
        self.page_inicio = self.create_page("Bienvenido a la página de inicio")
        self.page_config = self.create_page("Aquí van las configuraciones")
        self.page_about = self.create_page("Acerca de esta aplicación")
        for page in [self.page_inicio, self.page_config, self.page_about]:
            self.stack.addWidget(page)

    def handle_button_click(self):
        """Maneja el click de los botones del menú lateral."""
        sender = self.sender()
        for btn in [self.btn_inicio, self.btn_config, self.btn_about]:
            btn.setChecked(False)
        sender.setChecked(True)
        index = [self.btn_inicio, self.btn_config, self.btn_about].index(sender)
        self.stack.setCurrentIndex(index)

    def create_page(self, text: str) -> QWidget:
        """Crea una página simple con QLabel centrado usando color de tema."""
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"color: {THEME['text']}; font-size: 24px;")
        layout.addWidget(label)
        page.setLayout(layout)
        return page

    def apply_theme(self, theme: dict):
        """Aplica un tema a toda la interfaz."""
        global THEME
        THEME.update(theme)

        # Actualizar sidebar
        if hasattr(self, "sidebar"):
            self.sidebar.setStyleSheet(f"background-color: {THEME['sidebar_bg']};")

        # Actualizar botones
        for btn in [self.btn_inicio, self.btn_config, self.btn_about]:
            btn.setStyleSheet(btn.default_style())

        # Actualizar páginas
        if hasattr(self, "stack"):
            for i in range(self.stack.count()):
                page = self.stack.widget(i)
                label = page.layout().itemAt(0).widget()
                label.setStyleSheet(f"color: {THEME['text']}; font-size: 24px;")
