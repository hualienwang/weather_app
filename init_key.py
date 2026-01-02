from database import init_db, create_api_key

if __name__ == "__main__":
    init_db()
    key = create_api_key("admin")
    print(f"\n✅ 你的測試 API Key:\n{key}\n")