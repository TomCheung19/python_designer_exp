###########################################################################
###########################################################################

	# The programme aims at replicating the original urn game experiment as closely as possible, especially the process
    # of drawing from the distribution of ambiguous urn, and make it robust to other similar experiments of different conditions,
    # to experiments of more trials and to experiments with conditions as a within variable. Details could be seen in notes.
    # I planned to progress and link the experiment with only buttons, so the functions, applications and computation are
    # included in the button. So every button is different and the button is the key part of the programmme.
    # Written by BCGM8

###########################################################################
###########################################################################

from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QSound
from random import *
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

import random
import sys
import time
import pygame
import test_2

# load the interface as usual
app = QApplication([])
window = uic.loadUi("Assignment2_BCGM8.ui")

# initialize the interface such as hide the error messages
window.Error_message_lbl.hide()

class Experiment:
    # inputs are conditions in format of list eg. [2, 10, 100]
    #            ratios in format of list and tuple eg. [(2,0), (8,2), (53,47)]
    #            outputfile(optional, default is results.csv) in format of string
    def __init__(self, condition, ratio_each_condition, outputfile = "results.csv"):
        self.condition = condition
        self.condition_num = len(self.condition)
        self.ratio_each_condition = ratio_each_condition
        self.current_condition = None
        self.outputfile = outputfile
        self.current_page_index = 0
        self.result_list = []
        # the practice in experiment should be set down instead of being randomly generated
        self.practice_ambiguous_urn_label = "B"
        self.practice_certain_urn_label = "A"

    def step_forward(self):
        self.current_page_index += 1
        window.experiment_window.setCurrentIndex(self.current_page_index)


    def start_exp(self):

        # first determine which condition should be by checking how many participants we have, then evenly separate the /
        # new participants
        self.read_existing_file = open(self.outputfile, 'a', encoding= 'UTF-8') # create the result file if there is none.
        self.read_existing_file.close()
        self.read_existing_file = open(self.outputfile, 'r', encoding= 'UTF-8')
        self.all_existing_participants = len(self.read_existing_file.readlines())
        self.read_existing_file.close()


        self.current_condition = self.condition[int(self.all_existing_participants % self.condition_num)]

        self.current_ratio = self.ratio_each_condition[self.condition.index(self.current_condition)]

        # set up to hide the practice buttons and pics. These could be anywhere before the practice
        window.Practice_Choice_A_continue_bn.hide()
        window.Practice_Choice_B_continue_bn.hide()
        window.Practice_Result_A_blue_marble_pic.hide()
        window.Practice_Result_A_red_marble_pic.hide()
        window.Practice_Result_B_blue_marble_pic.hide()
        window.Practice_Result_B_red_marble_pic.hide()

        self.step_forward()

    def check_consent(self):
        if window.Consent_checkbox.isChecked():
            self.step_forward()
            test_2.main()
            window.close()
        else:
            window.consent_box = QMessageBox.about(window,'Error','Please tick the consent or you could exit the experiment.')
            window.consent_box.show()

    def check_demog(self):
        self.age = window.Age_spinbox.value()
        # here we use comboBox to get gender and education so that we could easily have more options
        self.gender = window.Gender_comboBox.currentText()
        self.education = window.Education_comboBox.currentText()
        self.contact = window.Contact_txt.toPlainText()
        self.error_message = "" # clear the message in case the second error
        # here we allow participants to choose age from 1 to
        if self.age < 12 or self.age > 90:
            self.error_message = "Error! Please choose the appropriate age then press the 'continue' button."
        elif self.gender == "":
            self.error_message = "Error! Please choose the appropriate gender then press the 'continue' button."
        elif self.education == "":
            self.error_message = "Error! Please choose the appropriate education level then press the 'continue' button."
        # the contact information is not important and we can leave it as the instruction text to avoid missing value.
        window.Error_message_lbl.setText(self.error_message)
        window.Error_message_lbl.show()

        if self.error_message == "":
            window.close()
            self.step_forward()

    def generation_of_practice_certain_urn_results(self):
        # It is same as the generation for formal experiment /
        # More notes to explain the process could be find below in the generation_of_certain_urn_results function
        self.practice_certain_urn_drawing = choice(["blue", "red"])  # because it is even, only need to choose from "blue" and "red"
        self.practice_trial_result = self.practice_certain_urn_drawing

    def generation_of_practice_ambiguous_urn_results(self):
        # It is same as the generation for formal experiment instead of the number of total marbles is set to 100 /
        # More notes to explain the process could be find below in the generation_of_ambiguous_urn_results function
        self.practice_ambiguous_urn_distribution = []
        self.practice_num_red_ball = 53
        self.practice_num_blue_ball = 47
        for practice_red_ball in range(0, self.practice_num_red_ball):
            self.practice_ambiguous_urn_distribution.append("red")
        for practice_blue_ball in range(0, self.practice_num_blue_ball):
            self.practice_ambiguous_urn_distribution.append("blue")
        self.practice_ambiguous_urn_drawing = choice(self.practice_ambiguous_urn_distribution)
        self.practice_trial_result = self.practice_ambiguous_urn_drawing


    def practice_choice_A(self):

        self.practice_current_trial_choice_urn_label = "A"
        window.Practice_Choice_A_continue_bn.show()
        self.practice_selected_urn = 1
        self.generation_of_practice_certain_urn_results()

        if self.practice_trial_result == "red":
            self.practice_losing_result_text = "Ooops. It is the red marble. Sorry, but you lose. Try to win next time."
            window.Practice_Results_lbl.setText(self.practice_losing_result_text)
            # the animates below makes the marble move out of the urn and vertically up
            window.practice_A_red_marble_animation = QPropertyAnimation(window.Practice_Result_A_red_marble_pic, b'pos')
            window.practice_A_red_marble_animation.setDuration(2000)
            # notice that QPoint only have the position coordinates and the setGeometry needs the width and height of the objects
            # And I use hard codes here for position, because I use the QLayouts in the interface. So it is set and being set /
            # is better for the real experiment.
            window.practice_A_red_marble_animation.setStartValue(QPoint(290, 480))
            window.practice_A_red_marble_animation.setEndValue(QPoint(290, 350))
            window.practice_A_red_marble_animation.start()
            window.Practice_Result_A_red_marble_pic.show()

        else:
            self.practice_winning_result_text = "It is the blue marble! Congratulations! You win!"
            window.Practice_Results_lbl.setText(self.practice_winning_result_text)
            # here I add a 'yeah' sound to celebrate the winning
            window.practice_winning_sound = QSound('yeah.wav')
            window.practice_winning_sound.play()
            window.practice_A_blue_marble_animation = QPropertyAnimation(window.Practice_Result_A_blue_marble_pic, b'pos')
            window.practice_A_blue_marble_animation.setDuration(2000)
            window.practice_A_blue_marble_animation.setStartValue(QPoint(290, 480))
            window.practice_A_blue_marble_animation.setEndValue(QPoint(290, 350))
            window.practice_A_blue_marble_animation.start()
            window.Practice_Result_A_blue_marble_pic.show()

        self.step_forward()



    def practice_choice_B(self):

        self.practice_current_trial_choice_urn_label = "B"
        window.Practice_Choice_B_continue_bn.show()
        self.practice_selected_urn = 0
        self.generation_of_practice_ambiguous_urn_results()

        if self.practice_trial_result == "red":
            self.practice_losing_result_text = "Ooops. It is the red marble. Sorry, but you lose. Try to win next time."
            window.Practice_Results_lbl.setText(self.practice_losing_result_text)
            # the animates below makes the marble move out of the urn and vertically up
            window.practice_B_red_marble_animation = QPropertyAnimation(window.Practice_Result_B_red_marble_pic, b'pos')
            window.practice_B_red_marble_animation.setDuration(2000)
            window.practice_B_red_marble_animation.setStartValue(QPoint(875, 495))
            window.practice_B_red_marble_animation.setEndValue(QPoint(875, 365))
            window.practice_B_red_marble_animation.start()
            window.Practice_Result_B_red_marble_pic.show()

        else:
            self.practice_winning_result_text = "It is the blue marble! Congratulations! You win!"
            window.Practice_Results_lbl.setText(self.practice_winning_result_text)
            # here I add a 'yeah' sound to celebrate the winning
            window.practice_winning_sound = QSound('yeah.wav')
            window.practice_winning_sound.play()
            window.practice_B_blue_marble_animation = QPropertyAnimation(window.Practice_Result_B_blue_marble_pic, b'pos')
            window.practice_B_blue_marble_animation.setDuration(2000)
            window.practice_B_blue_marble_animation.setStartValue(QPoint(875, 495))
            window.practice_B_blue_marble_animation.setEndValue(QPoint(875, 365))
            window.practice_B_blue_marble_animation.start()
            window.Practice_Result_B_blue_marble_pic.show()

        self.step_forward()

    def practice_choice_A_next_trial(self):
        # could add more functions if future experiments needs
        self.step_forward()

    def practice_choice_B_next_trial(self):
        self.step_forward()

    def start_formal_exp(self):
# if we need to conduct the experiments with more trials, we need to apply codes in this function into the below choice_A_next_trial /
# function and choice_B_next_trial function and it should be convenient.
        # get the random position of ambiguous urn
        self.ambiguous_urn_postion = randint(0,2)
        # 0 represents right(B), 1 represents left(A).
        if self.ambiguous_urn_postion == 1:
            self.ambiguous_urn_label = "A"
            self.certain_urn_label = "B"
        else:
            self.ambiguous_urn_label = "B"
            self.certain_urn_label = "A"

        # calculate the certain half marbles for the condition
        self.current_marbles_total = self.current_condition
        self.certain_marbles = int(self.current_marbles_total/2)

        # Because the description of drawing process will be different in face of only 2 marbles, we have to deal with text of 2 marbles separately.
        # To be specific, it is the "0,1,2" verse "0,1,2 ..., (the total number of marbles)"
        if self.current_marbles_total == 2:
            self.instruction_text = "Consider the following problem carefully, then choose your decision by pressing the button." \
                                    "\nOn the screen are two urns, labeled A and B, containing red and blue marbles, and you have " \
                                    "to draw a marble from one of the urns by pressing the button. If you get a blue marble, " \
                                    "you will be entered into a £30 lottery draw. Urn " + f"{self.certain_urn_label}" + " contains " \
                                    + f"{self.certain_marbles}" + " red marbles and " + f"{self.certain_marbles}" + " blue " \
                                    "marbles. Urn " + f"{self.ambiguous_urn_label}" + " contains " + f"{self.current_marbles_total}" + " marbles " \
                                    "in an unknown color ratio, from " + f"{self.current_marbles_total}" + " red marbles and " \
                                    "0 blue marbles to 0 red marbles and " + f"{self.current_marbles_total}" + " blue marbles. " \
                                    "The mixture of red and blue marbles in Urn " + f"{self.ambiguous_urn_label}" + " has been " \
                                    "decided by writing the numbers 0, 1, 2" + " on separate " \
                                    "slips of paper, shuffling the slips thoroughly, and then drawing one of them at random. " \
                                    "The number chosen was used to determine the number of blue marbles to be put into " \
                                    "Urn " + f"{self.ambiguous_urn_label}" + ", but you do not know the number. Every possible " \
                                    "mixture of red and blue marbles in Urn " + f"{self.ambiguous_urn_label}" + " is equally likely.\n" \
                                    "You have to decide whether you prefer to draw a marble at random from Urn A or Urn B. What " \
                                    "you hope is to draw a blue marble and be entered for the £30 lottery draw. \nConsider very " \
                                    "carefully from which urn you prefer to draw the marble, then press the button of your chosen " \
                                    "urn below. A marble will be drawn from your chosen urn straight afterwards. And you will be able " \
                                    "to see the result.\nNow you could press the button below to draw a marble.\n"
        else:
            self.instruction_text = "Consider the following problem carefully, then choose your decision by pressing the button." \
                                    "\nOn the screen are two urns, labeled A and B, containing red and blue marbles, and you have " \
                                    "to draw a marble from one of the urns by pressing the button. If you get a blue marble, " \
                                    "you will be entered into a £30 lottery draw. Urn " + f"{self.certain_urn_label}" + " contains " + \
                                    f"{self.certain_marbles}" + "red marbles and " + f"{self.certain_marbles}" + " blue " \
                                    "marbles. Urn " + f"{self.ambiguous_urn_label}" + " contains " + f"{self.current_marbles_total}" + " marbles " \
                                    "in an unknown color ratio, from " + f"{self.current_marbles_total}" + " red marbles and " \
                                    "0 blue marbles to 0 red marbles and " + f"{self.current_marbles_total}" + " blue marbles. " \
                                    "The mixture of red and blue marbles in Urn " + f"{self.ambiguous_urn_label}" + " has been " \
                                    "decided by writing the numbers 0, 1, 2, . . ., " + f"{self.current_marbles_total}" + " on separate " \
                                    "slips of paper, shuffling the slips thoroughly, and then drawing one of them at random. " \
                                    "The number chosen was used to determine the number of blue marbles to be put into " \
                                    "Urn " + f"{self.ambiguous_urn_label}" + ", but you do not know the number. Every possible " \
                                    "mixture of red and blue marbles in Urn " + f"{self.ambiguous_urn_label}" + " is equally likely.\n" \
                                    "You have to decide whether you prefer to draw a marble at random from Urn A or Urn B. What " \
                                    "you hope is to draw a blue marble and be entered for the £30 lottery draw. \nConsider very " \
                                    "carefully from which urn you prefer to draw the marble, then press the button of your chosen " \
                                    "urn below. A marble will be drawn from your chosen urn straight afterwards. And you will be able " \
                                    "to see the result.\nNow you could press the button below to draw a marble.\n"

        window.Instruction_lbl.setText(self.instruction_text)

        # prepare and hide the buttons and marble pictures for the next trial.
        window.Choice_A_continue_bn.hide()
        window.Choice_B_continue_bn.hide()
        window.Result_A_blue_marble_pic.hide()
        window.Result_A_red_marble_pic.hide()
        window.Result_B_blue_marble_pic.hide()
        window.Result_B_red_marble_pic.hide()


        self.step_forward()


    def generation_of_certain_urn_results(self):
        self.certain_urn_drawing = choice(["blue", "red"])  # because it is even, only need to choose from "blue" and "red"
        self.trial_result = self.certain_urn_drawing


    def generation_of_ambiguous_urn_results(self):
        # I hate to do this way, there is more convenient way in math to do the choosing from the ambiguous distribution
        # We can calculate the proportion of whichever the blue marble or the red marble of given condition then generate /
        # a random float between 0 and 1, then we compare the proportion and the random float to determine whether it /
        # is a blue marble or a red marble.
        # However, it is demanded to replicate the original experiment's drawing method by drawing from all the options.
        self.ambiguous_urn_distribution = []
        self.num_red_ball = self.current_ratio[0]
        self.num_blue_ball = self.current_ratio[1]
        if self.num_red_ball != 0:
            for red_ball in range(0, self.num_red_ball):
                self.ambiguous_urn_distribution.append("red")
        if self.num_blue_ball != 0:
            for blue_ball in range(0, self.num_blue_ball):
                self.ambiguous_urn_distribution.append("blue")
        self.ambiguous_urn_drawing = choice(self.ambiguous_urn_distribution)
        self.trial_result = self.ambiguous_urn_drawing


    def choice_A(self):
        self.current_trial_choice_urn_label = "A"
        window.Choice_A_continue_bn.show()

        if self.certain_urn_label == "A":
            self.selected_urn = 1
            self.generation_of_certain_urn_results()

        else:
            self.selected_urn = 0
            self.generation_of_ambiguous_urn_results()


        if self.trial_result == "red":
            self.losing_result_text = "Ooops. It is the red marble. Sorry, but you lose. Try to win next time."
            window.Results_lbl.setText(self.losing_result_text)
            # the animates below makes the marble move out of the urn and vertically up
            window.A_red_marble_animation = QPropertyAnimation(window.Result_A_red_marble_pic, b'pos')
            window.A_red_marble_animation.setDuration(2000)
            window.A_red_marble_animation.setStartValue(QPoint(290, 480))
            window.A_red_marble_animation.setEndValue(QPoint(290, 350))
            window.A_red_marble_animation.start()
            window.Result_A_red_marble_pic.show()

        else:
            self.winning_result_text = "It is the blue marble! Congratulations! You win!"
            window.Results_lbl.setText(self.winning_result_text)
            # here I add a 'yeah' sound to celebrate the winning
            window.winning_sound = QSound('yeah.wav')
            window.winning_sound.play()
            window.A_blue_marble_animation = QPropertyAnimation(window.Result_A_blue_marble_pic, b'pos')
            window.A_blue_marble_animation.setDuration(2000)
            window.A_blue_marble_animation.setStartValue(QPoint(290, 480))
            window.A_blue_marble_animation.setEndValue(QPoint(290, 350))
            window.A_blue_marble_animation.start()
            window.Result_A_blue_marble_pic.show()

        self.step_forward()

    def choice_B(self):
        self.current_trial_choice_urn_label = "B"
        window.Choice_B_continue_bn.show()

        if self.certain_urn_label == "B":
            self.selected_urn = 1
            self.generation_of_certain_urn_results()

        else:
            self.selected_urn = 0
            self.generation_of_ambiguous_urn_results()

# because the animation needs to be set for every single marble and it is flexible to set the animation separately for
# every marble, because different animations could be added in the future experiment. So, I decide to do this separately,
# and maybe it seems redundant, but it is not actually.
        if self.trial_result == "red":
            self.losing_result_text = "Ooops. It is the red marble. Sorry, but you lose. Try to win next time."
            window.Results_lbl.setText(self.losing_result_text)
            window.B_red_marble_animation = QPropertyAnimation(window.Result_B_red_marble_pic, b'pos')
            window.B_red_marble_animation.setDuration(2000)
            window.B_red_marble_animation.setStartValue(QPoint(875, 495))
            window.B_red_marble_animation.setEndValue(QPoint(875, 365))
            window.B_red_marble_animation.start()
            window.Result_B_red_marble_pic.show()

        else:
            self.winning_result_text = "It is the blue marble! Congratulations! You win!"
            window.Results_lbl.setText(self.winning_result_text)
            window.winning_sound = QSound('yeah.wav', window)
            window.winning_sound.play()
            window.B_blue_marble_animation = QPropertyAnimation(window.Result_B_blue_marble_pic, b'pos')
            window.B_blue_marble_animation.setDuration(2000)
            window.B_blue_marble_animation.setStartValue(QPoint(875, 495))
            window.B_blue_marble_animation.setEndValue(QPoint(875, 365))
            window.B_blue_marble_animation.start()
            window.Result_B_blue_marble_pic.show()

        self.step_forward()


    # save the results in list and transform all of them into strings
    def write_results(self):
        self.result_list.append(str(self.age))
        self.result_list.append(self.gender)
        self.result_list.append(self.education)
        self.result_list.append(self.contact)
        self.result_list.append(str(self.current_condition))
        self.result_list.append(str(self.ambiguous_urn_postion))
        self.result_list.append(str(self.selected_urn))
        self.result_list.append(self.trial_result)

        self.filewriter = open(self.outputfile, 'a')
        self.filewriter.write(",".join(self.result_list) + "\n")
        self.filewriter.close()


    # Though it seems that there is no need for separate continue buttons for each condition, I want to leave it for /
    # further possible functions if future experiments needs. And it would be helpful for the participants to check the /
    # results quickly. So these are no redundant codes.
    def choice_A_next_trial(self):
        self.write_results()
        self.step_forward()

    def choice_B_next_trial(self):
        self.write_results()
        self.step_forward()

# send signals to the buttons
    def buttons_connection(self):
        window.Continue_bn_page_welcome.clicked.connect(self.start_exp)
        window.Continue_bn_page_consent.clicked.connect(self.check_consent)
        window.Continue_bn_page_demog.clicked.connect(self.check_demog)
        window.Practice_Choice_A_bn.clicked.connect(self.practice_choice_A)
        window.Practice_Choice_B_bn.clicked.connect(self.practice_choice_B)
        window.Practice_Choice_A_continue_bn.clicked.connect(self.practice_choice_A_next_trial)
        window.Practice_Choice_B_continue_bn.clicked.connect(self.practice_choice_B_next_trial)
        window.Continue_bn_page_connection.clicked.connect(self.start_formal_exp)
        window.Choice_A_bn.clicked.connect(self.choice_A)
        window.Choice_B_bn.clicked.connect(self.choice_B)
        window.Choice_A_continue_bn.clicked.connect(self.choice_A_next_trial)
        window.Choice_B_continue_bn.clicked.connect(self.choice_B_next_trial)


myexp = Experiment([2,10,100],[(2,0),(8,2),(53,47)])
myexp.buttons_connection()


window.show()
app.exec_()