from ttkbootstrap import Frame,Label,Entry,PhotoImage,Button,Combobox
from ttkbootstrap.style import LIGHT,SUCCESS
from ttkbootstrap.dialogs import Messagebox
from Common.entities.Enums.gender import Gender



class UpdateCustomerFrame(Frame):
    def __init__(self,window,manager,customer_business):
        super().__init__(window)

        self.manager = manager
        self.customer_business = customer_business



        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.header_create_customer=Label(self,text="----------------------- Update Customer -----------------------")
        self.header_create_customer.grid(row=0,columnspan=5,column=0,padx=10,pady=10)

        self.image_arrow = PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2, 2)
        self.butten_arrow = Button(self, image=self.image_arrow, command=self.butten_arrow_clicked, bootstyle=LIGHT)
        self.butten_arrow.grid(row=0, column=0, padx=10, pady=(5, 20), sticky="w")

        self.label_firstname=Label(self,text="First Name")
        self.label_firstname.grid(row=1,column=0,padx=10,pady=(0,10),sticky="e")
        self.entry_firstname=Entry(self)
        self.entry_firstname.grid(row=1,column=1,pady=(0,10),padx=(0,10),sticky="ew")

        self.label_lastname = Label(self, text="Last Name")
        self.label_lastname.grid(row=1, column=3, padx=10, pady=(0, 10), sticky="e")
        self.entry_lastname = Entry(self)
        self.entry_lastname.grid(row=1, column=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_national_code = Label(self, text="National Code")
        self.label_national_code.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_national_code = Entry(self)
        self.entry_national_code.grid(row=2, column=1, columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_phon = Label(self, text="Phon Number")
        self.label_phon.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_phon = Entry(self)
        self.entry_phon.grid(row=3, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_email = Label(self, text="Email")
        self.label_email.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_email = Entry(self)
        self.entry_email.grid(row=4, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_brith_date = Label(self, text="Brith Date")
        self.label_brith_date.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_brith_date = Entry(self)
        self.entry_brith_date.grid(row=5, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_gender = Label(self, text="Gender")
        self.label_gender.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_gender = Combobox(self,values=[gender.name for gender in Gender],state="readonly")
        self.entry_gender.grid(row=6, column=1,columnspan=4, padx=(0, 10), sticky="ew")

        self.error_customer=Label(self)
        self.error_customer.grid(row=7,column=0,columnspan=5,pady=10)

        self.butten_save=Button(self,text="Save ✔",command=self.save_profile_button_clicked,bootstyle=SUCCESS)
        self.butten_save.grid(row=9,column=0,columnspan=5,pady=(5,25))


    def butten_arrow_clicked(self):
        self.manager.back()

    def save_profile_button_clicked(self):
        new_firstname = self.entry_firstname.get()
        new_lastname = self.entry_lastname.get()
        new_national_code = self.entry_national_code.get()
        new_phone_number = self.entry_phon.get()
        new_email = self.entry_email.get()
        new_birthdate = self.entry_brith_date.get()
        new_gender = self.entry_gender.get()

        response = self.customer_business.update_customer(self.customer_id,new_firstname,new_lastname
                                               ,new_national_code,new_phone_number,new_email,new_birthdate,new_gender)
        if response.success:
            Messagebox.show_info(response.message,"Success")

        else:
            Messagebox.show_error(response.message,"Error")


    def set_entry(self,customer_id):
        self.customer_id = customer_id
        response = self.customer_business.get_customer_by_id(customer_id)
        if response.success:
            self.entry_firstname.delete(0,"end")
            self.entry_firstname.insert(0,response.data.firstname)
            self.entry_lastname.delete(0, "end")
            self.entry_lastname.insert(0,response.data.lastname)
            self.entry_national_code.delete(0, "end")
            self.entry_national_code.insert(0,response.data.national_code)
            self.entry_phon.delete(0, "end")
            self.entry_phon.insert(0,response.data.phon_number)
            self.entry_email.delete(0, "end")
            self.entry_email.insert(0,response.data.email)
            self.entry_brith_date.delete(0, "end")
            self.entry_brith_date.insert(0,response.data.birth_date)

            self.entry_gender.config(state="normal")
            self.entry_gender.delete(0,"end")
            self.entry_gender.insert(0,response.data.gender.name)
            self.entry_gender.config(state="readonly")
