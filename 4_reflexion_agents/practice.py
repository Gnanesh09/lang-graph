ITR_details= []

class EmployeITR_fillig:
    def __init__(self, name, employee_id, annual_salary, bank_acc_no, pan_no,fin_year):
        self.name = name
        self.employee_id = employee_id
        self.annual_salary = annual_salary
        self.bank_acc_no = bank_acc_no
        self.pan_no = pan_no
        self.fin_year = fin_year

    def Tax_calculation(self):
        if self.annual_salary<=400000:
            tax=0
        elif self.annual_salary>=400001 and self.annual_salary<=800000:
            percentage=0.05
            tax= self.annual_salary*percentage
        elif self.annual_salary>=800001 and self.annual_salary<=1200000:
            percentage=0.1
            tax= self.annual_salary*percentage
        elif self.annual_salary>=1200001 and self.annual_salary<=1600000:
            percentage=0.15
            tax= self.annual_salary*percentage
        elif self.annual_salary>=1600001 and self.annual_salary<=2400000:
            percentage=0.25
            tax= self.annual_salary*percentage
        else:
            percentage=0.3
            tax= self.annual_salary*percentage
        

        return tax
    

        






while True:
    print("type following")
    print("itr->filing Income tax returns")
    print("exit->exit portal")
    user_input = input("You: ")
    if user_input.lower()=="exit":
        break
    if user_input.lower()=="itr":
        emp_name = input("enter yourname: ")
        emp_id = input(f"hey {emp_name} enter your id_no: ")
        emp_bank = input("enter bank acc no: ")
        emp_pan = input("enter PAN no: ")
        emp_salary = input("enter annual salary recevied: ")
        emp_finyear = input("enter financial year: ")

        employee = EmployeITR_fillig(emp_name,emp_id,int(emp_salary),emp_bank,emp_pan,emp_finyear)
        emp_tax = employee.Tax_calculation()
        ITR_details.append({
        "name": employee.name,
        "employee_id": employee.employee_id,
        "annual_salary": employee.annual_salary,
        "bank_acc_no": employee.bank_acc_no,
        "pan_no": employee.pan_no,
        "fin_year": employee.fin_year,
        "tax": emp_tax
    })
        print(f"ITR details filled successfully---)")


print("\nAll Employees ITR Details:")
for record in ITR_details:
    print(record)