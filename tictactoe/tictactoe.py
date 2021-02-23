# write your code here
def display_board(states):
    print('---------')
    print('| ' + states[0] + ' ' + states[1] + ' ' + states[2] + ' |')
    print('| ' + states[3] + ' ' + states[4] + ' ' + states[5] + ' |')
    print('| ' + states[6] + ' ' + states[7] + ' ' + states[8] + ' |')
    print('---------')

string = input()
display_board(list(string))