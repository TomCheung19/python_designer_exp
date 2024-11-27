###########################################################################
###########################################################################

	# The programme aims at see how people use information that are independent. We use two experiments with within-subjects
    # designs. Details could be seen in notes.
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
import MineSweeping
import csv

# load the interface as usual
app = QApplication([])
window = uic.loadUi("demog_ui.ui")
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
        self.all_result_list = []
        self.outputfile_exp1 = "result_exp1.csv"
        self.outputfile_exp2 = "result_exp2.csv"
        self.outputfile_all = "result_all.csv"
        self.exp1_header = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q16", "Q17", "Q18", "Q19", "Q20", "Q21"]
        self.exp2_header = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q16", "Q17"]
        self.all_header = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q16", "Q17", "Q18", "Q19", "Q20", "Q21", "Q22", "Q23", "Q24", "Q25", "Q26", "Q27", "Q28", "Q29", "Q30", "Q31", "Q32"]
        self.options_E1P1b = ["Scenario 1", "They are the same", "Scenario 2"]
        self.options_E1P2 = ["Scenario 1", "They are the same", "Scenario 2"]
        self.options_E2P1b = ["Scenario 1", "They are the same", "Scenario 2"]
        self.E1_P1b_sab_scenario = ""
        self.E1_P2_sab_scenario = ""
        self.E2_P1b_acc_scenario = ""


    def step_forward_demog(self):
        self.current_page_index_demog += 1
        window.experiment_window.setCurrentIndex(self.current_page_index_demog)

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

        self.step_forward_demog()

    def check_consent(self):
        if window.Consent_checkbox.isChecked():
            self.step_forward_demog()
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
        elif self.current_location == "":
            self.error_message = "Error! Please choose the appropriate current location then press the 'continue' button."
        # the contact information is not important and we can leave it as the instruction text to avoid missing value.
        window.Error_message_lbl.setText(self.error_message)
        window.Error_message_lbl.show()

        if self.error_message == "":
            # all use str() to avoid potential bugs
            self.demog_result.append(str(self.age))
            self.demog_result.append(str(self.gender))
            self.demog_result.append(str(self.education))
            self.demog_result.append(str(self.contact))
            self.demog_result.append(str(self.native_language))
            self.demog_result.append(str(self.current_location))

            window2.show()
            self.step_forward_demog()

    def start_exp1(self):
        # set the starting time of RT and animation
        window2.E1_P1a_air_crash_animation = QPropertyAnimation(window2.E1_P1a_air_crash_pic, b'pos')
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
        option_list.remove(radio_btn_3.text())

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
            self.E1_P1a_RT = int(round(self.E1_P1a_end_time - self.E1_P1a_start_time)*1000)
            self.randomize_options(window2.E1_P1b_choice1, window2.E1_P1b_choice2, window2.E1_P1b_choice3, self.options_E1P1b)
            # set starting time of next trial
            self.E1_P1b_start_time = time.time()

            self.step_forward_exp1()


    def E1_P1b_proceed(self):
    # get the choice
    # because the for in buttongroup does not work, I use this seemingly redundant code, but coding matters
        if window2.E1_P1b_choice1.isChecked():
            self.E1_P1b_sab_scenario = window2.E1_P1b_choice1.text()
        elif window2.E1_P1b_choice2.isChecked():
            self.E1_P1b_sab_scenario = window2.E1_P1b_choice2.text()
        elif window2.E1_P1b_choice3.isChecked():
            self.E1_P1b_sab_scenario = window2.E1_P1b_choice3.text()

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
            self.E1_P1b_RT = int(round(self.E1_P1b_end_time - self.E1_P1b_start_time)*1000)

            self.step_forward_exp1()


    def E1_P1b_reason_proceed(self):

        self.E1_P1b_reason = window2.E1_P1b_reason_txt.toPlainText()
        # important! set the starting time here instead of previous page
        self.E1_P2_start_time = time.time()
        self.randomize_options(window2.E1_P2_choice1, window2.E1_P2_choice2, window2.E1_P2_choice3,
                               self.options_E1P2)

        self.step_forward_exp1()

    def E1_P2_proceed(self):
        # below are not repeatable codes because more questions could be added and there is slightly different descriptions
        # so if using the function to reduce some repeat, there will be too many arguments, which in verse increases the work load.
        # get the choice
        # because the for in buttongroup does not work, I use this seemingly redundant code, but coding matters
        if window2.E1_P2_choice1.isChecked():
            self.E1_P2_sab_scenario = window2.E1_P2_choice1.text()
        elif window2.E1_P2_choice2.isChecked():
            self.E1_P2_sab_scenario = window2.E1_P2_choice2.text()
        elif window2.E1_P2_choice3.isChecked():
            self.E1_P2_sab_scenario = window2.E1_P2_choice3.text()

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
        elif self.E1_P2_probability_scenario1 < 0 or self.E1_P2_probability_scenario2 < 0:
            window2.E1_P2_probability_box = QMessageBox.about(window2, 'Error',
                                                               'Please choose the appropriate probability.')
            window2.E1_P2_probability_box.show()
        else:
            self.E1_P2_end_time = time.time()
            self.E1_P2_RT = int(round(self.E1_P2_end_time - self.E1_P2_start_time)*1000)

            self.step_forward_exp1()


    def E1_P2_reason_proceed(self):
        self.E1_P2_reason = window2.E1_P2_reason_txt.toPlainText()

        self.step_forward_exp1()

    def end_exp1(self):
        # end of experiment 1, then open the MineSweeping game and proceed to the experiment 2

        window3.show()
        MineSweeping.main()

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
        window3.E2_P1a_air_crash_animation.setStartValue(QPoint(1, 1))
        window3.E2_P1a_air_crash_animation.setEndValue(QPoint(1039, 400))
        # play the air crash sound
        window3.air_crash_sound = QSound('air_crash.wav')

        self.E2_P1a_start_time = time.time()
        self.step_forward_exp2()
        window3.E2_P1a_air_crash_animation.start()
        window3.air_crash_sound.play()


    def E2_P1a_proceed(self):
        #
        self.E2_P1a_sab_B_mistake_C_correct = window3.E2_P1a_sab_B_mistake_C_correct_sbx.value()
        self.E2_P1a_sab_B_mistake_C_incorrect = window3.E2_P1a_sab_B_mistake_C_incorrect_sbx.value()
        self.E2_P1a_acci_B_mistake_C_correct = window3.E2_P1a_acci_B_mistake_C_correct_sbx.value()
        self.E2_P1a_acci_B_mistake_C_incorrect = window3.E2_P1a_acci_B_mistake_C_incorrect_sbx.value()
        # the probability is set to be between 0 and 100 and the default value is set to -1 in order to rule out the negligence
        if self.E2_P1a_sab_B_mistake_C_correct < 0 or self.E2_P1a_sab_B_mistake_C_incorrect < 0 or self.E2_P1a_acci_B_mistake_C_correct < 0 or self.E2_P1a_acci_B_mistake_C_incorrect < 0:
            window3.E2_P1a_box = QMessageBox.about(window3, 'Error',
                                                   'Please choose the appropriate probability.')
            window3.E2_P1a_box.show()

        else:
            # get the reaction time, though it is an experiment with lots of reading
            self.E2_P1a_end_time = time.time()
            self.E2_P1a_RT = int(round(self.E2_P1a_end_time - self.E2_P1a_start_time)*1000)
            self.randomize_options(window3.E2_P1b_choice1, window3.E2_P1b_choice2, window3.E2_P1b_choice3, self.options_E2P1b)
            # set starting time of next trial
            self.E2_P1b_start_time = time.time()

            self.step_forward_exp2()


    def E2_P1b_proceed(self):
    # get the choice
    # because the for in buttongroup does not work, I use this seemingly redundant code, but coding matters
        if window3.E2_P1b_choice1.isChecked():
            self.E2_P1b_acc_scenario = window3.E2_P1b_choice1.text()
        elif window3.E2_P1b_choice2.isChecked():
            self.E2_P1b_acc_scenario = window3.E2_P1b_choice2.text()
        elif window3.E2_P1b_choice3.isChecked():
            self.E2_P1b_acc_scenario = window3.E2_P1b_choice3.text()

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
            self.E2_P1b_RT = int(round(self.E2_P1b_end_time - self.E1_P1b_start_time)*1000)

            self.step_forward_exp2()

    # save the results in list and transform all of them into strings

    # Though it seems that there is no need for separate continue buttons and result files, I want to leave it for /
    # further possible functions if future experiments needs. And it would be helpful for both the participants and the /
    # subjects to check the results quickly. So these are no redundant codes.
    # all use str() to avoid potential bugs
    def write_results_exp1(self):
        self.exp1_result_list.append(str(self.E1_P1a_prob_B_mistake_C_correct))
        self.exp1_result_list.append(str(self.E1_P1a_prob_B_mistake_C_incorrect))
        self.exp1_result_list.append(str(self.E1_P1a_RT))
        self.exp1_result_list.append(str(self.E1_P1b_sab_scenario))
        self.exp1_result_list.append(str(self.E1_P1b_confidence))
        self.exp1_result_list.append(str(self.E1_P1b_probability_scenario1))
        self.exp1_result_list.append(str(self.E1_P1b_probability_scenario2))
        self.exp1_result_list.append(str(self.E1_P1b_RT))
        self.exp1_result_list.append(str(self.E1_P1b_reason))
        self.exp1_result_list.append(str(self.E1_P2_sab_scenario))
        self.exp1_result_list.append(str(self.E1_P2_confidence))
        self.exp1_result_list.append(str(self.E1_P2_probability_scenario1))
        self.exp1_result_list.append(str(self.E1_P2_probability_scenario2))
        self.exp1_result_list.append(str(self.E1_P2_RT))
        self.exp1_result_list.append(str(self.E1_P2_reason))

        self.result_exp1 = self.demog_result[:]
        self.result_exp1.extend(self.exp1_result_list)

        with open(self.outputfile_exp1, 'a', encoding= 'UTF-8',newline='') as self.filewriter_exp1:
            self.csvwriter_exp1 = csv.writer(self.filewriter_exp1, dialect="excel")
            with open(self.outputfile_exp1, 'r', encoding= 'UTF-8') as self.filereader_exp1:
                self.exp1_reader = csv.reader(self.filereader_exp1)
                if not any(self.exp1_reader):
                    self.csvwriter_exp1.writerow(self.exp1_header)
                    self.csvwriter_exp1.writerow(self.result_exp1)
                else:
                    self.csvwriter_exp1.writerow(self.result_exp1)

    def write_results_exp2(self):
        self.exp2_result_list.append(str(self.E2_P1a_sab_B_mistake_C_correct))
        self.exp2_result_list.append(str(self.E2_P1a_sab_B_mistake_C_incorrect))
        self.exp2_result_list.append(str(self.E2_P1a_acci_B_mistake_C_correct))
        self.exp2_result_list.append(str(self.E2_P1a_acci_B_mistake_C_incorrect))
        self.exp2_result_list.append(str(self.E2_P1a_RT))
        self.exp2_result_list.append(str(self.E2_P1b_acc_scenario))
        self.exp2_result_list.append(str(self.E2_P1b_confidence))
        self.exp2_result_list.append(str(self.E2_P1b_probability_scenario1))
        self.exp2_result_list.append(str(self.E2_P1b_probability_scenario2))
        self.exp2_result_list.append(str(self.E2_P1b_RT))
        self.exp2_result_list.append(str(self.E2_P1b_reason))

        self.result_exp2 = self.demog_result[:]
        self.result_exp2.extend(self.exp2_result_list)


        with open(self.outputfile_exp2, 'a', encoding='UTF-8', newline='') as self.filewriter_exp2:
            self.csvwriter_exp2 = csv.writer(self.filewriter_exp2, dialect="excel")
            with open(self.outputfile_exp2, 'r', encoding='UTF-8') as self.filereader_exp2:
                self.exp2_reader = csv.reader(self.filereader_exp2)
                if not any(self.exp2_reader):
                    self.csvwriter_exp2.writerow(self.exp2_header)
                    self.csvwriter_exp2.writerow(self.result_exp2)
                else:
                    self.csvwriter_exp2.writerow(self.result_exp2)

    def write_results_all(self):

        self.all_result_list = self.demog_result[:]
        self.all_result_list.extend(self.exp1_result_list)
        self.all_result_list.extend(self.exp2_result_list)

        with open(self.outputfile_all, 'a', encoding='UTF-8', newline='') as self.filewriter_all:
            self.csvwriter_all = csv.writer(self.filewriter_all, dialect="excel")
            with open(self.outputfile_all, 'r', encoding='UTF-8') as self.filereader_all:
                self.all_reader = csv.reader(self.filereader_all)
                if not any(self.all_reader):
                    self.csvwriter_all.writerow(self.all_header)
                    self.csvwriter_all.writerow(self.all_result_list)
                else:
                    self.csvwriter_all.writerow(self.all_result_list)

    def E2_P1b_reason_proceed(self):

        self.E2_P1b_reason = window3.E2_P1b_reason_txt.toPlainText()

        self.write_results_exp1()

        self.write_results_exp2()

        self.write_results_all()

        self.step_forward_exp2()


# send signals to the buttons
    def buttons_connection(self):
        window.Continue_bn_page_welcome.clicked.connect(self.start_exp)
        window.Continue_bn_page_consent.clicked.connect(self.check_consent)
        window.Continue_bn_page_demog.clicked.connect(self.check_demog)
        window2.E1_instruction_next_btn.clicked.connect(self.start_exp1)
        window2.E1_P1a_next_btn.clicked.connect(self.E1_P1a_proceed)
        window2.E1_P1b_next_btn.clicked.connect(self.E1_P1b_proceed)
        window2.E1_P1b_reason_next_btn.clicked.connect(self.E1_P1b_reason_proceed)
        window2.E1_P2_next_btn.clicked.connect(self.E1_P2_proceed)
        window2.E1_P2_reason_next_btn.clicked.connect(self.E1_P2_reason_proceed)
        window2.E1_End_next_btn.clicked.connect(self.end_exp1)
        window3.E2_instruction_next_btn.clicked.connect(self.start_exp2)
        window3.E2_P1a_next_btn.clicked.connect(self.E2_P1a_proceed)
        window3.E2_P1b_next_btn.clicked.connect(self.E2_P1b_proceed)
        window3.E2_P1b_reason_next_btn.clicked.connect(self.E2_P1b_reason_proceed)



myexp = Experiment()
myexp.buttons_connection()


window.show()
app.exec_()