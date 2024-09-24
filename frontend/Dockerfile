# ใช้ Node.js เป็นฐาน
FROM node:20

# ตั้งค่า working directory
WORKDIR /app


# คัดลอกโค้ดทั้งหมดไปยัง container
COPY . .

RUN npm  install
# รันคำสั่ง build Vue
RUN npm run build

# ติดตั้ง serve เพื่อทำหน้าที่เสิร์ฟไฟล์
RUN npm install -g serve

# เปิดพอร์ต 80
EXPOSE 80

# ใช้ serve เพื่อเสิร์ฟไฟล์ build ของ Vue
CMD ["serve", "-s", "dist", "-l","80"]
