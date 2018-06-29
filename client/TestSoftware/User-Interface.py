# User-Interface.py
#
# This is the main Graphical User Interface for communicating
# with the setup in the lab.
# Developed with the help of many people
# For Baylor University, Summer 2016.
#
# This is a comment to see if I got git to work properly
# round 2 electric boogaloo
# 

#import qCard
#import loggerClass as logClass
#import testSummary
from Tkinter import *
#from client import webBus
#from TestStand import TestStand
from datetime import datetime
import subprocess
import os, shutil
import glob
import sys

if (1):
    fontc='#DDDDDD'
    topc='#333333'
    rightc='#333333'
    leftc='#333333'
    bottomc='#333333'
    backc='#222222'
    buttonsc=["#004D00","#664D00","#006080","#4d0066","#660000","#800000","#990000","#990099","#007A99","#008080","#00804D"]
    dimbuttonsc=["#006600","#806000","#007399","#600080","#960000","#B00000","#C90000","#B300B3","#008FB3","#009999","#00995C"]
    dimc="#555555"
    checkc="#222222"
else:
    fontc="black"
    topc="white"
    rightc="white"
    leftc="white"
    bottomc="white"
    backc="#DDDDDD"
    buttonsc=["DarkSeaGreen1","lemon chiffon","light cyan","lavender","red","#F30033","#E60066","DarkOrchid1","turquoise","#33ffcc","pale green"]
    dimbuttonsc=["#A1EFA1","#EFEAAD","#C0EFEF","#C6C6EA","#E50000","#DE0013","#D10046","#9F1EEF","#20D0B9","#13EFBC","#78EB78"]
    dimc="#DDDDDD"
    checkc="white"

class makeGui:
        def __init__(self, parent):

                # Create a list of QIECard slots:
                self.cardSlots = ["Card 2", "Card 3", "Card 4", "Card 5", "Card 7",
                             "Card 8","Card 9", "Card 10", "Card 18", "Card 19",
                             "Card 20", "Card 21", "Card 23", "Card 24",
                             "Card 25", "Card 26"]

                # Create a dict for converting GUI list of suites to stuff for
                # behind-the-scenes
                self.suiteDict = {
                                  "Bridge Register Suite"  : "bridge",
                                 }

                # Create a list of nGCCme slots:
                self.ngccmeSlots = ["nGCCme 1", "nGCCme 2"]

                # Create a placeholder argument for Andrew's script
                self.folderArgument = "/home/hep/999999999"

                # Create a list of Readout Modules:
                self.readoutSlots = ["RM 1", "RM 2", "RM 3", "RM 4"]

                # Create a string that uniquely defines a human log file
                self.humanLogName = "{:%b%d%Y_%H%M%S}".format(datetime.now())

                # Make an empty list that will eventually contain all of
                # the active card slots
                self.outSlotNumbers = []

                # make an empty list that will eventually contain all of
                # the TestSummary instances that get sent out
                self.outSummaries = []

                # Make a flag for fan power
                self.fanPowerFlag = False

                # Name the parent. This is mostly for bookkeeping purposes
                # and doesn't really get used too much.
                self.myParent = parent

                # Create some string variables for text entry/display boxes
                self.qieChoiceVar   =  StringVar()
                self.qieReadVar     =  StringVar()
                self.qieOutText     =  StringVar()
                self.nameChoiceVar  =  StringVar()
                self.infoCommentVar =  StringVar()
                self.runtimeNumber  =  StringVar()
                self.suiteChoiceVar =  StringVar()
                self.piChoiceVar    =  StringVar()
                self.iterationVar   =  StringVar()
                self.uploadFromStrEntry = StringVar()
                self.runNum         =  StringVar()
                self.allCardSelection = IntVar()
                self.overwriteVar     = IntVar()
                self.uploadFromStrVar = IntVar()
                self.armState       =  IntVar()
 
                # Place an all-encompassing frame in the parent window. All of the following
                # frames will be placed here (topMost_frame) and not in the parent window.
                self.topMost_frame = Frame(parent,bg=backc)
                self.topMost_frame.pack()

                # Add a flag to stop tests
                self.quitTestsFlag = False
                
                # Constants for controlling layout
                button_width = 6
                
                button_padx = "2m"
                button_pady = "1m"
                
                frame_padx = "3m"
                frame_pady = "2m"
                frame_ipadx = "3m"
                frame_ipady = "1m"
                # End layout constants

        
                ##########################################
                ###                                    ###
                ###     BEGIN MAKING SUB-FRAMES        ### 
                ###                                    ###
                ##########################################

                # Make and pack a sub-frame within topMost_frame that will contain
                # all of the controls for non-hardware related test information
                # (i.e. name of tester)
                self.info_frame = Frame(
                        self.topMost_frame,
                        borderwidth=5, relief=RIDGE,
                        height=50,
                        background=topc,
                        )
                self.info_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                # Make a top half-frame
                self.topHalf_frame = Frame(self.topMost_frame,bg=backc)
                self.topHalf_frame.pack(side=LEFT)

                # Make a frame for containing an experiment diagram
                self.experiment_frame = Frame(
                        self.topHalf_frame,
                        borderwidth=5, relief=RIDGE,
                        height=580, width=300,
                        background=leftc
                        )
                self.experiment_frame.pack_propagate=(False)
                self.experiment_frame.pack(
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                # Make a bottom half-frame
                self.botHalf_frame = Frame(self.topMost_frame,bg=backc)
                self.botHalf_frame.pack(side=LEFT)

                # Make and pack a sub-frame within the top right frame that will contain
                # all of the controls for talking with the QIE cards
                self.qie_frame = Frame(
                        self.botHalf_frame,
                        borderwidth=5, relief=RIDGE,
                        height=50,
                        background=rightc
                        )
                self.qie_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                # Make a uHTR frame. For now this will contain
                # information regarding the tests being conducted.
                self.uHTR_frame = Frame(
                        self.botHalf_frame,
                        borderwidth=5, relief=RIDGE,
                        height=250, width=400,
                        background=bottomc
                        )
                # We don't want this frame to shrink when placing widgets:

                #self.uHTR_frame.pack_propagate(False)          

                self.uHTR_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                ##########################################
                ###                                    ###
                ###     BEGIN MAKING WIDGETS           ### 
                ###                                    ###
                ##########################################

                ######################################
                #####                            #####
                #####    Widgets in info frame   #####
                #####                            #####
                ######################################

                # Make and pack a text label for name selector
                self.info_Label = Label(self.info_frame, text="Testing Information/Parameters")
                self.info_Label.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background=topc,
                        fg=fontc,font=(None,14)
                        )
                self.info_Label.pack(side=TOP)

                # Make a sub-sub-frame within the frame to hold another label and a dropdown box
                self.info_subTop_frame = Frame(self.info_frame,bg=topc)
                self.info_subTop_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                # Make a sub-sub-frame within the frame to hold the comment box
                self.info_subMid_frame = Frame(self.info_frame,bg=topc)
                self.info_subMid_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                # Make a sub-sub-frame within the frame to hold the run number
                self.info_subBot_frame = Frame(self.info_frame,background=topc)
                self.info_subBot_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                # Make a label for the name drop-down:
                self.info_nameLabel = Label(self.info_subTop_frame, text="Tester Name: ")
                self.info_nameLabel.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background=topc,
                        fg=fontc,font=(None,14)
                        )
                self.info_nameLabel.pack(side=LEFT)

                # Make and pack a listbox to pick which QIE card to talk to:
                self.info_nameBox = OptionMenu(self.info_subTop_frame, self.nameChoiceVar,"Bryan Caraway", "Grace Cummings", "Zach Eckert", "Loriza Hasa", "Frank Jensen", "Kamal Lamichhane", "Nesta Lenhert", "Chris Madrid", "Brooks McMaster", "Danny \"HF\" Noonan", "Joe Pastika", "Mark Saunders", "Sezen Sekmen", "Zach Shelton", "Caleb Smith", "Nadja Strobbe")
                self.info_nameBox.config(bg=topc,fg=fontc,font=(None,14), activebackground=dimc,activeforeground=fontc)
                self.info_nameBox["menu"].config(bg=topc,fg=fontc,font=(None,14),activebackground=dimc,activeforeground=fontc)
                self.info_nameBox.pack(side=LEFT)
                self.nameChoiceVar.set("Choose Name") # initializes the OptionMenu

                # Make a label for the name drop-down:
                self.info_commentLabel = Label(self.info_subMid_frame, text="User Testing Comments: ")
                self.info_commentLabel.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background=topc,
                        fg=fontc,font=(None,14)
                        )
                self.info_commentLabel.pack(side=LEFT)

                # Make a entrybox for testing comments
                self.info_commentBox = Entry(
                        self.info_subMid_frame,
                        textvariable=self.infoCommentVar
                        )
                self.info_commentBox.config(bg=topc,fg=fontc,font=(None,14))
                self.info_commentBox.pack(side=LEFT)

                # Make a label for the run number
                self.info_commentLabel = Label(self.info_subBot_frame, text="Run Number: ")
                self.info_commentLabel.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background=topc,
                        fg=fontc,font=(None,14)
                        )
                self.info_commentLabel.pack(side=LEFT)

                # Make an entrybox for the run number
                self.info_commentBox = Entry(
                        self.info_subBot_frame,
                        textvariable=self.runNum
                        )
                self.info_commentBox.config(bg=topc,fg=fontc,font=(None,14))
                self.info_commentBox.pack(side=LEFT)

                # Make a spacer
                self.info_commentLabel = Label(self.info_subBot_frame, text="   ")
                self.info_commentLabel.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background=topc,
                        fg=fontc,font=(None,14)
                        )
                self.info_commentLabel.pack(side=LEFT)

                #Make a button to determine the run number
                self.info_getRun_button = Button(self.info_subBot_frame, command = self.getRunNum)
                self.info_getRun_button.configure(text="Latest Run", background=buttonsc[9],fg=fontc,font=(None,14),activebackground=dimbuttonsc[9],activeforeground=fontc)
                self.info_getRun_button.configure(
                        width=button_width*2,
                        padx=button_padx,
                        pady=button_pady
                        )
                self.info_getRun_button.pack(side=LEFT)


                ######################################
                #####                            #####
                #####  Experiment Setup Frm      #####
                #####                            #####
                ######################################

                # Make a label for the entire frame
                self.experi_subFrame_lbl = Label(self.experiment_frame,text="Hardware Setup (Check boxes to add cards to test)")
                self.experi_subFrame_lbl.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background=leftc,
                        fg=fontc,font=(None,14)
                        )
                self.experi_subFrame_lbl.pack(side=TOP)

                # Make left subframe
                self.experi_subLeft_frame = Frame(self.experiment_frame,background=leftc)
                self.experi_subLeft_frame.pack(
                        side=LEFT,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                # Make right subframe
                self.experi_subRight_frame = Frame(self.experiment_frame,background=leftc)
                self.experi_subRight_frame.pack(
                        side=RIGHT,
                        ipady=frame_ipady,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                # Label for higher-level hardware
                self.experi_highlevel_lbl = Label(self.experi_subLeft_frame,text="High-Level\n")
                self.experi_highlevel_lbl.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background=leftc,
                        foreground=fontc
                        )
                self.experi_highlevel_lbl.pack(side=TOP)

                # Make and pack a checkbutton to enable ALL of the
                # QIE Card Slots
                self.allRadio = Checkbutton(
                        self.experi_subLeft_frame,
                        text="All slots",
                        variable=self.allCardSelection,
                        background=buttonsc[0],
                        activebackground=dimbuttonsc[0],
                        fg=fontc,font=(None,14),
                        activeforeground=fontc,
                        selectcolor=checkc,
                        command = self.allCheckBttnClick
                        )
                self.allRadio.configure(
                        padx=button_padx,
                        pady=button_pady
                        )
                self.allRadio.pack(side=TOP)

                self.blankLabel1 = Label(self.experi_subLeft_frame, text="", background=leftc)
                self.blankLabel1.pack(side=TOP)

                # Make and pack two checkbuttons that control each
                # nGCCme card
                self.ngccmeVarList = [IntVar(), IntVar()]
                
                for i in range(len(self.ngccmeSlots)):
                        self.ngccmeCheck = Checkbutton(
                                self.experi_subLeft_frame,
                                text = self.ngccmeSlots[i],
                                variable = self.ngccmeVarList[i],
                                background = buttonsc[1],   # sounds delicious
                                fg=fontc,font=(None,14),
                                activebackground=dimbuttonsc[1],
                                activeforeground=fontc,
                                selectcolor=checkc,
                                command = self.ngccmeCheckBttnClick
                                )
                        self.ngccmeCheck.configure(
                                padx=button_padx,
                                pady=button_pady,
                                )
                        self.ngccmeCheck.pack(side=TOP)

                self.blankLabel2 = Label(self.experi_subLeft_frame, text="", background=leftc)
                self.blankLabel2.pack(side=TOP)

                # Make and pack four checkbuttons that control all
                # four of the readout modules
                self.readoutVarList = [IntVar() for i in range(0,4)]
                
                for i in range(len(self.readoutSlots)):
                        self.readoutCheck = Checkbutton(
                                self.experi_subLeft_frame,
                                text = self.readoutSlots[i],
                                variable = self.readoutVarList[i],
                                background = buttonsc[2],
                                activebackground = dimbuttonsc[2],
                                fg=fontc,font=(None,14),
                                activeforeground=fontc,
                                selectcolor=checkc,
                                command = self.rmCheckBttnClick
                                )
                        self.readoutCheck.configure(
                                padx=button_padx,
                                pady=button_pady
                                )
                        self.readoutCheck.pack(side=TOP)

                # Label for individual card column
                self.experi_cards_lbl = Label(self.experi_subRight_frame,text="QIE Cards\n")
                self.experi_cards_lbl.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background=leftc,
                        fg=fontc,font=(None,14)
                        )
                self.experi_cards_lbl.pack(side=TOP)

        
                # Now we're dealing with individual card slots.
                # First, create many variables for the checkbuttons
                self.cardVarList = [IntVar() for i in range(0,17)]
                
                # Then, for each variable in cardVarList, add a
                # checkbutton that corresponds to it
                for i in range(len(self.cardSlots)):
                        self.cardRadio = Checkbutton(
                                self.experi_subRight_frame,
                                text = self.cardSlots[i],
                                variable = self.cardVarList[i+1],
                                background = buttonsc[3],
                                activebackground=dimbuttonsc[3],
                                fg=fontc,font=(None,14),
                                activeforeground=fontc,
                                selectcolor=checkc
                                )
                        self.cardRadio.configure(
                                padx=button_padx,
                                pady=button_pady,
                                )
                        self.cardRadio.pack(side=TOP)

                ######################################
                #####                            #####
                #####  Widgets in the QIE frame  #####
                #####                            #####
                ######################################

                #Make a text label for the frame
                self.qieFrameLabel = Label(self.qie_frame, text="Main Test & Suite Controls")
                self.qieFrameLabel.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background=rightc,
                        fg=fontc,font=(None,14)
                        )
                self.qieFrameLabel.pack(side=TOP)

                # Top sub-frame in QIE frame
                self.qie_subTop_frame = Frame(
                        self.qie_frame,
                        background=rightc
                        )
                self.qie_subTop_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                # Top sub-frame 1 in QIE frame
                self.qie_subTop_1_frame = Frame(
                        self.qie_frame,
                        background=rightc
                        )
                self.qie_subTop_1_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                # 2nd top sub-frame in QIE frame
                self.qie_subTop2_frame = Frame(
                        self.qie_frame,
                        background=rightc
                        )
                self.qie_subTop2_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
                        )

                # Make a sub-frame below the top sub-frame in QIE frame
                self.qie_subTopMid_frame = Frame(
                        self.qie_frame,
                        background=rightc
                        )
                self.qie_subTopMid_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
                        )

                # Make a 2nd sub-frame below the top sub-frame in QIE frame
                self.qie_subTopMid2_frame = Frame(
                        self.qie_frame,
                        background=rightc
                        )
                self.qie_subTopMid2_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
                        )

                # Mid sub-frame in QIE frame
                self.qie_subMid_frame = Frame(
                        self.qie_frame,
                        background=rightc
                        )
                self.qie_subMid_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

                # Bottom sub-frame in QIE frame
                self.qie_subBot_frame = Frame(
                        self.qie_frame,
                        background=rightc
                        )
                self.qie_subBot_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

#               # 2nd Bottom sub-frame in QIE frame
#                self.qie_subBot_2_frame = Frame(
#                        self.qie_frame,
#                        background="white"
#                        )
#                self.qie_subBot_2_frame.pack(
#                        side=TOP,
#                        ipadx=frame_ipadx,
#                        ipady=frame_ipady,
#                        padx=frame_padx,
#                        pady=frame_pady
#                        )
#
#               # 3rd Bottom sub-frame in QIE frame
#                self.qie_subBot_3_frame = Frame(
#                        self.qie_frame,
#                        background="white"
#                        )
#                self.qie_subBot_3_frame.pack(
#                        side=TOP,
#                        ipadx=frame_ipadx,
#                        ipady=frame_ipady,
#                        padx=frame_padx,
#                        pady=frame_pady
#                        )

#                # Make a label for rasp. pi selection
#                self.piSelectionLbl = Label(self.qie_subTop_frame, text="Choose the Pi to run on: ")
#                self.piSelectionLbl.configure(
#                        padx=button_padx,
#                        pady=button_pady,
#                        background=rightc,
#                        fg=fontc,font=(None,14)
#                        )
#                self.piSelectionLbl.pack(side=LEFT)
#
#                # Make a menu for the raspberry pi options
#                self.pi_choiceBox = OptionMenu(self.qie_subTop_frame, self.piChoiceVar,
#                                                "pi5", "pi6")
#                self.pi_choiceBox.config(bg=rightc,fg=fontc,font=(None,14),activebackground=dimc,activeforeground=fontc)
#                self.pi_choiceBox["menu"].config(bg=rightc,fg=fontc,font=(None,14),activebackground=dimc,activeforeground=fontc)
#                self.pi_choiceBox.pack(side=LEFT)
#                self.piChoiceVar.set("unused")

                # Make a label for number of iterations
                self.iter_label = Label(self.qie_subTop_1_frame, text="Number of iterations: ")
                self.iter_label.configure(bg=rightc,fg=fontc,font=(None,14))
                self.iter_label.pack(side=LEFT)

                # Make a field for number of iterations
                self.iter_entry = Entry(self.qie_subTop_1_frame, textvariable=self.iterationVar,bg=rightc,fg=fontc,font=(None,14))
                self.iter_entry.pack(side=RIGHT)
                self.iterationVar.set("5")

#                # Make a separation line
#                self.separationLabelTop = Label(self.qie_subTop2_frame, text="------------------------------------------")
#                self.separationLabelTop.configure(bg=rightc,fg=fontc,font=(None,14))
#                self.separationLabelTop.pack()
#
#                # Make a button to reset the backplane
#                self.qie_resetButton = Button(self.qie_subTopMid_frame, command={})
#                self.qie_resetButton.configure(text=".1.", bg=buttonsc[4],fg=fontc,font=(None,14),activebackground=dimbuttonsc[4],activeforeground=fontc)
#                self.qie_resetButton.configure(
#                        width=button_width*4,
#                        padx=button_padx,
#                        pady=button_pady
#                        )
#                self.qie_resetButton.pack(side=TOP)
#
#                # Make a button to cycle fan power
#                self.qie_fanButton = Button(self.qie_subTopMid_frame, command={})
#                self.qie_fanButton.configure(text=".2.", bg=buttonsc[5],fg=fontc,font=(None,14),activebackground=dimbuttonsc[5],activeforeground=fontc)
#                self.qie_fanButton.configure(
#                        width=button_width*4,
#                        padx=button_padx,
#                        pady=button_pady
#                        )
#                self.qie_fanButton.pack(side=TOP)
#
#
#                # Make a button to reset the backplane
#                self.qie_resetButton = Button(self.qie_subTopMid_frame, command={})
#                self.qie_resetButton.configure(text=".3.", bg=buttonsc[6],fg=fontc,font=(None,14),activebackground=dimbuttonsc[6],activeforeground=fontc)
#                self.qie_resetButton.configure(
#                        width=button_width*4,
#                        padx=button_padx,
#                        pady=button_pady
#                        )
#                self.qie_resetButton.pack(side=TOP)
#
#                # Make a button to reset the backplane
#                self.qie_magicButton = Button(self.qie_subTopMid_frame, command={})
#                self.qie_magicButton.configure(text=".4.", bg=buttonsc[7],fg=fontc,font=(None,14),activebackground=dimbuttonsc[7],activeforeground=fontc)
#                self.qie_magicButton.configure(
#                        width=button_width*4,
#                        padx=button_padx,
#                        pady=button_pady
#                        )
#                self.qie_magicButton.pack(side=TOP)

                # Make a separation line
                self.separationLabel = Label(self.qie_subTopMid2_frame, text="------------------------------------------")
                self.separationLabel.configure(bg=rightc,fg=fontc,font=(None,14))
                self.separationLabel.pack()

                # Make and pack a label for suite selection:
                self.qie_suiteLabel = Label(self.qie_subMid_frame, text="Select a suite to run: ")
                self.qie_suiteLabel.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background=rightc,
                        fg=fontc,font=(None,14)
                        )
                self.qie_suiteLabel.pack(side=LEFT)

                # Make and pack a menu for the suite selection
                self.qie_suiteMenu = OptionMenu(self.qie_subMid_frame, self.suiteChoiceVar,
                                                "Run Everything",
                                                "Run Register Test",
                                                "Process Run Control",
                                                "Process Plugin Output",
                                                )
                self.qie_suiteMenu.config(bg=rightc,fg=fontc,font=(None,14),activebackground=dimc,activeforeground=fontc)
                self.qie_suiteMenu["menu"].config(bg=rightc,fg=fontc,font=(None,14),activebackground=dimc,activeforeground=fontc)
                self.qie_suiteMenu.pack(side=LEFT)
                self.suiteChoiceVar.set("Run Everything")

#                # Make a checkbox to overwrite/not overwrite pre-existing data
#                self.overwriteBox = Checkbutton(self.qie_subBot_frame, text=".5.", variable=self.overwriteVar)
#                self.overwriteBox.configure(bg=buttonsc[8],fg=fontc,font=(None,14),activebackground=dimbuttonsc[8],activeforeground=fontc,selectcolor=checkc)
#                self.overwriteBox.pack(side=TOP,
#                                       padx = button_padx,
#                                       pady = button_pady,
#                                       ipady = button_pady*2,
#                                       ipadx = button_padx*2)
#                self.overwriteVar.set(1)

                #Make a button to run the main test suite
                self.qie_testSuite_button = Button(self.qie_subBot_frame, command = self.runTestSuite)
                self.qie_testSuite_button.configure(text="Run Selected Test Suite", background=buttonsc[9],fg=fontc,font=(None,14),activebackground=dimbuttonsc[9],activeforeground=fontc)
                self.qie_testSuite_button.configure(
                        width=button_width*4,
                        padx=button_padx,
                        pady=button_pady
                        )
                self.qie_testSuite_button.pack(side=TOP)

                # Make a separation line
                self.separationLabel = Label(self.qie_subBot_frame, text="------------------------------------------")
                self.separationLabel.configure(bg=rightc,fg=fontc,font=(None,14))
                self.separationLabel.pack()

#                # Make a checkbutton to manually type in desired upload folder
#                self.uploadFromStrBox = Checkbutton(self.qie_subBot_frame, text=".6.", variable = self.uploadFromStrVar, command = {})
#                self.uploadFromStrBox.configure(bg=buttonsc[10],fg=fontc,font=(None,14), wraplength=300,activebackground=dimbuttonsc[10],activeforeground=fontc,selectcolor=checkc)
#                self.uploadFromStrBox.pack(side=TOP,
#                                        padx = button_padx,
#                                        pady = button_pady,
#                                        ipady = button_pady*2,
#                                        ipadx = button_padx*2,
#                                        )
#
#                # Make a field for the manual folder entry (if so desired)
#                self.uploadFromStrField = Entry(self.qie_subBot_frame,
#                                                textvariable = self.uploadFromStrEntry, 
#                                                state = "readonly",
#                                                bg=rightc,
#                                                fg=fontc,font=(None,14),
#                                                disabledbackground=dimc,
#                                                readonlybackground=dimc
#                                                )
#                self.uploadFromStrField.configure(width=40)
#                self.uploadFromStrField.pack(side=TOP,
#                                             padx = button_padx,
#                                             pady = button_pady
#                                             )
#                

                # Make a button to submit the results from tests.
                self.qie_testSuite_button = Button(self.qie_subBot_frame, command = self.submitToDatabase)
                self.qie_testSuite_button.configure(text="Upload Results to Database", bg=buttonsc[10],fg=fontc,font=(None,14),activebackground=dimbuttonsc[10],activeforeground=fontc)
                self.qie_testSuite_button.configure(
                        width=button_width*4,
                        padx=button_padx,
                        pady=button_pady
                        )
                self.qie_testSuite_button.pack(side=TOP)


                #################################
                ###                           ###
                ###   WIDGETS IN uHTR FRAME   ###
                ###                           ###
                #################################
                # Make and pack a text label for the box label
                self.uHTR_frame_Label = Label(self.uHTR_frame, text="Expert Panel")
                self.uHTR_frame_Label.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background=bottomc,
                        fg=fontc,font=(None,14)
                        )
                self.uHTR_frame_Label.pack(side=TOP)

                # Make many text variables
                self.uHTR_slotNumber = [IntVar() for i in range(0,7)]

                # Make a subframe for the slot number label
                self.uHTR_sub2 = Frame(self.uHTR_frame, bg=bottomc)
                self.uHTR_sub2.pack(side=TOP, ipadx=frame_ipadx, ipady="1m",
                        padx=frame_padx, pady="1m")

#                # Slot number parameter label
#                self.uHTR_slotNo_Lbl = Label(self.uHTR_sub2, text="Slot Number: ",bg=bottomc,fg=fontc,font=(None,14))
#                self.uHTR_slotNo_Lbl.pack(side=LEFT,padx=button_padx,pady=button_pady)

                self.expertC = Checkbutton(
                        self.uHTR_sub2,
                        text = "Enable Expert Panel",
                        variable = self.armState,
                        command = self.expertArm,
                        background = buttonsc[3],
                        activebackground=dimbuttonsc[3],
                        fg=fontc,font=(None,14),
                        activeforeground=fontc,
                        selectcolor=checkc
                        )
                self.expertC.configure(
                        padx=button_padx,
                        pady=button_pady,
                        )
                self.expertC.pack(side=LEFT)

                # Make a subframe for the slot number vars
                self.uHTR_sub3 = Frame(self.uHTR_frame, bg=bottomc)
                self.uHTR_sub3.pack(side=TOP, ipadx=frame_ipadx, ipady="1m",
                        padx=frame_padx, pady="1m")

                # Make checkboxes for each uHTR slot
#                for i in range(0,6):
#                                self.uHTR_radio = Checkbutton(
#                                        self.uHTR_sub3,
#                                        text = str(i+1), anchor=S,
#                                        variable = self.uHTR_slotNumber[i+1],
#                                        background = buttonsc[3],
#                                        fg=fontc,font=(None,14),
#                                        activebackground=dimbuttonsc[3],
#                                        activeforeground=fontc,
#                                        selectcolor=checkc
#                                        )
#                                self.uHTR_radio.configure(
#                                        padx=button_padx,
#                                        pady=button_pady,
#                                        )
#                                self.uHTR_radio.pack(side=LEFT)
#                self.uHTR_slotNumber[1].set(1)
#                self.uHTR_slotNumber[2].set(1)
#
#                # Make top subframe 4
#                self.uHTR_sub4 = Frame(self.uHTR_frame, bg=bottomc)
#                self.uHTR_sub4.pack(side=TOP, ipadx=frame_ipadx, ipady="1m",
#                        padx=frame_padx, pady="1m")
#
#                # Button for doing uHTR tests
#                self.uHTR_tester_bttn = Button(self.uHTR_sub4, text=".7.", bg=buttonsc[8],fg=fontc,font=(None,14),activebackground=dimbuttonsc[8],activeforeground=fontc,
#                                                command={})
#                self.uHTR_tester_bttn.configure(
#                        padx=button_padx*2,
#                        pady=button_pady*2,
#                        )
#                self.uHTR_tester_bttn.pack(side=TOP)    

                # now, prepare the summaries:
        #       self.prepareOutCards()

###############################################################################################################
###############################################################################################################
###############################################################################################################

        #################################
        ###                           ###
        ###  BEGIN MEMBER FUNCTIONS   ###
        ###                           ###
        #################################
        
        def expertArm(self):
            if (self.armState.get() == 1):
                print "On"
            else:
                print "Off"

        def throwErrorBox(self,msg):
            self.top = Toplevel()
            self.top.title("Name Choice Error")
            self.top.config(height=50, width=360)
            self.top.pack_propagate(False)

            self.msg = Label(self.top, text=msg,fg=fontc)
            self.msg.pack()

            self.button = Button(self.top, text="OK", command=self.top.destroy)
            self.button.configure(bg=buttonsc[7],fg=fontc,activebackground=dimbuttonsc[7],activeforeground=fontc)
            self.button.pack()

################################################################################################
#### Functions for selecting various cards
################################################################################################

        def getRunNum(self):
            files = glob.glob('/home/hcalpro/DATA/FNAL*.root')
            numbers = []
            for file in files:
                 numbers.append(int(file[24:30]))
            self.runNum.set(max(numbers))
        
        def allCheckBttnClick(self):
                self.ngccmeVarList[0].set(self.allCardSelection.get())
                self.ngccmeVarList[1].set(self.allCardSelection.get())
                for i in range(0,4):
                        self.readoutVarList[i].set(self.allCardSelection.get())
                self.rmCheckBttnClick()

        def ngccmeCheckBttnClick(self):
                self.readoutVarList[0].set(self.ngccmeVarList[0].get())
                self.readoutVarList[1].set(self.ngccmeVarList[0].get())
                self.readoutVarList[2].set(self.ngccmeVarList[1].get())
                self.readoutVarList[3].set(self.ngccmeVarList[1].get())
                self.rmCheckBttnClick()

        def rmCheckBttnClick(self):
                for i in range(1,5): self.cardVarList[i].set(self.readoutVarList[0].get())
                for i in range(5,9): self.cardVarList[i].set(self.readoutVarList[1].get())
                for i in range(9,13): self.cardVarList[i].set(self.readoutVarList[2].get())
                for i in range(13,17): self.cardVarList[i].set(self.readoutVarList[3].get())

############################################################################################
#### Do a simple backplane reset
############################################################################################

        def qie_resetPress(self):
                # Instantiate a webBus member:
                b = webBus(self.piChoiceVar.get(),0)
                b.write(0x00,[0x06])
                b.sendBatch()
                print '\n\nBackplane for '+self.piChoiceVar.get()+' reset!\n\n'

############################################################################################
#### The "main" member function. This calls the various scripts to run tests.
############################################################################################

        def runTestSuite(self):
                if (self.nameChoiceVar.get() == "Choose Name"):
                    self.throwErrorBox("Select a tester name")
                elif ((self.runNum.get() == "") and (self.suiteChoiceVar.get() != "Run Register Test")):
                    self.throwErrorBox("Run Number Required")
                elif (self.suiteChoiceVar.get() == "Run Everything"):
                    os.system("./FixMe-Everything.sh %s %s %s %s" % (self.runNum.get(),'\''+self.iterationVar.get()+'\'','\''+self.nameChoiceVar.get()+'\'','\''+self.infoCommentVar.get()+'\''))
                elif (self.suiteChoiceVar.get() == "Process Run Control"):
                    os.system("./FixMe-RunControl.sh %s %s %s" % (self.runNum.get(),'\''+self.nameChoiceVar.get()+'\'','\''+self.infoCommentVar.get()+'\''))
                elif (self.suiteChoiceVar.get() == "Process Plugin Output"):
                    os.system("./FixMe-PluginOut.sh %s %s %s" % (self.runNum.get(),'\''+self.nameChoiceVar.get()+'\'','\''+self.infoCommentVar.get()+'\''))
                elif (self.suiteChoiceVar.get() == "Run Register Test"):
                    os.system("./FixMe-RegisterTest.sh %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" % (self.iterationVar.get(),
                        self.cardVarList[1].get(),self.cardVarList[2].get(),self.cardVarList[3].get(),self.cardVarList[4].get(),
                        self.cardVarList[5].get(),self.cardVarList[6].get(),self.cardVarList[7].get(),self.cardVarList[8].get(),
                        self.cardVarList[9].get(),self.cardVarList[10].get(),self.cardVarList[11].get(),self.cardVarList[12].get(),
                       self.cardVarList[13].get(),self.cardVarList[14].get(),self.cardVarList[15].get(),self.cardVarList[16].get(),'\''+self.nameChoiceVar.get()+'\'','\''+self.infoCommentVar.get()+'\''))
                    self.submitToDatabase()

############################################################################################
### Convert the checkboxes on the GUI to a list of QIE slots that will be useable
#### in the steps down the line. Essentially, we're converting numbers 1 through 16,
#### inclusive, into numbers in [2, 3, 4, 5, 7, 8, 9, 10, 18, 19, 20, 21, 23, 24, 25, 26]
############################################################################################
        
        def prepareOutSlots(self):
                self.outSlotNumbers = []
                for k in range(len(self.cardVarList)):
                        if (self.cardVarList[k].get() == 1):
                                if k in [1,2,3,4]:
                                        self.outSlotNumbers.append(k+1)
                                elif k in [5,6,7,8]:
                                        self.outSlotNumbers.append(k+2)
                                elif k in [9,10,11,12]:
                                        self.outSlotNumbers.append(k+9)
                                elif k in [13,14,15,16]:
                                        self.outSlotNumbers.append(k+10)

############################################################################################
#### For each selected QIE card, create an instance of the loggerClass so that results
#### may be reported.
############################################################################################

#        def prepareOutCards(self):
#                self.overwrite = False
#                if (self.overwriteVar.get() == 1): self.overwrite = True
#                for k in range(len(self.cardVarList)):
#                        if k in [1,2,3,4]:
#                                self.outSummaries.append(testSummary.testSummary((k+1), self.humanLogName, self.overwrite))
#                        elif k in [5,6,7,8]:
#                                self.outSummaries.append(testSummary.testSummary((k+2), self.humanLogName, self.overwrite))
#                        elif k in [9,10,11,12]:
#                                self.outSummaries.append(testSummary.testSummary((k+9), self.humanLogName, self.overwrite))
#                        elif k in [13,14,15,16]:
#                                self.outSummaries.append(testSummary.testSummary((k+10), self.humanLogName, self.overwrite))
#
#        def uploadFromStrBoxClick(self):
#                if self.uploadFromStrVar.get() == 1:
#                        self.uploadFromStrField.configure(state=NORMAL)
#                        self.makeWarningBox("Please be sure that you enter the appropriate folder (e.g. /home/hep/archivedResults/Jul142016_019485_Results/)") #5
#                else:
#                        self.uploadFromStrField.configure(state=DISABLED) 

############################################################################################
#### Self-explanatory. Calls Andrew's script to upload results to database.
############################################################################################

        def submitToDatabase(self):
            if ((self.runNum.get() == "") and (self.suiteChoiceVar.get() != "Run Register Test")):
                print ("Run Number Required")
            elif (self.suiteChoiceVar.get() == "Run Register Test"):
                os.system("./FixMe-Upload.sh %s %s %s %s" % (0,1,0,2))
            elif ((self.suiteChoiceVar.get() == "Process Run Control") or (self.suiteChoiceVar.get() == "Process Plugin Output")):
                os.system("./FixMe-Upload.sh %s %s %s %s" % (self.runNum.get(),0,1,1))
#                if self.uploadFromStrVar.get() == 1:
#                        self.folderArgument = self.uploadFromStrEntry.get()
#
#                else:
#                        self.folderArgument = '/home/hep'+self.folderArgument+'_Results'
#                        print "DEBUG:" + self.folderArgument
#
#                if (self.folderArgument == "/home/hep/999999999"):
#                        self.makeWarningBox("Please either run a test, or manually enter a folder.")
#                        return None
#        
#                subprocess.call("ssh cmshcal11 /home/django/testing_database/uploader/remote.sh "+self.folderArgument, shell=True)
#                print 'Files submitted to database!'
#
#                self.tempLogName =  self.humanLogName
#                self.humanLogName = "{:%b%d%Y_%H%M%S}".format(datetime.now())
#                sys.stdout = logClass.logger(self.humanLogName)
#                os.remove('/home/hep/logResults/'+self.tempLogName+'_tests.log')
#
#        def makeWarningBox(self, warningMessage):
#                self.top = Toplevel()
#                self.top.title("Attention!")
#                self.top.config(height=50, width=800)
#                self.top.pack_propagate(False)
#
#                self.msg = Label(self.top, text=warningMessage)
#                self.msg.pack()
#
#                self.button = Button(self.top, text="Continue", command=self.top.destroy)
#                self.button.configure(bg=buttonsc[4],fg=fontc,font=(None,14),activebackground=dimbuttonsc[4],activeforeground=fontc)
#                self.button.pack()
                
###############################################################################################################
###############################################################################################################
###############################################################################################################

def main():
    root = Tk()
    myapp = makeGui(root)
    #sys.stdout = logClass.logger(myapp.humanLogName)
    root.mainloop()

if __name__ == '__main__':
    sys.exit(main())
