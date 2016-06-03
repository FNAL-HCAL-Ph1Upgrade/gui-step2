# This is a program that will implement a GUI with which one can make
# commands for Jordan's nGCCe client

from Tkinter import *

class makeGui:
	def __init__(self, parent):

		#Initialize some parameters for use later on
		self.myParent = parent

		self.pyTitle = StringVar()
	
		self.checkVar7 = IntVar()
		self.checkVar6 = IntVar()
		self.checkVar5 = IntVar()
		self.checkVar4 = IntVar()
		self.checkVar3 = IntVar()
		self.checkVar2 = IntVar()
		self.checkVar1 = IntVar()
		self.checkVar0 = IntVar()

		self.ng_checkVar5 = IntVar()
		self.ng_checkVar4 = IntVar()
		self.ng_checkVar3 = IntVar()
		self.ng_checkVar2 = IntVar()
		self.ng_checkVar1 = IntVar()
		self.ng_checkVar0 = IntVar()

		#Topmost frame is called topMost_frame
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

		# Frame for asking the .py filename
		self.pyTitle_frame = Frame(
			self.topMost_frame,
			borderwidth=5, relief=RIDGE,
			height=50,
			background="white"
			)
		self.pyTitle_frame.pack(
			side=TOP,
			ipadx=frame_ipadx,
			ipady=frame_ipady,
			padx=frame_padx,
			pady=frame_pady
			)

		# Frame for writing to fanout board
		self.fanout_frame = Frame(
			self.topMost_frame,
			borderwidth=5, relief=RIDGE,
			height=50,
			background="white"
			)
		self.fanout_frame.pack(
			side=TOP,
			ipadx=frame_ipadx,
			ipady=frame_ipady,
			padx=frame_padx,
			pady=frame_pady
			)

		# Frame for writing to ngCCM 
		self.ngccm_frame = Frame(
			self.topMost_frame,
			borderwidth=5, relief=RIDGE,
			height=50,
			background="white"
			)
		self.ngccm_frame.pack(
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
		#####  Widgets in pyTitle frame  #####
		#####				 #####
		######################################

		#Make a text label for the .py filename box
		self.pyEntryLabel = Label(self.pyTitle_frame, text="Name of routine: ")
		self.pyEntryLabel.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.pyEntryLabel.pack(side=TOP)

		#Make a textbox for the .py filename
		self.pyEntry = Entry(self.pyTitle_frame, textvariable=self.pyTitle)
		self.pyEntry.pack(side=TOP)

		#Make a button to accept the .py file title
		self.titleButton = Button(self.pyTitle_frame, command=self.titleButtonClick)
		self.titleButton.configure(text="ACCEPT",background="lime")
		self.titleButton.configure(
			width=button_width,
			padx=button_padx,
			pady=button_pady
			)
		self.titleButton.pack(side=TOP)

		######################################
		#####				 #####
		#####  Widgets in fanout frame   #####
		#####				 #####
		######################################
		
		#Make a text label for the frame
		self.fanoutLabel = Label(self.fanout_frame, text="Fanout Board Controls")
		self.fanoutLabel.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.fanoutLabel.pack(side=TOP)

		# Top sub-frame in fanout
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

		#Make checkbox 7
		self.check7 = Checkbutton(self.fanout_subTop_frame,text="7", variable=self.checkVar7)
		self.check7.pack(side=LEFT)
		#Make checkbox 6
		self.check6 = Checkbutton(self.fanout_subTop_frame,text="6", variable=self.checkVar6)
		self.check6.pack(side=LEFT)
		#Make checkbox 5
		self.check5 = Checkbutton(self.fanout_subTop_frame,text="5", variable=self.checkVar5)
		self.check5.pack(side=LEFT)
		#Make checkbox 4
		self.check4 = Checkbutton(self.fanout_subTop_frame,text="4", variable=self.checkVar4)
		self.check4.pack(side=LEFT)
		#Make checkbox 3
		self.check3 = Checkbutton(self.fanout_subTop_frame,text="3", variable=self.checkVar3)
		self.check3.pack(side=LEFT)
		#Make checkbox 2
		self.check2 = Checkbutton(self.fanout_subTop_frame,text="2", variable=self.checkVar2)
		self.check2.pack(side=LEFT)
		#Make checkbox 1
		self.check1 = Checkbutton(self.fanout_subTop_frame,text="1", variable=self.checkVar1)
		self.check1.pack(side=LEFT)
		#Make checkbox 0
		self.check0 = Checkbutton(self.fanout_subTop_frame,text="0", variable=self.checkVar0)
		self.check0.pack(side=LEFT)

		#Make a button to write to address
		self.fanout_write_Button = Button(self.fanout_frame, command=self.fanoutClickWrite)
		self.fanout_write_Button.configure(text="WRITE",background="lime")
		self.fanout_write_Button.configure(
			width=button_width*2,
			padx=button_padx,
			pady=button_pady
			)
		self.fanout_write_Button.pack(side=LEFT)

		#Make a button to read what is at the fanout address
		self.fanout_read_Button = Button(self.fanout_frame, command=self.fanoutClickRead)
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

		#Make a text label for the frame
		self.ngCCMLabel = Label(self.ngccm_frame, text="ngCCM Board Controls")
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

		#Make checkbox 5
		self.ngCCM_check5 = Checkbutton(self.ngccm_subTop_frame,text="5", variable=self.ng_checkVar5)
		self.ngCCM_check5.pack(side=LEFT)
		#Make checkbox 4
		self.ngCCM_check4 = Checkbutton(self.ngccm_subTop_frame,text="4", variable=self.ng_checkVar4)
		self.ngCCM_check4.pack(side=LEFT)
		#Make checkbox 3
		self.ngCCM_check3 = Checkbutton(self.ngccm_subTop_frame,text="3", variable=self.ng_checkVar3)
		self.ngCCM_check3.pack(side=LEFT)
		#Make checkbox 2
		self.ngCCM_check2 = Checkbutton(self.ngccm_subTop_frame,text="2", variable=self.ng_checkVar2)
		self.ngCCM_check2.pack(side=LEFT)
		#Make checkbox 1
		self.ngCCM_check1 = Checkbutton(self.ngccm_subTop_frame,text="1", variable=self.ng_checkVar1)
		self.ngCCM_check1.pack(side=LEFT)
		#Make checkbox 0
		self.ngCCM_check0 = Checkbutton(self.ngccm_subTop_frame,text="0", variable=self.ng_checkVar0)
		self.ngCCM_check0.pack(side=LEFT)

		#Make a button to write the hex number
		self.ngCCM_write_Button = Button(self.ngccm_frame, command=self.ngccmClickWrite)
		self.ngCCM_write_Button.configure(text="WRITE",background="lime")
		self.ngCCM_write_Button.configure(
			width=button_width*2,
			padx=button_padx,
			pady=button_pady
			)
		self.ngCCM_write_Button.pack(side=LEFT)

		#Make a button to read what is at the address
		self.ngCCM_read_Button = Button(self.ngccm_frame, command=self.ngccmClickRead)
		self.ngCCM_read_Button.configure(text="READ",background="khaki")
		self.ngCCM_read_Button.configure(
			width=button_width*2,
			padx=button_padx,
			pady=button_pady
			)
		self.ngCCM_read_Button.pack(side=RIGHT)
	


	def titleButtonClick(self):
		print self.pyTitle.get()

	def fanoutClickWrite(self):
		hexVar = (self.checkVar0.get()*1)+(self.checkVar1.get()*2)+(self.checkVar2.get()*4)+\
		         (self.checkVar3.get()*8)+(self.checkVar4.get()*16)+(self.checkVar5.get()*32)+\
			 (self.checkVar6.get()*64)+(self.checkVar7.get()*128)
		print "0x{:02x}".format(hexVar)

	def fanoutClickRead(self):
		print "This should read the fanout value."

	def ngccmClickWrite(self):
		hexVar = (self.ng_checkVar0.get()*1)+(self.ng_checkVar1.get()*2)+(self.ng_checkVar2.get()*4)+\
			 (self.ng_checkVar3.get()*8)+(self.ng_checkVar4.get()*16)+(self.ng_checkVar5.get()*32)
		print "0x{:02x}".format(hexVar)

	def ngccmClickRead(self):
		print "This should read the ngCCM value."

root = Tk()
myapp = makeGui(root)
root.mainloop()
