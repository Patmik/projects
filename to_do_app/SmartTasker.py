import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import json


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
        self.item_height = item_height
        #self.journal = Journal.name

        #widets
        menu_buttons_frame = ttk.Frame(self)
        journal_button_add = ttk.Button(menu_buttons_frame, text = 'Add Journal',command = lambda: self.add_journal(self.journal_list_frame,text_data,item_height))
        journal_button_delete = ttk.Button(menu_buttons_frame, text = 'Delete Journal',command = lambda: self.delete_journal(self.journal_list_frame,text_data,item_height))

        menu_buttons_frame.pack(side='top')
        journal_button_add.pack(side ='left',expand=True)
        journal_button_delete.pack(side ='left',expand=True)
            
        journal_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        journals_list = JournalList(journal_list_frame,text_data,item_height).pack(side='top')
        journal_list_frame.pack(side='top',expand=True,fill='both')
        
        self.journal_list_frame = journal_list_frame

    def refresh_journals(self,frame_to_update,text_data,item_height):
        frame_to_update.pack_forget()
        self.journal_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        journals_list = JournalList(self.journal_list_frame,self.text_data,self.item_height).pack(side='top')
        self.journal_list_frame.pack(side='top',expand=True,fill='both')

    def add_journal(self,frame_to_update,text_data,item_height):
        new_journal_window = NewJournal(self.journal_name_entered)
        
        frame_to_update.pack_forget()
        self.journal_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        journals_list = JournalList(self.journal_list_frame,text_data,item_height).pack(side='top')
        self.journal_list_frame.pack(side='top',expand=True,fill='both')

    def journal_name_entered(self, journal_name):
        if journal_name in [x for x in memory_notes]:
            print('dziennik już w slowniku')
            pass
        else:
            self.text_data.append(journal_name)
            print(journal_name)
            self.refresh_journals(self.journal_list_frame,self.text_data, self.item_height)

    def delete_journal(self,frame_to_update,text_data,item_height):
        new_delete_journal_window = DeleteJournalWindow(text_data,self.journal_name_deleted)
        
        frame_to_update.pack_forget()
        self.journal_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        journals_list = JournalList(self.journal_list_frame,text_data,item_height).pack(side='top')
        self.journal_list_frame.pack(side='top',expand=True,fill='both')
    
    def journal_name_deleted(self,journals_name):

        for journal in journals_name:
            print(self.text_data, journal)
            self.text_data.remove(journal)
        self.refresh_journals(self.journal_list_frame,self.text_data, self.item_height)
        
    
class NewJournal(tk.Toplevel):
    def __init__(self, journal_name_entered):
        super().__init__()
        self.title('Nowy dziennik')
        self.geometry('300x400')
        self.iconbitmap(BASE_PATH  + '/brain_notes.ico')

        self.journal_name_entered = journal_name_entered
        self.journal_name = tk.StringVar()

        self.Label = ttk.Label(self,text='Nazwa dziennika').pack()
        self.button_accept = ttk.Button(self,text='Potwierdź',command= self.button_accept_pressed).pack()
        self.button_resign = ttk.Button(self,text='Zrezygnuj',command=lambda: self.destroy()).pack()
        self.entry_journal = ttk.Entry(self,textvariable=self.journal_name).pack(expand=True)

        self.focus()
        self.grab_set()

    def button_accept_pressed(self):
        self.journal_name_entered(self.journal_name.get())
        memory_notes[self.journal_name.get()]=[]
        Memory().save_journal(memory_notes)
        self.destroy()

class DeleteJournalWindow(tk.Toplevel):
    def __init__(self,text_data,journal_name_deleted):
        super().__init__()
        self.title('Usuń dziennik')
        self.geometry('300x400')
        self.iconbitmap(BASE_PATH  + '/brain_notes.ico')
        self.text_data = text_data
        self.Label = ttk.Label(self,text='Nazwa dziennika').pack()
        self.journal_name_deleted = journal_name_deleted

        self.button_accept = ttk.Button(self,text='Potwierdź',command= self.button_accept_pressed).pack()
        self.button_resign = ttk.Button(self,text='Zrezygnuj',command=lambda: self.destroy()).pack()
        self.journals = []
        self.journals_to_delete = []

        for index,item in enumerate(self.text_data):
            journal = DeleteJournal(self,item)
            self.journals.append(journal)
            
        self.focus()
        self.grab_set()


    def button_accept_pressed(self):
        for journal in self.journals:
            if journal.check_var.get() == 'off':
                pass
            if journal.check_var.get() == 'on':
                self.journals_to_delete.append(journal.name)
                print(journal.name)
                del memory_notes[journal.name]
        self.journal_name_deleted(self.journals_to_delete)
        Memory().save_journal(memory_notes)
        self.destroy()


class DeleteJournal(ttk.Frame):
     def __init__(self,parent,name):
        super().__init__(parent)
        self.name = name
        self.check_var = tk.StringVar()
        #ttk.Label(self,text = f'{name}').pack(side='left')
        ttk.Checkbutton(self,text = self.name,command=lambda: print(self.check_var.get()),variable = self.check_var, onvalue= 'on', offvalue ='off').pack(side='left')
        self.pack(side='top',expand=True,fill='both',padx=5,pady=5)   



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
        Journal(frame,f'{item}')

        return frame 


class Journal(ttk.Frame):
    def __init__(self,parent,name):
        global journal_name
        super().__init__(parent)
        self.name = name
        def selected_journal():
            journal_name = self.name
            print(journal_name)
            Tasks(self,memory_notes[self.name],100,self.name)
        k = ttk.Button(self, text = name,command= selected_journal).pack(side='top')  
        journal_name = self.name
        
        self.pack(side='top',expand=True,fill='both',padx=5,pady=5) 
    
        
class Tasks(ttk.Frame):
    def __init__(self,name,text_data,item_height,journal):
        super().__init__()

        self.place(relx=1.0, rely=1.0, anchor='se', relwidth= 0.7, relheight= 1)
        task_label = ttk.Label(self,text = 'Tasks').pack(side='top')
        
        #wdget_data
        self.text_data = text_data
        self.item_number = len(text_data)
        self.list_height = self.item_number*item_height
        self.item_height = item_height
        self.journal = journal

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

        optimize_button = ttk.Button(self,text = 'Optimize').pack(side='bottom',anchor='e')
    
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
        #memory_notes[journal_name].insert(0,task_name)
        Memory().save_journal(memory_notes)
        self.refresh_tasks(self.task_list_frame,self.text_data,self.item_height)

 
        

    def delete_task(self,frame_to_update,text_data,item_height):
        new_delete_window = DeleteTaskWindow(text_data,self.journal,self.tasks_name_deleted)
        frame_to_update.pack_forget()
        self.task_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        tasks_list = TaskList(self.task_list_frame,text_data,item_height).pack(side='top')
        self.task_list_frame.pack(side='top',expand=True,fill='both')

    def tasks_name_deleted(self,tasks_name):
        self.refresh_tasks(self.task_list_frame,self.text_data,self.item_height)


class NewTask(tk.Toplevel):
    def __init__(self,task_name_entered):
        super().__init__()
        self.title('Nowe zadanie')
        self.geometry('300x400')
        self.iconbitmap(BASE_PATH  + '/brain_notes.ico')
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
        #memory_notes[journal_name].insert(0,self.task_name.get())
        print(memory_notes)
        #Memory().save_journal(memory_notes)
        self.destroy()


class DeleteTaskWindow(tk.Toplevel):
    def __init__(self,text_data,journal,tasks_name_deleted):
        super().__init__()
        self.title('Usuń zadanie')
        self.geometry('300x400')
        self.iconbitmap(BASE_PATH  + '/brain_notes.ico')
        self.text_data = text_data
        self.Label = ttk.Label(self,text='Nazwa zadania').pack()
        self.journal = journal
        self.tasks_name_deleted = tasks_name_deleted

        self.button_accept = ttk.Button(self,text='Potwierdź',command= self.button_accept_pressed).pack()
        self.button_resign = ttk.Button(self,text='Zrezygnuj',command=lambda: self.destroy()).pack()
        self.tasks = []
        self.tasks_to_delete = []

        for index,item in enumerate(self.text_data):
            task = DeleteTask(self,item)
            print(task.name)
            self.tasks.append(task)
            
        self.focus()
        self.grab_set()


    def button_accept_pressed(self):
        for task in self.tasks:
            if task.check_var.get() == 'off':
                pass
            if task.check_var.get() == 'on':
                self.tasks_to_delete.append(task.name)
                memory_notes[self.journal].remove(task.name)
        self.tasks_name_deleted(self.tasks_to_delete)
        Memory().save_journal(memory_notes)
        self.destroy()


class DeleteTask(ttk.Frame):
     def __init__(self,parent,name):
        super().__init__(parent)
        self.name = name
        self.check_var = tk.StringVar()
        #ttk.Label(self,text = f'{name}').pack(side='left')
        ttk.Checkbutton(self,text = self.name,command=lambda: print(self.check_var.get()),variable = self.check_var, onvalue= 'on', offvalue ='off').pack(side='left')
        self.pack(side='top',expand=True,fill='both',padx=5,pady=5)   
        

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

        Task(frame,f'{item}')

        return frame 


class Task(ttk.Frame):
    def __init__(self, parent, label_text):
        super().__init__(parent)

        label = ttk.Label(self, text = label_text)
        label.pack(expand=True,fill='both')

        self.pack(side = 'top', expand=True, fill='both',padx=20,pady =20) 


class Memory():
    def __init__(self):
        self.notes = {}
        self.journals = [x for x in self.notes]

    def load_notes(self,journal):
        try:
            with open("notes.json","r") as f:
                self.notes = json.load(f)

            tasks = [self.notes[journal] for x in self.notes]
            return tasks
        
        except FileNotFoundError:
            pass

    def load_note(self):
        try:
            with open("notes.json","r") as f:
                self.notes = json.load(f)
                print('zal')
            for journal, tasks in self.notes.items():
                self.notes[journal]=tasks
            return self.notes        
        except FileNotFoundError:
            pass
        

    def save_journal(self,notes):
        with open("notes.json","w") as f:
            json.dump(notes,f)

    def delete_note(self,journal):
        current_journal = journal
        current_tasks = self.notes[current_journal]

        confirm = messagebox.askyesno("Delete note", f'Are you sure you want to delte {current_tasks}?')
        if confirm:
            del self.notes[current_journal]

            with open("notes.json", "w") as f:
                json.dump(self.notes,f)

    def delete_journal(self,journal):
        current_journal = journal
        current_tasks = self.notes[current_journal]

        confirm = messagebox.askyesno("Delete note", f'Are you sure you want to delte {current_tasks}?')
        if confirm:
            del self.notes[current_journal]

            with open("notes.json", "w") as f:
                json.dump(self.notes,f)
            


class App(tk.Tk):
    def __init__(self,title,size):
        super().__init__()
        global memory_notes
        #global journal_name
        memory_notes=Memory().load_note()

        # journal_name = '1231313'
        # self.selected_journal=journal_name
        self.jour = [x for x in memory_notes]
        
        #testy_debug
        # journal_list = ['Dziennik1','Dziennik2','Dziennik3','Dziennik4','Dziennik5','Dziennik6','Dziennik7','Dziennik8']
        task_list = ['Zadanie1','Zadanie2','Zadanie3','Zadanie4','Zadanie5','Zadanie6','Zadanie7','Zadanie8']

        self.title("SmartTasker")
        self.geometry(f'{size[0]}x{size[1]}+{int((self.winfo_screenwidth()-size[0])/2)}+{int((self.winfo_screenheight()-size[1])/2)}')
        self.minsize(int(size[0]/2),int(size[1]/2))
        self.iconbitmap(BASE_PATH  + '/brain_notes.ico')

        
        #widgets
        Journals(self,[x for x in memory_notes],100)
        
        self.mainloop()




app = App('Class based app',(800,600))


