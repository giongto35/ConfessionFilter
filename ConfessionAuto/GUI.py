from Tkinter import *
import RemoteController
import tkMessageBox

# Declare resources for text
TEXT_GG_SYNC = u"\u0110\u1ed3\u006e\u0067 \u0062\u1ed9 \u0068\u00f3\u0061 \u0076\u1edb\u0069 \u0047\u006f\u006f\u0067\u006c\u0065 \u0044\u0072\u0069\u0076\u0065"
TEXT_FB_POST = u"\u0110\u0103\u006e\u0067 \u006c\u00ea\u006e \u0046\u0061\u0063\u0065\u0062\u006f\u006f\u006b"
TEXT_NEAREST_POST = u"\u0042\u00e0\u0069 \u0070\u006f\u0073\u0074 \u0063\u0068\u01b0\u0061 \u0111\u01b0\u1ee3\u0063 \u0111\u0103\u006e\u0067 \u0067\u1ea7\u006e \u006e\u0068\u1ea5\u0074"

def post_callback(msg):
   	RemoteController.post_to_FB(msg)
   	tkMessageBox.showinfo(msg, "You posted")

def synchronize_callback(list_confession):
	posts = RemoteController.fetch_from_GGdoc()

	for post in posts:
		list_confession.insert(END, post.encode('utf-8'))

def select_post_callback(e):
	print(e.widget.curselection())

def set_text_box(text_box, str):
	if str != NONE:
		text_box.delete(0.0, END)
		text_box.insert(INSERT, str)

top = Tk()
top.wm_title("Confession Auto")
text_content = Text(top)
list_confession = Listbox(top)
list_confession.bind('<<ListboxSelect>>', lambda e: set_text_box(text_content, list_confession.get(e.widget.curselection()[0]) if e.widget.curselection() else NONE))
button_sync = Button(top, text=TEXT_GG_SYNC, command=lambda: synchronize_callback(list_confession))
button_post = Button(top, text=TEXT_FB_POST, command=lambda: post_callback(text_content.get("1.0",END)))
button_get_unposted = Button(top, text=TEXT_NEAREST_POST)

button_post.grid(row=0, column=0)
button_sync.grid(row=0, column=1)
button_get_unposted.grid(row = 0, column = 2)
text_content.grid(row=1, column=0, columnspan = 2)
list_confession.grid(row=1, column=2)
top.mainloop()