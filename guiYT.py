import tkinter as tk
from tkinter import ttk 
from tkinter.messagebox import showinfo
import tkinter.font as tkFont
from tkinter import filedialog
from pytubeMp3 import *
import sys 

class App:
    def __init__(self, root):
        """
        Initializes the GUI application.

        Parameters:
        root: The root window of the application.
        """
        #setting title
        root.title("Yt mass downloader")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # progressbar
        pb = ttk.Progressbar(
            root,
            orient='horizontal',
            mode='indeterminate',
            length=280
        )
        # place the progressbar
        pb.place(x=40,y=440,width=520,height=17)

        GButton_951=tk.Button(root)
        GButton_951["activeforeground"] = "#9d2525"
        GButton_951["bg"] = "#efefef"
        GButton_951["cursor"] = "spider"
        ft = tkFont.Font(family='Times',size=10)
        GButton_951["font"] = ft
        GButton_951["fg"] = "#000000"
        GButton_951["justify"] = "center"
        GButton_951["text"] = "Download"
        GButton_951.place(x=370,y=200,width=161,height=49)
        GButton_951["command"] = lambda : self.GButton_951_command(GLineEdit_744, GLineEdit_103, pb)

        GLineEdit_103=tk.Entry(root)
        GLineEdit_103["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_103["font"] = ft
        GLineEdit_103["fg"] = "#333333"
        GLineEdit_103["justify"] = "center"
        GLineEdit_103["text"] = "link_entr"
        GLineEdit_103.place(x=80,y=200,width=239,height=31)

        GLineEdit_744=tk.Entry(root)
        GLineEdit_744["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_744["font"] = ft
        GLineEdit_744["fg"] = "#333333"
        GLineEdit_744["justify"] = "center"
        GLineEdit_744["text"] = "folder_entr"
        GLineEdit_744.place(x=80,y=120,width=236,height=30)

        GLabel_88=tk.Label(root)
        ft = tkFont.Font(family='Times',size=12)
        GLabel_88["font"] = ft
        GLabel_88["fg"] = "#333333"
        GLabel_88["justify"] = "center"
        GLabel_88["text"] = "Output folder :"
        GLabel_88.place(x=40,y=80,width=156,height=30)

        GButton_734=tk.Button(root)
        GButton_734["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_734["font"] = ft
        GButton_734["fg"] = "#000000"
        GButton_734["justify"] = "center"
        GButton_734["text"] = "Browse"
        GButton_734.place(x=370,y=120,width=49,height=47)
        GButton_734["command"] = lambda: self.GButton_734_command(GLineEdit_744)

        GLabel_394=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_394["font"] = ft
        GLabel_394["fg"] = "#333333"
        GLabel_394["justify"] = "center"
        GLabel_394["text"] = "Link :"
        GLabel_394.place(x=50,y=170,width=70,height=25)

        GButton_941=tk.Button(root)
        GButton_941["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_941["font"] = ft
        GButton_941["fg"] = "#000000"
        GButton_941["justify"] = "center"
        GButton_941["text"] = "Insert textfile with links"
        GButton_941.place(x=370,y=280,width=163,height=50)
        GButton_941["command"] = lambda: self.GButton_941_command(GLineEdit_744)

        GMessage_413=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_413["font"] = ft
        GMessage_413["fg"] = "#333333"
        GMessage_413["justify"] = "center"
        GMessage_413["text"] = "I have a message to tell the world blablabla rick and morty edgar alan poe"
        GMessage_413.place(x=50,y=280,width=266,height=77)

    # when the start button is pressed we start a configuration prosses to find if we have a textfile for links and the type video or playlist
    def GButton_951_command(self, folder_entr, link_entr=0 ,progress_bar=0, links = 0): # Start DOwnloading button
        """
        Callback function for the download button.

        Parameters:
        folder_entr: The entry widget for the output folder path.
        link_entr: The entry widget for the YouTube link.
        progress_bar: The progress bar widget.
        links: A list of YouTube links from a text file.

        Returns:
        None
        """
        print("__Download__")
        if links and link_to_download == "" :  # If we have a textfile start the downloading for each link
            for link in links:
                identify_and_run(link)
            return # We finish the downloading 
            
        link_to_download = str(link_entr.get()) # The string given by the user as link in entry1
        output_folder = folder_entr.get() # The output folder given 
        
        
        Downloader_inst = Downloader(output_folder) # Instance of the main module
        # print(f"out{output_folder}")
        
        if output_folder == "":
            showinfo(message=f'Please enter output {output_folder}folder')
            return None 

        if not os.path.isdir(output_folder): # The validity for names can be vary for each os
            showinfo(message='Invalid output folder')
            return

        elif link_to_download == "" and not links:  # If no textfile given we check if a link was passed to the link-entry
            showinfo(message='Please enter url')
            return None 
        link_entr.delete(0,'end')

        def identify_and_run(link_to_download): # Here we check links for classification (video or playlist) and we call the downloading functions from the main module
            print("identify_and_run__")
            if Downloader_inst.identify_link_type(link_to_download) == 'Video':
                print("__Identifyed as video__")
                try:
                    # progress_bar.start()
                    Downloader_inst.download_song_and_create_dataframe(link_to_download, progress_bar)
                    # progress_bar.stop()
                   
                except Exception as e:  
                    showinfo(message='Invalid url try to copy the foul link')
                    return 
                
                
            elif Downloader_inst.identify_link_type(link_to_download) == 'Playlist':
                print("__Identifyied as playlist__")
                try:
                    # progress_bar.start()
                    Downloader_inst.Download_playlist(link_to_download)
                    # progress_bar.stop()

                except Exception as e:  
                    print(e)
                    showinfo(message='Invalid url try to copy the full link')
                    return 

            else:
                print("here")
                showinfo(message='Invalid url')

            showinfo(message='Download completed!')
            return None
        
        try:
            identify_and_run(link_to_download) # If we reach this point we should have a link passed into the variable link_to_download
        except Exception as e:
            print(e)
            return

    def GButton_734_command(self, folder_entr):
        """
        Callback function for the browse button.

        Parameters:
        folder_entr: The entry widget for the output folder path.

        Returns:
        None
        """
        print("__Browse__")
        directory = filedialog.askdirectory()
        folder_entr.delete(0,"end")
        folder_entr.insert(0, directory)


    def GButton_941_command(self, folder_entr):
        """
        Callback function for the button to select a text file with links.

        Parameters:
        folder_entr: The entry widget for the output folder path.

        Returns:
        None
        """
        print("__Select textfile with links__")
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        with open(file_path, "r" ) as f:
            links = f.readlines()
        
        output_folder = folder_entr.get()
        print(output_folder)
        
        Downloader(output_folder).DOWNLOAD_STARTER(links)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
