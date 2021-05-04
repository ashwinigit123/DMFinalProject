import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


def recommendBooks(title):
    books = pd.read_csv('/home/ashwinitrale8/mysite/books.csv')
    ratings = pd.read_csv('/home/ashwinitrale8/mysite/ratings.csv')

    ratings = ratings.sort_values("user_id")
    ratings.drop_duplicates(subset =["user_id","book_id"], keep = False, inplace = True)

    books= books.drop(columns=['best_book_id', 'work_id', 'isbn', 'isbn13', 'title','work_ratings_count',
                                   'work_text_reviews_count', 'ratings_1', 'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5',
                                    'image_url','small_image_url'])
    books = books.dropna()
    books.drop_duplicates(subset='original_title',keep=False,inplace=True)

    train = pd.merge(books, ratings)
    train =  train.sort_values('book_id', ascending=True)

    userRatings = train.pivot_table(index=['user_id'],columns=['original_title'],values='rating')
    userRatings = userRatings.dropna(thresh=10,axis=1).fillna(0)

    bookRatings = train.dropna(axis = 0, subset = ['original_title'])
    BookratingCount = (bookRatings.
         groupby(by = ['original_title'])['rating'].
         count().
         reset_index().
         rename(columns = {'rating': 'totalRatingCount'})
         [['original_title', 'totalRatingCount']]
        )

    rating_with_totalRatingCount = bookRatings.merge(BookratingCount, left_on = 'original_title', right_on = 'original_title', how = 'left')
    minPopularitythreshold = 50
    popularBooks= rating_with_totalRatingCount.query('totalRatingCount >= @minPopularitythreshold')

    userBookRating=popularBooks.pivot_table(index='original_title',columns='user_id',values='rating').fillna(0)

    userBookRatingMatrix = csr_matrix(userBookRating.values)
    knnModel = NearestNeighbors(algorithm='auto', metric = 'cosine',n_neighbors=5)
    knnModel.fit(userBookRatingMatrix)

    if title in train.values:
        query_index = userBookRating.index.get_loc(title)
        distances, indices = knnModel.kneighbors(userBookRating.iloc[query_index,:].values.reshape(1, -1), n_neighbors= 8)

        recommended_books = []
        for x in range(1,6):
            bookrecommended = [userBookRating.index[indices.flatten()[x]], distances.flatten()[x]]
            recommended_books.append(bookrecommended)
        recommended_books = [recommended_books]
        return recommended_books
    else :
        err =[]
        err.append("\nSorry we do not have a recommendation for you")
        errmsg =[]
        errmsg.append(err)
        return errmsg

if __name__ == '__main__':
    print(recommendBooks(["A Time to Kill"]))

