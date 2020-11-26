import random
import time

def main():
    while True:
        mode = start()
        if mode != None:
            play(mode)
        else:
            print('Goodbye :)')
            break
            
    
    #display(board)

def start():
    while True:
        print('Please choose the diffciulty\neasy: 9*9 board, 10 mines\nnormal: 16*16 board, 40 mines\nhard: 16*30 board, 99 mines\n')
        #print('Type e for easy; n for normal; h for hard')
        ip = input('Type e for easy; n for normal; h for hard; q for quit: ')
        if ip == 'e':
            return [9,9,10]
        if ip == 'n':
            return [16,16,40]
        if ip == 'h':
            return [16,30,99]
        if ip == 'q':
            return None


def play(mode):
    board = [[0 for x in range(mode[1])]for y in range(mode[0])] #the actual board that's not covered
    board_display = [['.' for x in range(mode[1])]for y in range(mode[0])] #initially covered board for printing
    create_mines(board,board_display,mode)
    neighbours(board)
    mines = mode[2]
    turn = 0#moves taken
    lost = False
    #display(board)
    count = 0#total number of blocks revealed (excluding mines)
    start_time = time.time()
    t = 0 #time taken
    while lost == False and count < mode[0]*mode[1]-mode[2]:
        display(board_display)
        print('Remainning mines: ' + str(mines) + ', Moves made: ' + str(turn) + ' ,Blocks Revealed: ' + str(count) + ', Time taken: ' + str(t)+ ' secs\n')
        #print('Please choose your next move')
        ip = input('You can take actions, r for the reveal, f for a flag, or unflag\nPlease choose your next move in the form: row, column, action. Split each of them with a comma: ').split(',')
        valid = False #the input is valid or not
        if len(ip) == 3:
            if ip[0] in [str(x) for x in range(len(board))] and ip[1] in [str(x) for x in range(len(board[0]))] and ip[2] in ['r','f']:#if the input is in legal format
                r = int(ip[0])
                c = int(ip[1])
                if not board_display[r][c] in range(9):#if the chosen block has been revealed
                    t = round(time.time()-start_time,2)
                    valid = True
                    
                    if ip[2] == 'r':
                        
                        [lost,count] = reveal(board,board_display,r,c,count)
                        #count += reveal(board,board_display,r,c)[1]
                    if ip[2] == 'f':
                        if board_display[r][c] == 'f':
                            board_display[r][c] = '.'
                            mines +=1
                        elif board_display[r][c] ==  '.':
                            board_display[r][c] = 'f'
                            mines -=1
                else:
                    print('The block [' + str(r) + ',' + str(c) + '] has been revealed, choose another block')
             
        if valid == False:
            print('Invalid input.\nAn example of valid input: 0,0,r means reveal the block on row 0 column 0\nYou can only flag or reveal blcoks that have not been revealed')
        
        
        else:
            turn += 1
        
        #display(board)
##        if count < mode[0]*mode[1]-mode[2]:
##            display(board_display)
##            print('Remainning mines: ' + str(mines) + ', Moves made: ' + str(turn) + ' ,Blocks Revealed: ' + str(count) )
        
    reveal_mines(board,board_display)
    print_result(lost, board_display, t, turn, count)
        
    return

def print_result(lost, board_display, t, turn, count):
    display(board_display)
    if lost:
        print('You stepped on a mine!')
    else:
        print('Congratulations, you win!!!')
    print('You spent ' + str(t) + ' secs on this game, successfully revealed ' + str(count) + ' blocks that are not mine using ' + str(turn) + ' moves.\n')
    return
        
def reveal_mines(board,board_display):
    for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == -1:
                    board_display[row][col] = '*'

def reveal(board,board_display,r,c,count):
    count_m = 0 #number of blocks revealed by this move
    lost = False
    if board[r][c] == -1:#stepped on a mine
        lost = True
        #reveal_mines(board,board_display)
    elif board[r][c] != 0:
        board_display[r][c] = board[r][c]
        count += 1
    else:
        count += reveal_check(board,board_display,r,c)
        
        
    
        
    
    return [lost,count+count_m]

def reveal_check(board,board_display,row,col):
    search_queue = [[row,col]]
    p = 0 #current position in the queue
    r = len(board)
    c = len(board[0])
    board_display[row][col] = board[row][col]
    count = 1 #number of blocks reavled by this move
    
    while len(search_queue) > p:#using bfs, search and reveal blocks
        row = search_queue[p][0]
        col = search_queue[p][1]
        if row > 0 and col > 0:
            if board[row-1][col-1] == 0 and ([row-1,col-1] in search_queue) == False:
                search_queue.append([row-1,col-1])
            if board_display[row-1][col-1] == '.':
                count += 1
                
                board_display[row-1][col-1] = board[row-1][col-1]
            
        if row > 0:
            if board[row-1][col] == 0 and ([row-1,col] in search_queue) == False:
                search_queue.append([row-1,col])
            if board_display[row-1][col] == '.':
                count += 1
            
                board_display[row-1][col] = board[row-1][col]
            
        if row > 0 and col < c-1:
            if board[row-1][col+1] == 0 and ([row-1,col+1] in search_queue) == False:
                search_queue.append([row-1,col+1])
            if board_display[row-1][col+1] == '.':
                count += 1
            
                board_display[row-1][col+1] = board[row-1][col+1]
            
        if col > 0:
            if board[row][col-1] == 0 and ([row,col-1] in search_queue) == False:
                search_queue.append([row,col-1])
            if board_display[row][col-1] == '.':
                count += 1
            
                board_display[row][col-1] = board[row][col-1]
            
        if col < c-1:
            if board[row][col+1] == 0 and ([row,col+1] in search_queue) == False:
                search_queue.append([row,col+1])
            if board_display[row][col+1] == '.':
                count += 1
            
                board_display[row][col+1] = board[row][col+1]
            
        if row < r-1 and col > 0:
            if board[row+1][col-1] == 0 and ([row+1,col-1] in search_queue) == False:
                search_queue.append([row+1,col-1])
            if board_display[row+1][col-1] == '.':
                count += 1
            
                board_display[row+1][col-1] = board[row+1][col-1]
            
        if row < r-1:
            if board[row+1][col] == 0 and ([row+1,col] in search_queue) == False:
                search_queue.append([row+1,col])
            if board_display[row+1][col] == '.':
                count += 1
            
                board_display[row+1][col] = board[row+1][col]
            
        if row < r-1 and col < c-1:
            if board[row+1][col+1] == 0 and ([row+1,col+1] in search_queue) == False:
                search_queue.append([row+1,col+1])
            if board_display[row+1][col+1] == '.':
                count += 1
            
                board_display[row+1][col+1] = board[row+1][col+1]
        p += 1
    return count
    

##def create_board(mode):
##        
##    board = [[0 for x in range(mode[1])]for y in range(mode[0])]
##    #for row in range(mode[0]):
##        #for col in range(mode[1]):
##        #board.append([0 for x in range(mode[1])])
##
##    create_mines(board,mode)
##    neighbours(board)
##
##    
##    return board


def create_mines(board,board_display,mode):
    mine_count = 0
    while(mine_count < mode[2]):
        row = random.choice(range(mode[0]))
        col = random.choice(range(mode[1]))
        if board[row][col] != -1 and board_display[row][col] == '.':
            board[row][col] = -1
            mine_count += 1

    return board
    
def neighbours(board):
    r = len(board)
    c = len(board[0])
    for row in range(r):
        for col in range(c):
            if board[row][col] == -1:
                #increase the number of the neibouring blocks of a mine block that are not mine blocks by 1
                if row > 0 and col > 0 and board[row-1][col-1] != -1:
                    board[row-1][col-1] += 1
                if row > 0 and board[row-1][col] != -1:
                    board[row-1][col] += 1
                if row > 0 and col < c-1 and board[row-1][col+1] != -1:
                    board[row-1][col+1] += 1
                if col > 0 and board[row][col-1] != -1:
                    board[row][col-1] += 1
                if col < c-1 and board[row][col+1] != -1:
                    board[row][col+1] += 1
                if row < r-1 and col > 0 and board[row+1][col-1] != -1:
                    board[row+1][col-1] += 1
                if row < r-1 and board[row+1][col] != -1:
                    board[row+1][col] += 1
                if row < r-1 and col < c-1 and board[row+1][col+1] != -1:
                    board[row+1][col+1] += 1
    return board          
            


    
def display(board):
    board_print = ''
    board_print += '\n'
    for row in range(len(board)+1):
        #print(board[row])
        #board_print.append('')
        if row > 0:
            board_print += str(row-1)
            if row > 10:
                board_print += '   '
            else:
                board_print += '    '
        else:
            board_print += '     '
        
            
        for col in range(len(board[0])):
            if row == 0:
                if col < 10:
                    board_print += '  ' + str(col)
                else:
                    board_print += ' ' + str(col)
            else:

                board_print += '  '+ str(board[row-1][col])

            if col == len(board[0])-1:
                board_print +='\n\n'
                if row == 0:
                    board_print += '\n'
    
    print(board_print)
main()
                


    
        
