#!/usr/bin/env python2.4

"""
This script is responsible for logging into OSPACE universe, selecting galaxy to play in
and downloading/updating corresponding client
"""
import os

import pygame
from pygame.locals import *

version = (0, 1, 0, "")
versionString = "%d.%d.%d%s" % version

# screen size
screenSize = 640, 480
screenFlags = SWSURFACE

class Widget:
    """This class implements generic Widget"""
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.isFocused = False

    def draw(self, screen):
        # TODO: draw rectangle, in reality, the background will contain all necessary graphics
        # except for texts
        # TODO: how to handle two state elements (button, checkbox)
        screen.fill((0, 64, 0, 255), self.rect)
        pygame.draw.rect(screen, (255, 255, 255, 255), self.rect, 1)
        # draw text
        font = pygame.font.SysFont("arial", 14)
        font.set_underline(self.isFocused)
        surf = font.render(self.text, True, (255, 255, 255, 255))
        screen.blit(surf, (self.rect.topleft))
    
    def onFocus(self):
        self.isFocused = True
    
    def onFocusLost(self):
        self.isFocused = False
    
    def onMouseButtonDown(self, event):
        pass
    
    def onMouseButtonUp(self, event):
        pass
    
    def onKeyDown(self, event):
        pass
    
    def onKeyUp(self, event):
        pass
    
class Label(Widget):
    """This class implements label"""
    pass

class Entry(Widget):
    """This class implements entry"""
    def __init__(self, x, y, width, height, text, char = None):
        Widget.__init__(self, x, y, width, height, text)
        self.char = char
        self.content = text
    
    def onKeyUp(self, event):
        Widget.onKeyUp(self, event)
    
    def onKeyDown(self, event):
        Widget.onKeyDown(self, event)
        if event.unicode == u"\x08":
            self.content = self.content[:-1]
        elif event.unicode in (u"\t", u"\r"):
            # TODO: focus next widget
            pass
        elif event.unicode in (u"\x1b",):
            # ignore
            pass
        else:
            self.content += event.unicode
        if self.char:
            self.text = len(self.content) * self.char
        else:
            self.text = self.content

class Button(Widget):
    """This class implements button"""
    def __init__(self, x, y, width, height, text, onCommand = None):
        Widget.__init__(self, x, y, width, height, text)
        self.onCommand = onCommand
        self.isDown = False
    
    def onFocusLost(self):
        Widget.onFocusLost(self)
        self.isDown = False
    
    def onMouseButtonDown(self, event):
        self.isDown = True
    
    def onMouseButtonUp(self, event):
        print self.isDown and self.onCommand
        if self.isDown and self.onCommand:
            self.onCommand()
        self.isDown = False
        
    def draw(self, screen):
        Widget.draw(self, screen)
        if self.isDown:
            pygame.draw.rect(screen, (0, 255, 0, 255), self.rect, 1)

class Theme:
    
    def __init__(self, name):
        self.name = name
        self.background = pygame.image.load(os.path.join("res", self.name, "background.png")).convert_alpha()
    
class LoginDialog:
    """First dialog that allows user to login or create new account"""
    
    def __init__(self, screen, theme):
        self.screen = screen
        self.focused = None
        self.theme = theme
        self.widgets = [
            Label(10, 10, 100, 20, _("Login")),
            Entry(120, 10, 210, 20, ""),
            Label(10, 40, 100, 20, _("Password")),
            Entry(120, 40, 210, 20, "", char = "*"),
            Button(230, 70, 100, 20, "Login", onCommand = self.onLogin),
            Button(120, 70, 100, 20, "Subscribe", onCommand = self.onNewAccount),
        ]
    
    def onLogin(self):
        print "LOGIN!"
    
    def onNewAccount(self):
        print "NEWACCOUNT!"
    
    def display(self):
        """Event loop"""
        self.draw()
        while True:
            event = pygame.event.wait()
            print event
            if event.type == QUIT:
                break
            elif event.type == MOUSEBUTTONDOWN:
                widget = self.findWidget(event.pos)
                if widget:
                    widget.onMouseButtonDown(event)
                self.draw()
            elif event.type == MOUSEBUTTONUP:
                widget = self.findWidget(event.pos)
                if widget:
                    widget.onMouseButtonUp(event)
                self.draw()
            elif event.type == KEYDOWN:
                if self.focused:
                    self.focused.onKeyDown(event)
                self.draw()
            elif event.type == KEYUP:
                if self.focused:
                    self.focused.onKeyUp(event)
                self.draw()
    
    def findWidget(self, (x, y)):
        for widget in self.widgets:
            if widget.rect.collidepoint(x, y):
                if self.focused and self.focused is not widget:
                    self.focused.onFocusLost()
                self.focused = widget
                widget.onFocus()
                return widget
        # no new widget to focus
        if self.focused:
            self.focused.onFocusLost()
            self.focused = None
    
    def draw(self):
        """Draw elements"""
        # draw background
        self.screen.blit(self.theme.background, (0, 0))
        # draw widgets
        for widget in self.widgets:
            widget.draw(self.screen)
        pygame.display.update()
        
def initLocalization():
    """initialize _ function"""
    # TODO: map it to corresponding locale
    import __builtin__
    __builtin__.__dict__["_"] = lambda x: x

def main():
    """Setup display and stard dialogue with a user"""
    initLocalization()
    # initialize pygame
    pygame.init()
    # main screen
    bestDepth = pygame.display.mode_ok(screenSize, screenFlags)
    screen = pygame.display.set_mode(screenSize, screenFlags, bestDepth)
    pygame.mouse.set_visible(True)
    pygame.display.set_caption(_("Outer Space Launcher %s") % versionString)
    pygame.display.set_icon(pygame.image.load("res/icon32.png").convert_alpha())
    # theme
    theme = Theme("basicTheme")
    # draw login dialog
    dlg = LoginDialog(screen, theme)
    dlg.display()
    # close screen
    pygame.display.quit()
    # launch synchronized application
    pass

main()
