from dearpygui.core import *
from dearpygui.simple import *


def update_drawing():
    y = get_value("movingArrowY")
    text_y = get_value("movingTextY")

    y2 = get_value("movingArrow2Y")
    text2_y = get_value("movingText2Y")
    # TODO: remove hardcoded magic numbers to a proper way of doing things.
    modify_draw_command("drawing##widget","movingArrow", p1=[200,y], p2=[100, y])
    modify_draw_command("drawing##widget","movingText", pos=[70,text_y])

    modify_draw_command("drawing##widget","movingArrow2", p1=[200,y2], p2=[100, y2])
    modify_draw_command("drawing##widget","movingText2", pos=[70,text2_y])

def arrowUP():
    # set_value("movingArrowY",(get_value("movingArrowY"))-13)
    # set_value("movingTextY",(get_value("movingTextY"))-13)
    update_drawing()

def arrowDOWN():
    # set_value("movingArrowY",(get_value("movingArrowY"))+13)
    # set_value("movingTextY",(get_value("movingTextY"))+13)
    update_drawing()

def arrow2UP():
    set_value("movingArrow2Y",(get_value("movingArrow2Y"))-13)
    set_value("movingText2Y",(get_value("movingText2Y"))-13)
    update_drawing()

def arrow2DOWN():
    set_value("movingArrow2Y",(get_value("movingArrow2Y"))+13)
    set_value("movingText2Y",(get_value("movingText2Y"))+13)
    update_drawing()

