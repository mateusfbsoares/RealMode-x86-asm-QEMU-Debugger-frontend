from pygdbmi.gdbcontroller import GdbController


def trim_by_part_and_type(response, type, part):
    """ get specific data """
    array = []
    for item in response:
        if item['type'] == type:
            array.append(item[part])
    return array


def initialize_session():
    # Start gdb process
    gdbmi = GdbController(['gdb', '-x', '.gdbinit', '--interpreter=mi3'])

    # Initial commands
    gdbmi.write('target remote localhost:1234')
    gdbmi.write('break *0x7e00')
    gdbmi.write('continue')
    return gdbmi


def get_context(gdbmi, is_first_call=False):
    response = gdbmi.write('context')
    # Get array with console output
    output_array = trim_by_part_and_type(response, 'console', 'payload')

    # cuts out first (repeated) half if its the first call
    if is_first_call is True:
        half_lenght = len(output_array) // 2
        output_array = output_array[:half_lenght]

    # Divides data in diferent arrays
    array_stack = []
    array_regs_and_flags = []
    array_code = []
    i = 0
    while output_array[i] != "REGISTERS":
        array_stack.append(output_array[i])
        i += 1
    i += 1
    while output_array[i] != "CODE":
        array_regs_and_flags.append(output_array[i])
        i += 1
    i += 1
    

    # get code string
    # array_code = output_array[i:] # we are not getting the code from the context user-defined command of the gdbinit. below is how we are getting it now.
    array_code = []
    full_code = gdbmi.write("x/40i $eip")
    for i in range(1,len(full_code)-1):
        array_code.append(full_code[i]["payload"].replace("\\n", ""))

    # array_code = array_code_aux

    # customize registers string
    # this is kinda repetitive. TODO: improve this block of code. make it more consise 
    array_regs = []
    #   remove spaces and \n's
    for i in range(7):
        string = array_regs_and_flags[i]
        string_len_half = int(len(string) / 2)
        array_regs.append(string[:string_len_half].replace(' ', '').replace('\n', ''))
        array_regs.append(string[string_len_half:].replace(' ', '').replace('\n', ''))
    for i in range(7, len(array_regs_and_flags)):
        array_regs.append(array_regs_and_flags[i].replace(' ', '').replace('\n', ''))
    #   do more slices
    array_regs = []
    for i in range(7):
        array_regs.append(array_regs_and_flags[i][:9])
        array_regs.append(array_regs_and_flags[i][9:])
    for i in range(7, len(array_regs_and_flags)):
        array_regs.append(array_regs_and_flags[i])
    array_regs_and_flags = array_regs
    # the block of code below makes the program incredibly slow, thus, I disabled it. TODO: optimize and enable it 
    #   add vaue for pointer registers 
    # for i in range(len(array_regs_and_flags)):
    #     if "SI" in array_regs_and_flags[i]:
    #         value = gdbmi.write(f"x {array_regs_and_flags[i][4:9]}")[1]["payload"]
    #         array_regs_and_flags[i] += f" --> {value}"
    #     elif "DI" in array_regs_and_flags[i]:
    #         value = gdbmi.write(f"x {array_regs_and_flags[i][4:9]}")[1]["payload"]
    #         array_regs_and_flags[i] += f" --> {value}"
    #     elif "SP" in array_regs_and_flags[i]:
    #         value = gdbmi.write(f"x {array_regs_and_flags[i][4:9]}")[1]["payload"]
    #         array_regs_and_flags[i] += f" --> {value}"
    #     elif "BP" in array_regs_and_flags[i]:
    #         value = gdbmi.write(f"x {array_regs_and_flags[i][4:9]}")[1]["payload"]
    #         array_regs_and_flags[i] += f" --> {value}"
    #     elif "CS" in array_regs_and_flags[i]:
    #         value = gdbmi.write(f"x {array_regs_and_flags[i][4:9]}")[1]["payload"]
    #         array_regs_and_flags[i] += f" --> {value}"
    #     elif "DS" in array_regs_and_flags[i]:
    #         value = gdbmi.write(f"x {array_regs_and_flags[i][4:9]}")[1]["payload"]
    #         array_regs_and_flags[i] += f" --> {value}"
    #     elif "ES" in array_regs_and_flags[i]:
    #         value = gdbmi.write(f"x {array_regs_and_flags[i][4:9]}")[1]["payload"]
    #         array_regs_and_flags[i] += f" --> {value}"
    #     elif "SS" in array_regs_and_flags[i]:
    #         value = gdbmi.write(f"x {array_regs_and_flags[i][4:9]}")[1]["payload"]
    #         array_regs_and_flags[i] += f" --> {value}"
    #     elif "IP" in array_regs_and_flags[i]:
    #         value = gdbmi.write(f"x {array_regs_and_flags[i][4:9]}")[1]["payload"]
    #         array_regs_and_flags[i] += f" --> {value}"

    # customize stack string
    space_str = " "
    array_stack.append("")
    array_stack.reverse()
    array_stack.pop()
    for i in range(2, len(array_stack)):
        ascii = f"{str(bytes.fromhex(array_stack[i]))}"
        ascii_len = len(ascii)
        integer = int(array_stack[i],16)
        array_stack[i] +=  f"  {ascii} {space_str * (18-ascii_len)} {integer}  "
        #     array_stack[i] += '\n'

    array_stack.reverse()
    array_stack.insert(0, "HEXA     ASCII            INTEGER  - lower memory adresses\n")
    array_stack[-1] += f"{space_str*36}+ higher memory adresses"
    return array_stack, array_regs, array_code
