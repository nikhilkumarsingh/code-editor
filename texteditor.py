from Tkinter import *
import ttk
from tkFileDialog import askopenfilename,askopenfile,asksaveasfilename
import tkMessageBox as pop_up
from ScrolledText import ScrolledText
import hackerearthapi as heapi

BASE = RAISED
SELECTED = FLAT
LANG = ['C','CPP','CPP11','CLOJURE','CSHARP','GO','HASKELL','JAVA','JAVASCRIPT','JAVASCRIPT_NODE','OBJECTIVEC','PASCAL','PERL','PHP','PYTHON','R','RUBY','RUST','SCALA']



class Tab(Frame):
    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.tab_name = name

class TabBar(Frame):
    def __init__(self, master=None, init_name=None):
        Frame.__init__(self, master)
        self.tabs = {}
        self.buttons = {}
        self.current_tab = None
        self.init_name = init_name
    
    def show(self):
        self.pack(side=TOP,fill=BOTH)
        self.switch_tab(self.init_name or self.tabs.keys()[-1])
    
    def add(self, tab):
        tab.pack_forget()                                   
        self.tabs[tab.tab_name] = tab                       
        b = Button(self, text=tab.tab_name, relief=BASE,command=(lambda name=tab.tab_name: self.switch_tab(name)))  
        b.pack(side=LEFT)                                               
        self.buttons[tab.tab_name] = b

    def rename(self,new):
        old = self.current_tab
        self.current_tab=new
        self.tabs[new] = self.tabs.pop(old)
        self.buttons[new] = self.buttons.pop(old)
        self.buttons[new].config(text = new ,command =(lambda name=new: self.switch_tab(name)))
        self.switch_tab(new)
        
        
    def delete(self, tabname):
        if tabname == self.current_tab:
            self.current_tab = None
            self.tabs[tabname].pack_forget()
            del self.tabs[tabname]
            self.switch_tab(self.tabs.keys()[0])
        else:
            del self.tabs[tabname]
        self.buttons[tabname].pack_forget()
        del self.buttons[tabname] 
        
    def switch_tab(self, name):
        if self.current_tab:
          self.buttons[self.current_tab].config(relief=BASE)
          self.tabs[self.current_tab].pack_forget()           
        self.tabs[name].pack(side=TOP,expand=True)                           
        self.current_tab = name                                 
        self.buttons[name].config(relief=SELECTED)
        

class Editor():
    def __init__(self):
        self.root = Tk()
        self.root.title('Code editor')
        self.lang=StringVar()
        self.lang.set('0')
        
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.new)
        self.filemenu.add_command(label="Open", command=self._open)
        self.filemenu.add_command(label="Save", command=self.save)
        self.filemenu.add_command(label="Save as...", command=self.save_as)
        self.filemenu.add_command(label="Close", command=self.close)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.langmenu = Menu(self.menubar, tearoff=0)
        k=0
        for lang in LANG:
            self.langmenu.add_radiobutton(label=lang, variable=self.lang,value = str(k),
                                 underline=0)
            k+=1
            
        self.menubar.add_cascade(label='Language', underline=0, menu=self.langmenu)
        
        self.menubar.add_command(label="Run", command=self.run)
        self.root.config(menu=self.menubar)



        self.bar = TabBar(self.root,"Untitled")
        self.bar.config(relief=FLAT)
        
        self.tab=[]
        self.text=[]
        self.tab_count=0
        self.tab_dict={}

        self.tab_dict["Untitled"]={'location':None,'index':0}
        self.tab.append(Tab(self.root,"Untitled"))
        self.textFrame=Frame(self.tab[0],pady = 5,padx=5)
        self.text.append(ScrolledText(self.textFrame,height=35,width=500,fg="blue"))
        self.text[0].pack(side=TOP)
        self.textFrame.pack()
        self.bar.add(self.tab[0])

        ScreenSizeX = self.root.winfo_screenwidth()  
        ScreenSizeY = self.root.winfo_screenheight() 
        FrameSizeX  = int(ScreenSizeX *0.5)
        FrameSizeY  = int(ScreenSizeY *0.9)-25
        FramePosX   = (ScreenSizeX - FrameSizeX)/2 
        FramePosY   = (ScreenSizeY - FrameSizeY)/2 - 45
        self.root.geometry("%sx%s+%s+%s"%(FrameSizeX,FrameSizeY,FramePosX,FramePosY))

        self.outputFrame = Frame(self.root,pady = 5,padx=5)
        self.outputLabel = ScrolledText(self.outputFrame,height = 10,width = 75,wrap = WORD,bg = "black",fg = "white")
        self.outputLabel.pack(side = LEFT,fill = BOTH)
        self.inputLabel = ScrolledText(self.outputFrame,height = 10,width = 50,wrap = WORD)
        self.inputLabel.pack(side = LEFT,fill = BOTH,expand = True)
        self.outputFrame.pack(side = BOTTOM,fill = BOTH,expand = True)

        self.bar.show()
        self.root.mainloop()

        

    def run(self):
        lang = LANG[int(self.lang.get())]
        code = self.text[self.tab_dict[self.bar.current_tab]['index']].get("1.0",END)
        inputs = self.inputLabel.get("1.0",END)
        result = heapi.run_code(lang,code,inputs)
        print result
        try:
            output = result['run_status']['output'] + "\n\nTime used(seconds):"+result['run_status']['time_used']+"\nMemory used(bytes):"+result['run_status']['memory_used']
        except:
            output = result['compile_status']
        self.outputLabel.delete('1.0', END)
        self.outputLabel.insert(END,output)
        
    def _open(self):
        Tk().withdraw()
        filename = askopenfilename(initialdir='C:\\Users\\vivek\\Desktop',title='Select a file')
        code=open(filename).read()

        self.tab_count += 1
        n=self.tab_count
        tabname=filename.split('/')[-1]
        self.tab_dict[tabname] ={'location':filename,'index':n}

        self.tab.append(Tab(self.root,tabname))
        self.textFrame=Frame(self.tab[n])
        self.text.append(ScrolledText(self.textFrame,height=35,width=500,fg="blue"))
        self.text[n].pack(side=TOP)
        self.textFrame.pack()
        self.bar.add(self.tab[n])
        self.text[n].insert(END,code)
        self.bar.switch_tab(tabname)

    def new(self):
        self.tab_count += 1
        n=self.tab_count
        newtabname = "Untitled"+str(n)
        self.tab_dict[newtabname] ={'location':None,'index':n}

        self.tab.append(Tab(self.root,newtabname))
        self.textFrame=Frame(self.tab[n])
        self.text.append(ScrolledText(self.textFrame,height=35,width=500))
        self.text[n].pack(side=TOP)
        self.textFrame.pack()
        self.bar.add(self.tab[n])
        self.bar.switch_tab(newtabname)
        
        

    def save(self):
        filename = self.tab_dict[self.bar.current_tab]['location']
        code = self.text[self.tab_dict[self.bar.current_tab]['index']].get("1.0",END)
        f=open(filename,mode='w')
        f.write(code)
        f.close()

    def save_as(self):
        filename = asksaveasfilename(initialdir='C:\\Users\\vivek\\Desktop',title='Choose location of file',defaultextension='.txt')
        code = self.text[self.tab_dict[self.bar.current_tab]['index']].get("1.0",END)
        self.tab_dict[filename.split('/')[-1]] = self.tab_dict.pop(self.bar.current_tab)
        self.tab_dict[filename.split('/')[-1]]['location'] = filename
        self.bar.rename(filename.split('/')[-1])
        self.bar.switch_tab(self.bar.current_tab)
        
        f=open(filename,mode='w')
        f.write(code)
        f.close()
        
    def close(self):
        if(self.tab_dict[self.bar.current_tab]['location'] == None): #set warning(save or not)
            try:
                self.bar.delete(self.bar.current_tab)
            except:
                self.root.destroy()  
            return
        self.save()
        self.bar.delete(self.bar.current_tab)

    


Editor()
















