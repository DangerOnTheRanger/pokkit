'''This contains GUI elements we invoke in other code.'''

# http://pyqt.sourceforge.net/Docs/PyQt5/sip-classes.html
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt, QCoreApplication
import typing

title = 'Pokkit'


def choose(prompt_: str, choices: typing.List[str]):
    '''Returns the index of the selected choice'''

    app = QApplication([])
    window = QWidget()
    window.setWindowTitle(title)

    prompt = QLabel(prompt_)
    prompt.setAlignment(Qt.AlignHCenter)

    button_layout = QHBoxLayout()
    result = [None]
    for i, choice in enumerate(choices):
        button = QPushButton(choice)
        button_layout.addWidget(button)
        def callback(*args, real_i=i):
            result[0] = real_i
            QCoreApplication.quit()
        button.clicked.connect(callback)

    window_layout = QVBoxLayout()
    window_layout.addWidget(prompt)
    window_layout.addSpacing(10)
    window_layout.addLayout(button_layout)
    window.setLayout(window_layout)

    window.show()
    app.exec_()

    return result[0]


if __name__ == '__main__':
    print(choose("Who's da best?", ["me", "you", "a person who isn't here"]))
