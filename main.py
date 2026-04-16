import os
import io
import fitz  # PyMuPDF
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from PIL import Image
from typing import Optional

app = FastAPI()

# Cấp phép CORS cho frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prompt chung cho cả Gemini và OpenAI
TRANSLATE_PROMPT = """
Bạn là một chuyên gia dịch thuật và phân tích tài liệu chuyên nghiệp. 
Hãy dịch toàn bộ nội dung trong trang tài liệu này sang tiếng Việt, giữ nguyên vẹn cấu trúc và ý nghĩa.

YÊU CẦU QUAN TRỌNG VỀ ĐỊNH DẠNG (MARKDOWN & TOÁN HỌC):
1. Sử dụng chuẩn Markdown cho tiêu đề, danh sách, in đậm, in nghiêng, và bảng biểu.
2. CÔNG THỨC TOÁN HỌC (BẮT BUỘC):
   - Công thức Toán học trên dòng riêng (block math): BẮT BUỘC sử dụng ký hiệu `$$` bao quanh. Ký hiệu `$$` phải nằm cùng dòng với block math hoặc riêng biệt. TUYỆT ĐỐI KHÔNG dùng `\\\\[` và `\\\\]`.
   - Công thức Toán học xen trong chữ (inline math): BẮT BUỘC sử dụng ký hiệu `$` bao quanh. TUYỆT ĐỐI KHÔNG dùng `\\\\(` và `\\\\)`.
3. CODE BLOCK: Sử dụng 3 dấu backticks để khoanh vùng khối mã.
4. BẮT BUỘC KHÔNG giải thích, KHÔNG thêm câu mở đầu. CHỈ trả về đúng nội dung đã dịch và định dạng.
"""

def extract_page_as_image(pdf_bytes: bytes, page_number: int) -> Image.Image:
    """Cắt 1 trang PDF và chuyển thành ảnh PIL."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    if page_number < 0 or page_number >= len(doc):
        raise ValueError("Số trang không hợp lệ")
        
    page = doc.load_page(page_number)
    # Tăng độ phân giải ảnh (zoom) để AI đọc text rõ hơn
    zoom = 2.0 
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # Chuyển đổi sang PIL Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img


def translate_with_gemini(img: Image.Image, api_key: str, model_name: str) -> str:
    """Dịch bằng Google Gemini API."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content([TRANSLATE_PROMPT, img])
    return response.text


def translate_with_openai(img: Image.Image, api_key: str, model_name: str) -> str:
    """Dịch bằng OpenAI GPT API (gpt-4o, gpt-4-vision, ...)."""
    import openai
    import base64

    # Chuyển ảnh sang base64
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": TRANSLATE_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=4096
    )
    return response.choices[0].message.content


# Default values (fallback nếu frontend không gửi)
DEFAULT_API_KEY = "xxx"
DEFAULT_MODEL_GEMINI = "gemini-2.5-flash"
DEFAULT_MODEL_OPENAI = "gpt-4o"


@app.post("/translate-page/")
async def translate_page(
    file: UploadFile = File(...), 
    page_number: int = Form(...),
    provider: str = Form("gemini"),
    model_name: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None),
):
    try:
        # Đọc file PDF
        pdf_bytes = await file.read()
        
        # Trích xuất trang cụ thể thành ảnh
        img = extract_page_as_image(pdf_bytes, page_number - 1)
        
        if provider == "openai":
            # OpenAI GPT
            key = api_key or os.environ.get("OPENAI_API_KEY", "")
            model = model_name or DEFAULT_MODEL_OPENAI
            if not key:
                return JSONResponse(status_code=400, content={
                    "success": False, 
                    "error": "Vui lòng nhập OpenAI API Key!"
                })
            translated = translate_with_openai(img, key, model)
        else:
            # Google Gemini (default)
            key = api_key or os.environ.get("GEMINI_API_KEY", DEFAULT_API_KEY)
            model = model_name or DEFAULT_MODEL_GEMINI
            translated = translate_with_gemini(img, key, model)
        
        return JSONResponse(content={
            "success": True,
            "translated_markdown": translated,
            "page": page_number,
            "provider": provider,
            "model": model
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
