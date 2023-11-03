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
        self.text_data.append(journal_name)
        print(journal_name)
        self.refresh_journals(self.journal_list_frame,self.text_data, self.item_height)

    def delete_journal(self,frame_to_update,text_data,item_height):
        self.text_data.pop()
        frame_to_update.pack_forget()
        self.journal_list_frame = ttk.Frame(self,borderwidth=10, relief=tk.RIDGE)
        journals_list = JournalList(self.journal_list_frame,text_data,item_height).pack(side='top')
        self.journal_list_frame.pack(side='top',expand=True,fill='both')

class NewJournal(tk.Toplevel):
    def __init__(self, journal_name_entered):
        super().__init__()
        self.title('Nowy dziennik')
        self.geometry('300x400')
        self.iconbitmap(BASE_PATH  + '/brain_notes.ico')

        self.journal_name_entered = journal_name_entered
        self.journal_name = tk.StringVar()

        self.Label = ttk.Label(self,text='Nazwa zadania').pack()
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
            Tasks().refresh_tasks()
            App().tasks.refresh_tasks()
        k = ttk.Button(self, text = name,command= selected_journal).pack(side='top')   
        journal_name = self.name

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
        memory_notes[journal_name].insert(0,self.task_name.get())
        print(memory_notes)
        Memory().save_journal(memory_notes)
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
        memory_notes=Memory().load_note()

        journal_name = None 

        #testy_debug
        # journal_list = ['Dziennik1','Dziennik2','Dziennik3','Dziennik4','Dziennik5','Dziennik6','Dziennik7','Dziennik8']
        task_list = ['Zadanie1','Zadanie2','Zadanie3','Zadanie4','Zadanie5','Zadanie6','Zadanie7','Zadanie8']

        self.title("SmartTasker")
        self.geometry(f'{size[0]}x{size[1]}+{int((self.winfo_screenwidth()-size[0])/2)}+{int((self.winfo_screenheight()-size[1])/2)}')
        self.minsize(int(size[0]/2),int(size[1]/2))
        self.iconbitmap(BASE_PATH  + '/brain_notes.ico')


        #widgets
        self.jounrals = Journals(self,[x for x in memory_notes],100)
        try:    
            self.tasks = Tasks(self,memory_notes[journal_name],100)
        except:
            self.tasks = Tasks(self,[],100) 

        App().tasks.refresh_tasks()

        

        # try:
        #     self.tasks = Tasks(self,memory_notes[journal_name],100)
        # except:
        #     self.tasks = Tasks(self,[],100)


        self.mainloop()



app = App('Class based app',(800,600))


#wywoływanie metody klasy w innej klasie 
# class KlasaB:
#     def metoda_b(self):
#         print("Metoda w KlasaB")

# class KlasaA:
#     def wywolaj_metode_b(self, obiekt_b):
#         obiekt_b.metoda_b()

# # Tworzymy instancję obiektu KlasaB
# obiekt_b = KlasaB()

# # Tworzymy instancję obiektu KlasaA
# obiekt_a = KlasaA()

# # Wywołujemy metodę z KlasaA, przekazując obiekt_b jako argument
# obiekt_a.wywolaj_metode_b(obiekt_b)
