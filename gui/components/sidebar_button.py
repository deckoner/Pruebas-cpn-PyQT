from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from gui.theme import THEME


class SidebarButton(QPushButton):
    """
    Botón lateral personalizado para el menú de la aplicación.

    Este botón utiliza variables de tema definidas en `THEME` para su estilo.
    Soporta iconos opcionales y mantiene un estilo moderno consistente en la aplicación.
    """

    def __init__(self, text: str, icon_path: str | None = None):
        """
        Inicializa un botón lateral con texto y un icono opcional.

        Args:
            text (str): Texto que se mostrará en el botón.
            icon_path (str | None, opcional): Ruta al icono del botón. Por defecto es None.
        """
        super().__init__(text)

        # Cambiar el cursor al pasar sobre el botón
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Permitir que el botón permanezca "seleccionado" (checked)
        self.setCheckable(True)

        # Aplicar el estilo usando las variables de tema
        self.setStyleSheet(self.default_style())

        # Agregar icono si se proporciona
        if icon_path:
            self.setIcon(QIcon(icon_path))

        # Configuración de tamaño: expandible horizontalmente, altura fija
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(50)

    def default_style(self) -> str:
        """
        Genera y devuelve el estilo CSS para el botón.

        El estilo utiliza los colores definidos en THEME para:
        - Color de fondo por defecto
        - Color de texto
        - Color de fondo al pasar el mouse (hover)
        - Color de fondo cuando está seleccionado (checked)

        Returns:
            str: Cadena con CSS para aplicar al botón.
        """
        return f"""
        QPushButton {{
            background-color: {THEME['button_bg']};
            color: {THEME['text']};
            border: none;
            text-align: left;
            padding-left: 20px;
            font-size: 16px;
        }}
        QPushButton:hover {{
            background-color: {THEME['button_hover']};
        }}
        QPushButton:checked {{
            background-color: {THEME['button_active']};
        }}
        """
