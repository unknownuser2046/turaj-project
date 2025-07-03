from library import LibrarySystem

# تعریف رمز عبور متصدی به صورت متغیر برای تغییر آسان
LIBRARIAN_PASSWORD = "admin"

def print_librarian_menu():
    print("\n=== Librarian Menu ===")
    print("1. Add Book")
    print("2. Edit Book")
    print("3. Search Books")
    print("4. View Overdue Books")
    print("5. View Statistics")
    print("6. Delete Book")
    print("7. View All Members")
    print("8. Edit Member")
    print("9. Delete Member")
    print("10. View Member History")
    print("11. View Top Borrowers")
    print("12. Exit")
    print("=" * 25)

def print_member_menu():
    print("\n=== Library Management System (Member) ===")
    print("1. View Available Books")
    print("2. Search Books")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. View My Borrowed Books")
    print("6. Exit")
    print("==========================")



def print_delete_book_menu():
    print("\n=== Delete Book Options ===")
    print("1. Delete by ISBN")
    print("2. Delete by Title")
    print("3. Delete by Author and Title")
    print("0. Back to Main Menu")
    print("==========================")

def handle_delete_book(library):
    while True:
        print_delete_book_menu()
        choice = input("Please select a delete option: ")
        
        if choice == "1":
            isbn = input("Enter book ISBN to delete: ")
            if library.delete_book(isbn):
                print("Book deleted successfully.")
            else:
                print("Error: Book cannot be deleted. It might be borrowed or not exist.")
            break
            
        elif choice == "2":
            title = input("Enter book title to delete: ")
            if library.delete_book_by_title(title):
                print("Book deleted successfully.")
            else:
                print("Error: Book cannot be deleted. It might be borrowed or not exist.")
            break
            
        elif choice == "3":
            author = input("Enter book author: ")
            title = input("Enter book title: ")
            if library.delete_book_by_author_and_title(author, title):
                print("Book deleted successfully.")
            else:
                print("Error: Book cannot be deleted. It might be borrowed or not exist.")
            break
            
        elif choice == "6":
            print("Goodbye!")
            break
            
        else:
            print("Invalid option. Please try again.")

def handle_member_mode(library, member_id):
    # Check for overdue books and show warning
    overdue_books = library.get_overdue_books()
    member_overdue = [book for book in overdue_books if book['member_id'] == member_id]
    if member_overdue:
        print("\n⚠️ WARNING: You have overdue books!")
        for book in member_overdue:
            print(f"Book: {book['book_title']} - {book['days_overdue']} days overdue")
        print("-" * 30)
    
    while True:
        print_member_menu()
        choice = input("Please select an option: ")
        
        if choice == "1":
            # View available books
            available_books = [book for book in library.books.values() if book.is_available]
            if available_books:
                print("\n=== Available Books ===")
                for book in available_books:
                    print(f"Title: {book.title}")
                    print(f"Author: {book.author}")
                    print(f"Category: {book.category}")
                    print(f"ISBN: {book.isbn}")
                    print("-" * 30)
            else:
                print("No books available for borrowing.")
                
        elif choice == "3":
            isbn = input("Book ISBN: ")
            if library.borrow_book(isbn, member_id):
                print("Book borrowed successfully.")
            else:
                print("Error: Cannot borrow the book.")
                
        elif choice == "4":
            isbn = input("Book ISBN: ")
            if library.return_book(isbn, member_id):
                print("Book returned successfully.")
            else:
                print("Error: Cannot return the book.")
                
        elif choice == "2":
            query = input("Search term (title, author or ISBN): ")
            results = library.search_books(query)
            
            if results:
                print("\n=== Search Results ===")
                for book in results:
                    status = "Available" if book.is_available else "Borrowed"
                    print(f"Title: {book.title}")
                    print(f"Author: {book.author}")
                    print(f"Category: {book.category}")
                    print(f"ISBN: {book.isbn}")
                    print(f"Status: {status}")
                    print("-" * 30)
            else:
                print("No books found.")
                
        elif choice == "5":
            history = library.get_member_borrow_history(member_id)
            
            if history:
                print("\n=== Your Borrow History ===")
                for record in history:
                    print(f"Book Title: {record['book_title']}")
                    print(f"ISBN: {record['book_isbn']}")
                    print(f"Borrowed: {record['borrow_date']}")
                    if record['is_returned']:
                        print(f"Returned: {record['return_date']}")
                    else:
                        print("Status: Not returned yet")
                    print("-" * 30)
            else:
                print("No borrow history found.")
                
        elif choice == "4":
            break
            
        else:
            print("Invalid option. Please try again.")

def handle_librarian_mode(library):
    while True:
        print_librarian_menu()
        choice = input("Please select an option: ")
        
        if choice == "1":
            title = input("Book title: ")
            author = input("Author: ")
            category = input("Category: ")
            isbn = input("ISBN number: ")
            
            if library.add_book(title, author, category, isbn):
                print("Book added successfully.")
            else:
                print("Error: This ISBN is already registered.")
                
        elif choice == "2":
            isbn = input("Book ISBN to edit: ")
            title = input("New title (press Enter to skip): ").strip() or None
            author = input("New author (press Enter to skip): ").strip() or None
            category = input("New category (press Enter to skip): ").strip() or None
            
            if library.edit_book(isbn, title, author, category):
                print("Book information updated successfully.")
            else:
                print("Error: Book not found.")
                
        elif choice == "3":
            query = input("Search term (title, author or ISBN): ")
            results = library.search_books(query)
            
            if results:
                print("\n=== Search Results ===")
                for book in results:
                    status = "Available" if book.is_available else "Borrowed"
                    print(f"Title: {book.title}")
                    print(f"Author: {book.author}")
                    print(f"Category: {book.category}")
                    print(f"ISBN: {book.isbn}")
                    print(f"Status: {status}")
                    print("-" * 30)
            else:
                print("No books found.")
                
        elif choice == "4":
            overdue_books = library.get_overdue_books()
            
            if overdue_books:
                print("\n=== Overdue Books ===")
                for book in overdue_books:
                    print(f"Title: {book['book_title']}")
                    print(f"ISBN: {book['book_isbn']}")
                    print(f"Member Name: {book['member_name']}")
                    print(f"Member ID: {book['member_id']}")
                    print(f"Days Overdue: {book['days_overdue']}")
                    print("-" * 30)
            else:
                print("No overdue books.")
                
        elif choice == "5":
            stats = library.get_statistics()
            print("\n=== System Statistics ===")
            print(f"Total Books: {stats['total_books']}")
            print(f"Available Books: {stats['available_books']}")
            print(f"Borrowed Books: {stats['books_borrowed']}")
            print(f"Total Members: {stats['total_members']}")
            print(f"Active Members: {stats['active_members']}")
            
        elif choice == "6":
            handle_delete_book(library)
                
        elif choice == "7":
            members = library.get_all_members()
            if members:
                print("\n=== All Members ===")
                for member in members:
                    print(f"Name: {member['name']}")
                    print(f"Member ID: {member['member_id']}")
                    print(f"Contact: {member['contact']}")
                    print(f"Status: {'Active' if member['is_active'] else 'Inactive'}")
                    print(f"Currently Borrowed Books: {member['borrowed_books_count']}")
                    print("-" * 30)
            else:
                print("⚠ No members registered.")

        elif choice == "8":
            member_id = input("Enter member ID to edit: ")
            name = input("Enter new name (press Enter to skip): ").strip() or None
            contact = input("Enter new contact (press Enter to skip): ").strip() or None
            
            if library.edit_member(member_id, name, contact):
                print("Member information updated successfully.")
            else:
                print("Error: Member not found.")

        elif choice == "9":
            member_id = input("Enter member ID to delete: ")
            if library.delete_member(member_id):
                print("Member deleted successfully.")
            else:
                print("Error: Cannot delete member. They might have borrowed books or not exist.")

        elif choice == "10":
            member_id = input("Enter member ID: ")
            history = library.get_member_borrow_history(member_id)
            
            if history:
                print("\n=== Borrow History ===")
                for record in history:
                    print(f"Book Title: {record['book_title']}")
                    print(f"ISBN: {record['book_isbn']}")
                    print(f"Borrowed: {record['borrow_date']}")
                    if record['is_returned']:
                        print(f"Returned: {record['return_date']}")
                    else:
                        print("Status: Not returned yet")
                    print("-" * 30)
            else:
                print("No borrow history found.")
                
        elif choice == "11":
            top_borrowers = library.get_top_borrowers()
            if top_borrowers:
                print("\n=== Top Borrowers ===")
                for borrower in top_borrowers:
                    print(f"Name: {borrower['name']}")
                    print(f"Member ID: {borrower['member_id']}")
                    print(f"Total Borrows: {borrower['total_borrows']}")
                    print("-" * 30)
            else:
                print("No borrowing history available.")
                
        elif choice == "12":
            print("Goodbye!")
            break
            
        else:
            print("Invalid option. Please try again.")

def main():
    library = LibrarySystem()
    
    while True:
        print("\n=== Welcome to Library Management System ===")
        print("1. Login as Librarian")
        print("2. Login as Member")
        print("0. Exit")
        print("==========================")
        
        role_choice = input("Please select your role: ")
        
        if role_choice == "1":
            # Librarian mode with password
            password = input("Enter librarian password: ").strip()
            if password != LIBRARIAN_PASSWORD:
                print("Incorrect password. Access denied.")
                continue
            handle_librarian_mode(library)
        elif role_choice == "2":
            # Member mode
            member_id = input("Please enter your Member ID: ")
            if member_id in library.members:
                handle_member_mode(library, member_id)
            else:
                print("Error: Invalid Member ID")
        elif role_choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()