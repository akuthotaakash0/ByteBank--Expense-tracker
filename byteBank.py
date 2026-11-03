import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class ExpenseAnalyzer:
    """ByteBank - Digital Expense Analyzer: A comprehensive expense management system"""
    
    def __init__(self, filename: str = "expenses.json"):
        self.filename = filename
        self.expenses: List[Dict] = []
        self.categories = ["Food", "Transport", "Entertainment", "Utilities", "Healthcare", "Education", "Shopping", "Other"]
        self.load_data()
    
    def load_data(self):
        """Load expenses from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.expenses = json.load(f)
                print(f"✓ Data loaded successfully ({len(self.expenses)} expenses)")
            except json.JSONDecodeError:
                print("⚠ Error reading file. Starting with empty data.")
                self.expenses = []
        else:
            print("⚠ No existing data found. Starting fresh.")
            self.expenses = []
    
    def save_data(self):
        """Save expenses to JSON file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.expenses, f, indent=2)
            print("✓ Data saved successfully")
        except Exception as e:
            print(f"✗ Error saving data: {e}")
    
    def add_expense(self):
        """Add a new expense entry"""
        print("\n" + "="*50)
        print("ADD NEW EXPENSE")
        print("="*50)
        
        try:
            description = input("Description: ").strip()
            if not description:
                print("✗ Description cannot be empty")
                return
            
            amount = float(input("Amount: ₹"))
            
            print("\nCategories:")
            for i, cat in enumerate(self.categories, 1):
                print(f"{i}. {cat}")
            
            cat_choice = int(input("Select category (1-8): "))
            if 1 <= cat_choice <= len(self.categories):
                category = self.categories[cat_choice - 1]
            else:
                print("✗ Invalid category. Using 'Other'")
                category = "Other"
            
            date = input("Date (DD/MM/YYYY) or press Enter for today: ").strip()
            if not date:
                date = datetime.now().strftime("%d/%m/%Y")
            
            expense = {
                "id": len(self.expenses) + 1,
                "description": description,
                "amount": amount,
                "category": category,
                "date": date,
                "timestamp": datetime.now().isoformat()
            }
            
            self.expenses.append(expense)
            self.save_data()
            print(f"\n✓ Expense added successfully! (ID: {expense['id']})")
            
        except ValueError:
            print("✗ Invalid input. Please enter valid values.")
    
    def update_expense(self):
        """Update an existing expense"""
        print("\n" + "="*50)
        print("UPDATE EXPENSE")
        print("="*50)
        
        try:
            exp_id = int(input("Enter expense ID to update: "))
            expense = next((e for e in self.expenses if e["id"] == exp_id), None)
            
            if not expense:
                print("✗ Expense not found")
                return
            
            print(f"\nCurrent: {expense['description']} - ₹{expense['amount']} ({expense['category']})")
            print("\nLeave blank to keep current value")
            
            description = input(f"New description [{expense['description']}]: ").strip()
            if description:
                expense["description"] = description
            
            amount_str = input(f"New amount [₹{expense['amount']}]: ").strip()
            if amount_str:
                expense["amount"] = float(amount_str)
            
            print("\nCategories:")
            for i, cat in enumerate(self.categories, 1):
                print(f"{i}. {cat}")
            cat_str = input(f"New category [{expense['category']}] (1-8): ").strip()
            if cat_str:
                cat_choice = int(cat_str)
                if 1 <= cat_choice <= len(self.categories):
                    expense["category"] = self.categories[cat_choice - 1]
            
            date = input(f"New date [{expense['date']}]: ").strip()
            if date:
                expense["date"] = date
            
            expense["last_modified"] = datetime.now().isoformat()
            self.save_data()
            print("\n✓ Expense updated successfully!")
            
        except ValueError:
            print("✗ Invalid input")
    
    def delete_expense(self):
        """Delete an expense"""
        print("\n" + "="*50)
        print("DELETE EXPENSE")
        print("="*50)
        
        try:
            exp_id = int(input("Enter expense ID to delete: "))
            expense = next((e for e in self.expenses if e["id"] == exp_id), None)
            
            if not expense:
                print("✗ Expense not found")
                return
            
            print(f"\nExpense: {expense['description']} - ₹{expense['amount']}")
            confirm = input("Are you sure you want to delete? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                self.expenses = [e for e in self.expenses if e["id"] != exp_id]
                self.save_data()
                print("\n✓ Expense deleted successfully!")
            else:
                print("✗ Deletion cancelled")
                
        except ValueError:
            print("✗ Invalid input")
    
    def view_all_expenses(self):
        """Display all expenses"""
        print("\n" + "="*50)
        print("ALL EXPENSES")
        print("="*50)
        
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        
        print(f"\n{'ID':<5} {'Date':<12} {'Description':<25} {'Category':<15} {'Amount':>10}")
        print("-" * 80)
        
        for exp in self.expenses:
            print(f"{exp['id']:<5} {exp['date']:<12} {exp['description'][:24]:<25} "f"{exp['category']:<15} ₹{exp['amount']:>9.2f}")
        
        print(f"\nTotal Expenses: {len(self.expenses)}")
    
    def filter_by_category(self):
        """Filter expenses by category"""
        print("\n" + "="*50)
        print("FILTER BY CATEGORY")
        print("="*50)
        
        print("\nCategories:")
        for i, cat in enumerate(self.categories, 1):
            print(f"{i}. {cat}")
        
        try:
            choice = int(input("\nSelect category (1-8): "))
            if 1 <= choice <= len(self.categories):
                category = self.categories[choice - 1]
                filtered = [e for e in self.expenses if e["category"] == category]
                
                if not filtered:
                    print(f"\nNo expenses found in '{category}' category.")
                    return
                
                print(f"\n{'ID':<5} {'Date':<12} {'Description':<25} {'Amount':>10}")
                print("-" * 60)
                
                total = 0
                for exp in filtered:
                    print(f"{exp['id']:<5} {exp['date']:<12} {exp['description'][:24]:<25} "f"₹{exp['amount']:>9.2f}")
                    total += exp['amount']
                
                print(f"\nTotal in {category}: ₹{total:.2f}")
            else:
                print("✗ Invalid category")
        except ValueError:
            print("✗ Invalid input")
    
    def generate_summary(self):
        """Generate expense summary and analytics"""
        print("\n" + "="*50)
        print("EXPENSE SUMMARY & ANALYTICS")
        print("="*50)
        
        if not self.expenses:
            print("No expenses to summarize.")
            return
        
        total = sum(e['amount'] for e in self.expenses)
        avg = total / len(self.expenses)
        
        # Category-wise breakdown
        cat_totals = {}
        for exp in self.expenses:
            cat = exp['category']
            cat_totals[cat] = cat_totals.get(cat, 0) + exp['amount']
        
        print(f"\n📊 OVERALL STATISTICS")
        print("-" * 50)
        print(f"Total Expenses: {len(self.expenses)}")
        print(f"Total Amount: ₹{total:.2f}")
        print(f"Average Amount: ₹{avg:.2f}")
        print(f"Highest Expense: ₹{max(e['amount'] for e in self.expenses):.2f}")
        print(f"Lowest Expense: ₹{min(e['amount'] for e in self.expenses):.2f}")
        
        print(f"\n📈 CATEGORY BREAKDOWN")
        print("-" * 50)
        print(f"{'Category':<20} {'Amount':>12} {'Percentage':>12}")
        print("-" * 50)
        
        for cat in sorted(cat_totals.keys(), key=lambda x: cat_totals[x], reverse=True):
            amount = cat_totals[cat]
            percentage = (amount / total) * 100
            print(f"{cat:<20} ₹{amount:>10.2f} {percentage:>11.1f}%")
        
        # Top 5 expenses
        print(f"\n💰 TOP 5 EXPENSES")
        print("-" * 50)
        sorted_exp = sorted(self.expenses, key=lambda x: x['amount'], reverse=True)[:5]
        for i, exp in enumerate(sorted_exp, 1):
            print(f"{i}. {exp['description'][:30]:<30} ₹{exp['amount']:>10.2f} ({exp['category']})")
    
    def generate_report(self):
        """Generate and export detailed report"""
        print("\n" + "="*50)
        print("GENERATE REPORT")
        print("="*50)
        
        if not self.expenses:
            print("No expenses to report.")
            return
        
        report_file = f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("BYTEBANK - DIGITAL EXPENSE ANALYZER\n")
                f.write("DETAILED EXPENSE REPORT\n")
                f.write("="*70 + "\n\n")
                f.write(f"Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Total Expenses: {len(self.expenses)}\n\n")
                
                total = sum(e['amount'] for e in self.expenses)
                f.write(f"TOTAL AMOUNT: ₹{total:.2f}\n")
                f.write("="*70 + "\n\n")
                
                f.write("DETAILED EXPENSE LIST\n")
                f.write("-"*70 + "\n")
                f.write(f"{'ID':<5} {'Date':<12} {'Description':<30} {'Category':<15} {'Amount':>10}\n")
                f.write("-"*70 + "\n")
                
                for exp in self.expenses:
                    f.write(f"{exp['id']:<5} {exp['date']:<12} {exp['description'][:29]:<30} "
                    f"{exp['category']:<15} ₹{exp['amount']:>9.2f}\n")
                
                f.write("\n" + "="*70 + "\n")
                f.write("CATEGORY SUMMARY\n")
                f.write("-"*70 + "\n")
                
                cat_totals = {}
                for exp in self.expenses:
                    cat = exp['category']
                    cat_totals[cat] = cat_totals.get(cat, 0) + exp['amount']
                
                for cat, amount in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
                    percentage = (amount / total) * 100
                    f.write(f"{cat:<20} ₹{amount:>10.2f} ({percentage:>5.1f}%)\n")
                
                f.write("\n" + "="*70 + "\n")
                f.write("End of Report\n")
            
            print(f"\n✓ Report generated successfully: {report_file}")
            
        except Exception as e:
            print(f"✗ Error generating report: {e}")
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("BYTEBANK - DIGITAL EXPENSE ANALYZER")
        print("="*50)
        print("1. Add Expense")
        print("2. Update Expense")
        print("3. Delete Expense")
        print("4. View All Expenses")
        print("5. Filter by Category")
        print("6. Generate Summary")
        print("7. Generate Report")
        print("8. Exit")
        print("="*50)
    
    def run(self):
        """Main application loop"""
        print("\n" + "🏦 "*15)
        print("WELCOME TO BYTEBANK - DIGITAL EXPENSE ANALYZER")
        print("Your roots to success...")
        print("🏦 "*15)
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (1-8): ").strip()
                
                if choice == '1':
                    self.add_expense()
                elif choice == '2':
                    self.update_expense()
                elif choice == '3':
                    self.delete_expense()
                elif choice == '4':
                    self.view_all_expenses()
                elif choice == '5':
                    self.filter_by_category()
                elif choice == '6':
                    self.generate_summary()
                elif choice == '7':
                    self.generate_report()
                elif choice == '8':
                    print("\n" + "="*50)
                    print("Thank you for using ByteBank!")
                    print("Your data has been saved.")
                    print("="*50)
                    break
                else:
                    print("\n✗ Invalid choice. Please select 1-8.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nExiting application...")
                break
            except Exception as e:
                print(f"\n✗ An error occurred: {e}")
                input("\nPress Enter to continue...")

# Main execution
if __name__ == "__main__":
    analyzer = ExpenseAnalyzer()
    analyzer.run()