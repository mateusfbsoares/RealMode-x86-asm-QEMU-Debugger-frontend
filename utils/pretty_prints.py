def pretty_print_array(array):
    for i in array:
        print(i)


def pretty_string_from_array(array):
    string = ""
    for i in array:
        i = i.replace(":\\t", " ")
        string = string + str(i) + "\n"
    return string

# # input loop
# p = input()
# while p!="exit":
#     if p=="stack":
#         pretty_print_array(array_stack)
#     elif p=="reg":
#         pretty_print_array(array_regs_and_flags)
#     elif p=="code":
#         pretty_print_array(array_code)
#     print('')
#     p = input()
