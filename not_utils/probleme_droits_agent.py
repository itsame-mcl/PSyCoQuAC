from tkinter import *

def update(ind, root, frames, frameCnt):
    label = Label(root)
    label.pack()
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)

def execution(file_name, ind):
    root = Tk()
    frameCnt = ind
    frames = [PhotoImage(file = file_name, format = 'gif -index %i' %(i)) for i in range(frameCnt)]
    root.after(0, update, 0, root, frames, frameCnt)
    root.mainloop()