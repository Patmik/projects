import tkinter as tk
from tkinter import ttk
from pathlib import Path

BASE_PATH = str(Path(__file__).resolve().parent)


class Journals(ttk.Frame):
    def __init__(self,name,text_data,item_height):
        super().__init__()

        self.place(x = 0 , y = 0, relwidth= 0.3, relheight= 1)
        journal_label = ttk.Label(self,text = 'Journals').pack(side='top')
        
        #widget_data
        self.text_data = text_data
        self.item_number = len(text_data)
        self.list_height = self.item_number*item_height
        
        #widets
        menu_buttons_frame = ttk.Frame(self)
        journal_button_add = ttk.Button(menu_buttons_frame, text = 'Add Journal',command = lambda: self.add_journal('Dziennki_nowy',self.journal_list_frame,text_data,item_height))
        journal_button_delete = ttk.Button(menu_buttons_frame, text = 'Delete Journal',command = lambda: self.delete_journal(self.journal_list_frame,text_data,item_height))

        menu_buttons_frame.pack(side='top')
        journal_button_add.pack(side ='left',expand=True)
        journal_button_delete.pack(side ='left',expand=True)
            
        journal_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        journals_list = JournalList(journal_list_frame,text_data,item_height).pack(side='top')
        journal_list_frame.pack(side='top',expand=True,fill='both')
        
        self.journal_list_frame = journal_list_frame

    def add_journal(self,text,frame_to_update,text_data,item_height):
        self.text_data.append(text)
        frame_to_update.pack_forget()
        self.journal_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        journals_list = JournalList(self.journal_list_frame,text_data,item_height).pack(side='top')
        self.journal_list_frame.pack(side='top',expand=True,fill='both')

    
    def delete_journal(self,frame_to_update,text_data,item_height):
        self.text_data.pop()
        frame_to_update.pack_forget()
        self.journal_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        journals_list = JournalList(self.journal_list_frame,text_data,item_height).pack(side='top')
        self.journal_list_frame.pack(side='top',expand=True,fill='both')

class JournalList(ttk.Frame):
    def __init__(self, parent,text_data, item_height):  #text_data,
        super().__init__(master= parent)
        self.pack(expand=True,fill='both')
        
        #widget data
        
        self.text_data = text_data
        self.item_number = len(text_data)
        self.list_height = self.item_number*item_height


        #canvas
        self.canvas = tk.Canvas(self,background='red',bg = 'white',scrollregion=(0,0,self.winfo_width(),self.list_height))
        self.canvas.pack(expand=True,fill='both')

        #display frame
        self.frame = ttk.Frame(self)

        for index,item in enumerate(self.text_data):
            self.create_item(index,item).pack(expand=True,fill='both',pady =4, padx = 10)

        #scrollbar
        self.scrollbar = ttk.Scrollbar(self,orient='vertical',command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely= 0, relheight=1, anchor='ne')


        #events
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta/60),"units"))
        self.bind('<Configure>',self.update_size)

    def update_size(self,event):
        if self.list_height >= self.winfo_height():
            height = self.list_height
            self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta/60),"units"))
            self.scrollbar.place(relx=1, rely= 0, relheight=1, anchor='ne')
        else:
            height = self.winfo_height()
            self.canvas.unbind_all('<MouseWheel>')
            self.scrollbar.place_forget()

        self.canvas.create_window((0,0),window = self.frame, anchor ='nw',width= self.winfo_width(), height=height)


    def create_item(self,index,item):
        frame = ttk.Frame(self.frame)
        
        #widgets
        Journal(frame,f'{item} {index} ')

        return frame 



class Journal(ttk.Frame):
    def __init__(self,parent,name):
        super().__init__(parent)

        ttk.Button(self, text = name).pack(side='top')   

        self.pack(side='top',expand=True,fill='both',padx=5,pady=5) 


class Tasks(ttk.Frame):
    def __init__(self,name,text_data,item_height):
        super().__init__()

        self.place(relx=1.0, rely=1.0, anchor='se', relwidth= 0.7, relheight= 1)
        task_label = ttk.Label(self,text = 'Tasks').pack(side='top')

        #wdget_data
        self.text_data = text_data
        self.item_number = len(text_data)
        self.list_height = self.item_number*item_height
        self.item_height = item_height

        #widgets
        task_menu_buttons_frame = ttk.Frame(self)
        task_button_add = ttk.Button(task_menu_buttons_frame, text = 'Add Task',command = lambda: self.add_task(self.task_list_frame,text_data,item_height))
        task_button_delete = ttk.Button(task_menu_buttons_frame, text = 'Delete Task',command = lambda: self.delete_task(self.task_list_frame,text_data,item_height))
        


        task_menu_buttons_frame.pack(side='top',anchor='e')
        task_button_add.pack(side ='left',expand=True)
        task_button_delete.pack(side ='left',expand=True)
            
        task_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        tasks_list = TaskList(task_list_frame,text_data,item_height).pack(side='top')
        task_list_frame.pack(side='top',expand=True,fill='both')

        self.task_list_frame = task_list_frame

    
    def refresh_tasks(self,frame_to_update,text_data,item_height):
        frame_to_update.pack_forget()
        self.task_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        tasks_list = TaskList(self.task_list_frame,text_data,item_height).pack(side='top')
        self.task_list_frame.pack(side='top',expand=True,fill='both')

    def add_task(self,frame_to_update,text_data,item_height):
        new_task_window = NewTask(self.task_name_entered)

        frame_to_update.pack_forget()
        self.task_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        tasks_list = TaskList(self.task_list_frame,text_data,item_height).pack(side='top')
        self.task_list_frame.pack(side='top',expand=True,fill='both')

    def task_name_entered(self,task_name):
        self.text_data.append(task_name)
        print(task_name)
        self.refresh_tasks(self.task_list_frame,self.text_data,self.item_height)

    def delete_task(self,frame_to_update,text_data,item_height):
        self.text_data.pop()
        frame_to_update.pack_forget()
        self.task_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        tasks_list = TaskList(self.task_list_frame,text_data,item_height).pack(side='top')
        self.task_list_frame.pack(side='top',expand=True,fill='both')    


class NewTask(tk.Toplevel):
    def __init__(self,task_name_entered):
        super().__init__()
        self.title('Nowe zadanie')
        self.geometry('300x400')
        self.task_name_entered = task_name_entered
        self.task_name = tk.StringVar()

        self.Label = ttk.Label(self,text='Nazwa zadania').pack()
        self.button_accept = ttk.Button(self,text='Potwierdź',command= self.button_accept_pressed).pack()
        self.button_resign = ttk.Button(self,text='Zrezygnuj',command=lambda: self.destroy()).pack()
        self.entry_task = ttk.Entry(self,textvariable=self.task_name).pack(expand=True)

        self.focus()
        self.grab_set()

    def button_accept_pressed(self):
        self.task_name_entered(self.task_name.get())
        self.destroy()


class TaskList(ttk.Frame):
    def __init__(self, parent,text_data, item_height):  #text_data,
        super().__init__(master= parent)
        self.pack(expand=True,fill='both')
        
        #widget data
        self.text_data = text_data
        self.item_number = len(text_data)
        self.list_height = self.item_number*item_height


        #canvas
        self.canvas = tk.Canvas(self,background='red',bg = 'white',scrollregion=(0,0,self.winfo_width(),self.list_height))
        self.canvas.pack(expand=True,fill='both')

        #display frame
        self.frame = ttk.Frame(self)



        #scrollbar
        self.scrollbar = ttk.Scrollbar(self,orient='vertical',command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely= 0, relheight=1, anchor='ne')

        for index,item in enumerate(self.text_data):
            self.create_item(index,item).pack(expand=True,fill='both',pady =4, padx = 10)


        #events
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta/60),"units"))
        self.bind('<Configure>',self.update_size)

    def update_size(self,event):
        if self.list_height >= self.winfo_height():
            height = self.list_height
            self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta/60),"units"))
            self.scrollbar.place(relx=1, rely= 0, relheight=1, anchor='ne')
        else:
            height = self.winfo_height()
            self.canvas.unbind_all('<MouseWheel>')
            self.scrollbar.place_forget()

        self.canvas.create_window((0,0),window = self.frame, anchor ='nw',width= self.winfo_width(), height=height)


    def create_item(self,index,item):
        frame = ttk.Frame(self.frame)

        Task(frame,f'{item} {index} ')

        return frame 


class Task(ttk.Frame):
    def __init__(self, parent, label_text):
        super().__init__(parent)

        label = ttk.Label(self, text = label_text)
        label.pack(expand=True,fill='both')

        self.pack(side = 'top', expand=True, fill='both',padx=20,pady =20) 


class App(tk.Tk):
    def __init__(self,title,size):
        super().__init__()

        #testy_debug
        journal_list = ['Dziennik1','Dziennik2','Dziennik3','Dziennik4','Dziennik5','Dziennik6','Dziennik7','Dziennik8']
        task_list = ['Zadanie1','Zadanie2','Zadanie3','Zadanie4','Zadanie5','Zadanie6','Zadanie7','Zadanie8']

        self.title("SmartTasker")
        self.geometry(f'{size[0]}x{size[1]}+{int((self.winfo_screenwidth()-size[0])/2)}+{int((self.winfo_screenheight()-size[1])/2)}')
        self.minsize(int(size[0]/2),int(size[1]/2))
        self.iconbitmap(BASE_PATH  + '/brain_notes.ico')

        #widgets
        self.jounrals = Journals(self,journal_list,100)
        self.tasks = Tasks(self,task_list,100)


        self.mainloop()







App('Class based app',(800,600))