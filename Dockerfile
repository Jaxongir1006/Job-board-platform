# 1. Image
FROM python:3.13.5-slim

# 2. Workdir
WORKDIR /app

# 3. Faqat requirements.txt ni avval nusxalash
COPY requirements.txt .

# 4. Pip install (bu qatorda o‘zgarish bo‘lmasa, cache ishlaydi)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Keyin qolgan fayllarni ko‘chirish
COPY . .

# 6. Port ochish (optional)
EXPOSE 8000

# 7. Command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
