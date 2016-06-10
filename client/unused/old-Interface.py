# This is a program that will implement a GUI with which one can make
# commands for Jordan's nGCCe client

from Tkinter import *
import client

class makeGui:
	def __init__(self, parent):

		# Name the parent. This is mostly for bookkeeping purposes
		# and doesn't really get used too much.
		self.myParent = parent

		# Create some string variables for text entry/display boxes
		self.ngccmHexText = StringVar()
		self.fanoutHexText = StringVar()
	
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
		# all of the controls for communicating with the fanout board
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

		# Make and pack a sub-frame within topMost_frame that will contain
		# all of the controls for communicating with the ngccms
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

		# Make and pack a sub-frame within topMost_frame that will contain
		# all of the controls for talking with the QIE cards
		self.qie_frame = Frame(
			self.topMost_frame,
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


		##########################################
		###                                    ###
		###	BEGIN MAKING WIDGETS           ### 
		###		                       ###
		##########################################


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
		self.qieFrameLabel = Label(self.qie_frame, text="QIE Chips   -   Hex Codes: 0x19 to 0x1c")
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

		#Make a button to write the hex number
		self.qie_write_Button = Button(self.qie_subBot_frame, command=self.qieClickWrite)
		self.qie_write_Button.configure(text="WRITE",background="green")
		self.qie_write_Button.configure(
			width=button_width*2,
			padx=button_padx,
			pady=button_pady
			)
		self.qie_write_Button.pack(side=RIGHT)

		#Make a button to read what is at the address
		self.qie_read_Button = Button(self.qie_subTop_frame, command=self.qieClickRead)
		self.qie_read_Button.configure(text="READ",background="khaki")
		self.qie_read_Button.configure(
			width=button_width*2,
			padx=button_padx,
			pady=button_pady
			)
		self.qie_read_Button.pack(side=RIGHT)


	#################################
	###			      ###
	###  BEGIN MEMBER FUNCTIONS   ###
	###			      ###
	#################################

	def checksToHex(self,inCheck0,inCheck1,inCheck2,inCheck3,inCheck4,inCheck5,inCheck6,inCheck7):
		hexVar = (inCheck0*1)+(inCheck1*2)+(inCheck2*4)+(inCheck3*8)+(inCheck4*16)+\
			 (inCheck5*32)+(inCheck6*64)+(inCheck7*128)
		return hexVar

	def fanoutClickWrite(self):
		hexCon = self.checksToHex(self.checkVar0.get(),self.checkVar1.get(),self.checkVar2.get(),self.checkVar3.get(),
			 self.checkVar4.get(),self.checkVar5.get(),self.checkVar6.get(),self.checkVar7.get())
		client.write_byte(0x72, hexCon)
		self.fanoutClickRead()

	def fanoutClickRead(self):
		self.fanoutHexText.set(client.read_byte_s(0x72))
		print self.fanoutHexText.get()

	def ngccmClickWrite(self):
		hexCon = self.checksToHex(self.ng_checkVar0.get(), self.ng_checkVar1.get(), self.ng_checkVar2.get(),
			 self.ng_checkVar3.get(),self.ng_checkVar4.get(),self.ng_checkVar5.get(), 0, 0)
		client.write_byte(0x74, hexCon)
		self.ngccmClickRead()

	def ngccmClickRead(self):
		self.ngccmHexText.set(client.read_byte_s(0x74))
		print self.ngccmHexText.get()

	def qieClickRead(self): print "This is a read placeholder"
	def qieClickWrite(self): print "This is a write placeholder"

root = Tk()
myapp = makeGui(root)
root.mainloop()
