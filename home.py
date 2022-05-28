import tkinter as inspectify
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter.ttk as ttk 
import threading
import shutil
from facerec import *
from register import *
from face_detection import *
# from dbHandler import *
from handler import *
import time
import csv
import numpy as np
import ntpath
import os

active_page = 0
thread_event = None
left_frame = None
right_frame = None
heading = None
webcam = None
img_label = None
img_read = None
img_list = []
slide_caption = None
slide_control_panel = None
current_slide = -1

root = inspectify.Tk()
root.geometry("1000x900+200+100")
root.title ("INSPECTIFY")
#s=ttk.Style()
#s.theme_names() ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative') 

#s.theme_use('clam')


# create Pages
pages = []
for i in range(5):
    pages.append(inspectify.Frame(root, bg="white"))
    pages[i].pack(side="top", fill="both", expand=True)
    pages[i].place(x=0, y=0, relwidth=1, relheight=1)


def goBack():
    global active_page, thread_event, webcam

    if (active_page==4 and not thread_event.is_set()):
        thread_event.set()
        webcam.release()

    for widget in pages[active_page].winfo_children():
        widget.destroy()

    pages[0].lift()
    active_page = 0


def basicPageSetup(pageNo):
    global left_frame, right_frame, heading

    back_img = inspectify.PhotoImage(file= r"/Users/samikshajain/desktop/INSPECTIFY/img/backk.png")
    back_button = inspectify.Button(pages[pageNo], image=back_img, bg="white", bd=0, highlightthickness=0,
           activebackground="white", command=goBack)
    back_button.image = back_img
    back_button.place(x=10, y=10)

    heading = inspectify.Label(pages[pageNo], fg="white", bg="white", font="Arial 20 bold", pady=10)
    heading.pack()

    content = inspectify.Frame(pages[pageNo], bg="white", pady=20)
    content.pack(expand="true", fill="both")

    left_frame = inspectify.Frame(content, bg="white")
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = inspectify.LabelFrame(content, text="Detected Criminals", bg="white", font="Arial 20 bold", bd=4,
                             foreground="#0504aa", labelanchor="n")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    content.grid_columnconfigure(0, weight=1, uniform="group1")
    content.grid_columnconfigure(1, weight=1, uniform="group1")
    content.grid_rowconfigure(0, weight=1)


def showImage(frame, img_size):
    global img_label, left_frame

    img = cv2.resize(frame, (img_size, img_size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    if (img_label == None):
        img_label = inspectify.Label(left_frame, image=img, bg="#202d42")
        img_label.image = img
        img_label.pack(padx=20)
    else:
        img_label.configure(image=img)
        img_label.image = img


def getNewSlide(control):
    global img_list, current_slide

    if(len(img_list) > 1):
        if(control == "prev"):
            current_slide = (current_slide-1) % len(img_list)
        else:
            current_slide = (current_slide+1) % len(img_list)

        img_size = left_frame.winfo_height() - 200
        showImage(img_list[current_slide], img_size)

        slide_caption.configure(text = "Image {} of {}".format(current_slide+1, len(img_list)))


def selectMultiImage(opt_menu, menu_var):
    global img_list, current_slide, slide_caption, slide_control_panel

    filetype = [("images", "*.jpg *.jpeg *.png")]
    path_list = filedialog.askopenfilenames(title="Choose atleast 5 images", filetypes=filetype)

    if(len(path_list) < 5):
        messagebox.showerror("Error", "Choose atleast 5 images.")
    else:
        img_list = []
        current_slide = -1

        # Resetting slide control panel
        if (slide_control_panel != None):
            slide_control_panel.destroy()

        # Creating Image list
        for path in path_list:
            img_list.append(cv2.imread(path))

        # Creating choices for profile pic menu
        menu_var.set("")
        opt_menu['menu'].delete(0, 'end')

        for i in range(len(img_list)):
            ch = "Image " + str(i+1)
            opt_menu['menu'].add_command(label=ch, command= inspectify._setit(menu_var, ch))
            menu_var.set("Image 1")


        # Creating slideshow of images
        img_size =  left_frame.winfo_height() - 200
        current_slide += 1
        showImage(img_list[current_slide], img_size)

        slide_control_panel = inspectify.Frame(left_frame, bg="#202d42", pady=20)
        slide_control_panel.pack()

        back_img = inspectify.PhotoImage(file="previous.png")
        next_img = inspectify.PhotoImage(file="next.png")

        prev_slide = inspectify.Button(slide_control_panel, image=back_img, bg="#202d42", bd=0, highlightthickness=0,
                            activebackground="#202d42", command=lambda : getNewSlide("prev"))
        prev_slide.image = back_img
        prev_slide.grid(row=0, column=0, padx=60)

        slide_caption = inspectify.Label(slide_control_panel, text="Image 1 of {}".format(len(img_list)), fg="#ff9800",
                              bg="#202d42", font="Arial 15 bold")
        slide_caption.grid(row=0, column=1)

        next_slide = inspectify.Button(slide_control_panel, image=next_img, bg="#202d42", bd=0, highlightthickness=0,
                            activebackground="#202d42", command=lambda : getNewSlide("next"))
        next_slide.image = next_img
        next_slide.grid(row=0, column=2, padx=60)


def register(entries, required, menu_var):
    global img_list

    # Checking if no image selected
    if(len(img_list) == 0):
        messagebox.showerror("Error", "Select Images first.")
        return

    # Fetching data from entries
    entry_data = {}
    for i, entry in enumerate(entries):
        # print(i)
        val = entry[1].get()
        # print(val)

        if (len(val) == 0 and required[i] == 1):
            messagebox.showerror("Field Error", "Required field missing :\n\n%s" % (entry[0]))
            return
        else:
            entry_data[entry[0]] = val.lower()


    # Setting Directory
    path = os.path.join('face_samples', "temp_criminal")
    if not os.path.isdir(path):
        os.mkdir(path)

    no_face = []
    for i, img in enumerate(img_list):
        # Storing Images in directory
        id = registerCriminal(img, path, i + 1)
        if(id != None):
            no_face.append(id)

    # check if any image doesn't contain face
    if(len(no_face) > 0):
        no_face_st = ""
        for i in no_face:
            no_face_st += "Image " + str(i) + ", "
        messagebox.showerror("Registration Error", "Registration failed!\n\nFollowing images doesn't contain"
                        " face or Face is too small:\n\n%s"%(no_face_st))
        shutil.rmtree(path, ignore_errors=True)
    else:
        # Storing data in database
        insertData(entry_data)
        rowId=1
        if(rowId >= 0):
            messagebox.showinfo("Success", "Criminal Registered Successfully.")
            shutil.move(path, os.path.join('face_samples', entry_data["Name"]))

            # save profile pic
            profile_img_num = int(menu_var.get().split(' ')[1]) - 1
            if not os.path.isdir("profile_pics"):
                os.mkdir("profile_pics")
            cv2.imwrite("profile_pics/criminal %d.png"%rowId, img_list[profile_img_num])

            goBack()
        else:
            shutil.rmtree(path, ignore_errors=True)
            messagebox.showerror("Database Error", "Some error occured while storing data.")


## update scrollregion when all widgets are in canvas
def on_configure(event, canvas, win):
    canvas.configure(scrollregion=canvas.bbox('all'))
    canvas.itemconfig(win, width=event.width)

## Register Page ##
def getPage1():
    global active_page, left_frame, right_frame, heading, img_label
    active_page = 1
    img_label = None
    opt_menu = None
    menu_var = inspectify.StringVar(root)
    pages[1].lift()

    basicPageSetup(1)
    heading.configure(text="Register Criminal", bg="white")
    right_frame.configure(text="Enter Details", fg="#0504aa", bg="white")

    btn_grid = inspectify.Frame(left_frame, bg="white")
    btn_grid.pack()

    inspectify.Button(btn_grid, text="Select Images", command=lambda: selectMultiImage(opt_menu, menu_var), font="Arial 20 bold ", bg="white",
           fg="#0504aa", pady=10, bd=0, highlightthickness=0, activebackground="white",
           activeforeground="white").grid(row=0, column=0, padx=25, pady=25)


    # Creating Scrollable Frame
    canvas = inspectify.Canvas(right_frame, bg="white", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand="true", padx=30)
    scrollbar = inspectify.Scrollbar(right_frame, command=canvas.yview, width=20, troughcolor="white", bd=0,
                          activebackground="white", bg="white", relief="raised")
    scrollbar.pack(side="left", fill="y")

    scroll_frame = inspectify.Frame(canvas, bg="white", pady=20)
    scroll_win = canvas.create_window((0, 0), window=scroll_frame, anchor='nw')

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda event, canvas=canvas, win=scroll_win: on_configure(event, canvas, win))


    inspectify.Label(scroll_frame, text="* Required Fields", bg="white", fg="red", font="Arial 13 bold").pack()
    # Adding Input Fields
    input_fields = ("Name", "Father's Name", "Gender", "DOB(yyyy-mm-dd)", "Crimes Done", "Profile Image")
    ip_len = len(input_fields)
    required = [1, 1, 1, 1, 1, 1]

    entries = []
    for i, field in enumerate(input_fields):
        print()
        row = inspectify.Frame(scroll_frame, bg="white")
        row.pack(side="top", fill="x", pady=15)

        label = inspectify.Text(row, width=20, height=1, bg="white", fg="#0504aa", font="Arial 15 bold", highlightthickness=0, bd=0)
        label.insert("insert", field)
        label.pack(side="left")

        if(required[i] == 1):
            label.tag_configure("star", foreground="red", font="Arial 13 bold")
            label.insert("end", "  *", "star")
        label.configure(state="disabled")

        if(i != ip_len-1):
            ent = inspectify.Entry(row, font="Arial 13", selectbackground="#90ceff")
            ent.pack(side="right", expand="true", fill="x", padx=10)
            entries.append((field, ent))
        else:
            menu_var.set("Image 1")
            choices = ["Image 1"]
            opt_menu = inspectify.OptionMenu(row, menu_var, *choices)
            opt_menu.pack(side="right", fill="x", expand="true", padx=10)
            opt_menu.configure(font="Arial 13", bg="white", fg="white", bd=0, highlightthickness=0, activebackground="white")
            menu = opt_menu.nametowidget(opt_menu.menuname)
            menu.configure(font="Arial 13", bg="white", activebackground="white", bd=0)

    # print(entries)

    inspectify.Button(scroll_frame, text="Register", command=lambda: register(entries, required, menu_var), font="Arial 20",
           bg="white", fg="#0504aa", pady=10, padx=30, bd=0, highlightthickness=0, activebackground="white",
           activeforeground="white").pack(pady=25)


def showCriminalProfile(name):
    top = inspectify.Toplevel(bg="#202d42")
    top.title("Criminal Profile")
    top.geometry("1500x900+%d+%d"%(root.winfo_x()+10, root.winfo_y()+10))

    inspectify.Label(top, text="Criminal Profile", fg="white", bg="#202d42", font="Arial 20 bold", pady=10).pack()

    content = inspectify.Frame(top, bg="#202d42", pady=20)
    content.pack(expand="true", fill="both")
    content.grid_columnconfigure(0, weight=3, uniform="group1")
    content.grid_columnconfigure(1, weight=5, uniform="group1")
    content.grid_rowconfigure(0, weight=1)

    (id, crim_data) = retrieveData(name)

    path = os.path.join("profile_pics", "criminal %d.png"%id)
    profile_img = cv2.imread(path)

    profile_img = cv2.resize(profile_img, (500, 500))
    img = cv2.cvtColor(profile_img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    img_label = inspectify.Label(content, image=img, bg="#202d42")
    img_label.image = img
    img_label.grid(row=0, column=0)

    info_frame = inspectify.Frame(content, bg="#202d42")
    info_frame.grid(row=0, column=1, sticky='w')

    for i, item in enumerate(crim_data.items()):
        inspectify.Label(info_frame, text=item[0], pady=15, fg="yellow", font="Arial 15 bold", bg="#202d42").grid(row=i, column=0, sticky='w')
        inspectify.Label(info_frame, text=":", fg="red", padx=50, font="Arial 15 bold", bg="#202d42").grid(row=i, column=1)
        val = "---" if (item[1]=="") else item[1]
        inspectify.Label(info_frame, text=val.capitalize(), fg="white", font="Arial 15", bg="#202d42").grid(row=i, column=2, sticky='w')


def startRecognition():
    global img_read, img_label

    if(img_label == None):
        messagebox.showerror("Error", "No image selected. ")
        return

    crims_found_labels = []
    for wid in right_frame.winfo_children():
        wid.destroy()

    frame = cv2.flip(img_read, 1, 0)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_coords = detect_faces(gray_frame)

    if (len(face_coords) == 0):
        messagebox.showerror("Error", "Image doesn't contain any face or face is too small.")
    else:
        (model, names) = train_model()
        print('Training Successful. Detecting Faces')
        (frame, recognized) = recognize_face(model, frame, gray_frame, face_coords, names)

        img_size = left_frame.winfo_height() - 40
        frame = cv2.flip(frame, 1, 0)
        showImage(frame, img_size)

        if (len(recognized) == 0):
            messagebox.showerror("Error", "No criminal recognized.")
            return

        for i, crim in enumerate(recognized):
            crims_found_labels.append(inspectify.Label(right_frame, text=crim[0], bg="red",
                                            font="Arial 15 bold", pady=20))
            crims_found_labels[i].pack(fill="x", padx=20, pady=10)
            crims_found_labels[i].bind("<Button-1>", lambda e, name=crim[0]:showCriminalProfile(name))


def selectImage():
    global left_frame, img_label, img_read
    for wid in right_frame.winfo_children():
        wid.destroy()

    filetype = [("images", "*.jpg *.jpeg *.png")]
    path = filedialog.askopenfilename(title="Choose a image", filetypes=filetype)

    if(len(path) > 0):
        img_read = cv2.imread(path)

        img_size =  left_frame.winfo_height() - 40
        showImage(img_read, img_size)


## Detection Page ##
def getPage2():
    global active_page, left_frame, right_frame, img_label, heading
    img_label = None
    active_page = 2
    pages[2].lift()

    basicPageSetup(2)
    heading.configure(text="Detect Criminal")
    right_frame.configure(text="Detected Criminals", fg="#0504aa")

    btn_grid = inspectify.Frame(left_frame, bg="white")
    btn_grid.pack()
    


    inspectify.Button(btn_grid, text="Choose Image", command=selectImage, font="Arial 20 bold ", padx=20, bg="white",
            fg="#0504aa", pady=10, bd=0, highlightthickness=0, activebackground="white",
            activeforeground="white").grid(row=0, column=0, padx=25, pady=25)
    inspectify.Button(btn_grid, text="Identify", command=startRecognition, font="Arial 20 bold ", padx=20, bg="white",
           fg="#0504aa", pady=10, bd=0, highlightthickness=0, activebackground="white",
           activeforeground="white").grid(row=0, column=1, padx=25, pady=25)

# def path_leaf(path):
#     head,tail = ntpath.split(path)


def videoLoop(path,model, names):
    p=path
    q=ntpath.basename(p)
    filenam, file_extension = os.path.splitext(q)
    # print(filename)
    global thread_event, left_frame, webcam, img_label
    start=time.time()
    webcam = cv2.VideoCapture(p)
    old_recognized = []
    crims_found_labels = []
    times = []
    img_label = None
    field=['S.No.', 'Name', 'Time']
    g=filenam+'.csv'
    # filename = "g.csv"
    filename = g
    # with open('people.csv', 'w', ) as csvfile:
    # peoplewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # os.path.join(path, vid.split('.')[0]+'_'+str(count)+'.png'
    num=0
    try:
        # with open('people_Details.csv', 'w', ) as csvfile:
        with open(filename, 'w') as csvfile:
            # peoplewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(field)   
            while not thread_event.is_set():
                
                # Loop until the camera is working
                
                    
                    while (True):
                        # Put the image from the webcam into 'frame'
                        (return_val, frame) = webcam.read()
                        if (return_val == True):
                            break
                        # else:
                        #     print("Failed to open webcam. Trying again...")

                    # Flip the image (optional)
                    frame = cv2.flip(frame, 1, 0)
                    # Convert frame to grayscale
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Detect Faces
                    face_coords = detect_faces(gray_frame)
                    (frame, recognized) = recognize_face(model, frame, gray_frame, face_coords, names)

                    # Recognize Faces
                    recog_names = [item[0] for item in recognized]
                    if(recog_names != old_recognized):
                        for wid in right_frame.winfo_children():
                            wid.destroy()
                        del(crims_found_labels[:])

                        for i, crim in enumerate(recognized):
                            num+=1
                            x=time.time()-start
                            crims_found_labels.append(inspectify.Label(right_frame, text=crim[0], bg="orange",
                                                            font="Arial 15 bold", pady=20))
                            crims_found_labels[i].pack(fill="x", padx=20, pady=10)
                            crims_found_labels[i].bind("<Button-1>", lambda e, name=crim[0]: showCriminalProfile(name))
                            y=crim[0]
                            print(x,y)
                            arr = [num,y,x]
                            # peoplewriter.writerow(arr)
                            csvwriter.writerow(arr)  
                            
                            # print('hello')
                        old_recognized = recog_names

                    # Display Video stream
                    img_size = min(left_frame.winfo_width(), left_frame.winfo_height()) - 20

                    showImage(frame, img_size)

    except RuntimeError:
        print("[INFO]Caught Runtime Error")
    except inspectify.TclError:
        print("[INFO]Caught Tcl Error")


# video inspection Page ##
def getPage4(path):
    p=path
    # print(p)
    global active_page, video_loop, left_frame, right_frame, thread_event, heading
    active_page = 4
    pages[4].lift()

    basicPageSetup(4)
    heading.configure(text="Video inspection", fg ="#0504aa")
    right_frame.configure(text="Detected Criminals")
    left_frame.configure(pady=40)

    btn_grid = inspectify.Frame(right_frame, bg="white")
    btn_grid.pack()

    (model, names) = train_model()
    print('Training Successful. Detecting Faces')

    thread_event = threading.Event()
    thread = threading.Thread(target=videoLoop, args=(p,model, names))
    thread.start()

def getPage3():
    global active_page, video_loop, left_frame, right_frame, thread_event, heading
    active_page = 3
    pages[3].lift()

    basicPageSetup(3)
    heading.configure(text="Video inspection")

    btn_grid = inspectify.Frame(left_frame,bg="white")
    btn_grid.pack()

    inspectify.Button(btn_grid, text="Select Video", command=selectvideo, font="Arial 20 ", padx=20, bg="white",
                fg="#0504aa", pady=10, bd=0, highlightthickness=0, activebackground="white",
                activeforeground="white").grid(row=0, column=0, padx=25, pady=25)
    
    

    # inspectify.Button(btn_grid, text="Recognize", command=getPage3(), font="Arial 15 bold", padx=20, bg="white",
    #        fg="white", pady=10, bd=0, highlightthickness=0, activebackground="white",
    #        activeforeground="white").grid(row=0, column=1, padx=25, pady=25)


def selectvideo():
    global left_frame, img_label, img_read
    for wid in right_frame.winfo_children():
        wid.destroy()

    filetype = [("video", "*.mp4 *.mkv")]
    path = filedialog.askopenfilename(title="Choose a video", filetypes=filetype)
    p=''
    p=path
    
    if(len(path) > 0):
        # vid_read = cv2.imread(path)
        # print(vid_read)
        getPage4(p)
        # img_read = cv2.imread(path)

    #     img_size =  left_frame.winfo_height() - 40
    #     showImage(img_read, img_size)

# def getPage3():
#     global active_page, left_frame, right_frame, img_label, heading
#     img_label = None
#     active_page = 2
#     pages[2].lift()

#     basicPageSetup(2)
#     heading.configure(text="Video inspection")
#     right_frame.configure(text="Detected Criminals")

#     btn_grid = inspectify.Frame(left_frame, bg="white")
#     btn_grid.pack()

#     inspectify.Button(btn_grid, text="Select video", command=selectvideo, font="Arial 15 bold", padx=20, bg="white",
#             fg="white", pady=10, bd=0, highlightthickness=0, activebackground="white",
#             activeforeground="white").grid(row=0, column=0, padx=25, pady=25)
#     inspectify.Button(btn_grid, text="Recognize", command=startRecognition, font="Arial 15 bold", padx=20, bg="white",
#            fg="white", pady=10, bd=0, highlightthickness=0, activebackground="white",
#            activeforeground="white").grid(row=0, column=1, padx=25, pady=25)

def selectvideo1():
    # global left_frame, img_label, img_read
    # for wid in right_frame.winfo_children():
    #     wid.destroy()

    filetype = [("video", "*.mp4 *.mkv")]
    path = filedialog.askopenfilename(title="Choose a video", filetypes=filetype)
    p=''
    p=path
    
    if(len(path) > 0):
        # vid_read = cv2.imread(path)
        # print(vid_read)
       detect(p)

######################################## Home Page ####################################
inspectify.Label(pages[0], text="INSPECTIFY", fg="#0504aa", bg="white",
      font="Arial 50 bold", pady=30).pack()



logo = inspectify.PhotoImage(file = r"/Users/samikshajain/desktop/INSPECTIFY/img/background.png")
inspectify.Label(pages[0], image=logo, bg="white").pack(side='left')

btn_frame = inspectify.Frame(pages[0], bg="#FFFFFF", pady=170)
btn_frame.pack()

##inspectify.Button(btn_frame, text="Input Video", command=selectvideo1)
inspectify.Button(btn_frame, text="Register a new Criminal", command=getPage1)
inspectify.Button(btn_frame, text="Image Inspection", command=getPage2)
inspectify.Button(btn_frame, text="Video Inspection", command=getPage3)


for btn in btn_frame.winfo_children():
	btn.configure(font="Arial 20 bold", width=17, bg="#FFFFFF", fg="#0504aa", pady=15, bd=0, highlightthickness=0, activebackground="white", activeforeground="white")
	btn.pack(pady=30)
	
pages[0].lift()
root.mainloop()
