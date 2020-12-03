################################################################################
##
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PyQt5
# V: 1.0.0
##
################################################################################

# ==> GUI FILE
from main import *


class UIFunctions(MainWindow):

    def toggleMenu(self, maxHeight, enable):
        if enable:

            # GET WIDTH
            height = self.Top_Bar.height()
            maxExtend = maxHeight
            standard = 40

            # SET MAX WIDTH
            if height == 40:
                heightExtended = maxExtend
            else:
                heightExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(
                self.Top_Bar, b"minimumHeight")
            self.animation.setDuration(400)
            self.animation.setStartValue(height)
            self.animation.setEndValue(heightExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
