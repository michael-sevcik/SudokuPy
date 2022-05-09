import pygame as pg
from GUI import GUI_class
from sys import exit

windowStartupWidth = 550
windowStartupHeight = 550
fpsRate = 30

def main():
    GUI = GUI_class(550, 550, 30)

    run = True
    while run:
        run = GUI.check()
        #events = pg.event.get()
        #for event in events:
        #    if event.type == pg.VIDEORESIZE:
        #        GUI.resize(event.size)
        #    if event.type == pg.MOUSEBUTTONUP and event.button == 1:
        #        GUI.mouse_click(events)
        #    if event.type == pg.QUIT:
        #        pg.quit()
        #        run = False
        #        exit()
        #    if GUI.isElementPicked and event.type == pg.KEYDOWN:
        #        GUI.key_pressed(event)
        
        #print(int(GUI.fpsClock.get_fps()))
        #GUI.FPS_hold()

if __name__ == '__main__':
    main()