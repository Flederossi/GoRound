from tkinter import *
from tkinter import filedialog
import os.path
import os

filename = ""
synt = ["func", "import", "package", "if", "for", "return", "main", "type", "struct", "nil", "string", "float32", "float64", "int", "Print", "Println"]
auto_str = ""
alt = False

if os.path.isfile("config.txt"):
	with open("config.txt", "r") as f:
		data = f.read().split(";")
		print("Data: " + str(data))
		red = data[0]
		blue = data[1]
		green = data[2]
		orange = data[3]
		lila = data[4]
		ins_key = data[5]

else:
	with open("config.txt", "w") as f:
		f.write("#f92472;#63cde7;#a6e22b;#fd9622;#ac80d1;Control_R")

	with open("config.txt", "r") as f:
		data = f.read().split(";")
		print("Data: " + str(data))
		red = data[0]
		blue = data[1]
		green = data[2]
		orange = data[3]
		lila = data[4]
		ins_key = data[5]

def syntax():
	global red, blue, green, orange, lila

	for tag in textarea.tag_names():
		textarea.tag_delete(tag)

	textarea.tag_config("red_tag", foreground=red)
	textarea.tag_config("blue_tag", foreground=blue)
	textarea.tag_config("green_tag", foreground=green)
	textarea.tag_config("orange_tag", foreground=orange)
	textarea.tag_config("lila_tag", foreground=lila)

	syntax_tag("func", "blue_tag", 4)
	syntax_tag("import", "red_tag", 6)
	syntax_tag("package", "red_tag", 7)
	syntax_tag("return", "red_tag", 6)
	syntax_tag("main", "green_tag", 4)
	syntax_tag("type", "blue_tag", 4)
	syntax_tag("struct", "green_tag", 6)
	syntax_tag("(", "orange_tag", 1)
	syntax_tag(")", "orange_tag", 1)
	syntax_tag("{", "orange_tag", 1)
	syntax_tag("}", "orange_tag", 1)
	syntax_tag("=", "red_tag", 1)
	syntax_tag(":", "red_tag", 1)
	syntax_tag("'", "green_tag", 1)
	syntax_tag('"', "green_tag", 1)
	syntax_tag("float32", "lila_tag", 7)
	syntax_tag("float64", "lila_tag", 7)
	syntax_tag("int", "lila_tag", 3)
	syntax_tag("string", "lila_tag", 6)
	syntax_tag("Print", "lila_tag", 5)
	syntax_tag("Println", "lila_tag", 7)
	syntax_tag("+", "red_tag", 1)
	syntax_tag("-", "red_tag", 1)
	syntax_tag("*", "red_tag", 1)
	syntax_tag("/", "red_tag", 1)
	syntax_tag("<", "red_tag", 1)
	syntax_tag(">", "red_tag", 1)
	syntax_tag("if", "red_tag", 2)
	syntax_tag("for", "red_tag", 3)
	syntax_tag("return", "red_tag", 6)
	syntax_tag("nil", "red_tag", 3)
	for i in range(10):
		syntax_tag(str(i), "lila_tag", 1)

def syntax_tag(string, tag, offset):
	string_start = textarea.search(string, '1.0', END)

	while string_start:
		string_end = string_start + "+" + str(offset) + "c"
		textarea.tag_add(tag, string_start, string_end)
		if string == "(":
			if textarea.get(string_end + "-2c wordstart", string_end + "-1c").lstrip() != "import":
				textarea.tag_add("green_tag", string_end + "-2c wordstart", string_end + "-1c")
		string_start = textarea.search(string, string_end, END)

def new_file():
	global filename
	textarea.delete(1.0,END)
	filename = ""
	root.title("Untitled - GoRound")
	lbl.config(text="GoRound - 1.9.2 ~ Untitled | Line: " + str(textarea.index(INSERT).split('.')[0]) + ", Column: " + str(textarea.index(INSERT).split('.')[1]))

def save_file():
	global filename
	if filename == "":
		save_file_as()
	else:
		with open(filename, 'w') as f:
			f.write(textarea.get(1.0,END))

def save_file_as():
	global filename
	try:
		filename = filedialog.asksaveasfilename(defaultextension=".go")
		with open(filename, 'w') as f:
			f.write(textarea.get(1.0,END))
			root.title(filename + " - GoRound")
			lbl.config(text="GoRound - 1.9.2 ~ " + filename + " | Line: " + str(textarea.index(INSERT).split('.')[0]) + ", Column: " + str(textarea.index(INSERT).split('.')[1]))
	except:
		pass

def open_file():
	global filename
	try:
		filename = filedialog.askopenfilename()
		with open(filename, 'r') as f:
			textarea.delete(1.0,END)
			textarea.insert(1.0,f.read())
			root.title(filename + " - GoRound")
			lbl.config(text="GoRound - 1.9.2 ~ " + filename + " | Line: " + str(textarea.index(INSERT).split('.')[0]) + ", Column: " + str(textarea.index(INSERT).split('.')[1]))
			syntax()
	except:
		pass

def autosyntax():
	global synt, auto_str

	character = textarea.get(INSERT)
	x, y, width, height = textarea.bbox(INSERT)

	screen_x = x + (0 if character == u'\n' else width)
	screen_y = y + height + 2
	for word in synt:
		if textarea.get("insert-1c wordstart", "insert").lstrip() == word[0:len(textarea.get("insert-1c wordstart", "insert").lstrip())] and textarea.get("insert-1c wordstart", "insert").lstrip() != "":
			autolbl.config(text=word, bg="black")
			auto_str = word
			break
		else:
			autolbl.config(text="", bg='#%02x%02x%02x' % (40, 41, 35))
			auto_str = ""

	autolbl.place(x=screen_x, y=screen_y)

	root.after(10, autosyntax)

def insert_auto(event):
	global auto_str

	if auto_str != "":
		length = len(textarea.get("insert-1c wordstart", "insert").lstrip())
		length2 = len(textarea.get("insert", "insert wordend").lstrip())
		if length < len(auto_str) and length2 == 0:
			textarea.insert("insert", auto_str[-int(len(auto_str) - length):])
		syntax()

def key_pressed(event):
	global alt
	if event.keysym == "7" and alt == True:
		textarea.insert(textarea.index(INSERT), "}")
		textarea.mark_set("insert", "%d.%d" % (int(textarea.index(INSERT).split(".")[0]), int(textarea.index(INSERT).split(".")[1]) - 1))
	elif event.keysym == "8" and alt == True:
		textarea.insert(textarea.index(INSERT), "]")
		textarea.mark_set("insert", "%d.%d" % (int(textarea.index(INSERT).split(".")[0]), int(textarea.index(INSERT).split(".")[1]) - 1))
	else:
		alt = event.keysym == "Alt_R"
	if event.keysym == "parenleft":
		textarea.insert(textarea.index(INSERT), ")")
		textarea.mark_set("insert", "%d.%d" % (int(textarea.index(INSERT).split(".")[0]), int(textarea.index(INSERT).split(".")[1]) - 1))
	elif event.keysym == "quotedbl":
		textarea.insert(textarea.index(INSERT), '"')
		textarea.mark_set("insert", "%d.%d" % (int(textarea.index(INSERT).split(".")[0]), int(textarea.index(INSERT).split(".")[1]) - 1))
	elif event.keysym == "quoteright":
		textarea.insert(textarea.index(INSERT), "'")
		textarea.mark_set("insert", "%d.%d" % (int(textarea.index(INSERT).split(".")[0]), int(textarea.index(INSERT).split(".")[1]) - 1))
	syntax()

def del_dou(event):
	if textarea.get("insert-1c", "insert") == "(":
		textarea.delete("insert", "insert+1c")
	return "break"

def update_cursor():
	global filename
	if filename == "":
		lbl.config(text="GoRound - 1.9.2 ~ Untitled | Line: " + str(textarea.index(INSERT).split('.')[0]) + ", Column: " + str(textarea.index(INSERT).split('.')[1]))
	else:
		lbl.config(text="GoRound - 1.9.2 ~ " + filename + " | Line: " + str(textarea.index(INSERT).split('.')[0]) + ", Column: " + str(textarea.index(INSERT).split('.')[1]))
	root.after(10, update_cursor)

def close():
	root.destroy()

root = Tk()
root.title("Untitled - GoRound")
root.geometry("900x500")
root.minsize(900,500)
root.bind("<Key>", key_pressed)
root.bind("<" + ins_key + ">", insert_auto)
root.bind("<BackSpace>", del_dou)
root.state("zoomed")

menubar = Menu(root)
root.config(menu = menubar)
submenu1 = Menu(menubar,tearoff=0)

menubar.add_cascade(label="File", menu=submenu1)
submenu1.add_command(label="New", command=new_file)
submenu1.add_command(label="Save", command=save_file)
submenu1.add_command(label="Save As", command=save_file_as)
submenu1.add_command(label="Open", command=open_file)
submenu1.add_separator()
submenu1.add_command(label="Exit", command=close)

lbl = Label(root, text="GoRound - 1.9.2 ~ Untitled", bg="lightgray", anchor='sw')
lbl.pack(side=BOTTOM, fill=BOTH)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

textarea = Text(root, yscrollcommand=scrollbar.set, selectbackground="gray", insertwidth = 3, inactiveselectbackground="darkgray", font=('Lucida Console', 16), fg="#e0db74", insertbackground='white', bg='#%02x%02x%02x' % (40, 41, 35))
textarea.pack(side=LEFT, fill=BOTH, expand=True)

lbl.config(text="GoRound - 1.9.2 ~ Untitled | Line: " + str(textarea.index(INSERT).split('.')[0]) + ", Column: " + str(textarea.index(INSERT).split('.')[1]))

scrollbar.config(command = textarea.yview)

autolbl = Label(bg="black", fg="white", font=('Lucida Console', 14), text="")

update_cursor()
autosyntax()

root.mainloop()