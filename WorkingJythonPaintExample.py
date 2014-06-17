#!/usr/local/bin/jython
# -*- coding: utf-8 -*-

"""
ZetCode Jython Swing tutorial

This program draws ten
rectangles filled with different
colors.

author: Jan Bodnar
website: www.zetcode.com
last modified: November 2010
"""

from java.awt import Color
from javax.swing import JFrame
from javax.swing import JPanel

class Canvas(JPanel):

    def __init__(self):
        super(Canvas, self).__init__()

    def paintComponent(self, g):

        self.drawColorRectangles(g)

    def drawColorRectangles(self, g):

        g.setColor(Color(125, 167, 116))
        g.fillRect(10, 15, 90, 60)

        g.setColor(Color(42, 179, 231))
        g.fillRect(130, 15, 90, 60)

        g.setColor(Color(70, 67, 123))
        g.fillRect(250, 15, 90, 60)

        g.setColor(Color(130, 100, 84))
        g.fillRect(10, 105, 90, 60)

        g.setColor(Color(252, 211, 61))
        g.fillRect(130, 105, 90, 60)

        g.setColor(Color(241, 98, 69))
        g.fillRect(250, 105, 90, 60)

        g.setColor(Color(217, 146, 54))
        g.fillRect(10, 195, 90, 60)

        g.setColor(Color(63, 121, 186))
        g.fillRect(130, 195, 90, 60)

        g.setColor(Color(31, 21, 1))
        g.fillRect(250, 195, 90, 60)
        

class Example(JFrame):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.canvas = Canvas()
        self.getContentPane().add(self.canvas)
        self.setTitle("Colors")
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setSize(360, 300)
        self.setLocationRelativeTo(None)
        self.setVisible(True)


if __name__ == '__main__':
    Example()
