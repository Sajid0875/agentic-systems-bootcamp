class Library:
    def __init__(self, books):
        self.books = books

    def __len__(self):
        return len(self.books)

    def __getitem__(self, index):
        return self.books[index]

    def __iter__(self):
        return iter(self.books)


library = Library([
    "Python",
    "FastAPI",
    "LangGraph"
])

print(len(library))
print(library[1])

for book in library:
    print(book)