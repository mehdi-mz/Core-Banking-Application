# from tkinter import Frame,Label,Entry,Button,PhotoImage
from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage
from ttkbootstrap.style import INFO

# from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
import random
from io import BytesIO


class Captchacomponent(Frame):
    def __init__(self,master):
        super().__init__(master)

        # self.U ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # self.L = "abcdefghijklmnopqrstuvwxyz"
        self.N ="1234567890"
        # self.X = self.L+self.N
        self.res= "".join(random.sample(self.N,4))
        self.data_captcha=str(self.res)

        # self.audio = AudioCaptcha()
        self.image = ImageCaptcha(fonts=[r'assets\font\verdana.ttf'])

        # self.data = self.audio.generate(self.data_captcha)
        # self.audio.write(self.data_captcha, 'out.wav')

        self.data = self.image.generate(self.data_captcha)
        # self.captcha= self.image.write(self.data_captcha, 'out.png')
        self.image_data=BytesIO(self.data.read())

        self.image_captcha=PhotoImage(data=self.image_data.getvalue())
        self.label_captcha=Label(self,image=self.image_captcha)
        self.label_captcha.grid(row=0,column=0)

        self.image_refresh=PhotoImage(file=r"assets\image\icons8-refresh-50.png").subsample(4,4)

        self.butten_refresh=Button(self,image=self.image_refresh,command=self.butten_refresh_clicked,bootstyle=INFO)
        self.butten_refresh.grid(row=0,column=1,pady=10)

        self.entry_captcha=Entry(self)
        self.entry_captcha.grid(row=1,column=0,columnspan=2,sticky="ew")

    def butten_refresh_clicked(self):
        # self.U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # self.L = "abcdefghijklmnopqrstuvwxyz"
        self.N = "1234567890"
        # self.X =  self.L + self.N
        self.res = "".join(random.sample(self.N, 4))
        self.data_captcha = str(self.res)

        # self.audio = AudioCaptcha()
        self.image = ImageCaptcha(fonts=[r'assets\font\verdana.ttf'])

        # self.data = self.audio.generate(self.data_captcha)
        # self.audio.write(self.data_captcha, 'out.wav')

        self.data = self.image.generate(self.data_captcha)
        # self.captcha = self.image.write(self.data_captcha, 'out.png')
        self.image_data=BytesIO(self.data.read())

        self.image_captcha = PhotoImage(data=self.image_data.getvalue())
        self.label_captcha.config(image=self.image_captcha)

    def get_entry_data(self):
        entry_captcha=self.entry_captcha.get()
        return entry_captcha

    def get_data_captcha(self):
        return self.data_captcha

    def clear_captcha(self):
        self.entry_captcha.delete(0,"end")
        self.butten_refresh_clicked()


