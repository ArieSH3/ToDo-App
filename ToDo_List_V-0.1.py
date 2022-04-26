'''
	Creating a ToDo App with tkinter and possibly later recreate
		it with PyQt5 as it has more features and a more modern look.

	App will store a list of items which user can add or remove
		as well as keep track of the date when the item needs to
		be completed if needed.
'''


import tkinter as tk
import pickle # Used for storing data (encodes it I think)
import time
# import PyQt5 # Maybe use in another project



class ToDo_App:
	def __init__(self, root):
		# ============= ROOT ==========================================
		self.root = root

		# ============= RESOURCES =====================================
		self.width, self.height = 800, 600
		self.screenwidth = self.root.winfo_screenwidth()
		self.screenheight = self.root.winfo_screenheight()

			# Format for setting App in the middle of the screen in root.geometry()
		self.app_middle_align = '{}x{}+{}+{}'.format(\
			self.width, self.height, \
			int((self.screenwidth - self.width)/2), \
			int((self.screenheight - self.height)/2))

		self.background_top_col = '#FAF5F8' #
		self.background_bot_col = '#2F2536'
		self.list_background_col = '#FAF5F8' #
		self.button_col = '#BDBDFF'
		self.label_font_col = '#2F2536' #
		self.font_col = '#2F2536' #
		self.check_col = '#60BDC3'

		self.font = 'Helvetica 10 bold'
		self.label_font = 'Helvetica 24 bold'

		self.marked = set() # Used to check if item in list in checked/marked or not

		# ============= ROOT CONFIG ====================================
		self.root.geometry(self.app_middle_align)
		self.root.resizable(False,False)
		self.root.config(bg=self.background_top_col)
		self.root.title('~To Do App~')


		# -_-_-_-_-_-_- MAIN WINDOW -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
		# ==== FRAMEs ====
		# = TOP =
		self.frame_title = tk.Frame(self.root)
		self.frame_title.config(bg=self.background_bot_col, height=self.height/9)
		self.frame_title.pack(padx=10, pady=(10,0), fill='x')

		# = MIDDLE =
		self.frame_middle = tk.Frame(self.root)
		self.frame_middle.config(bg=self.background_top_col, width=self.width, height=self.height/1.4)
		self.frame_middle.pack(fill='both', expand=True)

		self.frame_list = tk.Frame(self.frame_middle)
		self.frame_list.config(bg=self.background_bot_col, width=self.width/1.3, height=self.height/2)
		self.frame_list.pack(padx=(10,0), pady=(10,0), fill='y', side='left')

		self.frame_commands = tk.Frame(self.frame_middle)
		self.frame_commands.config(bg=self.background_bot_col)
		self.frame_commands.pack(padx=10, pady=(10,0), fill='both', expand=True, side='left')

		# = BOTTOM =
		self.frame_input = tk.Frame(self.root)
		self.frame_input.config(bg=self.background_bot_col, width=self.width)#, height=1)
		self.frame_input.pack(padx=10, pady=10, fill='both')


		
		# === WIDGETS FOR TOP ===
		# = LABEL =
		self.label_title = tk.Label(self.frame_title)
		self.label_title.config(text='~ ~ ~To ~ Do ~ App~ ~ ~', bg=self.background_bot_col, fg=self.background_top_col, font=self.label_font)
		self.label_title.pack()

		

		# === WIDGETS FOR MIDDLE ===
		# = LISTBOX =
		self.listbox_items = tk.Listbox(self.frame_list)
		self.listbox_items.config(height = 18, width=88, borderwidth=0, bg=self.list_background_col, font=self.font, fg=self.font_col)
		self.listbox_items.pack(side='left', fill='both', padx=5, pady=5)

		# = BUTTONs =
		self.button_add = tk.Button(self.frame_commands, command=self.add_item)
		self.button_add.config(text='Add', font=self.font, fg=self.font_col, bg=self.button_col)
		self.button_add.pack(padx=10, pady=(10,0), fill='x', side='top')

		self.button_remove = tk.Button(self.frame_commands, command=self.remove_item)
		self.button_remove.config(text='Remove', font=self.font, fg=self.font_col, bg=self.button_col)
		self.button_remove.pack(padx=10, pady=(10,0), fill='x', side='top')

		self.button_remove_all = tk.Button(self.frame_commands, command=self.remove_all)
		self.button_remove_all.config(text='Remove All', font=self.font, fg=self.font_col, bg=self.button_col)
		self.button_remove_all.pack(padx=10, pady=(10,0), fill='x', side='top')

		self.button_open_item = tk.Button(self.frame_commands, command=self.open_selected_item_in_list)
		self.button_open_item.config(text='Open', font=self.font, fg=self.font_col, bg=self.button_col)
		self.button_open_item.pack(padx=10, pady=(10,0), fill='x', side='top')

		self.button_completed_item = tk.Button(self.frame_commands, command=self.mark_completed_item)
		self.button_completed_item.config(text='Mark', font=self.font, fg=self.font_col, bg=self.button_col)
		self.button_completed_item.pack(padx=10, pady=(10,0), fill='x', side='top')

		# = LABEL =
		self.label_list_size_display = tk.Label(self.frame_commands)
		self.label_list_size_display.config(text='Num of Items: {}'.format(self.listbox_items.size()), bg=self.background_bot_col, font=self.font, fg=self.list_background_col)
		self.label_list_size_display.pack(padx=10, pady=10, fill='x', side='bottom')
		
		# = TOP LEVEL =
		self.toplevel_display_item = tk.Toplevel(self.root)
		self.toplevel_display_item.resizable(True, True)
		self.toplevel_display_item.geometry(self.app_middle_align)

		

		# === WIDGETS FOR BOTTOM ===
		# = TEXT =
		self.text_input = tk.Text(self.frame_input)
		self.text_input.config(height=5, borderwidth=0, bg=self.list_background_col, font=self.font, fg=self.font_col, wrap=tk.WORD)
		self.text_input.pack(padx=5, pady=5, fill='both', side='bottom')



		# === BUTTON BINDS ===
		# Binds Enter to add_item method
		self.root.bind('<Return>', self.add_item)
		
		# When listbox out of focus it will deselect any selected items
		# Lambda needs to be used because it represents a function and bind takes a function
		#	as second argument( Another function can be created that just calls list.selection_clear
		#	but this is more efficient)
		self.listbox_items.bind('<FocusOut>', lambda e: self.listbox_items.selection_clear(0, tk.END))





		# -_-_-_-_-_-_- LIST ITEM DISPLAY WINDOW -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
		# = TOP LEVEL =
		# self.toplevel_item_display = tk.Toplevel(self.root)
		# self.toplevel_item_display.resizable(True, True)
		# self.toplevel_item_display.geometry(self.app_middle_align)
		# self.toplevel_item_display.config(bg=self.background_top_col)
		# self.toplevel_item_display.title('~To Do App~/Item Display')

		# # = FRAMEs =
		# self.frame_display = tk.Frame(self.toplevel_item_display)
		# self.frame_display.config(bg=self.background_bot_col)
		# self.frame_display.pack()




	# ============ METHODS =============================================================

	def add_item(self, event=None): # Add item to the list(box) and to the storage file (Pickle)
		to_input = self.text_input.get('1.0', 'end').strip()
		if len(to_input)>0:
			t = time.localtime()
			
			self.listbox_items.insert('end', '({}/{}/{} {}:{}) : {}'.format( \
				t.tm_mday, t.tm_mon, t.tm_year, t.tm_hour, t.tm_min, to_input))
	
	
		# Clear the input field 
		self.text_input.delete('1.0', 'end')
		self.get_list_size()


	def remove_item(self): # Remove item from list(box) and from storage file (Pickle)
		self.listbox_items.delete(self.listbox_items.curselection())
		self.get_list_size()

	
	def remove_all(self): # Remove all items from list(box) and from storage file (Pickle)
		self.listbox_items.delete(0, tk.END)
		self.get_list_size()

	
	def get_list_size(self): # Return the size of the list to the user
		self.label_list_size_display['text'] = 'Num of Items: {}'.format(self.listbox_items.size())
		#print('Text from list:', self.listbox_items.get(0, tk.END)[self.listbox_items.curselection()[0]])
		#print(type(self.listbox_items.curselection()))

	
	def open_selected_item_in_list(self): # Will open selected item in list in a new window in text widget since it can wrap text and listbox cant
		
		if self.listbox_items.curselection():
			# -_-_-_-_-_-_- LIST ITEM DISPLAY WINDOW -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
			# = TOP LEVEL =
			self.toplevel_item_display = tk.Toplevel(self.root)
			self.toplevel_item_display.resizable(True, True)
			self.toplevel_item_display.geometry(self.app_middle_align)
			self.toplevel_item_display.config(bg=self.background_top_col)
			self.toplevel_item_display.title('~To Do App~/Item Display')

			# = FRAMEs =
			self.frame_display = tk.Frame(self.toplevel_item_display)
			self.frame_display.config(bg=self.background_bot_col)
			self.frame_display.pack(fill='both', expand=True)

			# = TEXT =
			self.text_item_display = tk.Text(self.frame_display)
			self.text_item_display.config(bg=self.list_background_col, font=self.font, fg=self.font_col, wrap=tk.WORD)
			self.text_item_display.pack(padx=20, pady=20, fill='both', expand=True)



			# Add item from list to text display so it can be read properly
			self.text_item_display.insert(tk.INSERT, self.listbox_items.get(0, tk.END)[self.listbox_items.curselection()[0]])
			# Disabling the editing of the file as it is only meant for reading and/or copying
			self.text_item_display['state'] = 'disabled'

	def mark_completed_item(self): # Will 'check' the item in list that is completed so user can keep track
		list_of_all_items = self.listbox_items.get(0, 'end')
		print('Test: ', self.listbox_items.get(self.listbox_items.curselection()))
		# Checks if item in listbox selected
		if self.listbox_items.curselection():
			# Checks if time and text are not in marked set
			# MIGHT CAUSE A BIT OF TROUBLE WITH MARKING IF SAME TEXT POSTED AT THE SAME TIME (Minute is the lowest time variable)
			if self.listbox_items.get(self.listbox_items.curselection()) not in self.marked:
				# Changes the colour of the item background
				self.listbox_items.itemconfig(self.listbox_items.curselection()[0], {'bg':self.check_col})
				# Adds item text to the marked set
				self.marked.add(self.listbox_items.get(self.listbox_items.curselection()))
				
			else:
				# Changes colour of item background back to original (unmarked)
				self.listbox_items.itemconfig(self.listbox_items.curselection()[0], {'bg':self.background_top_col})
				# Removes item from marked set as it is no longer marked
				self.marked.remove(self.listbox_items.get(self.listbox_items.curselection()))
				


	def retrieve_list(self): # Retrieve list content from pickled file
		pass

	def move_up(self): # Move item up in list(box) and storage file
		pass

	def move_down(self): # Move item down in list(box) and storage file
		pass




if __name__ == '__main__':
	root = tk.Tk()
	window = ToDo_App(root)


	root.mainloop()