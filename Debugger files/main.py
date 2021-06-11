# TODO: make the code more modular --> create separated .py files for each functionality and improt here

from dearpygui.core import *
from dearpygui.simple import *
import pyautogui
import realmode_debugger
from utils import pretty_prints
import time
from utils import drawings

# The way I'm using global vars is horrible. TODO: fix this as soon as possible!
import global_vars

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
drawings_window_name = ""


# Function definitions #
def sendInputToGDB():
    input_str =get_value("gdbInput")
    output_str = ""
    response = gdbmi.write(input_str)
    for i in range(1,len(response)-1):
        output_str += str(response[i]["payload"]) + '\n'
    set_value("gdbOutput", output_str)

def update_context(sender, data, is_end_of_program=False, is_first_call=False, update_text=True):
    current_instruction = ''
   
    array_stack, array_regs_and_flags, array_code = realmode_debugger.get_context(data, is_first_call)

    array_code = pretty_prints.pretty_string_from_array(array_code)
    array_regs_and_flags = pretty_prints.pretty_string_from_array(array_regs_and_flags)
    array_stack = pretty_prints.pretty_string_from_array(array_stack)

    code_text = str(array_code)
    regs_text = str(array_regs_and_flags)
    stack_text = str(array_stack)

    # if update_text is false, it means we want to use this function to get the current instrucion
    if update_text is False:
        first_code_text_line = ""
        current_char = ''
        i = 0
        while current_char!='\n':
            current_char = code_text[i]
            first_code_text_line += current_char
            i += 1
        # catch interrupts
        if " int "in first_code_text_line:
            current_instruction = "int"
        # catch end of program
        # if "0x7e17" in first_code_text_line:
        #     current_instruction = "end_of_program"
        if " push " in first_code_text_line:
            if global_vars.STACK_DEPTH == 0:
                global_vars.STACK_DEPTH += 1
                drawings.arrowDOWN()
                drawings.arrow2DOWN()
            else:
                global_vars.STACK_DEPTH += 1
                drawings.arrow2DOWN()

        if " pop " in first_code_text_line:
            if global_vars.STACK_DEPTH == 1:
                global_vars.STACK_DEPTH -= 1
                drawings.arrow2UP()
                drawings.arrowUP()
            else:
                global_vars.STACK_DEPTH -= 1
                drawings.arrow2UP()
        if "add " in first_code_text_line and "sp" in first_code_text_line:
            hex_number = first_code_text_line.split(',')[1]
            number = int(hex_number, 16)
            number = int(number/2)
            for i in range(number):
                if global_vars.STACK_DEPTH == 1:
                    global_vars.STACK_DEPTH -= 1
                    drawings.arrow2UP()
                    drawings.arrowUP()
                else:
                    global_vars.STACK_DEPTH -= 1
                    drawings.arrow2UP()

        if "sub " in first_code_text_line and "sp" in first_code_text_line:
            hex_number = first_code_text_line.split(',')[1]
            number = int(hex_number, 16)
            number = int(number / 2)
            for i in range(number):
                if global_vars.STACK_DEPTH == 0:
                    global_vars.STACK_DEPTH += 1
                    drawings.arrowDOWN()
                    drawings.arrow2DOWN()
                else:
                    global_vars.STACK_DEPTH += 1
                    drawings.arrow2DOWN()


        return current_instruction

    if update_text is True:
        if is_first_call is True:
            add_text(code_text, parent=code_window_name, wrap=WRAP_SIZE)
            add_text(stack_text, parent=stack_window_name, wrap=WRAP_SIZE)
            add_text(regs_text, parent=registers_window_name, wrap=WRAP_SIZE)

        else:
            # This is probably a bad way of doing thigs, but I don't have time now to properly do it.
            # TODO: write a better way of updating text other than deleting the current and instaciating a new one.
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
    current_instruction = ''
    current_instruction = update_context(sender=sender, data=data, is_first_call=False, update_text=False)
    if current_instruction=="end_of_program":
        # this code is repeated from below. TODO: make a separate function "clear_texts" to improve reusability. got no time for that now ;)
        code_children = get_item_children(code_window_name)
        for i in code_children:
            delete_item(i)
        # TODO: improve reusability here too. same as the TODO above.
        add_text("\n\n############# Reached End Of Program #############", parent=code_window_name, wrap=WRAP_SIZE)
        return 1
 
    elif current_instruction=="int":
        gdbmi.write("stepo")
        update_context(sender=sender, data=data, is_first_call=False)
    else:

        gdbmi.write("ni")
        update_context(sender=sender, data=data, is_first_call=False)
    

gdbmi = realmode_debugger.initialize_session()

# Program #
with window(code_window_name, width=int(MAIN_WINDOW_WIDTH / 3), height=MAIN_WINDOW_HEIGHT - BOTTOM, no_close=True, no_bring_to_front_on_focus=True, no_move=True, no_resize=True):
    set_window_pos(code_window_name, 0, 0)

with window(registers_window_name, width=int((MAIN_WINDOW_WIDTH / 3)/2), height=MAIN_WINDOW_HEIGHT - BOTTOM, no_close=True, no_bring_to_front_on_focus=True, no_move=True, no_resize=True):
    set_window_pos(registers_window_name, int(MAIN_WINDOW_WIDTH / 3), 0)

with window(drawings_window_name, width=int((MAIN_WINDOW_WIDTH / 3)/2) + 3, height=MAIN_WINDOW_HEIGHT - BOTTOM, no_scrollbar=True, no_close=True, no_bring_to_front_on_focus=True, no_move=True, no_resize=True):
    set_window_pos(drawings_window_name, int(MAIN_WINDOW_WIDTH / 3) + int((MAIN_WINDOW_WIDTH / 3)/2), 0)
    add_drawing(".", width=int((MAIN_WINDOW_WIDTH / 3)/2) + 3, height=20)
    add_drawing("drawing##widget", width=int((MAIN_WINDOW_WIDTH / 3)/2) + 3, height=int(MAIN_WINDOW_HEIGHT - BOTTOM))
 
    add_value("movingArrowY",8)
    add_value("movingTextY", 0)

    add_value("movingArrow2Y", -5)
    add_value("movingText2Y", 0)

    # TODO: de-hardcode all the magic values and make this code better.
    draw_arrow("drawing##widget",[200, 8], [100, 8], [0, 255, 0], 1, 10, tag="movingArrow")
    draw_text("drawing##widget",text="SP", pos=[70, 0], size=18, tag="movingText")

    draw_arrow("drawing##widget",[200, -5], [100, -5], [255, 0, 0], 1, 10, tag="movingArrow2")
    draw_text("drawing##widget",text="End of\nStack", pos=[70, 7], size=18, tag="movingText2")

with window(stack_window_name, width=int(MAIN_WINDOW_WIDTH / 3), height=MAIN_WINDOW_HEIGHT - BOTTOM, no_close=True, no_bring_to_front_on_focus=True, no_move=True, no_resize=True):
    set_window_pos(stack_window_name, int(MAIN_WINDOW_WIDTH / 3) * 2, 0)

with window("Interactive Window", width=int(MAIN_WINDOW_WIDTH/3), height=int(BOTTOM * (6 / 10)), no_title_bar=True, no_close=True, no_bring_to_front_on_focus=True, no_move=True, no_resize=True):
    set_window_pos("Interactive Window", 0, MAIN_WINDOW_HEIGHT - BOTTOM)
    add_button("Step", callback=single_step, callback_data=gdbmi)

with window("Interactive Window 2", width=int(MAIN_WINDOW_WIDTH/3), height=int(BOTTOM * (6 / 10)), no_title_bar=True, no_close=True, no_bring_to_front_on_focus=True, no_move=True, no_resize=True):
    set_window_pos("Interactive Window 2", int(MAIN_WINDOW_WIDTH/3), MAIN_WINDOW_HEIGHT - BOTTOM)
    add_input_text("gdbInput",hint="write to gdb", width=100)
    add_button("sendInput", callback=sendInputToGDB)
with window("GDB output", width=int(MAIN_WINDOW_WIDTH/3), height=int(BOTTOM * (6 / 10)), no_title_bar=False, no_close=True, no_bring_to_front_on_focus=True, no_move=True, no_resize=True):
    set_window_pos("GDB output", int(MAIN_WINDOW_WIDTH/3 * 2), MAIN_WINDOW_HEIGHT - BOTTOM)
    add_text(name="gdbOutput")
 

update_context(None, data=gdbmi, is_first_call=True)


def main_callback(sender, data):
    if is_key_pressed(mvKey_Return):
        single_step(sender, gdbmi)



set_render_callback(main_callback)

start_dearpygui()
