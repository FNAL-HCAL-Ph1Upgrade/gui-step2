# User-Interface.py
#
# This is the main Graphical User Interface for communicating
# with the setup in the lab.
# Developed with the help of many people
# For Baylor University, Summer 2016.

# This is a comment to see if I got git to work properly

from Tkinter import *
from client import webBus
from qieCommands import qieCommands
from datetime import datetime

class makeGui:
	def __init__(self, parent):

		# Create a list of QIECard slots:
		self.cardSlots = ["Card 1", "Card 2", "Card 3", "Card 4", "Card 5",
			     "Card 6","Card 7", "Card 8", "Card 9", "Card 10",
			     "Card 11", "Card 12", "Card 13", "Card 14",
			     "Card 15", "Card 16"]

		# Create a list of nGCCme slots:
		self.ngccmeSlots = ["nGCCme 1", "nGCCme 2"]

		# Create a list of Readout Modules:
		self.readoutSlots = ["RM 1", "RM 2", "RM 3", "RM 4"]
	
		# Instantiate a qieCommands class member
		self.myCommands = qieCommands()

		# Instantiate a webBus member:
		self.gb = webBus("pi5")		

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
		self.allCardSelection = IntVar()
	
		# Place an all-encompassing frame in the parent window. All of the following
		# frames will be placed here (topMost_frame) and not in the parent window.
		self.topMost_frame = Frame(parent)
		self.topMost_frame.pack()

		# Add a flag to stop tests
		self.quitTestsFlag = False
		
		#----- constants for controlling layout
		button_width = 6
		
		button_padx = "2m"
		button_pady = "1m"
		
		frame_padx = "3m"
		frame_pady = "2m"
		frame_ipadx = "3m"
		frame_ipady = "1m"
		#---------- end layout constants ------

	
		##########################################
		###                                    ###
		###	BEGIN MAKING SUB-FRAMES        ### 
		###		                       ###
		##########################################

		# Make and pack a sub-frame within topMost_frame that will contain
		# all of the controls for non-hardware related test information
		# (i.e. name of tester)
		self.info_frame = Frame(
			self.topMost_frame,
			borderwidth=5, relief=RIDGE,
			height=50,
			background="white",
			)
		self.info_frame.pack(
			side=TOP,
			ipadx=frame_ipadx,
			ipady=frame_ipady,
			padx=frame_padx,
			pady=frame_pady
			)

		# Make a top half-frame
		self.topHalf_frame = Frame(self.topMost_frame)
		self.topHalf_frame.pack(side=LEFT)

		# Make a frame for containing an experiment diagram
		self.experiment_frame = Frame(
			self.topHalf_frame,
			borderwidth=5, relief=RIDGE,
			height=580, width=300,
			background="white"
			)
		self.experiment_frame.pack_propagate=(False)
		self.experiment_frame.pack(
			ipadx=frame_ipadx,
			ipady=frame_ipady,
			padx=frame_padx,
			pady=frame_pady
			)

		# Make a bottom half-frame
		self.botHalf_frame = Frame(self.topMost_frame)
		self.botHalf_frame.pack(side=RIGHT)

		# Make and pack a sub-frame within topMost_frame that will contain
		# all of the controls for talking with the QIE cards
		self.qie_frame = Frame(
			self.botHalf_frame,
			borderwidth=5, relief=RIDGE,
			height=50,
			background="white"
			)
		self.qie_frame.pack(
			side=TOP,
			ipadx=frame_ipadx,
			ipady=frame_ipady,
			padx=frame_padx,
			pady=frame_pady
			)

		# Make a runtime frame. For now this will contain
		# information regarding the tests being conducted.
		self.runtime_frame = Frame(
			self.botHalf_frame,
			borderwidth=5, relief=RIDGE,
			height=250, width=400,
			background="white"
			)
		# We don't want this frame to shrink when placing widgets:
		self.runtime_frame.pack_propagate(False)		

		self.runtime_frame.pack(
			side=TOP,
			ipadx=frame_ipadx,
			ipady=frame_ipady,
			padx=frame_padx,
			pady=frame_pady
			)

		##########################################
		###                                    ###
		###	BEGIN MAKING WIDGETS           ### 
		###		                       ###
		##########################################

		######################################
		#####				 #####
		#####    Widgets in info frame   #####
		#####				 #####
		######################################

		# Make and pack a text label for name selector
		self.info_Label = Label(self.info_frame, text="Testing Information/Parameters")
		self.info_Label.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.info_Label.pack(side=TOP)

		# Make a sub-sub-frame within the frame to hold another label and a dropdown box
		self.info_subTop_frame = Frame(self.info_frame,background="white")
		self.info_subTop_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

		# Make a sub-sub-frame within the frame to hold comment box
		self.info_subBot_frame = Frame(self.info_frame,background="white")
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
			background="white"
			)
		self.info_nameLabel.pack(side=LEFT)

		# Make and pack a listbox to pick which QIE card to talk to:
		self.info_nameBox = OptionMenu(self.info_subTop_frame, self.nameChoiceVar,
					      "shogan","csmith","asmith","jpotarf",
					      "jlawrence","abaas")
		self.info_nameBox.pack(side=LEFT)
		self.nameChoiceVar.set("shogan") # initializes the OptionMenu

		# Make a label for the name drop-down:
		self.info_commentLabel = Label(self.info_subBot_frame, text="User Testing Comments: ")
		self.info_commentLabel.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.info_commentLabel.pack(side=LEFT)

		# Make a entrybox for testing comments
		self.info_commentBox = Entry(
			self.info_subBot_frame,
			textvariable=self.infoCommentVar
			)
		self.info_commentBox.pack(side=LEFT)

		######################################
		#####                            #####
		#####  Experiment Setup Frm      #####
		#####				 #####
		######################################

		# Make a label for the entire frame
		self.experi_subFrame_lbl = Label(self.experiment_frame,text="Hardware Setup (Check boxes to add cards to test)")
		self.experi_subFrame_lbl.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.experi_subFrame_lbl.pack(side=TOP)

		# Make left subframe
		self.experi_subLeft_frame = Frame(self.experiment_frame,background="white")
		self.experi_subLeft_frame.pack(
			side=LEFT,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)

		# Make right subframe
		self.experi_subRight_frame = Frame(self.experiment_frame,background="white")
		self.experi_subRight_frame.pack(
			side=LEFT,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)

		# Make far right subframe
		self.experi_farRight_frame = Frame(self.experiment_frame,background="white")
		self.experi_farRight_frame.pack(
			side=LEFT,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)


		# Label for higher-level hardware
		self.experi_highlevel_lbl = Label(self.experi_subLeft_frame,text="High-Level\n")
		self.experi_highlevel_lbl.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.experi_highlevel_lbl.pack(side=TOP)

		# Make and pack a checkbutton to enable ALL of the
		# QIE Card Slots
		self.allRadio = Checkbutton(
			self.experi_subLeft_frame,
			text="All slots",
			variable=self.allCardSelection,
			background="DarkSeaGreen1",
			command = self.allCheckBttnClick
			)
		self.allRadio.configure(
			padx=button_padx,
			pady=button_pady
			)
		self.allRadio.pack(side=TOP)

		self.blankLabel1 = Label(self.experi_subLeft_frame, text="", background="white")
		self.blankLabel1.pack(side=TOP)

		# Make and pack two checkbuttons that control each
		# nGCCme card
		self.ngccmeVarList = [IntVar(), IntVar()]
		
		for i in range(len(self.ngccmeSlots)):
			self.ngccmeCheck = Checkbutton(
				self.experi_subLeft_frame,
				text = self.ngccmeSlots[i],
				variable = self.ngccmeVarList[i],
				background = "lemon chiffon",   # sounds delicious
				command = self.ngccmeCheckBttnClick
				)
			self.ngccmeCheck.configure(
				padx=button_padx,
				pady=button_pady,
				)
			self.ngccmeCheck.pack(side=TOP)

		self.blankLabel2 = Label(self.experi_subLeft_frame, text="", background="white")
		self.blankLabel2.pack(side=TOP)

		# Make and pack four checkbuttons that control all
		# four of the readout modules
		self.readoutVarList = [IntVar() for i in range(0,4)]
		
		for i in range(len(self.readoutSlots)):
			self.readoutCheck = Checkbutton(
				self.experi_subLeft_frame,
				text = self.readoutSlots[i],
				variable = self.readoutVarList[i],
				background = "light cyan",
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
			background="white"
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
				background = "lavender"
				)
			self.cardRadio.configure(
				padx=button_padx,
				pady=button_pady,
				)
			self.cardRadio.pack(side=TOP)

		# Now, we add stuff to the farRight frame
		
		# Far-right label
		# Label for card barcode column
		self.experi_barcode_lbl = Label(self.experi_farRight_frame,text="Barcodes\n")
		self.experi_barcode_lbl.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.experi_barcode_lbl.pack(side=TOP)

		# Create many barcode variables
		self.barcodeVarList = [StringVar() for i in range(0,17)]

		# Then, for each variable in barcodeVarList, add a Entry corresponding to it
		for i in range(1,17):
			self.barcodeEntry = Entry(
				self.experi_farRight_frame,
				textvariable=self.barcodeVarList[i],
				borderwidth=4
				)
			self.barcodeEntry.pack(side=TOP)

		######################################
		#####				 #####
		#####  Widgets in the QIE frame  #####
		#####				 #####
		######################################

		#Make a text label for the frame
		self.qieFrameLabel = Label(self.qie_frame, text="QIE Cards   -   Hex Codes: 0x19 to 0x1c")
		self.qieFrameLabel.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.qieFrameLabel.pack(side=TOP)

		# Top sub-frame in QIE frame
		self.qie_subTop_frame = Frame(
			self.qie_frame,
			background="white"
			)
		self.qie_subTop_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

		# Make a sub-frame below the top sub-frame in QIE frame
                self.qie_subTopMid_frame = Frame(
                        self.qie_frame,
                        background="white"
                        )
                self.qie_subTopMid_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

		# Mid sub-frame in QIE frame
		self.qie_subMid_frame = Frame(
			self.qie_frame,
			background="white"
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
                        background="white"
                        )
                self.qie_subBot_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

		# Make and pack a text label for the following option menu
                self.qieChoiceLabel = Label(self.qie_subTop_frame, text="Choose QIE card to communicate with: ")
                self.qieChoiceLabel.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background="white"
                        )
		self.qieChoiceLabel.pack(side=LEFT)

		# Make and pack a listbox to pick which QIE card to talk to:
		self.qie_listBox = OptionMenu(self.qie_subTop_frame, self.qieChoiceVar,
					      '0x19','0x1a','0x1b','0x1c')
		self.qie_listBox.pack(side=LEFT)
		self.qieChoiceVar.set('0x19') # initializes the OptionMenu

		# Make and pack a label for the following qie_outputText box
		self.qie_outputTextLabel = Label(self.qie_subTopMid_frame, text="QIE Returned: ")
		self.qie_outputTextLabel.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.qie_outputTextLabel.pack(side=LEFT)

		# Make and pack a textbox to display the output from talking with QIE cards
		self.qie_outputText = Entry(self.qie_subTopMid_frame, textvariable=self.qieOutText,state="readonly",readonlybackground="gray90")
		self.qie_outputText.pack(side=LEFT)

		# Make and pack a text label for the read test to run
                self.qieReadLabel = Label(self.qie_subMid_frame, text="Select a test to run: ")
                self.qieReadLabel.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background="white"
                        )
                self.qieReadLabel.pack(side=LEFT)

		# Make and pack a PLACEHOLDER LISTBOX for the variable to read:
                self.qie_readBox = OptionMenu(self.qie_subMid_frame, self.qieReadVar,
                                              "Unique ID","Herm Test","Brdg Test",
				              "255 Test","Zero Test","FW Version", "Humidity",
					      "Temperature","Get Status")
                self.qie_readBox.pack(side=LEFT)
                self.qieReadVar.set("Unique ID") # initializes the OptionMenu

		#Make a button to read what is at the address
		self.qie_read_Button = Button(self.qie_subMid_frame, command=self.qieClickRead)
		self.qie_read_Button.configure(text="RUN TEST",background="khaki")
		self.qie_read_Button.configure(
			width=button_width*2,
			padx=button_padx,
			pady=button_pady
			)
		self.qie_read_Button.pack(side=RIGHT)

		#Make a button to run the main test suite
		self.qie_testSuite_button = Button(self.qie_subBot_frame, command = self.runTestSuite)
		self.qie_testSuite_button.configure(text="RUN MAIN TEST SUITE", background="turquoise")
		self.qie_testSuite_button.configure(
			width=button_width*4,
			padx=button_padx,
			pady=button_pady
			)
		self.qie_testSuite_button.pack(side=LEFT)

		#################################
		###			      ###
		### WIDGETS IN RUNTIME FRAME  ###
		###			      ###
		#################################
		
		# Make and pack a text label for name selector
		self.runtime_Label = Label(self.runtime_frame, text="Testing Status & Runtime Information")
		self.runtime_Label.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.runtime_Label.pack(side=TOP)

		# Top sub-frame in runtime frame
		self.runtime_subTop_frame = Frame(
			self.runtime_frame,
			background="white"
			)
		self.runtime_subTop_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

		# Make a label for number of tests run
		self.testsRun_Label = Label(self.runtime_subTop_frame, text="Number of tests run: ")
		self.testsRun_Label.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.testsRun_Label.pack(side=LEFT)

		# Make a box to actually display the number of labels run
		self.runtime_outputText = Entry(
			self.runtime_subTop_frame,
			textvariable=self.runtimeNumber)
		self.runtime_outputText.pack(side=LEFT)
		self.runtimeNumber.set(1)

		#Make a button that removes all barcodes
		self.clearBarcodeBttn = Button(
			self.runtime_frame,
			text="Clear Entered Barcodes",
			background="salmon1",
			command=self.clearBarcodePress
			)
		self.clearBarcodeBttn.configure(
			padx=button_padx*2,
			pady=button_pady*2
			)
		self.clearBarcodeBttn.pack(side=TOP)

		#Make a widget that closes the GUI
		self.closeButton = Button(self.runtime_frame, text="Close Window", background="orange red",
					  command=self.closeButtonPress)
		self.closeButton.configure(
			padx=button_padx*2,
			pady=button_pady*2,
			)
		self.closeButton.pack(side=TOP)
	
	#################################
	###			      ###
	###  BEGIN MEMBER FUNCTIONS   ###
	###			      ###
	#################################
	
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

	def clearBarcodePress(self):
		for i in range(1,17):
			self.barcodeVarList[i].set("")


	def checksToHex(self,inCheck0,inCheck1,inCheck2,inCheck3,inCheck4,inCheck5,inCheck6,inCheck7):
		hexVar = (inCheck0*1)+(inCheck1*2)+(inCheck2*4)+(inCheck3*8)+(inCheck4*16)+\
			 (inCheck5*32)+(inCheck6*64)+(inCheck7*128)
		return hexVar
	
	def closeButtonPress(self):
		# IF ANYTHING SHOULD BE DONE ON CANCELLATION
		# PUT IT IN THIS FUNCTION
		self.myParent.destroy()

	def qieClickRead(self):     # Where the magic(?) happens
		# See what test the user has selected, and then run that test from the
		# qieCommands.py file. Display the results in the text field within the
		# QIE frame on the main GUI window.
		tempInt = int(self.qieChoiceVar.get(),16)
		if self.qieReadVar.get() == "Herm Test": 
			self.qieOutText.set(str(hex(tempInt))+":    "+qieCommands.hermTest(tempInt))
		elif self.qieReadVar.get() == "Brdg Test":
			self.qieOutText.set(str(hex(tempInt))+":    "+qieCommands.brdgTest(tempInt))
		elif self.qieReadVar.get() == "255 Test":
			self.qieOutText.set(str(hex(tempInt))+":    "+qieCommands.tff_Test(tempInt))
		elif self.qieReadVar.get() == "Zero Test":
			self.qieOutText.set(str(hex(tempInt))+":    "+qieCommands.zeroTest(tempInt))
		elif self.qieReadVar.get() == "FW Version":
			self.qieOutText.set(str(hex(tempInt))+":    "+qieCommands.fwVerTest(tempInt))
		elif self.qieReadVar.get() == "Get Status":
			self.qieOutText.set(str(hex(tempInt))+":    "+qieCommands.statusCheck(tempInt))
		elif self.qieReadVar.get() == "Temperature":
			self.qieOutText.set(str(hex(tempInt))+":    "+str(qieCommands.sensorTemp(0,tempInt))+" C")  #This will be changed as more slots get used
		elif self.qieReadVar.get() == "Humidity":
			self.qieOutText.set(str(hex(tempInt))+":    "+str(qieCommands.sensorHumid(0,tempInt))) #Will be changes as more RM slots get used
		elif self.qieReadVar.get() == "Unique ID":
			self.qieOutText.set(str(hex(tempInt))+":    "+str(qieCommands.getUniqueID(0,tempInt)))

	def runTestSuite(self):
		print str(datetime.now())
		#ONCE IT'S TIME TO TEST OTHER READOUT MODULES, MAKE THE APPROPRIATE CHANGES HERE
		for k in range(0,int(self.runtimeNumber.get())):
			if (k%10 == 0):
				print "Number of tests completed: ", k
			for card in (0x19,0x1a,0x1b,0x1c):
				self.runTestSuiteHelper(card,k)
		print "\nSuite Completed! Thank you! (:"
		print str(datetime.now())

	def runTestSuiteHelper(self,card,inNumber):
		self.myCommands.runCompleteSuite(card,inNumber)

# These next few lines call the class and display the window
# on the computer screen
root = Tk()
myapp = makeGui(root)
root.mainloop()
