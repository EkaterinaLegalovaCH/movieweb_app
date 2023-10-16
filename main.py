from DataManager.json_data_manager import JSONDataManager

def main():
    data_manager = JSONDataManager("data/data.json")
    all_users = data_manager.get_all_users()
    print(all_users)
    movies_by_user = data_manager.get_user_movies('1')
    print(movies_by_user)
    data_manager.add_user_movie('1')


if __name__ == "__main__":
    main()
