# User-Interface.py
#
# This is the main Graphical User Interface for communicating
# with the setup in the lab.
# Developed with the help of many people
# For Baylor University, Summer 2016.

# This is a comment to see if I got git to work properly

from Tkinter import *
from client import webBus
import qieCommands
from datetime import datetime

class makeGui:
	def __init__(self, parent):

		# Instantiate a webBus member:
		self.gb = webBus("pi5")		

		# Name the parent. This is mostly for bookkeeping purposes
		# and doesn't really get used too much.
		self.myParent = parent

		# Create some string variables for text entry/display boxes
		self.ngccmHexText   =  StringVar()
		self.fanoutHexText  =  StringVar()
		self.qieChoiceVar   =  StringVar()
		self.qieReadVar     =  StringVar()
#		self.qieWriteVar    =  StringVar()
		self.qieOutText     =  StringVar()
		self.nameChoiceVar  =  StringVar()
		self.infoCommentVar =  StringVar()
	
		# Create integer variables for the fanout box's checkbuttons.
		# Although they're integers, they should only ever hold the
		# values 1 or 0.
		self.checkVar7 = IntVar()
		self.checkVar6 = IntVar()
		self.checkVar5 = IntVar()
		self.checkVar4 = IntVar()
		self.checkVar3 = IntVar()
		self.checkVar2 = IntVar()
		self.checkVar1 = IntVar()
		self.checkVar0 = IntVar()

		# More integer variables for checkbuttons. This time for the ngCCM box.
		self.ng_checkVar5 = IntVar()
		self.ng_checkVar4 = IntVar()
		self.ng_checkVar3 = IntVar()
		self.ng_checkVar2 = IntVar()
		self.ng_checkVar1 = IntVar()
		self.ng_checkVar0 = IntVar()

		# Place an all-encompassing frame in the parent window. All of the following
		# frames will be placed here (topMost_frame) and not in the parent window.
		self.topMost_frame = Frame(parent)
		self.topMost_frame.pack()
		
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
		self.topHalf_frame.pack(side=TOP)

		# Make a bottom half-frame
		self.botHalf_frame = Frame(self.topMost_frame)
		self.botHalf_frame.pack(side=TOP)

		# Make and pack a sub-frame within topMost_frame that will contain
		# all of the controls for communicating with the fanout board
		self.fanout_frame = Frame(
			self.topHalf_frame,
			borderwidth=5, relief=RIDGE,
			height=50,
			background="white"
			)
		self.fanout_frame.pack(
			side=LEFT,
			ipadx=frame_ipadx,
			ipady=frame_ipady,
			padx=frame_padx,
			pady=frame_pady
			)

		# Make and pack a sub-frame within topMost_frame that will contain
		# all of the controls for communicating with the ngccms
		self.ngccm_frame = Frame(
			self.topHalf_frame,
			borderwidth=5, relief=RIDGE,
			height=50,
			background="white"
			)
		self.ngccm_frame.pack(
			side=LEFT,
			ipadx=frame_ipadx,
			ipady=frame_ipady,
			padx=frame_padx,
			pady=frame_pady
			)

		# Make and pack a sub-frame within topMost_frame that will contain
		# all of the controls for talking with the QIE cards
		self.qie_frame = Frame(
			self.botHalf_frame,
			borderwidth=5, relief=RIDGE,
			height=50,
			background="white"
			)
		self.qie_frame.pack(
			side=LEFT,
			ipadx=frame_ipadx,
			ipady=frame_ipady,
			padx=frame_padx,
			pady=frame_pady
			)

		self.placehold_frame = Frame(
			self.botHalf_frame,
			borderwidth=5, relief=RIDGE,
			height=250, width=400,
			background="white"
			)
		# We don't want this frame to shrink when placing widgets:
		self.placehold_frame.pack_propagate(False)		

		self.placehold_frame.pack(
			side=LEFT,
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
		#####				 #####
		#####  Widgets in fanout frame   #####
		#####				 #####
		######################################
		
		# Make and pack a text label for the fanout frame
		self.fanoutLabel = Label(self.fanout_frame, text="Clock Fanout Board   -   Hex Code: 0x72")
		self.fanoutLabel.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.fanoutLabel.pack(side=TOP)

		# Make a sub-sub-frame within the fanout frame that will allow us to better control
		# the layout. This one is called subTop_frame, as it will go on top of the subBot_frame
		# (which gets created below).
		self.fanout_subTop_frame = Frame(
			self.fanout_frame,
			background="white"
			)
		self.fanout_subTop_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

		# Make a sub-sub-frame within the fanout frame. This one will go beneath the subTop_frame
		# (created above)
		self.fanout_subBot_frame = Frame(
			self.fanout_frame,
			background="white"
			)
		self.fanout_subBot_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

		#Make and pack a simple "multiplexer: " label
		self.fanoutPlexLabel = Label(self.fanout_subTop_frame,text="Multiplexer: ")
		self.fanoutPlexLabel.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.fanoutPlexLabel.pack(side=LEFT)

		#Add a text field that outputs the hex address. Make it readonly.
                self.fanoutHexTextBox = Entry(self.fanout_subTop_frame, textvariable=self.fanoutHexText,state="readonly",readonlybackground="gray90")
                self.fanoutHexTextBox.pack(side=LEFT)

		#Make checkbox 7
		self.check7 = Checkbutton(self.fanout_subBot_frame,text="7", variable=self.checkVar7)
		self.check7.pack(side=LEFT)
		#Make checkbox 6
		self.check6 = Checkbutton(self.fanout_subBot_frame,text="6", variable=self.checkVar6)
		self.check6.pack(side=LEFT)
		#Make checkbox 5
		self.check5 = Checkbutton(self.fanout_subBot_frame,text="5", variable=self.checkVar5)
		self.check5.pack(side=LEFT)
		#Make checkbox 4
		self.check4 = Checkbutton(self.fanout_subBot_frame,text="4", variable=self.checkVar4)
		self.check4.pack(side=LEFT)
		#Make checkbox 3
		self.check3 = Checkbutton(self.fanout_subBot_frame,text="3", variable=self.checkVar3)
		self.check3.pack(side=LEFT)
		#Make checkbox 2
		self.check2 = Checkbutton(self.fanout_subBot_frame,text="2", variable=self.checkVar2)
		self.check2.pack(side=LEFT)
		#Make checkbox 1
		self.check1 = Checkbutton(self.fanout_subBot_frame,text="1", variable=self.checkVar1)
		self.check1.pack(side=LEFT)
		#Make checkbox 0
		self.check0 = Checkbutton(self.fanout_subBot_frame,text="0", variable=self.checkVar0)
		self.check0.pack(side=LEFT)

		#Make a button to write to fanout and assign it to the member function "self.fanoutClickWrite"
		self.fanout_write_Button = Button(self.fanout_subBot_frame, command=self.fanoutClickWrite)
		self.fanout_write_Button.configure(text="WRITE",background="green")
		self.fanout_write_Button.configure(
			width=button_width*2,
			padx=button_padx,
			pady=button_pady
			)
		self.fanout_write_Button.pack(side=RIGHT)

		#Make a button to read what is at the fanout. Member function is "self.fanoutClickRead"
		self.fanout_read_Button = Button(self.fanout_subTop_frame, command=self.fanoutClickRead)
		self.fanout_read_Button.configure(text="READ",background="khaki")
		self.fanout_read_Button.configure(
			width=button_width*2,
			padx=button_padx,
			pady=button_pady
			)
		self.fanout_read_Button.pack(side=RIGHT)


		######################################
		#####				 #####
		##### Widgets in the ngCCM frame #####
		#####				 #####
		######################################
	
		# I'm going to spare some comments here. For the most part, this is the exact
		# same logic as what is in the "Widgets in the fanout frame" section of code.

		#Make a text label for the frame
		self.ngCCMLabel = Label(self.ngccm_frame, text="ngCCM Board   -   Hex Code: 0x74")
		self.ngCCMLabel.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.ngCCMLabel.pack(side=TOP)

		# Top sub-frame in ngCCM
		self.ngccm_subTop_frame = Frame(
			self.ngccm_frame,
			background="white"
			)
		self.ngccm_subTop_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

		# Bottom sub-frame in ngCCM
                self.ngccm_subBot_frame = Frame(
                        self.ngccm_frame,
                        background="white"
                        )
                self.ngccm_subBot_frame.pack(
                        side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

		#Add textbox that says "Multiplexer: "
                self.ngccmPlexLabel = Label(self.ngccm_subTop_frame,text="Multiplexer: ")
                self.ngccmPlexLabel.configure(
                        padx=button_padx,
                        pady=button_pady,
                        background="white"
                        )
                self.ngccmPlexLabel.pack(side=LEFT)

		#Add a text field that outputs the hex address
		self.ngccmHexTextBox = Entry(self.ngccm_subTop_frame, textvariable=self.ngccmHexText,state="readonly",readonlybackground="gray90")
		self.ngccmHexTextBox.pack(side=LEFT)

		#Make checkbox 5 (We only use 5 checkboxes because of some hardware things)
		self.ngCCM_check5 = Checkbutton(self.ngccm_subBot_frame,text="5", variable=self.ng_checkVar5)
		self.ngCCM_check5.pack(side=LEFT)
		#Make checkbox 4
		self.ngCCM_check4 = Checkbutton(self.ngccm_subBot_frame,text="4", variable=self.ng_checkVar4)
		self.ngCCM_check4.pack(side=LEFT)
		#Make checkbox 3
		self.ngCCM_check3 = Checkbutton(self.ngccm_subBot_frame,text="3", variable=self.ng_checkVar3)
		self.ngCCM_check3.pack(side=LEFT)
		#Make checkbox 2
		self.ngCCM_check2 = Checkbutton(self.ngccm_subBot_frame,text="2", variable=self.ng_checkVar2)
		self.ngCCM_check2.pack(side=LEFT)
		#Make checkbox 1
		self.ngCCM_check1 = Checkbutton(self.ngccm_subBot_frame,text="1", variable=self.ng_checkVar1)
		self.ngCCM_check1.pack(side=LEFT)
		#Make checkbox 0
		self.ngCCM_check0 = Checkbutton(self.ngccm_subBot_frame,text="0", variable=self.ng_checkVar0)
		self.ngCCM_check0.pack(side=LEFT)

		#Make a button to write the hex number
		self.ngCCM_write_Button = Button(self.ngccm_subBot_frame, command=self.ngccmClickWrite)
		self.ngCCM_write_Button.configure(text="WRITE",background="green")
		self.ngCCM_write_Button.configure(
			width=button_width*2,
			padx=button_padx,
			pady=button_pady
			)
		self.ngCCM_write_Button.pack(side=RIGHT)

		#Make a button to read what is at the address
		self.ngCCM_read_Button = Button(self.ngccm_subTop_frame, command=self.ngccmClickRead)
		self.ngCCM_read_Button.configure(text="READ",background="khaki")
		self.ngCCM_read_Button.configure(
			width=button_width*2,
			padx=button_padx,
			pady=button_pady
			)
		self.ngCCM_read_Button.pack(side=RIGHT)

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
		self.qie_testSuite_button.pack()

		#################################
		###			      ###
		###  WIDGETS IN P.HOLD FRAME  ###
		###			      ###
		#################################


		#Make a widget that closes the GUI
		self.closeButton = Button(self.placehold_frame, text="Close Window", background="orange red",
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

	def checksToHex(self,inCheck0,inCheck1,inCheck2,inCheck3,inCheck4,inCheck5,inCheck6,inCheck7):
		hexVar = (inCheck0*1)+(inCheck1*2)+(inCheck2*4)+(inCheck3*8)+(inCheck4*16)+\
			 (inCheck5*32)+(inCheck6*64)+(inCheck7*128)
		return hexVar
	
	def closeButtonPress(self):
		# IF ANYTHING SHOULD BE DONE ON CANCELLATION
		# PUT IT IN THIS FUNCTION
		self.myParent.destroy()

	def fanoutClickWrite(self):
		hexCon = self.checksToHex(self.checkVar0.get(),self.checkVar1.get(),self.checkVar2.get(),self.checkVar3.get(),
			 self.checkVar4.get(),self.checkVar5.get(),self.checkVar6.get(),self.checkVar7.get())
		self.gb.write(0x72,[hexCon])
		self.gb.sendBatch()
		self.fanoutClickRead()

	def fanoutClickRead(self):
		self.gb.read(0x72,1)
		self.fanoutHexText.set(hex(int(self.gb.sendBatch()[0])))

	def ngccmClickWrite(self):
		hexCon = self.checksToHex(self.ng_checkVar0.get(), self.ng_checkVar1.get(), self.ng_checkVar2.get(),
			 self.ng_checkVar3.get(),self.ng_checkVar4.get(),self.ng_checkVar5.get(), 0, 0)
		self.gb.write(0x74,[hexCon])
		self.gb.sendBatch()
		self.ngccmClickRead()

	def ngccmClickRead(self):
		self.gb.read(0x74,1)
		self.ngccmHexText.set(hex(int(self.gb.sendBatch()[0])))

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
		#ONCE IT'S TIME TO TEST OTHER READOUT MODULES, MAKE THE APPROPRIATE CHANGES HERE
		for card in (0x19,0x1a,0x1b,0x1c):
			with open(self.nameChoiceVar.get()+"_"+str(hex(card))+"_readableLog.log", 'w') as humanFile:
				with open(self.nameChoiceVar.get()+"_"+str(hex(card))+"_machineLog.log", 'w') as machineFile:
					self.runTestSuiteHelper(card,humanFile,machineFile)
		print "\nSuite Completed! Thank you! (:"

	def runTestSuiteHelper(self,card,humanFile,machineFile):
		dateString = str(datetime.now())
		humanFile.write("Test performed by: "+self.nameChoiceVar.get())
		humanFile.write("\nTime of testing: "+dateString)
		humanFile.write("\nTesting comment(s):"+self.infoCommentVar.get()+"\n")
		machineFile.write(dateString+"\n")
		machineFile.write(self.nameChoiceVar.get()+"\n")
		machineFile.write(self.infoCommentVar.get()+"\n\n")
		qieCommands.runCompleteSuite(card,humanFile,machineFile)	

# These next few lines call the class and display the window
# on the computer screen
root = Tk()
myapp = makeGui(root)
root.mainloop()
