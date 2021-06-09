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
    array_code = output_array[i:]

		# customize code string
    array_code_aux = []
    for i in array_code:
        array_code_aux.append(i.replace("\\n", ''))

    array_code = array_code_aux

    # customize registers string
    array_regs = []
    for i in range(7):
        string = array_regs_and_flags[i]
        string_len_half = int(len(string) / 2)
        array_regs.append(string[:string_len_half].replace(' ', '').replace('\n', ''))
        array_regs.append(string[string_len_half:].replace(' ', '').replace('\n', ''))
    for i in range(7, len(array_regs_and_flags)):
        array_regs.append(array_regs_and_flags[i].replace(' ', '').replace('\n', ''))

    # customize stack string
    array_stack.append("")
    array_stack.append("STACK")
    array_stack.reverse()
    array_stack.pop()
    array_stack[0] += "    ^     - lower memory adresses"
    for i in range(2, len(array_stack)):
        array_stack[i] += "    |"
    array_stack[-1] += "     + higher memory adresses"

    return array_stack, array_regs, array_code
