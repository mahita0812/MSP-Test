# message_app.py
import tkinter as tk
from tkinter import ttk
from login_gui import LoginGUI
from tkinter import messagebox
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
llm1=ChatOpenAI(openai_api_key="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", temperature=0.3)

template_sub="you have to generate a subject line for the acknowledgement email about ticket {issue_id} related to {issue_description}. Maybe a simple subject like: 'Support Ticket ticket_id: description'  "
 
subject_prompt=ChatPromptTemplate.from_messages([
    ("system",template_sub)
   
])

template="You are an L1 resource of our company 'OSI Digital' and have to write an acknowledgement email for the ticket {ticket_id} to {requester_name} stating you are working regarding the issue given by user which has {priority} as the ticket priority and has a severity of {severity} where 4 means high severity. write the mail in such a way that you show the customer that you are working to resolve the issue depending on the severity and priority but don't tell the user his/her priority and severity in the mail. If the user priority and severity is low, don't mention the priority and severity but if the priority and severity is high like if severity is 4 or priority is high then stress in the mail that we are working really hard and its our topmost priority add 1-2 lines like that to make it sound that we are equally concerned and will fix the issue as soon as possible. Keep the mail short and concise maybe upto 3-4 lines only. After thank you, mention company name and i don't want any your_name field. I don't want best regards at the end, i only want thank you"
human_template="{text}"
 
body_prompt=ChatPromptTemplate.from_messages([
    ("system",template),
    ("human", human_template)
   
])

class MessageApp:
    temp = None
    mail_subject = None
    mail_body = None
    def __init__(self, excel_file):
        self.df = pd.read_excel(excel_file)

        self.root = tk.Tk()
        self.root.title("Message App")
        self.root.geometry("800x600")  # Set the initial size of the main window

        self.login_screen = None
        self.message_list_screen = None
        self.message_details_screen = None

        # self.show_login_gui()

        # self.root.mainloop()
        self.root.after(100, self.show_login_gui)
        self.root.mainloop()


    def show_login_gui(self):
        # Function to show the login GUI
        if self.login_screen:
            self.login_screen.destroy()

        self.login_screen = tk.Toplevel(self.root)
        self.login_screen.title("Login")

        login_gui = LoginGUI(self.login_screen, self.authenticate, self.show_message_list)

    def authenticate(self, email, password):
        # Add your authentication logic here
        # For demonstration purposes, let's assume a simple authentication with a hardcoded email and password
        if email == "abc" and password == "1":
            tk.messagebox.showinfo("Authentication", "Login successful!")
            self.show_message_list()
        else:
            tk.messagebox.showerror("Authentication", "Invalid credentials")

    def show_message_list(self):
        # Function to show the list of messages
        if self.message_list_screen:
            self.message_list_screen.destroy()

        self.message_list_screen = tk.Toplevel(self.root)
        self.message_list_screen.title("Message List")
        self.message_list_screen.geometry("800x600")  # Set the size of the message list screen

        # Listbox to display messages
        listbox = tk.Listbox(self.message_list_screen, selectmode=tk.SINGLE)
        listbox.pack(pady=10)

        for message in self.df['Issue_id']:
            listbox.insert(tk.END, message)

        # Button to go to message details screen
        select_button = tk.Button(self.message_list_screen, text="Select Message", command=self.show_message_details)
        select_button.pack()

    def show_message_details(self):
        # Function to show the message details screen
        selected_index = self.message_list_screen.children['!listbox'].curselection()
        if not selected_index:
            return

        selected_index = selected_index[0]
        selected_message = self.df.loc[selected_index]
        self.temp = selected_message.to_dict()

        if self.message_details_screen:
            self.message_details_screen.destroy()

        # Create and show the message details screen dynamically
        self.message_details_screen = tk.Toplevel(self.root)
        self.message_details_screen.title("Message Details")
        self.message_details_screen.geometry("800x600")  # Set the size of the message details screen

        tree = ttk.Treeview(self.message_details_screen)
        tree['columns'] = list(self.df.columns)

        for column in tree['columns']:
            tree.heading(column, text=column)
            tree.column(column, anchor='n')

        tree.pack(padx=10, pady=10)

        generate_button = tk.Button(self.message_details_screen, text="Generate", command=self.generate)
        generate_button.pack()



        # Insert data into the Treeview
        tree.insert("", "end", values=list(selected_message))

    def generate(self):
        # Add your logic for generating based on the selected message
        # You can use self.df and the selected message details for this
        sub_message=subject_prompt.format_messages(issue_id=self.temp['Issue_id'], issue_description=self.temp['message'])
        out=llm1.predict_messages(sub_message)

        # print("test")
        self.mail_subject = out.content
        print(out.content)

        message_1=body_prompt.format_messages(ticket_id=self.temp['ticket_type'], requester_name=self.temp['request name'], priority=self.temp['priority'], severity=self.temp['severity'], text=self.temp['message'])
        result=llm1.predict_messages(message_1)
        self.mail_body = result.content
        print(result.content)
        # return result.content

        if self.message_details_screen:
            # Create labels to display the variables
            label_var1 = tk.Label(self.message_details_screen, text=f" \n Subject: {self.mail_subject}", anchor='w', justify='left')
            label_var1.pack()
            print('\n')
            label_var2 = tk.Label(self.message_details_screen, text=f"{self.mail_body}", anchor='w', justify='left')
            label_var2.pack()
        pass

if __name__ == "__main__":
    excel_file_path = "Data_1.xlsx"  # Replace with your actual Excel file path
    app = MessageApp(excel_file_path)
