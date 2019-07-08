from tkinter import filedialog
from tkinter import *
import subprocess,os

#sudo apt-get install python3-tk
#to create mount point - sudo mkdir /media/dcp_sdb
#sudo apt install sshpass

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    filename = filename+"/*"
    folder_path.set(filename)



def browse_button1():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    #format selected hdd 
    #scp files to formatted hdd
    print(folder_path.get())
    print ()


def doStuff():
    selected = rightBT3.curselection()
    global folder_path
    if selected: # only do stuff if user made a selection
        print(selected)
        for index in selected:
            dname = rightBT3.get(index).split()[0]
            print(dname) # how you get the value of the selection from a listbox
            dn = "/dev/"+dname
            disknamenumber=dn+"1"
            dn1 = "/media/dcp_"+dname
            str1 = "/run/user/1000/gvfs/sftp:host=davinci.local/Volumes/ARECA_IN/PROJETS/MILANNOIR/SUB_MILANNOIR/*"
            fp1 = '''"robin erard"@davinci.local:'''+str1.split("davinci.local")[1]
            #fp1 = '''"robin erard"@davinci.local:'''+folder_path.get().split("davinci.local")[1]
            test = subprocess.Popen(["sudo","umount","%s" % disknamenumber], stdout=subprocess.PIPE).communicate()[0]
            #test = subprocess.Popen(["sudo","parted","-s","-a","minimal","%s" % dn,"mklabel","msdos","--","mkpart","primary","ext3","0%","100%"], stdout=subprocess.PIPE).communicate()[0]
            test = subprocess.Popen(["sudo","parted","-s","-a","minimal","%s" % dn,"mklabel","msdos",], stdout=subprocess.PIPE).communicate()[0]
            test = subprocess.Popen(["sudo","parted","%s" % dn,"mkpart","primary","ext3","0%","100%"], stdout=subprocess.PIPE).communicate()[0]
            test = subprocess.Popen(["sudo","mkfs.ext2","-j","-I","128","%s" % disknamenumber], stdout=subprocess.PIPE).communicate()[0]
            test = subprocess.Popen(["sudo","mount","%s" % disknamenumber,"%s" % dn1], stdout=subprocess.PIPE).communicate()[0]
            test = subprocess.Popen(["sudo","chmod","-R","777","%s" % dn1], stdout=subprocess.PIPE).communicate()[0]
            #test = subprocess.Popen(["sudo","scp","-i","/home/robinerard/.ssh/id_rsa","-r", fp1,"%s" % dn1], stdout=subprocess.PIPE)
            #os.system("sudo scp -i /home/robinerard/.ssh/id_rsa ")
            test = subprocess.Popen(["sudo","sshpass","-p","XXXXXX","scp","-r", fp1,"%s" % dn1], stdout=subprocess.PIPE)
            # sshpass -p 'myPass' scp -P 2122 ~/myDir/testPB.txt tomcat@xxx.xxx.xx.xxx:/chroot/tomcat/testPB
            test = subprocess.Popen(["sudo","chmod","-R","755","%s" % dn1], stdout=subprocess.PIPE).communicate()[0]
            print ("Task Completed")


def clear(lb):
    lb.select_clear(0, END) # unselect all

#todo- 1.layout 2.scp correct rsa file path or use sshpass or use pexpect/paramiko 3. msdos partition


#sudo scp -i ~/.ssh/id_rsa -r "robin erard"@davinci.local:/Volumes/ARECA_IN/PROJETS/MILANNOIR/SUB_MILANNOIR/* /media/dcp_sdb
#scp -i ~/.ssh/id_rsa -r "robin erard"@davinci.local:/Volumes/ARECA_IN/PROJETS/MILANNOIR/SUB_MILANNOIR/* /media/dcp_sdb

#/run/user/1000/gvfs/sftp:host=davinci.local/Volumes/ARECA_IN/PROJETS/MILANNOIR/SUB_MILANNOIR/*



#sudo scp -i ~/.ssh/id_rsa -r davinci.local:/Volumes/ARECA_IN/PROJETS/MILANNOIR/SUB_MILANNOIR/* /media/dcp_sdb

root = Tk()
root.geometry("600x380")
root.title("Drive Format")

folder_path = StringVar()
button2 = Button(text="Browse", command=browse_button,bg="navy")
button2.configure(foreground="white")
button2.grid(row=1, column=6)
lbl1 = Label(master=root,textvariable=folder_path,bg="SkyBlue3")
lbl1.grid(row=1, column=7)
lbl5 = Label(master=root,textvariable="",bg="SkyBlue3")
lbl5.grid(row=2, column=7)
folder_path.set("Folder : ")

rightBT3 = Listbox(master=root,selectmode='multiple',exportselection=0,bg="SkyBlue1")
rightBT3.grid(row=5, column=0)


test = subprocess.Popen(["sudo","-i","lsblk","-o", "NAME,FSTYPE,SIZE"], stdout=subprocess.PIPE)
output = test.communicate()[0]
disks = output.decode("utf-8").split("\n")
disks = list(filter(None, disks))
i=0
for disk in disks:
    rightBT3.insert(i,disk)
    i=i+1


doStuffBtn = Button(master=root, text='Format & Copy', command=doStuff,bg="navy")
doStuffBtn.configure(foreground="white")
doStuffBtn.grid(row=6, column=0)

#button3 = Button(text="Copy files", command=browse_button1)
#button3.grid(row=6, column=6)

#clearBtn = Button(root, text='Clear', command=lambda: clear(rightBT3))
#clearBtn.grid(row=2, column=5)

#mystr = StringVar()
#entry = Entry(textvariable=mystr, state=DISABLED)
#mystr.set('Output')
#entry.grid(row=7, column=5)

#http://cs111.wellesley.edu/~cs111/archive/cs111_spring15/public_html/labs/lab12/tkintercolor.html
root.configure(background='SkyBlue3')
root.mainloop()




