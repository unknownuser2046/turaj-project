import datetime
import pickle
from typing import List, Dict, Optional

class Book:
    def __init__(self, title: str, author: str, category: str, isbn: str):
        self.title = title
        self.author = author
        self.category = category
        self.isbn = isbn
        self.is_available = True

class Member:
    def __init__(self, name: str, member_id: str, contact: str):
        self.name = name
        self.member_id = member_id
        self.contact = contact
        self.borrowed_books: List[str] = []  # List of ISBN numbers
        self.is_active = True

class BorrowRecord:
    def __init__(self, book_isbn: str, member_id: str):
        self.book_isbn = book_isbn
        self.member_id = member_id
        self.borrow_date = datetime.datetime.now()
        self.return_date: Optional[datetime.datetime] = None

class LibrarySystem:
    def __init__(self):
        self.books: Dict[str, Book] = {}  # ISBN -> Book
        self.members: Dict[str, Member] = {}  # member_id -> Member
        self.borrow_records: List[BorrowRecord] = []
        self.load_data()

    def load_data(self):
        try:
            with open('library_data.pkl', 'rb') as f:
                data = pickle.load(f)
                self.books = data['books']
                self.members = data['members']
                self.borrow_records = data['borrow_records']
        except FileNotFoundError:
            pass

    def save_data(self):
        data = {
            'books': self.books,
            'members': self.members,
            'borrow_records': self.borrow_records
        }
        with open('library_data.pkl', 'wb') as f:
            pickle.dump(data, f)

    def add_book(self, title: str, author: str, category: str, isbn: str) -> bool:
        if isbn in self.books:
            return False
        self.books[isbn] = Book(title, author, category, isbn)
        self.save_data()
        return True

    def add_member(self, name: str, member_id: str, contact: str) -> bool:
        if member_id in self.members:
            return False
        self.members[member_id] = Member(name, member_id, contact)
        self.save_data()
        return True

    def edit_member(self, member_id: str, name: str = None, contact: str = None) -> bool:
        if member_id not in self.members:
            return False
        member = self.members[member_id]
        if name:
            member.name = name
        if contact:
            member.contact = contact
        self.save_data()
        return True

    def delete_member(self, member_id: str) -> bool:
        if member_id not in self.members:
            return False
        member = self.members[member_id]
        if member.borrowed_books:  # Can't delete member with borrowed books
            return False
        del self.members[member_id]
        self.save_data()
        return True

    def get_member_borrow_history(self, member_id: str) -> List[Dict]:
        if member_id not in self.members:
            return []
        history = []
        for record in self.borrow_records:
            if record.member_id == member_id:
                book = self.books[record.book_isbn]
                history.append({
                    'book_title': book.title,
                    'book_isbn': book.isbn,
                    'borrow_date': record.borrow_date,
                    'return_date': record.return_date,
                    'is_returned': record.return_date is not None
                })
        return history

    def get_all_members(self) -> List[Dict]:
        return [{
            'member_id': member.member_id,
            'name': member.name,
            'contact': member.contact,
            'is_active': member.is_active,
            'borrowed_books_count': len(member.borrowed_books)
        } for member in self.members.values()]

    def get_top_borrowers(self, limit: int = 5) -> List[Dict]:
        members_with_counts = [{
            'member_id': member.member_id,
            'name': member.name,
            'total_borrows': len([r for r in self.borrow_records if r.member_id == member.member_id])
        } for member in self.members.values()]
        
        return sorted(members_with_counts, key=lambda x: x['total_borrows'], reverse=True)[:limit]

    def borrow_book(self, isbn: str, member_id: str) -> bool:
        if isbn not in self.books or member_id not in self.members:
            return False
        
        book = self.books[isbn]
        member = self.members[member_id]
        
        if not book.is_available or not member.is_active:
            return False
            
        book.is_available = False
        member.borrowed_books.append(isbn)
        self.borrow_records.append(BorrowRecord(isbn, member_id))
        self.save_data()
        return True

    def return_book(self, isbn: str, member_id: str) -> bool:
        if isbn not in self.books or member_id not in self.members:
            return False
            
        book = self.books[isbn]
        member = self.members[member_id]
        
        if isbn not in member.borrowed_books:
            return False
            
        book.is_available = True
        member.borrowed_books.remove(isbn)
        
        # Update borrow record
        for record in self.borrow_records:
            if record.book_isbn == isbn and record.member_id == member_id and not record.return_date:
                record.return_date = datetime.datetime.now()
                break
                
        self.save_data()
        return True

    def get_overdue_books(self, days_threshold: int = 14) -> List[Dict]:
        overdue_books = []
        current_time = datetime.datetime.now()
        
        for record in self.borrow_records:
            if not record.return_date:  # Book hasn't been returned
                days_borrowed = (current_time - record.borrow_date).days
                if days_borrowed > days_threshold:
                    book = self.books[record.book_isbn]
                    member = self.members[record.member_id]
                    overdue_books.append({
                        'book_title': book.title,
                        'book_isbn': book.isbn,
                        'member_name': member.name,
                        'member_id': member.member_id,
                        'days_overdue': days_borrowed - days_threshold
                    })
        
        return overdue_books

    def search_books(self, query: str) -> List[Book]:
        query = query.lower()
        return [book for book in self.books.values()
                if query in book.title.lower() or
                   query in book.author.lower() or
                   query in book.isbn.lower()]

    def find_book_by_title(self, title: str) -> Optional[str]:
        title = title.lower()
        for isbn, book in self.books.items():
            if book.title.lower() == title:
                return isbn
        return None

    def find_book_by_author_and_title(self, author: str, title: str) -> Optional[str]:
        author = author.lower()
        title = title.lower()
        for isbn, book in self.books.items():
            if book.author.lower() == author and book.title.lower() == title:
                return isbn
        return None

    def delete_book_by_title(self, title: str) -> bool:
        isbn = self.find_book_by_title(title)
        if isbn:
            return self.delete_book(isbn)
        return False

    def delete_book_by_author_and_title(self, author: str, title: str) -> bool:
        isbn = self.find_book_by_author_and_title(author, title)
        if isbn:
            return self.delete_book(isbn)
        return False

    def delete_book(self, isbn: str) -> bool:
        if isbn not in self.books:
            return False
            
        # Check if book is currently borrowed
        if not self.books[isbn].is_available:
            return False
            
        # Delete the book
        del self.books[isbn]
        self.save_data()
        return True

    def get_statistics(self) -> Dict:
        total_books = len(self.books)
        available_books = sum(1 for book in self.books.values() if book.is_available)
        total_members = len(self.members)
        active_members = sum(1 for member in self.members.values() if member.is_active)
        books_borrowed = total_books - available_books
        
        return {
            'total_books': total_books,
            'available_books': available_books,
            'books_borrowed': books_borrowed,
            'total_members': total_members,
            'active_members': active_members
        }