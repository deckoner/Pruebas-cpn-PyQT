from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QStackedWidget, QSizePolicy
)
from PyQt6.QtCore import Qt
from gui.theme import THEME
from gui.components.sidebar_button import SidebarButton


class MainWindow(QMainWindow):
    """
    Ventana principal con menú horizontal responsivo y soporte de tema dinámico.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplicación PyQt - Menú horizontal responsivo")
        self.setGeometry(100, 100, 900, 600)

        # --- Layout principal ---
        main_widget = QWidget()
        main_layout = QVBoxLayout()  # Menú arriba, contenido abajo
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # --- Menú superior (horizontal) ---
        self.menu_bar = QWidget()
        self.menu_layout = QHBoxLayout()
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_layout.setSpacing(0)
        self.menu_bar.setLayout(self.menu_layout)
        self.menu_bar.setFixedHeight(50)
        self.menu_bar.setStyleSheet(f"background-color: {THEME['sidebar_bg']};")
        main_layout.addWidget(self.menu_bar)

        # --- Botones del menú ---
        self.btn_inicio = SidebarButton("Inicio")
        self.btn_product = SidebarButton("Productos")
        self.btn_gestion_product = SidebarButton("Gestión de productos")
        self.btn_config = SidebarButton("Configuración")
        self.btn_about = SidebarButton("Acerca de")

        # Lista de botones
        self.buttons = [
            self.btn_inicio,
            self.btn_product,
            self.btn_gestion_product,
            self.btn_config,
            self.btn_about
        ]

        # --- Añadir botones al layout con tamaño equitativo ---
        for i, btn in enumerate(self.buttons):
            btn.clicked.connect(self.handle_button_click)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.menu_layout.addWidget(btn)
            # Asignar igual peso a todos los botones (distribución equitativa)
            self.menu_layout.setStretch(i, 1)

        # --- Estado inicial ---
        self.btn_inicio.setChecked(True)

        # --- Contenedor de páginas ---
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # --- Páginas ---
        self.page_inicio = self.create_page("Bienvenido a la página de inicio")
        self.page_product = self.create_page("Aquí va la tabla de productos")
        self.page_gestion_product = self.create_page("Aquí podrás crear productos nuevos y gestionar los demás")
        self.page_config = self.create_page("Configuraciones")
        self.page_about = self.create_page("Acerca de nosotros")

        # --- Agregar páginas al stack ---
        self.pages = [
            self.page_inicio,
            self.page_product,
            self.page_gestion_product,
            self.page_config,
            self.page_about
        ]

        for page in self.pages:
            self.stack.addWidget(page)

    def handle_button_click(self):
        """Maneja el click de los botones del menú."""
        sender = self.sender()
        for btn in self.buttons:
            btn.setChecked(False)
        sender.setChecked(True)
        index = self.buttons.index(sender)
        self.stack.setCurrentIndex(index)

    def create_page(self, text: str) -> QWidget:
        """Crea una página simple con QLabel centrado."""
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

        # Actualizar barra de menú
        if hasattr(self, "menu_bar"):
            self.menu_bar.setStyleSheet(f"background-color: {THEME['sidebar_bg']};")

        # Actualizar botones
        for btn in self.buttons:
            btn.setStyleSheet(btn.default_style())

        # Actualizar páginas
        if hasattr(self, "stack"):
            for i in range(self.stack.count()):
                page = self.stack.widget(i)
                label = page.layout().itemAt(0).widget()
                label.setStyleSheet(f"color: {THEME['text']}; font-size: 24px;")
