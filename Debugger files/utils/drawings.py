from dearpygui.core import *
from dearpygui.simple import *


def update_drawing():
    y = get_value("arrowY")
    text_y = get_value("textY")
    # TODO: remove hardcoded magic numbers to a proper way of doing things.
    modify_draw_command("drawing##widget","movingArrow", p1=[200,y], p2=[100, y])
    modify_draw_command("drawing##widget","movingText", pos=[70,text_y])

def arrowUP():
    set_value("arrowY",(get_value("arrowY"))-13)
    set_value("textY",(get_value("textY"))-13)
    update_drawing()

def arrowDOWN():
    set_value("arrowY",(get_value("arrowY"))+13)
    set_value("textY",(get_value("textY"))+13)
    update_drawing()
