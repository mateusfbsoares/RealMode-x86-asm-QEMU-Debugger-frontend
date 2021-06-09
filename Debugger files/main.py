from dearpygui.core import *
from dearpygui.simple import *
import pyautogui
import realmode_debugger
from utils import pretty_prints
import time

width, height = pyautogui.size()

# constants
MAIN_WINDOW_WIDTH = width
MAIN_WINDOW_HEIGHT = height
MAIN_WINDOW_TITLE = "RealMode Debugger"
WRAP_SIZE = 430
BOTTOM = 150

# window object settings
set_main_window_title(MAIN_WINDOW_TITLE)
set_main_window_size(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
set_main_window_pos(0, 0)
# set_global_font_scale(1.25)
set_theme("Dark")

# window names
code_window_name = "CODE"
registers_window_name = "REGISTERS"
stack_window_name = "STACK"


# Functions definitions #
def update_context(sender, data, is_first_call=False):
    array_stack, array_regs_and_flags, array_code = realmode_debugger.get_context(data, is_first_call)

    array_code = pretty_prints.pretty_string_from_array(array_code)
    array_regs_and_flags = pretty_prints.pretty_string_from_array(array_regs_and_flags)
    array_stack = pretty_prints.pretty_string_from_array(array_stack)

    code_text = str(array_code)
    regs_text = str(array_regs_and_flags)
    stack_text = str(array_stack)

    if is_first_call is True:
        add_text(code_text, parent=code_window_name, wrap=WRAP_SIZE)
        add_text(stack_text, parent=stack_window_name, wrap=WRAP_SIZE)
        add_text(regs_text, parent=registers_window_name, wrap=WRAP_SIZE)

    else:
        # This is probably a very very bad way of doing thigs, but I don't have time now to properly do it.. TODO:
        #  make it better
        code_children = get_item_children(code_window_name)
        for i in code_children:
            delete_item(i)

        regs_children = get_item_children(registers_window_name)
        for i in regs_children:
            delete_item(i)

        stack_children = get_item_children(stack_window_name)
        for i in stack_children:
            delete_item(i)

        add_text(code_text, parent=code_window_name, wrap=WRAP_SIZE)
        add_text(regs_text, parent=registers_window_name, wrap=WRAP_SIZE)
        add_text(stack_text, parent=stack_window_name, wrap=WRAP_SIZE)


def single_step(sender, data):
    gdbmi.write("ni")
    update_context(sender=sender, data=data, is_first_call=False)

def step_over_line(sender, data):
    gdbmi.write("stepo")
    update_context(sender=sender, data=data, is_first_call=False)



gdbmi = realmode_debugger.initialize_session()

# Program #
with window(code_window_name, width=int(MAIN_WINDOW_WIDTH / 3), height=MAIN_WINDOW_HEIGHT - BOTTOM):
    set_window_pos(code_window_name, 0, 0)

with window(registers_window_name, width=int(MAIN_WINDOW_WIDTH / 3), height=MAIN_WINDOW_HEIGHT - BOTTOM):
    set_window_pos(registers_window_name, int(MAIN_WINDOW_WIDTH / 3), 0)

with window(stack_window_name, width=int(MAIN_WINDOW_WIDTH / 3), height=MAIN_WINDOW_HEIGHT - BOTTOM):
    set_window_pos(stack_window_name, int(MAIN_WINDOW_WIDTH / 3) * 2, 0)

with window("Interactive Window", width=int(MAIN_WINDOW_WIDTH), height=int(BOTTOM * (6 / 10)), no_title_bar=True):
    set_window_pos("Interactive Window", 0, MAIN_WINDOW_HEIGHT - BOTTOM)
    add_button("Step", callback=single_step, callback_data=gdbmi)
    add_button("Step Over Line", callback=step_over_line, callback_data=gdbmi)

update_context(None, data=gdbmi, is_first_call=True)


def main_callback(sender, data):
    if is_key_pressed(mvKey_Return) or is_key_pressed(mvKey_Spacebar):
        single_step(sender, gdbmi)


set_render_callback(main_callback)

start_dearpygui()
