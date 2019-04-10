#!/usr/bin/python
# -*- coding: utf-8 -*

from tkinter import *
import tkinter.filedialog
from tkinter.messagebox import *
from isql import isql

import unicodedata

class App:
	def __init__(self, root):
		root.title('isql')
		root.bind('<Return>', self.parse)

		self.sentence_frame = LabelFrame(root, text="Input Sentence", padx=5, pady=5)
		self.sentence_frame.pack(fill="both", expand="yes", padx=10, pady=5)

		self.input_sentence_string = StringVar() 
		self.input_sentence_string.set("Enter a sentence...")
		self.input_sentence_entry = Entry(self.sentence_frame, textvariable=self.input_sentence_string, width=50)
		self.input_sentence_entry.pack()
		self.input_sentence_entry.bind('<Button-1>', self.clearEntry)


		self.database_frame = LabelFrame(root, text="Database Selection", padx=5, pady=5)
		self.database_frame.pack(fill="both", expand="yes", padx=10, pady=5)

		self.database_path_label = Label(self.database_frame, text="No SQL dump selected...")
		self.database_path_label.pack(side="left")

		self.load_database_button = Button(self.database_frame, text="Choose a SQL dump", command=self.find_sql_file, width=20)
		self.load_database_button.pack(side="right")


		self.go_button = Button(root, text="Go!", command=self.lanch_parsing)
		self.go_button.pack(side="right", fill="both", expand="yes", padx=10, pady=2)

		self.reset_button = Button(root, text="Reset", fg="red", command=self.reset_window)
		self.reset_button.pack(side="right", fill="both", expand="yes", padx=10, pady=2)

	def clearEntry(self, event):
		self.input_sentence_string.set("")

	def parse(self, event):
		self.lanch_parsing()

	def find_sql_file(self):
		filename = tkinter.filedialog.askopenfilename(title="Select a SQL file",filetypes=[('sql files','.sql'),('all files','.*')])
		self.database_path_label["text"] = filename


	def reset_window(self):
		self.database_path_label["text"] = "No SQL dump selected..."
		self.input_sentence_string.set("Enter a sentence...")
		return

	def lanch_parsing(self):
		try:
			thesaurus_path = None
			json_output_path = None
			stopwords_path = None

			if (str(self.database_path_label["text"]) != "No SQL dump selected...") and (str(self.input_sentence_string.get()) != "Enter a sentence..."):
				isql(self.database_path_label["text"], str("F:\isql-python3\lang\english.csv"), self.input_sentence_string.get() , str("F:\isql-python3\output.json"), thesaurus_path, stopwords_path)
				showinfo('Result', 'Parsing done!')
			else:
				showwarning('Warning','You must fill in all fields, please.')
		except Exception as e:
			showwarning('Error', e)
		return

root = Tk()
App(root)
root.resizable(width=FALSE, height=FALSE)
root.mainloop()