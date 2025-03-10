import sys
import random
import string
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QCheckBox, 
                            QSlider, QLineEdit, QSpinBox, QMessageBox, QGroupBox,
                            QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QLinearGradient, QBrush, QPainter

class StyleHelper:
    PRIMARY_COLOR = "#6200EE"
    SECONDARY_COLOR = "#03DAC6"
    TERTIARY_COLOR = "#B00020"
    BACKGROUND_COLOR = "#F5F5F5"
    SURFACE_COLOR = "#FFFFFF"
    TEXT_COLOR = "#333333"
    
    @staticmethod
    def set_button_style(button, primary=True, accent=False):
        if primary:
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {StyleHelper.PRIMARY_COLOR if not accent else StyleHelper.SECONDARY_COLOR};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {StyleHelper.PRIMARY_COLOR if not accent else StyleHelper.SECONDARY_COLOR}DD;
                }}
                QPushButton:pressed {{
                    background-color: {StyleHelper.PRIMARY_COLOR if not accent else StyleHelper.SECONDARY_COLOR}AA;
                }}
                """
            )
        else:
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: transparent;
                    color: #6200EE;
                    border: 1px solid #6200EE;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #6200EE11;
                }
                QPushButton:pressed {
                    background-color: #6200EE22;
                }
                """
            )
    
    @staticmethod
    def set_checkbox_style(checkbox):
        checkbox.setStyleSheet(
            """
            QCheckBox {
                spacing: 8px;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 2px solid #6200EE;
            }
            QCheckBox::indicator:unchecked {
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #6200EE;
                image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iZmVhdGhlciBmZWF0aGVyLWNoZWNrIj48cG9seWxpbmUgcG9pbnRzPSIyMCA2IDkgMTcgNCAxMiI+PC9wb2x5bGluZT48L3N2Zz4=);
            }
            """
        )
    
    @staticmethod
    def set_slider_style(slider):
        slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                height: 8px;
                background: #E0E0E0;
                border-radius: 4px;
                margin: 0px;
            }
            QSlider::handle:horizontal {
                background: #6200EE;
                border: none;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::sub-page:horizontal {
                background: #BB86FC;
                border-radius: 4px;
            }
            """
        )
    
    @staticmethod
    def set_spinbox_style(spinbox):
        spinbox.setStyleSheet(
            """
            QSpinBox {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border: none;
                background: #EEEEEE;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: #DDDDDD;
            }
            """
        )
    
    @staticmethod
    def set_groupbox_style(groupbox):
        groupbox.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                margin-top: 15px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                color: #6200EE;
            }
            """
        )
    
    @staticmethod
    def set_lineedit_style(lineedit):
        lineedit.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #CCCCCC;
                border-radius: 6px;
                padding: 10px;
                background-color: #F8F8F8;
                font-family: 'Courier New';
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit:focus {
                border: 2px solid #6200EE;
            }
            """
        )

class PasswordStrengthMeter(QFrame):
    def __init__(self, parent=None):
        super(PasswordStrengthMeter, self).__init__(parent)
        self.strength = 0  # 0-100
        self.setMinimumHeight(10)
        self.setMaximumHeight(10)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
    def setStrength(self, value):
        self.strength = value
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#EEEEEE")))
        painter.drawRoundedRect(self.rect(), 5, 5)
        
        # Foreground (strength indicator)
        if self.strength > 0:
            width = int(self.width() * (self.strength / 100))
            rect = self.rect()
            rect.setWidth(width)
            
            # Determine color based on strength
            if self.strength < 30:
                color = QColor("#F44336")  # Red
            elif self.strength < 60:
                color = QColor("#FFC107")  # Yellow/Orange
            else:
                color = QColor("#4CAF50")  # Green
                
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(rect, 5, 5)

class CustomAnimation(QPropertyAnimation):
    def __init__(self, target, prop):
        super(CustomAnimation, self).__init__(target, prop)
        self.setDuration(300)
        self.setEasingCurve(QEasingCurve.OutCubic)

class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Password Generator')
        self.setGeometry(300, 300, 550, 500)
        self.setStyleSheet(f"background-color: {StyleHelper.BACKGROUND_COLOR};")
        
        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        self.setCentralWidget(central_widget)
        
        # App title
        title_label = QLabel("Secure Password Generator")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet(f"color: {StyleHelper.PRIMARY_COLOR};")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Password display
        password_group = QGroupBox("Generated Password")
        StyleHelper.set_groupbox_style(password_group)
        password_layout = QVBoxLayout()
        password_layout.setContentsMargins(15, 20, 15, 15)
        password_layout.setSpacing(10)
        
        self.password_field = QLineEdit()
        self.password_field.setReadOnly(True)
        self.password_field.setFont(QFont("Courier New", 12, QFont.Bold))
        self.password_field.setMinimumHeight(50)
        self.password_field.setAlignment(Qt.AlignCenter)
        StyleHelper.set_lineedit_style(self.password_field)
        
        # Password strength meter
        self.strength_meter = PasswordStrengthMeter()
        
        # Label to show password strength
        self.strength_label = QLabel("Password Strength: Medium")
        self.strength_label.setAlignment(Qt.AlignRight)
        self.strength_label.setStyleSheet("color: #757575; font-style: italic;")
        
        password_buttons = QHBoxLayout()
        password_buttons.setSpacing(10)
        
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setMinimumHeight(40)
        StyleHelper.set_button_style(self.copy_button, primary=False)
        self.copy_button.clicked.connect(self.copy_password)
        
        self.generate_button = QPushButton("Generate Password")
        self.generate_button.setMinimumHeight(40)
        StyleHelper.set_button_style(self.generate_button, accent=True)
        self.generate_button.clicked.connect(self.generate_password)
        
        password_buttons.addWidget(self.copy_button)
        password_buttons.addWidget(self.generate_button)
        
        password_layout.addWidget(self.password_field)
        password_layout.addWidget(self.strength_meter)
        password_layout.addWidget(self.strength_label)
        password_layout.addLayout(password_buttons)
        password_group.setLayout(password_layout)
        main_layout.addWidget(password_group)
        
        # Password Length control
        length_group = QGroupBox("Password Length")
        StyleHelper.set_groupbox_style(length_group)
        length_layout = QVBoxLayout()
        length_layout.setContentsMargins(15, 20, 15, 15)
        
        length_control = QHBoxLayout()
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setMinimum(8)
        self.length_slider.setMaximum(256)
        self.length_slider.setValue(16)
        self.length_slider.setTickPosition(QSlider.TicksBelow)
        self.length_slider.setTickInterval(16)
        StyleHelper.set_slider_style(self.length_slider)
        self.length_slider.valueChanged.connect(self.update_length_display)
        
        self.length_spin = QSpinBox()
        self.length_spin.setMinimum(8)
        self.length_spin.setMaximum(256)
        self.length_spin.setValue(16)
        StyleHelper.set_spinbox_style(self.length_spin)
        self.length_spin.valueChanged.connect(self.update_length_slider)
        
        # Add length labels
        length_label_layout = QHBoxLayout()
        min_label = QLabel("8")
        min_label.setAlignment(Qt.AlignLeft)
        max_label = QLabel("256")
        max_label.setAlignment(Qt.AlignRight)
        length_label_layout.addWidget(min_label)
        length_label_layout.addWidget(max_label)
        
        length_control.addWidget(self.length_slider)
        length_control.addWidget(self.length_spin)
        
        length_layout.addLayout(length_control)
        length_layout.addLayout(length_label_layout)
        length_group.setLayout(length_layout)
        main_layout.addWidget(length_group)
        
        # Character options
        char_group = QGroupBox("Character Options")
        StyleHelper.set_groupbox_style(char_group)
        char_layout = QVBoxLayout()
        char_layout.setContentsMargins(15, 20, 15, 15)
        char_layout.setSpacing(10)
        
        self.use_uppercase = QCheckBox("Include Uppercase Letters (A-Z)")
        StyleHelper.set_checkbox_style(self.use_uppercase)
        self.use_uppercase.setChecked(True)
        
        self.use_lowercase = QCheckBox("Include Lowercase Letters (a-z)")
        StyleHelper.set_checkbox_style(self.use_lowercase)
        self.use_lowercase.setChecked(True)
        
        self.use_numbers = QCheckBox("Include Numbers (0-9)")
        StyleHelper.set_checkbox_style(self.use_numbers)
        self.use_numbers.setChecked(True)
        
        self.use_special = QCheckBox("Include Special Characters (!@#$%^&*)")
        StyleHelper.set_checkbox_style(self.use_special)
        self.use_special.setChecked(True)
        
        self.avoid_similar = QCheckBox("Avoid Similar Characters (l, 1, I, 0, O)")
        StyleHelper.set_checkbox_style(self.avoid_similar)
        
        char_layout.addWidget(self.use_uppercase)
        char_layout.addWidget(self.use_lowercase)
        char_layout.addWidget(self.use_numbers)
        char_layout.addWidget(self.use_special)
        char_layout.addWidget(self.avoid_similar)
        char_group.setLayout(char_layout)
        main_layout.addWidget(char_group)
        
        # Status bar with gradient
        self.statusBar().setStyleSheet(
            """
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6200EE, stop:1 #03DAC6);
                color: white;
                font-weight: bold;
                padding: 5px;
            }
            """
        )
        self.statusBar().showMessage('Ready')
        
        # Generate initial password
        self.generate_password()
        
    def update_length_display(self, value):
        self.length_spin.setValue(value)
        self.update_strength_meter()
        
    def update_length_slider(self, value):
        self.length_slider.setValue(value)
        self.update_strength_meter()
        
    def update_strength_meter(self):
        length = self.length_slider.value()
        
        # Calculate password entropy (simplified)
        char_space = 0
        if self.use_uppercase.isChecked():
            char_space += 26
        if self.use_lowercase.isChecked():
            char_space += 26
        if self.use_numbers.isChecked():
            char_space += 10
        if self.use_special.isChecked():
            char_space += 32
            
        if char_space == 0:
            strength = 0
        else:
            # Basic entropy calculation - normalized to 0-100
            import math
            entropy = length * math.log2(char_space) if char_space > 0 else 0
            strength = min(100, entropy / 128 * 100)
        
        # Animate the strength meter
        self.strength_meter.setStrength(strength)
        
        # Update strength label
        if strength < 30:
            self.strength_label.setText("Password Strength: Weak")
            self.strength_label.setStyleSheet("color: #F44336; font-style: italic;")
        elif strength < 60:
            self.strength_label.setText("Password Strength: Medium")
            self.strength_label.setStyleSheet("color: #FFC107; font-style: italic;")
        else:
            self.strength_label.setText("Password Strength: Strong")
            self.strength_label.setStyleSheet("color: #4CAF50; font-style: italic;")
    def reset_copy_button(self):
        # Reset the button to its original state
        if hasattr(self, 'original_copy_text') and hasattr(self, 'original_copy_style'):
            self.copy_button.setText(self.original_copy_text)
        self.copy_button.setStyleSheet(self.original_copy_style)
    def generate_password(self):
        # Reset copy button to original state if it was in "copied" state
        if hasattr(self, 'copy_reset_timer') and self.copy_reset_timer.isActive():
            self.copy_reset_timer.stop()
            self.reset_copy_button()
        
        length = self.length_slider.value()
        
        # Check if at least one option is selected
        if not any([self.use_uppercase.isChecked(), 
                self.use_lowercase.isChecked(),
                self.use_numbers.isChecked(),
                self.use_special.isChecked()]):
            QMessageBox.warning(self, "Warning", "Please select at least one character type.")
            return
        
        # Define character sets
        chars = ""
        
        if self.use_uppercase.isChecked():
            if self.avoid_similar.isChecked():
                chars += "".join(c for c in string.ascii_uppercase if c not in "IO")
            else:
                chars += string.ascii_uppercase
                
        if self.use_lowercase.isChecked():
            if self.avoid_similar.isChecked():
                chars += "".join(c for c in string.ascii_lowercase if c not in "lo")
            else:
                chars += string.ascii_lowercase
                
        if self.use_numbers.isChecked():
            if self.avoid_similar.isChecked():
                chars += "".join(c for c in string.digits if c not in "01")
            else:
                chars += string.digits
                
        if self.use_special.isChecked():
            chars += "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
        
        # Generate password
        password = "".join(random.choice(chars) for _ in range(length))
        
        # Create fade animation for password field
        self.password_field.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #CCCCCC;
                border-radius: 6px;
                padding: 10px;
                background-color: #F8F8F8;
                font-family: 'Courier New';
                font-size: 16px;
                font-weight: bold;
                color: rgba(0, 0, 0, 0);
            }
            """
        )
        
        # Update UI
        self.password_field.setText(password)
        
        # Fade in animation
        animation = CustomAnimation(self.password_field, b"styleSheet")
        animation.setStartValue(
            """
            QLineEdit {
                border: 2px solid #CCCCCC;
                border-radius: 6px;
                padding: 10px;
                background-color: #F8F8F8;
                font-family: 'Courier New';
                font-size: 16px;
                font-weight: bold;
                color: rgba(0, 0, 0, 0);
            }
            """
        )
        animation.setEndValue(
            """
            QLineEdit {
                border: 2px solid #6200EE;
                border-radius: 6px;
                padding: 10px;
                background-color: #F8F8F8;
                font-family: 'Courier New';
                font-size: 16px;
                font-weight: bold;
                color: rgba(0, 0, 0, 255);
            }
            """
        )
        animation.start()
        
        self.statusBar().showMessage(f'Generated a {length}-character password')
        self.update_strength_meter()
        
    def copy_password(self):
        if self.password_field.text():
            clipboard = QApplication.clipboard()
            clipboard.setText(self.password_field.text())
            
            # Store original button text and style
            self.original_copy_text = self.copy_button.text()
            self.original_copy_style = self.copy_button.styleSheet()
            
            # Change button appearance to show success
            self.copy_button.setText("✓ Copied!")
            self.copy_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
                """
            )
            
            # Update status bar
            self.statusBar().showMessage('Password copied to clipboard!', 3000)
            
            # Reset button after longer delay (2 seconds) if user doesn't generate new password
            self.copy_reset_timer = QTimer()
            self.copy_reset_timer.setSingleShot(True)
            self.copy_reset_timer.timeout.connect(self.reset_copy_button)
            self.copy_reset_timer.start(2000)  # Reset after 2 seconds

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better cross-platform appearance
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec_())