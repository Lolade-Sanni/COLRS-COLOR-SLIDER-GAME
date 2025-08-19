# IMPORTING NECESSARY MODULES
import time
import _tkinter
import random as r

from PIL import ImageTk, Image
from customtkinter import *
from tkinter import messagebox


def rand_colour():
    """ This function generates a random color and returns its hexadecimal and a tuple of it RGB values"""
    R = r.randint(1, 255)
    G = r.randint(1, 255)
    B = r.randint(1, 255)
    r_g_b = (R, G, B)
    return '#' + ''.join(f'{i:02X}' for i in r_g_b), r_g_b

class App(CTk):
    # DECLARING APP VARIABLES
    color = rand_colour()
    padding = {"padx":10, "pady":5}
    title_font = ("Bahnschrift", 72)
    heading_font = ("Bahnschrift", 20)
    normal_font = ("Bahnschrift", 16)
    mode_set = {"EASY":(60, 20), "MEDIUM":(45, 15), "HARD":(30, 10), "IMPOSSIBLE":(20, 5)}

    right_arrow = CTkImage(Image.open("images/arrow_icon.png"), size=(30, 100))
    left_arrow = CTkImage(Image.open("images/arrow_icon.png").rotate(180), size=(30, 100))
    k = 0

    DIFFICULTY = ["EASY", "MEDIUM", "HARD", "IMPOSSIBLE"]

    timer = None
    degree_error = None
    won = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("COLRS")
        self.iconbitmap("images/s0urcec0de.ico")
        self.geometry("600x400")
        self.resizable(False,False)

        self.create_start_screen()
        self.mainloop()

    def _clear(self):
        """This function clears all widgets in the existing screen"""
        for widgets in self.winfo_children():
            widgets.destroy()

    def set_values(self):
        """This Function sets the value of the timer and permissible degree of error based on the selected difficulty"""
        self.timer = self.mode_set[self.DIFFICULTY[self.k]][0]
        self.degree_error = self.mode_set[self.DIFFICULTY[self.k]][1]

    def lose_dialog(self):
        """This function creates a loss dialog box"""
        box = messagebox.askyesno("YOU LOST :(", "SORRY YOU LOST, DO YOU WANT TO PLAY AGAIN?")
        if box :
            self.create_difficulty_screen()
            return
        else:
            self.quit()

    def win_dialog(self):
        """This function creates a win dialog box"""
        self.color = rand_colour()
        self.won = True
        answer = messagebox.askyesno("YOU WON!", "YOU WON, DO YOU WANT TO PLAY AGAIN?")
        if answer:
            self.create_difficulty_screen()
            return
        else:
            self.quit()

    def create_start_screen(self):
        """This function creates the start screen"""
        frame = CTkFrame(self, fg_color=rand_colour()[0])
        label = CTkLabel(frame, text="COLRS", font=self.title_font, corner_radius=10)
        label.pack(expand=1)

        play_btn = CTkButton(self, text="PLAY", height=50, font=self.heading_font, command=self.create_difficulty_screen)
        frame.pack(side=TOP, fill=BOTH, expand=1, **self.padding)
        play_btn.pack(side=BOTTOM, fill=X, **self.padding)

    def create_difficulty_screen(self):
        """This function creates the difficulty selection screen"""

        def increase_difficulty():
            if self.k == 3:
                self.k = 0
            else:
                self.k += 1
            difficulty_label.configure(text=self.DIFFICULTY[self.k])
            self.title(f"COLRS :{self.DIFFICULTY[self.k]}")

        def decrease_difficulty():
            if self.k == 0:
                self.k = 3
            else:
                self.k += -1
            difficulty_label.configure(text=self.DIFFICULTY[self.k])
            self.title(f"COLRS :{self.DIFFICULTY[self.k]}")

        self._clear()
        self.won = False

        heading_frame= CTkFrame(self)
        heading_label = CTkLabel(heading_frame, text="SELECT A DIFFICULTY", font=self.heading_font)
        img_frame = CTkFrame(self)
        left_btn = CTkButton(img_frame, text="", image=self.left_arrow, height=100, width=30,
                             command=decrease_difficulty)
        img= CTkLabel(img_frame, text="", fg_color=self.color[0], corner_radius=10)
        right_btn = CTkButton(img_frame, text="", image=self.right_arrow, height=100, width=30,
                              command=increase_difficulty)
        frame = CTkFrame(self)

        difficulty_label = CTkLabel(frame, text=self.DIFFICULTY[self.k], font=self.heading_font )
        select_btn = CTkButton(frame, text="SELECT", font=self.heading_font, command=self.create_color_view_screen)

        heading_frame.pack(side=TOP, fill=X, **self.padding)
        heading_label.pack(fill=X, **self.padding)
        img_frame.pack(side=TOP, fill=BOTH, expand=1, **self.padding)
        left_btn.pack(side=LEFT, **self.padding)
        right_btn.pack(side=RIGHT, **self.padding)
        img.pack(expand=1, fill=BOTH, **self.padding)
        frame.pack(side=TOP, fill=X, **self.padding)
        difficulty_label.pack(side=TOP, **self.padding)
        select_btn.pack(side=TOP, **self.padding)

    def create_color_view_screen(self):
        """This function creates the color view screen"""
        def change_color():
            self.color = rand_colour()
            color_frame.configure(fg_color=self.color[0])
        self._clear()

        heading_frame = CTkFrame(self)
        heading_label = CTkLabel(heading_frame, text="MEMORIZE THIS COLOUR AND WHEN READY, BEGIN!",
                                 font=self.heading_font)
        color_frame = CTkFrame(self, fg_color=self.color[0])
        btn_frame = CTkFrame(self)
        change_frame = CTkFrame(btn_frame, fg_color="transparent")
        change_color_btn = CTkButton(change_frame, text="CHANGE COLOR", font=self.normal_font, command=change_color, width=100)
        change_difficulty_btn = CTkButton(change_frame, text="CHANGE DIFFICULTY", font=self.normal_font, command=self.create_difficulty_screen)

        begin_btn = CTkButton(btn_frame, text="BEGIN", width=200, font=self.heading_font, command=self.create_game_screen)

        heading_frame.pack(side=TOP, fill=X, **self.padding)
        heading_label.pack(fill=X, **self.padding)
        color_frame.pack(side=TOP, fill=BOTH, expand=1,  **self.padding)

        btn_frame.pack(side=TOP, fill=BOTH, **self.padding)
        change_frame.pack(side=TOP)

        change_color_btn.pack(side=LEFT, fill=X, **self.padding)
        change_difficulty_btn.pack(side=LEFT,fill=X, **self.padding)
        begin_btn.pack(side=TOP, **self.padding)

    def create_game_screen(self):
        """This function creates the game screen"""
        def run_timer():
            if not self.won:
                timer_label.configure(text=f"TIMER: {self.timer//60:02}:{self.timer%60:02}")
                if self.timer:
                    self.timer -= 1
                    timer_label.after(1000,run_timer)
                else:
                    self.lose_dialog()

        def increase_R():
            if RED.get() < 253:
                RED.set(RED.get() + 3)
                update()

        def increase_G():
            if GREEN.get() < 251:
                GREEN.set(GREEN.get() + 3)
                update()
        def increase_B():
            if BLUE.get() < 253:
                BLUE.set(BLUE.get() + 3)
                update()

        def decrease_R():
            if RED.get() >= 4:
                RED.set(RED.get() - 3)
                update()
        def decrease_G():
            if GREEN.get() >= 4:
                GREEN.set(GREEN.get() - 3)
                update()
        def decrease_B():
            if BLUE.get() >= 4:
                BLUE.set(BLUE.get() - 3)
                update()

        def update(event=NONE):
            def check_percentage():
                red_error = (abs(self.color[1][0] - RED.get()) / self.color[1][0]) * 100
                green_error = (abs(self.color[1][1] - GREEN.get()) / self.color[1][1]) * 100
                blue_error = (abs(self.color[1][2] - BLUE.get()) / self.color[1][2]) * 100
                percentage_error = (red_error + green_error + blue_error) / 3
                return percentage_error
            color_code = f"#{RED.get():02X}{GREEN.get():02X}{BLUE.get():02X}"
            if check_percentage() <= self.degree_error:
                time.sleep(1)
                red_slider["state"] = "disabled"
                blue_slider["state"] = "disabled"
                green_slider["state"] = "disabled"
                self.win_dialog()
            try:
                color_frame.configure(fg_color=color_code)
            except _tkinter.TclError:
                pass

        self._clear()
        RED = IntVar()
        GREEN = IntVar()
        BLUE = IntVar()

        self.set_values()
        timer_frame = CTkFrame(self)
        timer_label = CTkLabel(timer_frame, text="",
                               font=self.heading_font)
        timer_label.after(1, run_timer)
        color_frame = CTkFrame(self, fg_color=rand_colour()[0])
        slider_frame = CTkFrame(self)

        red_label = CTkLabel(slider_frame, text="RED", font=self.normal_font,fg_color="red", corner_radius=5)
        red_slider = CTkSlider(slider_frame, from_=1, to=255, width=120, fg_color="red",
                               variable=RED, command=update)

        green_label = CTkLabel(slider_frame, text="GREEN", font=self.normal_font, fg_color="green", corner_radius=5)
        green_slider = CTkSlider(slider_frame, from_=1, to=255, width=120, fg_color="green",
                                 variable=GREEN, command=update)

        blue_label = CTkLabel(slider_frame, text="BLUE", font=self.normal_font, fg_color="blue", corner_radius=5)
        blue_slider = CTkSlider(slider_frame, from_=1, to=255, width=120, fg_color="blue",
                                variable=BLUE, command=update)

        RED.set(1)
        GREEN.set(1)
        BLUE.set(1)
        red_label.pack(side=LEFT, fill=X, **self.padding)
        red_slider.pack(side=LEFT, fill=X)

        green_label.pack(side=LEFT, fill=X, **self.padding)
        green_slider.pack(side=LEFT, fill=X)

        blue_label.pack(side=LEFT, fill=X, **self.padding)
        blue_slider.pack(side=LEFT, fill=X)


        timer_frame.pack(side=TOP, fill=X, **self.padding)
        timer_label.pack(fill=X, **self.padding)

        color_frame.pack(side=TOP, fill=BOTH, expand=1, **self.padding)
        slider_frame.pack(side=TOP, fill=X, expand=0, **self.padding)

        self.bind("<r>", lambda event: increase_R())
        self.bind("<R>", lambda event: decrease_R())
        self.bind("<g>", lambda event: increase_G())
        self.bind("<G>", lambda event: decrease_G())
        self.bind("<b>", lambda event: increase_B())
        self.bind("<B>", lambda event: decrease_B())

App()