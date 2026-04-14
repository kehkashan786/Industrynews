import tkinter as tk
from tkinter import messagebox, ttk

class Account:
    def __init__(self, name, Acc_no, Balance):
        self.name = name
        self.Acc_no = Acc_no
        self.Balance = Balance
    
    def display(self):
        return f"Name: {self.name}\nAccount Number: {self.Acc_no}\nBalance: \u20B9{self.Balance:.2f}"
    
    def credit(self, cd):
        self.Balance = self.Balance + cd
        return f"\u20B9{cd:.2f} credited. New balance: \u20B9{self.Balance:.2f}"
    
    def debit(self, db):
        if db < self.Balance:
            self.Balance = self.Balance - db
            return f"\u20B9{db:.2f} debited. New balance: \u20B9{self.Balance:.2f}"
        else:
            return "Not Sufficient Balance"

class BankingApp:
    def __init__(self, root, account):
        self.root = root
        self.account = account
        self.root.title("Banking System")
        self.root.geometry("400x650")
        self.root.resizable(False, False)
     
        
        # Create header
        header_frame = tk.Frame(root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        
        header=tk.Label(
            header_frame, 
            text="Banking System", 
            font=("Arial", 24, "bold"), 
            bg="#2c3e50", 
            fg="white"
        )
        header.pack(pady=20)
        
        # Account information
        info_frame = tk.Frame(root, bg="#f0f0f0", pady=20)
        info_frame.pack(fill=tk.X)
        
        tk.Label(
            info_frame, 
            text=f"Welcome, {account.name}", 
            font=("Arial", 16), 
            bg="#f0f0f0"
        ).pack()
        
        tk.Label(
            info_frame, 
            text=f"Account: {account.Acc_no}", 
            font=("Arial", 12), 
            bg="#f0f0f0"
        ).pack()
        
        # Balance display
        self.balance_var = tk.StringVar()
        self.update_balance_display()
        
        balance_frame = tk.Frame(root, bg="#ecf0f1", pady=15)
        balance_frame.pack(fill=tk.X)
        
        tk.Label(
            balance_frame,
            textvariable=self.balance_var,
            font=("Arial", 18, "bold"),
            bg="#ecf0f1"
        ).pack()
        
        # Operations frame
        op_frame = tk.Frame(root, bg="#f0f0f0", pady=20)
        op_frame.pack(fill=tk.BOTH,  padx=30)
        
        # Amount entry
        amount_frame = tk.Frame(op_frame, bg="#f0f0f0")
        amount_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            amount_frame,
            text="Amount (\u20B9):",
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=5)
        
        self.amount_entry = tk.Entry(amount_frame, font=("Arial", 12), width=15)
        self.amount_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        buttons_frame = tk.Frame(op_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Deposit button
        tk.Button(
            buttons_frame,
            text="Deposit",
            font=("Arial", 12),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10,
            command=self.deposit
        ).pack(side=tk.LEFT, padx=10)
        
        # Withdraw button
        tk.Button(
            buttons_frame,
            text="Withdraw",
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10,
            command=self.withdraw
        ).pack(side=tk.LEFT, padx=10)
        
        # Transaction history
        history_frame = tk.Frame(root, bg="#f0f0f0", pady=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=30)
        
        tk.Label(
            history_frame,
            text="Transaction History",
            font=("Arial", 14),
            bg="#f0f0f0"
        ).pack(anchor="w")
        
        # Create a frame for the transaction history with a scrollbar
        self.history_list_frame = tk.Frame(history_frame, bg="white", bd=1, relief=tk.SUNKEN)
        self.history_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.transaction_history = tk.Text(self.history_list_frame, height=8, font=("Arial", 10))
        self.transaction_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(self.history_list_frame, command=self.transaction_history.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.transaction_history.config(yscrollcommand=scrollbar.set)
        
        # Footer
        footer_frame = tk.Frame(root, bg="#2c3e50", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Label(
            footer_frame,
            text="© 2025 Banking System", 
            font=("Arial", 10),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=10)
        
        # Initialize transaction history
        self.add_transaction("Account opened")

    def update_balance_display(self):
        self.balance_var.set(f"Balance: \u20B9{self.account.Balance:.2f}")
    
    def get_amount(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Please enter a positive amount")
                return None
            return amount
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            return None
    
    def deposit(self):
        amount = self.get_amount()
        if amount:
            result = self.account.credit(amount)
            self.update_balance_display()
            self.add_transaction(f"Deposited: \u20B9{amount:.2f}")
            messagebox.showinfo("Success", result)
            self.amount_entry.delete(0, tk.END)
    
    def withdraw(self):
        amount = self.get_amount()
        if amount:
            result = self.account.debit(amount)
            if "Not Sufficient" not in result:
                self.update_balance_display()
                self.add_transaction(f"Withdrew: \u20B9{amount:.2f}")
            messagebox.showinfo("Transaction Result", result)
            self.amount_entry.delete(0, tk.END)
    
    def add_transaction(self, transaction_text):
        timestamp = tk.StringVar()
        from datetime import datetime
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        
        self.transaction_history.insert(
            "1.0", #tk.END
            f"[{timestamp}] {transaction_text}\n"
        )
        self.transaction_history.see(tk.END)  # Scroll to the bottom


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    user = Account("Kehkashan", 1234567890, 34000)
    app = BankingApp(root, user)
    root.mainloop()