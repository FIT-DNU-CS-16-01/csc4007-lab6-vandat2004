from google import genai

# DÁN API KEY MỚI CỦA BẠN VÀO ĐÂY
API_KEY = ""

try:
    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Xin chào Gemini! Hãy trả lời một câu ngắn."
    )

    print("=== KẾT QUẢ ===")
    print(response.text)

except Exception as e:
    print("=== LỖI ===")
    print(e)