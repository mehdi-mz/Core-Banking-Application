
from Presentation.Desktop.Window import ApplicationWindow

from Presentation.Desktop.frames.Login import LoginFrame
from Presentation.Desktop.frames.Register import RegisterFrame
from Presentation.Desktop.frames.home import HomeFrame
from Presentation.Desktop.frames.account_management import AccountManagmentFrame
from Presentation.Desktop.frames.reset_password import ResetPasswordFrame
from Presentation.Desktop.frames.my_profile import MyProfileFrame
from Presentation.Desktop.frames.transaction_manajement import TransactionManajementFrame
from Presentation.Desktop.frames.create_transaction import CreateTransaction
from Presentation.Desktop.frames.create_customer import CreateCustomerFrame
from Presentation.Desktop.frames.admin_home import AdminHomeFrame
from Presentation.Desktop.frames.employee_request_approval import EmployeeRequestApprovalFrame
from Presentation.Desktop.frames.employee_management import EmployeeManagmentFrame
from Presentation.Desktop.frames.update_employee import UpdateEmployeeFrame
from Presentation.Desktop.frames.customer_management import CustomerManagementFrame
from Presentation.Desktop.frames.deactivated_employees import DeactivatedEmployeeFrame
from Presentation.Desktop.frames.update_customer import UpdateCustomerFrame
from Presentation.Desktop.frames.transfer_from_card import TransferFromCard
from Presentation.Desktop.frames.rejected_employees import RejectEmployeeFrame
from Presentation.Desktop.frames.customer_accounts import CustomerAccountsFrame
from Presentation.Desktop.frames.update_account import UpdateAccountFrame
from Presentation.Desktop.frames.admin_reset_Employee_Password import AdminResetEmployeePasswordFrame
from Presentation.Desktop.frames.request_employee import RequestEmployeeFrame
from Presentation.Desktop.frames.navbar import Navbar

from BusinessLogic.employee_business_logic import EmployeeBusinessLogic
from BusinessLogic.account_business_logic import AccountBusinessLogic
from BusinessLogic.transaction_business_logic import TransactionBusinessLogic
from BusinessLogic.customer_business_logic import CustomerBusinessLogic

from Common.Decorators.performance_logger_decorator import PerformanceLogger


class ViewManager:
    def __init__(self,employee_business:EmployeeBusinessLogic,
                       account_business:AccountBusinessLogic,
                        transaction_business:TransactionBusinessLogic,
                        customer_business : CustomerBusinessLogic
                 ):
        self.current_user=None

        self.frames={}
        self.histori=[]
        self.current_frame = None
        self.window=ApplicationWindow()

        self.navbar = Navbar(self.window,self)
        self.navbar.grid(row=0,column=0,sticky="ew")

        self.add_frame("create transation",CreateTransaction(self.window,self,transaction_business),(500,450))
        self.add_frame("card to card",TransferFromCard(self.window,self,transaction_business,customer_business),(500,450))

        self.add_frame("customer accounts",CustomerAccountsFrame(self.window,self,account_business,customer_business),(1500,650))
        self.add_frame("update account",UpdateAccountFrame(self.window,self,account_business),(700,500))


        self.add_frame("My Profile",MyProfileFrame(self.window,self,employee_business),(650,600))

        self.add_frame("admin reset password",AdminResetEmployeePasswordFrame(self.window,self,employee_business),(450,400))
        self.add_frame("reset password",ResetPasswordFrame(self.window,self,employee_business),(450,380))


        self.add_frame("create customer",CreateCustomerFrame(self.window,self,customer_business,account_business),(950,700))
        self.add_frame("update customer",UpdateCustomerFrame(self.window,self,customer_business),(950,500))

        self.add_frame("update employee",UpdateEmployeeFrame(self.window,self,employee_business),(650,600))
        self.add_frame("request employee",RequestEmployeeFrame(self.window,self,employee_business),(1350,600))
        self.add_frame("reject employee", RejectEmployeeFrame(self.window, self, employee_business), (1360,600))
        self.add_frame("deactivated employee",DeactivatedEmployeeFrame(self.window,self,employee_business,),(1360,600))
        self.add_frame("request approval",EmployeeRequestApprovalFrame(self.window,self,employee_business),(1000,600))


        self.add_frame("employee management",EmployeeManagmentFrame(self.window,self,employee_business),(1360,700))
        self.add_frame("account manajment", AccountManagmentFrame(self.window, self, account_business,customer_business), (1500, 650))
        self.add_frame("Transaction Manajement", TransactionManajementFrame(self.window, self,transaction_business), (1400,650))
        self.add_frame("customer management", CustomerManagementFrame(self.window, self,customer_business),(1500, 650))

        self.add_frame("Home", HomeFrame(self.window, self), (600,400))
        self.add_frame("home admin", AdminHomeFrame(self.window, self), (600,400))

        self.add_frame("Register", RegisterFrame(self.window,self,employee_business),(600,500))
        self.add_frame("Login", LoginFrame(self.window,self,employee_business),(550,450))


        self.show_frame("Login")


        self.window.show()


    def add_frame(self,name,frame,size):
        self.frames[name]=(frame,size)
        self.frames[name][0].grid(row=1,column=0,sticky="snew")


    def resaze_window(self,frame_name):
        current_frame_data=self.frames[frame_name]
        frame_size=current_frame_data[1]
        self.window.resaiz(*frame_size)


    def show_frame(self,name,**kwargs):
        if self.current_frame:
            self.histori.append(self.current_frame)
        self.resaze_window(name)
        frame = self.frames[name][0]
        self.current_frame = name
        frame.tkraise()
        return frame

    @PerformanceLogger
    def back(self):
        if not self.histori:
            return None
        previous = self.histori.pop()
        self.current_frame = previous
        self.resaze_window(previous)
        frame = self.frames[previous][0]
        frame.tkraise()
        return frame
