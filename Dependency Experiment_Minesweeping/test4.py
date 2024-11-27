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
import csv

# load the interface as usual
app = QApplication([])
window = uic.loadUi("test_ui.ui")
window2 = uic.loadUi("experiment1.ui")
window3 = uic.loadUi("experiment2.ui")

# initialize the interface such as hide the error messages
window.Error_message_lbl.hide()
# set the groups for radio buttons
window2.btngroup1 = QButtonGroup(window2)
window2.btngroup1.addButton(window2.E1_P1b_choice1)
window2.btngroup1.addButton(window2.E1_P1b_choice2)
window2.btngroup1.addButton(window2.E1_P1b_choice3)

window2.btngroup2 = QButtonGroup(window2)
window2.btngroup2.addButton(window2.E1_P2_choice1)
window2.btngroup2.addButton(window2.E1_P2_choice2)
window2.btngroup2.addButton(window2.E1_P2_choice3)

window3.btngroup3 = QButtonGroup(window3)
window3.btngroup3.addButton(window3.E2_P1b_choice1)
window3.btngroup3.addButton(window3.E2_P1b_choice2)
window3.btngroup3.addButton(window3.E2_P1b_choice3)



class Experiment:
    # initialize the page indexes and the result lists of different windows
    #
    #
    def __init__(self):
        self.current_page_index_demog = 0
        self.current_page_index_exp1 = 0
        self.current_page_index_exp2 = 0
        self.demog_result = []
        self.exp1_result_list = []
        self.exp2_result_list = []
        self.outputfile_exp1 = "result_exp1.csv"
        self.outputfile_exp2 = "result_exp2.csv"
        self.outputfile_all = "result_all.csv"
        self.options_E1P1b = ["Scenario 1", "They are the same", "Scenario 2"]
        self.options_E1P2 = ["Scenario 1", "They are the same", "Scenario 2"]
        self.options_E2P1b = ["Scenario 1", "They are the same", "Scenario 2"]
        self.E1_P1b_sab_scenario = ""
        self.E1_P2_sab_scenario = ""
        self.E2_P1b_acc_scenario = ""


    def step_forward_demog(self):
        self.current_page_index += 1
        window.experiment_window.setCurrentIndex(self.current_page_index)

    def step_forward_exp1(self):
        self.current_page_index_exp1 += 1
        window2.experiment_window.setCurrentIndex(self.current_page_index_exp1)

    def step_forward_exp2(self):
        self.current_page_index_exp2 += 1
        window3.experiment_window.setCurrentIndex(self.current_page_index_exp2)


    def start_exp(self):

        # first create the result files.
        # because it is the within subject research, we do not randomly assign participants
        # and we leave the random part to the choices of the questions
        self.read_existing_exp1_file = open(self.outputfile_exp1, 'a', encoding= 'UTF-8') # create the result file if there is none.
        self.read_existing_exp1_file.close()
        self.read_existing_exp2_file = open(self.outputfile_exp2, 'a', encoding= 'UTF-8') # create the result file if there is none.
        self.read_existing_exp2_file.close()
        self.read_existing_all_file = open(self.outputfile_all, 'a', encoding= 'UTF-8') # create the result file if there is none.
        self.read_existing_all_file.close()

        self.step_forward()

    def check_consent(self):
        if window.Consent_checkbox.isChecked():
            self.step_forward()
        else:
            window.consent_box = QMessageBox.about(window,'Error','Please tick the consent or you could exit the experiment.')
            window.consent_box.show()

    def check_demog(self):
        self.age = window.Age_spinbox.value()
        # here we use comboBox to get gender and education so that we could easily have more options
        self.gender = window.Gender_comboBox.currentText()
        self.education = window.Education_comboBox.currentText()
        self.contact = window.Contact_txt.toPlainText()
        self.native_language = window.Native_Language_comboBox.currentText()
        self.current_location = window.Current_Location_comboBox.currentText()
        self.error_message = "" # clear the message in case the second error
        # here we allow participants to choose age from 1 to
        if self.age < 12 or self.age > 90:
            self.error_message = "Error! Please choose the appropriate age then press the 'continue' button."
        elif self.gender == "":
            self.error_message = "Error! Please choose the appropriate gender then press the 'continue' button."
        elif self.education == "":
            self.error_message = "Error! Please choose the appropriate education level then press the 'continue' button."
        elif self.native_language == "":
            self.error_message = "Error! Please choose the appropriate native language then press the 'continue' button."
        elif self.current_condition == "":
            self.error_message = "Error! Please choose the appropriate current location then press the 'continue' button."
        # the contact information is not important and we can leave it as the instruction text to avoid missing value.
        window.Error_message_lbl.setText(self.error_message)
        window.Error_message_lbl.show()

        if self.error_message == "":
            self.demog_result.append(str(self.age))
            self.demog_result.append(str(self.gender))
            self.demog_result.append(str(self.education))
            self.demog_result.append(str(self.contact))
            self.demog_result.append(str(self.native_language))
            self.demog_result.append(str(self.current_location))

            window2.show()
            self.step_forward()

    def start_exp1(self):
        # set the starting time of RT and animation
        window2.E1_P1a_air_crash_animation = QPropertyAnimation(window2.E1_P1a_air_crush_pic, b'pos')
        window2.E1_P1a_air_crash_animation.setDuration(3000)
        # notice that QPoint only have the position coordinates and the setGeometry needs the width and height of the objects
        # And I use hard codes here for position, because I use the QLayouts in the interface. So it is set and being set /
        # is better for the real experiment.
        window2.E1_P1a_air_crash_animation.setStartValue(QPoint(1, 1))
        window2.E1_P1a_air_crash_animation.setEndValue(QPoint(1039, 400))
        # play the air crash sound
        window2.air_crash_sound = QSound('air_crash.wav')

        self.E1_P1a_start_time = time.time()
        self.step_forward_exp1()
        window2.E1_P1a_air_crash_animation.start()
        window2.air_crash_sound.play()

    def randomize_options(self, radio_btn_1, radio_btn_2, radio_btn_3, option_list):
        # here we use the random.choice to accomplish the choice sampling without putting back
        radio_btn_1.setText(random.choice(option_list))
        option_list.remove(radio_btn_1.text())
        radio_btn_2.setText(random.choice(option_list))
        option_list.remove(radio_btn_2.text())
        radio_btn_3.setText(random.choice(option_list))
        option_list.remove(radio_btn_1.text())

    def E1_P1a_proceed(self):
        #
        self.E1_P1a_prob_B_mistake_C_correct = window2.E1_P1a_B_mistake_C_correct_sbx.value()
        self.E1_P1a_prob_B_mistake_C_incorrect = window2.E1_P1a_B_mistake_C_incorrect_sbx.value()
        # the probability is set to be between 0 and 100 and the default value is set to -1 in order to rule out the negligence
        if self.E1_P1a_prob_B_mistake_C_correct < 0 or self.E1_P1a_prob_B_mistake_C_incorrect < 0:
            window2.E1_P1a_box = QMessageBox.about(window2, 'Error',
                                                   'Please choose the appropriate probability.')
            window2.E1_P1a_box.show()

        else:
            # get the reaction time, though it is an experiment with lots of reading
            self.E1_P1a_end_time = time.time()
            self.E1_P1a_RT = int(round(self.E1_P1a_end_time - self.E1_P1a_start_time))
            self.randomize_options(window2.E1_P1b_choice1, window2.E1_P1b_choice2, window2.E1_P1b_choice3, self.options_E1P1b)
            # set starting time of next trial
            self.E2.P1b_start_time = time.time()

            self.step_forward_exp1()


    def E1_P1b_proceed(self):
    # get the choice
        for E1_P1b_choice in window2.btngroup1.children():
            if E1_P1b_choice.isChecked():
                self.E1_P1b_sab_scenario = E1_P1b_choice.text()

        self.E1_P1b_confidence = window2.E1_P1b_confidence_sbx.value()
        self.E1_P1b_probability_scenario1 = window2.E1_P1b_probability_scenario1_sbx.value()
        self.E1_P1b_probability_scenario2 = window2.E1_P1b_probability_scenario2_sbx.value()
    # send the error message if missing value exists
        if self.E1_P1b_sab_scenario == "":
            window2.E1_P1b_choice_box = QMessageBox.about(window2, 'Error',
                                                   'Please choose the scenario.')
            window2.E1_P1b_choice_box.show()
        elif self.E1_P1b_confidence < 0:
            window2.E1_P1b_confidence_box = QMessageBox.about(window2, 'Error',
                                                   'Please choose the appropriate confidence.')
            window2.E1_P1b_confidence_box.show()
        elif self.E1_P1b_probability_scenario1 < 0 or self.E1_P1b_probability_scenario2 < 0:
            window2.E1_P1b_probability_box = QMessageBox.about(window2, 'Error',
                                                   'Please choose the appropriate probability.')
            window2.E1_P1b_probability_box.show()
        else:
            # get RT in the form of millisecond
            self.E1_P1b_end_time = time.time()
            self.E1_P1b_RT = int(round(self.E1_P1b_end_time - self.E1_P1b_start_time))

            self.step_forward_exp1()


    def P1b_reason_proceed(self):

        self.E1_P1b_reason = window2.E1_P1b_reason_txt.toPlainText()
        # important! set the starting time here instead of previous page
        self.E2.P2_start_time = time.time()
        self.randomize_options(window2.E1_P2_choice1, window2.E1_P2_choice2, window2.E1_P2_choice3,
                               self.options_E1P2)

        self.step_forward_exp1()

    def E1_P2_proceed(self):
        # below are not repeatable codes because more questions could be added and there is slightly different descriptions
        # so if using the function to reduce some repeat, there will be too many arguments, which in verse increases the work load.
        # get the choice
        for E1_P2_choice in window2.btngroup2.children():
            if E1_P2_choice.isChecked():
                self.E1_P2_sab_scenario = E1_P2_choice.text()

        self.E1_P2_confidence = window2.E1_P2_confidence_sbx.value()
        self.E1_P2_probability_scenario1 = window2.E1_P2_probability_scenario1_sbx.value()
        self.E1_P2_probability_scenario2 = window2.E1_P2_probability_scenario2_sbx.value()
        # send the error message if missing value exists
        if self.E1_P2_sab_scenario == "":
            window2.E1_P2_choice_box = QMessageBox.about(window2, 'Error',
                                                          'Please choose the scenario.')
            window2.E1_P2_choice_box.show()
        elif self.E1_P2_confidence < 0:
            window2.E1_P2_confidence_box = QMessageBox.about(window2, 'Error',
                                                              'Please choose the appropriate confidence.')
            window2.E1_P2_confidence_box.show()
        elif self.E1_P2_probability_scenario1 < 0 or self.E1_P1b_probability_scenario2 < 0:
            window2.E1_P2_probability_box = QMessageBox.about(window2, 'Error',
                                                               'Please choose the appropriate probability.')
            window2.E1_P2_probability_box.show()
        else:
            self.E1_P2_end_time = time.time()
            self.E1_P2_RT = int(round(self.E1_P2_end_time - self.E1_P2_start_time))

            self.step_forward_exp1()


    def P2_reason_proceed(self):
        self.E1_P2_reason = window2.E1_P2_reason_txt.toPlainText()

        self.step_forward_exp1()

    def end_exp1(self):
        # end of experiment 1, then open the MineSweeping game and proceed to the experiment 2

        window3.show()
        test_2.main()

    def start_exp2(self):
# if we need to conduct the experiments with more trials, we need to apply codes in this function into the below trials  /
# and some adjustments and it should be convenient.
        # get the random position of ambiguous urn
        # set the starting time of RT and animation

        window3.E2_P1a_air_crash_animation = QPropertyAnimation(window3.E2_P1a_air_crash_pic, b'pos')
        window3.E2_P1a_air_crash_animation.setDuration(3000)
        # notice that QPoint only have the position coordinates and the setGeometry needs the width and height of the objects
        # And I use hard codes here for position, because I use the QLayouts in the interface. So it is set and being set /
        # is better for the real experiment.
        window3.E1_P1a_air_crash_animation.setStartValue(QPoint(1, 1))
        window3.E1_P1a_air_crash_animation.setEndValue(QPoint(1039, 400))
        # play the air crash sound
        window3.air_crash_sound = QSound('air_crash.wav')

        self.E2_P1a_start_time = time.time()
        self.step_forward_exp2()
        window3.E1_P1a_air_crash_animation.start()
        window3.air_crash_sound.play()


    def E2_P1a_proceed(self):
        #
        self.E2_P1a_sab_B_mistake_C_correct = window3.E2_P1a_sab_B_mistake_C_correct_sbx.value()
        self.E2_P1a_sab_B_mistake_C_incorrect = window3.E2_P1a_sab_B_mistake_C_incorrect_sbx.value()
        self.E2_P1a_acci_B_mistake_C_correct = window3.E2_P1a_acci_B_mistake_C_correct_sbx.value()
        self.E2_P1a_acci_B_mistake_C_incorrect = window3.E2_P1a_acci_B_mistake_C_incorrect_sbx.value()
        # the probability is set to be between 0 and 100 and the default value is set to -1 in order to rule out the negligence
        if self.E2_P1a_sab_B_mistake_C_correct < 0 or self.E2_P1a_sab_B_mistake_C_incorrect < 0 or self.E2_P1a_acci_B_mistake_C_correct or self.E2_P1a_acci_B_mistake_C_incorrect:
            window3.E2_P1a_box = QMessageBox.about(window3, 'Error',
                                                   'Please choose the appropriate probability.')
            window3.E2_P1a_box.show()

        else:
            # get the reaction time, though it is an experiment with lots of reading
            self.E2_P1a_end_time = time.time()
            self.E2_P1a_RT = int(round(self.E2_P1a_end_time - self.E2_P1a_start_time))
            self.randomize_options(window2.E2_P1b_choice1, window2.E2_P1b_choice2, window2.E2_P1b_choice3, self.options_E2P1b)
            # set starting time of next trial
            self.E2.P1b_start_time = time.time()

            self.step_forward_exp2()


    def E2_P1b_proceed(self):
    # get the choice
        for E2_P1b_choice in window3.btngroup3.children():
            if E2_P1b_choice.isChecked():
                self.E2_P1b_acc_scenario = E2_P1b_choice.text()

        self.E2_P1b_confidence = window3.E2_P1b_confidence_sbx.value()
        self.E2_P1b_probability_scenario1 = window3.E2_P1b_probability_scenario1_sbx.value()
        self.E2_P1b_probability_scenario2 = window3.E2_P1b_probability_scenario2_sbx.value()
    # send the error message if missing value exists
        if self.E2_P1b_acc_scenario == "":
            window3.E2_P1b_choice_box = QMessageBox.about(window3, 'Error',
                                                   'Please choose the scenario.')
            window3.E2_P1b_choice_box.show()
        elif self.E2_P1b_confidence < 0:
            window3.E2_P1b_confidence_box = QMessageBox.about(window3, 'Error',
                                                   'Please choose the appropriate confidence.')
            window3.E2_P1b_confidence_box.show()
        elif self.E2_P1b_probability_scenario1 < 0 or self.E2_P1b_probability_scenario2 < 0:
            window3.E2_P1b_probability_box = QMessageBox.about(window3, 'Error',
                                                   'Please choose the appropriate probability.')
            window3.E2_P1b_probability_box.show()
        else:
            # get RT in the form of millisecond
            self.E2_P1b_end_time = time.time()
            self.E2_P1b_RT = int(round(self.E2_P1b_end_time - self.E1_P1b_start_time))

            self.step_forward_exp2()

    # save the results in list and transform all of them into strings

    # Though it seems that there is no need for separate continue buttons and result files, I want to leave it for /
    # further possible functions if future experiments needs. And it would be helpful for both the participants and the /
    # subjects to check the results quickly. So these are no redundant codes.

    def write_results_exp1(self):
        self.demog_result.append(str(self.age))
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