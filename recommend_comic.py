import pandas as pd
from models import get_user_history_reading, get_all_genres, get_all_comic_genres

# Gợi ý manga dựa trên thể loại người dùng thường đọc
def calculate_comic_suggestions(user_id, user_preferences, comic_df, top_n=6):
    user_pref = user_preferences.loc[user_id]
    comic_df['score'] = comic_df.dot(user_pref)
    recommended_comic = comic_df.sort_values(by='score', ascending=False)
    return recommended_comic

def recommend_comic(user_id): 
    data = get_user_history_reading(user_id)
    all_genres = get_all_genres()
    all_comic = get_all_comic_genres()

    # Tạo DataFrame từ dữ liệu
    comic_df = pd.DataFrame(all_comic)
    if data is None or len(data) == 0:
        genre_count_df = pd.DataFrame(0, index=[user_id], columns=all_genres)
    else:    
        df = pd.DataFrame(data)
        print(df)
        # Tạo DataFrame mới với index là các user_id và các cột là tất cả các genre_id, ban đầu có giá trị 0
        genre_count_df = pd.DataFrame(0, index=df['user_id'].unique(), columns=all_genres)

        # Đếm số lần xuất hiện của mỗi genre_id cho mỗi user_id
        for user_id, sub_df in df.groupby('user_id'):
            counts = sub_df['genre_id'].value_counts()
            genre_count_df.loc[user_id, counts.index] = counts.values

    # Tạo DataFrame mới với index là các comicbook_id và các cột là tất cả các genre_id, ban đầu có giá trị 0
    genre_count_comic_df = pd.DataFrame(0, index=comic_df['comicbook_id'].unique(), columns=all_genres)

    #Đánh dấu xuất hiện thể loại truyện cho từng comic
    for comicbook_id, sub_df in comic_df.groupby('comicbook_id'):
        counts = sub_df['genre_id'].value_counts()
        genre_count_comic_df.loc[comicbook_id, counts.index] = counts.values

    recommendations = calculate_comic_suggestions(user_id, genre_count_df, genre_count_comic_df)

    # Loại bỏ các truyện đã đọc khỏi danh sách đề xuất
    read_comics = set(df['comic_id'])
    recommendations = recommendations[~recommendations.index.isin(read_comics)].head(6)

    print(recommendations)

    return recommendations.index.tolist()