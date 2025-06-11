from library import LibrarySystem

def print_menu():
    print("\n=== Library Management System ===")
    print("1. Add New Book")
    print("2. Add New Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Search Book")
    print("6. Show Overdue Books")
    print("7. Show Statistics")
    print("8. Delete Book")
    print("9. View All Members")
    print("10. Edit Member")
    print("11. Delete Member")
    print("12. View Member's Borrow History")
    print("13. View Top Borrowers")
    print("0. Exit")
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
                print("✓ Book deleted successfully.")
            else:
                print("⚠ Error: Book cannot be deleted. It might be borrowed or not exist.")
            break
            
        elif choice == "2":
            title = input("Enter book title to delete: ")
            if library.delete_book_by_title(title):
                print("✓ Book deleted successfully.")
            else:
                print("⚠ Error: Book cannot be deleted. It might be borrowed or not exist.")
            break
            
        elif choice == "3":
            author = input("Enter book author: ")
            title = input("Enter book title: ")
            if library.delete_book_by_author_and_title(author, title):
                print("✓ Book deleted successfully.")
            else:
                print("⚠ Error: Book cannot be deleted. It might be borrowed or not exist.")
            break
            
        elif choice == "0":
            break
            
        else:
            print("⚠ Invalid option. Please try again.")

def main():
    library = LibrarySystem()
    
    while True:
        print_menu()
        choice = input("Please select an option: ")
        
        if choice == "1":
            title = input("Book title: ")
            author = input("Author: ")
            category = input("Category: ")
            isbn = input("ISBN number: ")
            
            if library.add_book(title, author, category, isbn):
                print("✓ Book added successfully.")
            else:
                print("⚠ Error: This ISBN is already registered.")
                
        elif choice == "2":
            name = input("Member name: ")
            member_id = input("Membership number: ")
            contact = input("Contact information: ")
            
            if library.add_member(name, member_id, contact):
                print("✓ New member registered successfully.")
            else:
                print("⚠ Error: This membership number is already registered.")
                
        elif choice == "3":
            isbn = input("Book ISBN: ")
            member_id = input("Membership number: ")
            
            if library.borrow_book(isbn, member_id):
                print("✓ Book borrowed successfully.")
            else:
                print("⚠ Error: Cannot borrow the book.")
                
        elif choice == "4":
            isbn = input("Book ISBN: ")
            member_id = input("Membership number: ")
            
            if library.return_book(isbn, member_id):
                print("✓ Book returned successfully.")
            else:
                print("⚠ Error: Cannot return the book.")
                
        elif choice == "5":
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
                print("⚠ No books found.")
                
        elif choice == "6":
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
                print("✓ No overdue books.")
                
        elif choice == "7":
            stats = library.get_statistics()
            print("\n=== System Statistics ===")
            print(f"Total Books: {stats['total_books']}")
            print(f"Available Books: {stats['available_books']}")
            print(f"Borrowed Books: {stats['books_borrowed']}")
            print(f"Total Members: {stats['total_members']}")
            print(f"Active Members: {stats['active_members']}")
            
        elif choice == "8":
            handle_delete_book(library)
                
        elif choice == "9":
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

        elif choice == "12":
            member_id = input("Enter member ID to edit: ")
            name = input("Enter new name (press Enter to skip): ").strip() or None
            contact = input("Enter new contact (press Enter to skip): ").strip() or None
            
            if library.edit_member(member_id, name, contact):
                print("✓ Member information updated successfully.")
            else:
                print("⚠ Error: Member not found.")

        elif choice == "13":
            member_id = input("Enter member ID to delete: ")
            if library.delete_member(member_id):
                print("✓ Member deleted successfully.")
            else:
                print("⚠ Error: Cannot delete member. They might have borrowed books or not exist.")

        elif choice == "14":
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
                print("⚠ No borrow history found for this member.")

        elif choice == "15":
            top_borrowers = library.get_top_borrowers()
            if top_borrowers:
                print("\n=== Top Borrowers ===")
                for i, borrower in enumerate(top_borrowers, 1):
                    print(f"{i}. Name: {borrower['name']}")
                    print(f"   Member ID: {borrower['member_id']}")
                    print(f"   Total Books Borrowed: {borrower['total_borrows']}")
                    print("-" * 30)
            else:
                print("⚠ No borrowing history available.")
                
        elif choice == "0":
            print("Exiting program...")
            break
            
        else:
            print("⚠ Invalid option. Please try again.")

if __name__ == "__main__":
    main()