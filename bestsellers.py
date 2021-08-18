import os
import requests
import json
from dotenv import load_dotenv
load_dotenv() # running this will create environment variables

api_key = os.getenv('api_key')
print(type(api_key))

def bestsellers_category():
  #api_key = os.getenv('api_key')
  url = f"https://api.nytimes.com/svc/books/v3/lists/names.json?&api-key={api_key}"
  #print(url) don't print url (remember you're trying to hide it)
  response = requests.get(url)
  print(response)
  results = response.json()['results']
  print(results)
#   for name_dict in results:
#     print(name_dict['list_name'] + ': ' + name_dict['list_name_encoded'])
  

def select_category(user_input):
#   user_input = input('Enter a book category: ')

  url = 'https://api.nytimes.com/svc/books/v3/lists/current/' + user_input + '.json?&api-key=' + api_key

  output = requests.get(url)
  data = output.json()
  print(data['results']['books'])
  entire_book_dic= {}
  for book in data['results']['books']:
    rank = book['rank']
    isbn10 = book['primary_isbn10']
    isbn13 = book['primary_isbn13']
    publisher = book['publisher']
    title = book['title']
    author = book['author']
    book_image = book['book_image']
    product_url = book['amazon_product_url']
    buy_links = book['buy_links']
    entire_book_dic[book_image] = [title, author, product_url, isbn13]
  return entire_book_dic

#     print(rank, isbn10, isbn13, publisher, title, author, book_image, buy_links)
    
    
def homepage_bestsellers():
  homepage_url = 'https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?&api-key=' + api_key
  response = requests.get(homepage_url)
  book_list = response.json()
  entire_book_dic = {}
  book_dic = {}
  count = 0
  home_book_lst = []
  for book in book_list['results']['books']:
#     print(count)
    if(count==3):
        count=0
        home_book_lst.append(book_dic)
        book_dic={}
    rank = book['rank']
    isbn10 = book['primary_isbn10']
    isbn13 = book['primary_isbn13']
    publisher = book['publisher']
    title = book['title']
    author = book['author']
    book_image = book['book_image']
    product_url = book['amazon_product_url']
    buy_links = book['buy_links'] 
    book_dic[book_image] = [title, author, product_url]
    entire_book_dic[book_image] = [title, author, product_url, isbn13]
    count+=1
#   print(book_list['results']['books'])
#   print(book_dic)
  return home_book_lst,entire_book_dic

def main():
    bestsellers_category()
#   homepage_bestsellers()
#   data = homepage_bestsellers()
#   for key,value in data[0].items():
#         print(value[2][0]['url']) #gets url
#         print(key)#gets cover
#   print(data[0])
  
if __name__ == "__main__":
  main()

