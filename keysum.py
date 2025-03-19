import spacy
from collections import Counter
import PyPDF2  # Để xử lý file PDF
import requests  # Để tải file PDF từ URL
from bs4 import BeautifulSoup  # Để xử lý nội dung HTML
import io  # Để sử dụng BytesIO
import argparse  # Để xử lý tham số dòng lệnh

# Tải mô hình ngôn ngữ của SpaCy
nlp = spacy.load("en_core_web_sm")

# Hàm đọc nội dung từ file PDF (tải cục bộ hoặc từ URL)
def read_text_from_pdf(file_path_or_url):
    try:
        # Kiểm tra nếu đường dẫn là URL
        if file_path_or_url.startswith("http"):
            response = requests.get(file_path_or_url)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            file = io.BytesIO(response.content)  # Chuyển bytes thành file-like object
        else:
            file = open(file_path_or_url, "rb")  # Mở file PDF cục bộ
        
        # Đọc nội dung file PDF
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        file.close()  # Đóng file nếu là file cục bộ
        return text.strip()
    except FileNotFoundError:
        print("File không tồn tại. Hãy kiểm tra lại đường dẫn.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Đã xảy ra lỗi khi tải URL: {e}")
        return None
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        return None

# Hàm tải và đọc nội dung từ URL HTML
def read_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        soup = BeautifulSoup(response.text, 'html.parser')
        # Trích xuất văn bản từ các thẻ <p>, <h1>, <h2>,...
        text = " ".join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])
        return text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Đã xảy ra lỗi khi tải URL: {e}")
        return None

# Hàm tiền xử lý văn bản (loại bỏ stop words)
def preprocess_text(text):
    doc = nlp(text)
    processed_text = " ".join([token.text for token in doc if token.is_alpha and not token.is_stop])
    return processed_text

# Hàm trích xuất cấu trúc Subject-Verb-Object (SVO)
def extract_svo(text):
    doc = nlp(text)
    svos = []
    for token in doc:
        if token.dep_ == "ROOT":  # Tìm động từ chính
            subjects = [w.text for w in token.lefts if w.dep_ in ("nsubj", "nsubjpass")]
            objects = [w.text for w in token.rights if w.dep_ in ("dobj", "pobj", "attr")]
            if subjects and objects:
                svos.append((subjects[0], token.text, objects[0]))
    return svos

# Hàm trích xuất từ khóa dựa trên tần suất
def extract_keywords(text, top_n=10):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    keyword_freq = Counter(keywords)
    return keyword_freq.most_common(top_n)

# Hàm hiển thị "map keyword" (bản đồ từ khóa)
def create_keyword_map(keywords, svos):
    keyword_map = {}
    for keyword, _ in keywords:
        keyword_map[keyword] = {
            "related_svos": [svo for svo in svos if keyword in svo]
        }
    
    print("\n=== Bản đồ từ khóa ===")
    for keyword, data in keyword_map.items():
        print(f"- Từ khóa: {keyword}")
        if data["related_svos"]:
            for svo in data["related_svos"]:
                print(f"  + SVO liên quan: {svo}")
        else:
            print("  + Không có SVO liên quan.")

# Hàm tóm tắt nội dung
def summarize_text(text):
    print("\n=== Bắt đầu xử lý văn bản ===\n")
    processed_text = preprocess_text(text)
    svos = extract_svo(text)
    keywords = extract_keywords(processed_text)

    print("Từ khóa nổi bật:")
    for word, freq in keywords:
        print(f"- {word}: xuất hiện {freq} lần")

    print("\nCấu trúc SVO:")
    for subject, verb, obj in svos:
        print(f"- Chủ ngữ: {subject} → Động từ: {verb} → Tân ngữ: {obj}")

    print("\nTóm tắt:")
    key_elements = ", ".join([kw[0] for kw in keywords])
    print(f"Văn bản này nói về các yếu tố chính như: {key_elements}.")

    # Gọi hàm tạo bản đồ từ khóa
    create_keyword_map(keywords, svos)

# Chương trình chính
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and summarize a text from PDF or URL.")
    parser.add_argument("file_path_or_url", help="Path to the PDF file or URL")
    args = parser.parse_args()

    file_path_or_url = args.file_path_or_url

    # Kiểm tra xem là URL HTML hay file PDF (URL hoặc cục bộ)
    if file_path_or_url.startswith("http") and file_path_or_url.endswith(".pdf"):
        text = read_text_from_pdf(file_path_or_url)  # Link PDF
    elif file_path_or_url.startswith("http"):
        text = read_text_from_url(file_path_or_url)  # Link HTML
    elif file_path_or_url.endswith(".pdf"):
        text = read_text_from_pdf(file_path_or_url)  # File PDF cục bộ
    else:
        print("Định dạng không được hỗ trợ.")
        text = None

    # Nếu đọc nội dung thành công, xử lý và tóm tắt văn bản
    if text:
        summarize_text(text)