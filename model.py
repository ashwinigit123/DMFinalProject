import pandas as pd

def newRecommendations_50(title):
    ratings=pd.read_csv('/home/ashwinitrale8/mysite/ratings.csv')
    books = pd.read_csv('/home/ashwinitrale8/mysite/books.csv')
    books = books.filter(['book_id', 'authors', 'original_title', 'title',
                             'average_rating'])
    train=pd.merge(books,ratings)

    userRatings = train.pivot_table(index=['user_id'],columns=['title'],values='rating')

    userRatings=userRatings.dropna(thresh=10,axis=1).fillna(0)

    corrMatrix50 = userRatings.corr(method = 'pearson', min_periods = 50)
    bookRating = corrMatrix50[[title]][:]
    bookRating = bookRating.dropna()
    df = pd.DataFrame(bookRating.sort_values(by = title, ascending = False))[1:]
    return df.head(1)
if __name__ == '__main__':
    print(newRecommendations_50(["Harry Potter and the Order of the Phoenix (Harry Potter, #5)"]))
    # text = "you are super good"
    # sentence = map(nltk.word_tokenize, text)
    # sentence = filter(lambda lst: lst, sentence)
    # print(sentence)
    # print(sklearn.__version__ )
