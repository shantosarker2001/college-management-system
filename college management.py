import mysql.connector as mysql
db = mysql.connect(host="localhost", user="root",
                   password="", database="college")
command_handler = db.cursor(buffered=True)

def teacher_session():
    while 1:
        print()
        print("Teacher's Menu")
        print("1.Take attendance of registered students")
        print("2.View Attendance")
        print("3.Log Out")
        user_option= input(str("Option: "))
        if user_option=="1":
            print("")
            print("Attendance of Registered Students")
            command_handler.execute("SELECT username FROM users WHERE previledge='student'")
            records=command_handler.fetchall()
            date =input(str("Date: DD/MM/YYYY: "))
            for record in records:
                record=str(record).replace("'","")
                record=str(record).replace(",","")
                record=str(record).replace("(","")
                record=str(record).replace(")","")
                #Present|Absent|Late
                status=input(str("Status for "+ str(record)+" P/A/L :"))
                query_vals=(str(record),date,status)
                command_handler.execute("INSERT INTO attendance(username,date,status) VALUES(%s,%s,%s)",query_vals)
                db.commit()
                print(record + " Marked as " + status)
        elif user_option=="2":
            print("")
            print("Viewing all students registers")
            command_handler.execute("SELECT username,date,status FROM attendance")
            records=command_handler.fetchall()
            print("Displayig all registers: ")
            for record in records:
                print(record)
        elif user_option=="3":
            break
        else:
            print("No valid option was selected")
            
#Student Session Section       
def student_session(username):
    while 1:
        print("")
        print("Student's Menu")
        print("")
        print("1. View Attendance")
        print("2. Download Attendance")
        print("3. Log Out")
        user_option=input(str("Option: "))
        if user_option =="1":
            print("Displaying attendance ")
            username=(str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username=%s",username)
            records=command_handler.fetchall()
            for record in records:
                print(record)
        
        elif user_option=="2":
            print("Downloading Attendance")
            username=(str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username=%s",username)
            records=command_handler.fetchall()
            for record in records:
                with open("C:/Users/NHC/Desktop/Project/register.txt","w") as f:
                    f.write(str(record)+"\n")
                f.close()
            print("All records are saved successfully")
        elif user_option == "3":
            break
        else:
            print("No valid option selected")       
                
                
def admin_session():
    print("")
    print("Login Succesfull")
    print("")
    print("Wellcome to Admin Session")
    while 1:
        print()
        print("Admin Menu")
        print("1.Register New Student")
        print("2.Register New Teacher")
        print("3.Delete Existing Student")
        print("4.Delete Existing Teacher")
        print("5.Log Out")

        user_option = input(str("Option: "))
        if user_option == "1":
            print("")
            print("Register New Student")
            username = input(str("Student username "))
            password = input(str("Student password "))
            query_vals = (username, password)
            command_handler.execute(
                "INSERT INTO users(username,password,previledge) VALUES(%s,%s,'student')", query_vals)
            db.commit()
            print(username + " has been registered as a student")

        elif user_option == "2":
            
            print("")
            print("Register New Teacher")
            username = input(str("Teacher username "))
            password = input(str("Teacher password "))
            query_vals = (username, password)
            command_handler.execute(
                "INSERT INTO users(username,password,previledge) VALUES(%s,%s,'teacher')", query_vals)
            db.commit()
            print(username + " has been registered as a teacher")

        elif user_option == "3":
            print("")
            print("Delete Existing Student Account")
            username = input(str("Student username: "))
            query_vals = (username, "student")
            command_handler.execute(
                "DELETE FROM users WHERE username=%s AND previledge=%s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found")
            else:
                print(username + " has been deleted")

        elif user_option == "4":
            print("")
            print("Delete Existing Teacher Account")
            username = input(str("Teacher username: "))
            query_vals = (username, "teacher")
            command_handler.execute(
                "DELETE FROM users WHERE username=%s AND previledge=%s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found")
            else:
                print(username + " has been deleted")

        elif user_option == "5":
            break
        else:
            print("No valid option selected")


def auth_student():
    print("")
    print("Student's Log In ")
    print("")
    username=input(str("Username: "))
    password=input(str("Password: "))
    query_vals=(username,password,'student')
    command_handler.execute("SELECT username FROM users WHERE username=%s AND password=%s AND previledge=%s",query_vals)
    #username=command_handler.fetchone()
    if command_handler.rowcount<=0:
        print("Invalid Login Details!")
    else:
        student_session(username)
def auth_teacher():
    print()
    print("Teacher Login")
    username = input(str("Username: "))
    password = input(str("Password: "))
    query_vals = (username, password)
    command_handler.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s AND previledge='teacher'", query_vals)
    if command_handler.rowcount <= 0:
        print("Login Not recognised")
    else:
        teacher_session()


def auth_admin():
    print()
    print("Admin Login")
    print()
    username = input(str("Username: "))
    password = input(str("Password: "))
    if username == "admin":
        if password == "admin2000":
            admin_session()
        else:
            print("Incorrect Password")
    else:
        print("Login details not recognized")


def main():
    while 1:
        print("")
        print("Wellcome to College Management System")
        print("")
        print("Login As Student")
        print("Login As Teacher")
        print("Login As Admin")

        user_option = input(str("Option: "))
        if user_option == "1":
            auth_student()
        elif user_option == "2":
            auth_teacher()
        elif user_option == "3":
            auth_admin()
        else:
            print("No valid option was selected")


main()
