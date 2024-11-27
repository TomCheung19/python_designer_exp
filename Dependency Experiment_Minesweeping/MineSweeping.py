import random
import sys
import time

import pygame

# number of mines
MINE_COUNT = 35
# size of each block
SIZE = 20
# rows of the block
BLOCK_ROW_NUM = 16
# column of the block
BLOCK_COL_NUM = 30
# size of the game interface
SCREEN_WIDTH, SCREEN_HEIGHT = BLOCK_COL_NUM * SIZE, (BLOCK_ROW_NUM + 2) * SIZE


def get_mine_flag_num(board_list):
# calculate how many mines are left
    num = 0
    for line in board_list:
        for num_dict in line:
            if num_dict.get("closed_num") == "mine_flag":
                num += 1

    return num


def open_all_mine(board_list):
# show all mines
    for row, line in enumerate(board_list):
        for col, num_dict in enumerate(line):
            if num_dict.get("opened_num") == "mine":
                num_dict["opened"] = True


def get_mine_num(row, col, board_list):
# calculate number of mines around the chosen block
# generate the range of blocks of the chosen position
    row_start = row - 1 if row - 1 >= 0 else row
    row_stop = row + 2 if row + 1 <= BLOCK_ROW_NUM - 1 else row + 1
    col_start = col - 1 if col - 1 >= 0 else col
    col_stop = col + 2 if col + 1 <= BLOCK_COL_NUM - 1 else col + 1

    # calculate the number of mines
    mine_num = 0
    for i in range(row_start, row_stop):
        for j in range(col_start, col_stop):
            if board_list[i][j].get("opened_num") == "mine":
                mine_num += 1
    return mine_num


def set_nums_blank(row, col, board_list):

# see if all blocks around the chosen block are safe
# continue the process until 'find' the mine around

    mine_num = get_mine_num(row, col, board_list)
    print("row=%d, col=%d, mine_num=%d" % (row, col, mine_num))
    if mine_num == 0:
        board_list[row][col]['opened'] = True
        board_list[row][col]["opened_num"] = 0
        board_list[row][col]["closed_num"] = "empty"
        # see if the diagonal blocks are safe
        for i, j in [(-1, -1), (1, 1), (1, -1), (-1, 1)]:
            if 0 <= row + i <= 15 and 0 <= col + j <= 29:
                mine_num = get_mine_num(row + i, col + j, board_list)
                if mine_num:
                    board_list[row + i][col + j]['opened'] = True
                    board_list[row + i][col + j]["opened_num"] = mine_num
                    board_list[row + i][col + j]["closed_num"] = "empty"

        # see if the other 4 positions are empty
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= row + i <= 15 and 0 <= col + j <= 29:
                if not board_list[row + i][col + j].get("opened"):
                    set_nums_blank(row + i, col + j, board_list)
    else:
        board_list[row][col]['opened'] = True
        board_list[row][col]["opened_num"] = mine_num
        board_list[row][col]["closed_num"] = "empty"


def left_click_block(row, col, board_list):
# define the left click

    if board_list[row][col].get("opened") is False and board_list[row][col].get("opened_num") != "mine":
        # come out with the number of surrounding mines of chosen block if there is no mine in the block
        mine_num = get_mine_num(row, col, board_list)
        print("number of mines", mine_num)
        board_list[row][col]["opened_num"] = mine_num
        board_list[row][col]["opened"] = True  # check as opened
        board_list[row][col]["closed_num"] = "empty"  # if not opened then checked as empty to calculate the mines correctly
        if mine_num == 0:
            # see if there are blank blocks nearby
            set_nums_blank(row, col, board_list)
    # if hit the mine
    elif board_list[row][col].get("opened") is False and board_list[row][col].get("opened_num") == "mine":
        board_list[row][col]["opened_num"] = "hit"  # checked as hit
        board_list[row][col]["opened"] = True  # check as opened
        board_list[row][col]["closed_num"] = "empty"  # if not opened then checked as empty to calculate the mines correctly
        return True


def create_random_board(row, col, mine_num):
# generate a random game board
    # 随机布雷
    nums = [{"opened": False, "opened_num": 0, 'closed_num': "empty"} for _ in range(row * col - mine_num)]  # generate blocks except mine blocks
    nums += [{"opened": False, "opened_num": "mine", 'closed_num': "empty"} for _ in range(mine_num)]  # generate mines
    random.shuffle(nums)  # randomize the blocks
    return [list(x) for x in zip(*[iter(nums)] * col)] # return the game board


def right_click_block(row, col, board_list):
# define the right click of flagging mines
    if board_list[row][col].get("opened") is False:
        if board_list[row][col]["closed_num"] == "empty":
            board_list[row][col]["closed_num"] = "mine_flag"
        elif board_list[row][col]["closed_num"] == "mine_flag":
            board_list[row][col]["closed_num"] = "empty"


def click_block(x, y, board_list):
# check the chosen block clicked the cursor
    # calculate the corresponding row and column of the block clicked by the cursor
    for row, line in enumerate(board_list):
        for col, _ in enumerate(line):
            if col * SIZE <= x <= (col + 1) * SIZE and (row + 2) * SIZE <= y <= (row + 2 + 1) * SIZE:
                print("the clicking position is: ", row, col)
                return row, col


def run(screen):
    bgcolor = (225, 225, 225)  # background color

    # show the game board
    board_list = create_random_board(BLOCK_ROW_NUM, BLOCK_COL_NUM, MINE_COUNT)

    # default block image (without clicking)
    img_blank = pygame.image.load('imgs/blank.png').convert()
    img_blank = pygame.transform.smoothscale(img_blank, (SIZE, SIZE))
    # "mine_flag" image
    img_mine_flag = pygame.image.load('imgs/flag.png').convert()
    img_mine_flag = pygame.transform.smoothscale(img_mine_flag, (SIZE, SIZE))
    # "mine" image
    img_mine = pygame.image.load('imgs/mine.png').convert()
    img_mine = pygame.transform.smoothscale(img_mine, (SIZE, SIZE))
    # "hit" image
    img_blood = pygame.image.load('imgs/blood.png').convert()
    img_blood = pygame.transform.smoothscale(img_blood, (SIZE, SIZE))
    # "face" image
    face_size = int(SIZE * 1.25)
    img_face_fail = pygame.image.load('imgs/face_fail.png').convert()
    img_face_fail = pygame.transform.smoothscale(img_face_fail, (face_size, face_size))
    img_face_normal = pygame.image.load('imgs/face_normal.png').convert()
    img_face_normal = pygame.transform.smoothscale(img_face_normal, (face_size, face_size))
    img_face_success = pygame.image.load('imgs/face_success.png').convert()
    img_face_success = pygame.transform.smoothscale(img_face_success, (face_size, face_size))
    # "face" image
    face_pos_x = (SCREEN_WIDTH - face_size) // 2
    face_pos_y = (SIZE * 2 - face_size) // 2
    # the number of mines image
    img0 = pygame.image.load('imgs/unmaskedGrid.png').convert()
    img0 = pygame.transform.smoothscale(img0, (SIZE, SIZE))
    img1 = pygame.image.load('imgs/1.png').convert()
    img1 = pygame.transform.smoothscale(img1, (SIZE, SIZE))
    img2 = pygame.image.load('imgs/2.png').convert()
    img2 = pygame.transform.smoothscale(img2, (SIZE, SIZE))
    img3 = pygame.image.load('imgs/3.png').convert()
    img3 = pygame.transform.smoothscale(img3, (SIZE, SIZE))
    img4 = pygame.image.load('imgs/4.png').convert()
    img4 = pygame.transform.smoothscale(img4, (SIZE, SIZE))
    img5 = pygame.image.load('imgs/5.png').convert()
    img5 = pygame.transform.smoothscale(img5, (SIZE, SIZE))
    img6 = pygame.image.load('imgs/6.png').convert()
    img6 = pygame.transform.smoothscale(img6, (SIZE, SIZE))
    img7 = pygame.image.load('imgs/7.png').convert()
    img7 = pygame.transform.smoothscale(img7, (SIZE, SIZE))
    img8 = pygame.image.load('imgs/8.png').convert()
    img8 = pygame.transform.smoothscale(img8, (SIZE, SIZE))
    img_dict = {
        0: img0,
        1: img1,
        2: img2,
        3: img3,
        4: img4,
        5: img5,
        6: img6,
        7: img7,
        8: img8,
        'mine_flag': img_mine_flag,
        'mine': img_mine,
        'empty': img_blank,
        'hit': img_blood,
    }
    # if you hit the mine then game is over
    game_over = False
    # game status
    game_status = "normal"
    # set the font of the display of remaining mines and used time
    font = pygame.font.SysFont('Arial', SIZE * 2)
    f_width, f_height = font.size('999')
    red = (200, 40, 40)
    # mines flagged
    flag_count = 0
    # time elapsed
    elapsed_time = 0
    last_time = time.time()
    start_record_time = False

    # the clock is to avoid operating while too fast to break down
    clock = pygame.time.Clock()
    while True:
        # check the event such as clicking the mouse and the keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
                b1, b2, b3 = pygame.mouse.get_pressed()
                mouse_click_type = None
                if b1 and not b2 and not b3:  # define what is left-clicking
                    mouse_click_type = "left"
                elif not b1 and not b2 and b3:  # define what is right-clicking
                    mouse_click_type = "right"
                print("the [%s] mouse button is clicked" % mouse_click_type)
                x, y = pygame.mouse.get_pos()
                if game_status == "normal" and 2 * SIZE <= y <= SCREEN_HEIGHT:
                    # calculate the block clicked
                    position = click_block(x, y, board_list)
                    if position:
                        # if right-clicked then update the mines and flags
                        if mouse_click_type == "right":
                            right_click_block(*position, board_list)
                            # update the number of remaining mines
                            flag_count = get_mine_flag_num(board_list)
                            start_record_time = True  # start to record time
                        elif mouse_click_type == "left":
                            # if a safe block is left-clicked
                            game_over = left_click_block(*position, board_list)
                            print("hitting the mine", game_over)
                            flag_count = get_mine_flag_num(board_list)
                            start_record_time = True
                            if game_over:
                                # if lose, then show all the mines
                                open_all_mine(board_list)
                                # set game status to fail
                                game_status = "fail"
                                # stop recording time
                                start_record_time = False
                            elif flag_count == MINE_COUNT:
                                open_all_mine(board_list)
                                # set game status to win
                                game_status = "win"
                                start_record_time = False


                elif face_pos_x <= x <= face_pos_x + face_size and face_pos_y <= y <= face_pos_y + face_size:
                    # start another round
                    print("have pressed the face to quit")
                    pygame.quit()
                    # sys.exit() # do not exit the whole system because there is still a GUI to run

        # set the background color
        screen.fill(bgcolor)

        # show the status of the block
        for i, line in enumerate(board_list):
            for j, num_dict in enumerate(line):
                if num_dict.get("opened"):
                    screen.blit(img_dict[num_dict.get("opened_num")], (j * SIZE, (i + 2) * SIZE))
                else:
                    screen.blit(img_dict[num_dict.get("closed_num")], (j * SIZE, (i + 2) * SIZE))

        # show the face
        if game_status == "win":
            screen.blit(img_face_success, (face_pos_x, face_pos_y))
        elif game_status == "fail":
            screen.blit(img_face_fail, (face_pos_x, face_pos_y))
        else:
            screen.blit(img_face_normal, (face_pos_x, face_pos_y))

        # show the number of remaining mines
        mine_text = font.render('%02d' % (MINE_COUNT - flag_count), True, red)
        screen.blit(mine_text, (30, (SIZE * 2 - f_height) // 2 - 2))

        # show the time elapsed
        if start_record_time and time.time() - last_time >= 1:
            elapsed_time += 1
            last_time = time.time()
        mine_text = font.render('%03d' % elapsed_time, True, red)
        screen.blit(mine_text, (SCREEN_WIDTH - f_width - 30, (SIZE * 2 - f_height) // 2 - 2))

        # show the interface of the game
        pygame.display.update()
        # set FPS
        clock.tick(60)  # run the while 60 time per minute which means 60 FPS


def main():
# start the minesweeping game
    pygame.init()
    pygame.display.set_caption("MineSweeping")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        run(screen)

# main()