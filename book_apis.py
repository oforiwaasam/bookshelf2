import requests
import datetime


# ----------Open Library Books API---------- #

# searching book info by ISBN number
def ol_isbn(isbn):
    book_dic = {}
    result = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:' +
                          isbn + '&jscmd=data&format=json')
    result_json = result.json()

#     print(result_json)
    data = result_json['ISBN:' + isbn]
    book_title = data['title']
#     print('Book title: ' + book_title)

    authors_str = ''
    authors_list = []
    author_key = 'authors'
    if author_key in data:
        for author in data['authors']:
            authors_str += author['name'] + ', '
            authors_list.append(author['name'])
        size = len(authors_str)
        authors = authors_str[:size - 2]

#         print('Author(s): ' + authors)

    else:
        authors = 'Information on author(s) not available!'
        authors_list.append("Unknown")
#         print(authors)
#     print(data)
    url = data['url']
    cover_key = 'cover'
    if cover_key in data:
        cover_url = data['cover']['large']
    else:
        cover_url = 'No cover picture available!'
#     print(book_title, authors_list, cover_url)
    authors_list = ''.join(authors_list)
    book_dic[cover_url] = [book_title, authors_list, url, isbn]
    return book_dic


# searching book info by book name
def ol_book_names(book):
    result = requests.get('http://openlibrary.org/search.json?q=' + book)
    result_json = result.json()
#     print('First 20 results for ' + book)
#     print('---------------------' + '-' * len(book))
    books_dic = {}
    num_books = 0
    for book in result_json['docs']:
        # print(book)
        num_books += 1
        key = 'isbn'
        if key in book:
            if len(book['isbn']) > 1:
                book_isbn = book['isbn'][1]
            else:
                book_isbn = book['isbn'][0]

            # get book info using its isbn
#             print('ISBN Number: ' + book_isbn)
            results = ol_isbn(book_isbn)
            books_dic.update(results)
#             books_dic[results[2]]= [results[0],results[1], results[3]]           
#             print(results)
#         else:
#             print('Information about book not available!')
        if num_books == 3:
            break
    # print(result_json)
    return books_dic


# searching book info for books written by specified author
def ol_authors(author):
    books_dic={}
    result = requests.get('https://openlibrary.org/search/authors.json?q=' +
                          author)
    result_json = result.json()
    num_found = result_json['numFound']
    if num_found == 1:
        ol_id = result_json['docs'][0]['key']
        books = requests.get('https://openlibrary.org/authors/' + ol_id +
                             '/works.json')
        books_json = books.json()
        list_of_books = []
        for book in books_json['entries']:
            list_of_books.append(book['title'])
            books_dic[book['title']] = [book['title'], author, None, None]
            print('Below are the books written by ' + author + ': ')

            # later transform this so that the brackets don't appear
            print(list_of_books)

    else:

        # figure out how to make sure that authors for whose names could be
        # written differently do not fall in this else statement

        print("Please enter the exact name of the author! Options below!!!")
        authors = ""
        for author in result_json['docs']:
            authors+= author['text'][1]
        return 1, authors
        
    return 0, books_dic
    


# search book info by work or book Open Library ID
def ol_work_id(book_ol_id):
    books_dic={}
    result = requests.get('https://openlibrary.org' + book_ol_id + '.json')
    result_json = result.json()
    # print(result_json)
    results = ol_book_names(result_json['title'])
    books_dic.update(results)
    return books_dic


# search book info for books on subject provided
def ol_subjects(subject):
    begin_time = datetime.datetime.now()
    subject = subject.lower()
    books_dic={}
    result = requests.get('https://openlibrary.org/subjects/' + subject + '.json')
    result_json = result.json()
    # print(result_json)
    num_books = 0
    for work in result_json['works']:
        # print(work)
        num_books += 1
        results = ol_work_id(work['key'])
        books_dic.update(results)
        if num_books == 5:
            break
    print(datetime.datetime.now() - begin_time)
    return books_dic

# # get ISBN
# def get_ISBN(book):
#     result = requests.get('http://openlibrary.org/search.json?q=' + book)
#     result_json = result.json()
# #     print('First 20 results for ' + book)
# #     print('---------------------' + '-' * len(book))
#     num_books = 0
#     for book in result_json['docs']:
#         # print(book)
#         num_books += 1
#         key = 'isbn'
#         if key in book:
#             if len(book['isbn']) > 1:
#                 book_isbn = book['isbn'][1]
#             else:
#                 book_isbn = book['isbn'][0]

#             # get book info using its isbn
#             print('ISBN Number: ' + book_isbn)
#         if num_books == 20:
#             break

#     return book_isbn

# main function to test my individual functions
def main():
#     # everything in main was used to test if functions work well
    isbn = '9780980200447'
#     mill_isbn = '9780199670802'
#     data_structures = '9780132576277'
#     aquarium = '9780793820788'
#     petit_pays = '9782246857334'
#     buildings = '9781564588852'
    cinderella_murder = '9781476763699'
    
#     blackout = '9781982133276'
#     weird = '9780563533603'  # no info on author
#     ol_books(data_structures)
    
#     # results = ol_isbn(blackout)
#     # print(results)

#     author = 'Ahmed Manan'
    author = "Sam"
    print(ol_authors(author))

#     manan_book = 'Where the wild frontiers are'
#     data_structures_book = 'Data Structures and Algorithm Analysis in Java'
#     faye = 'Petit Pays'
# #     ol_book_names(manan_book)

#     # look into how to make the following functions work efficiently
# #     ol_subjects()
# #     ol_work_id()

#     ahmed_manan_book_ol_id = '/works/OL16563824W'
#     # ol_work_id(ahmed_manan_book_ol_id)

#     burundi_subject = 'burundi'
#     ol_subjects(burundi_subject)

#     print(ol_isbn(isbn))
#     print(ol_book_names("cinderella_murder"))print(ol_authors("Manan Ahmed Asif"))
#     print(ol_authors("Ahmed"))
#     print(ol_authors("Manan Ahmed Asif"))
#     print(ol_work_id("cinderella_murder"))
#     print(ol_subjects("Math"))


if __name__ == "__main__":
    main()

