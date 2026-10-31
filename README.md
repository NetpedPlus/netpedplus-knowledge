# netpedplus-knowledge (private)

ความรู้ (playbook) สำหรับ AI ในโปรแกรม NetPED+ — Hermes เขียน, Claude ตรวจ, Hermes merge หลัง Claude ให้ผ่าน

## วิธีทำงาน
1. **เลือกงาน**: ดู `TODO.md` แก้สถานะเป็น `กำลังทำ (Hermes)` ใน branch ของงานนั้น
2. **Hermes**: สร้าง branch `pb/<ชื่อเรื่อง>` → เขียนไฟล์ใน `playbooks/` ตาม `GUIDE.md`
   → รัน `python tools/check_playbook.py` ต้องไม่มี ERROR → push → เปิด Pull Request (กรอกแม่แบบให้ครบ)
3. **Claude**: ตรวจเฉพาะไฟล์ที่เปลี่ยนใน PR (diff) + สุ่มเทียบคำสั่งกับ URL ในตาราง → คอมเมนต์ใน PR (ไม่ merge เอง)
4. **Hermes merge เอง** ได้เฉพาะเมื่อ: คอมเมนต์ล่าสุดของ Claude ใน PR ขึ้นต้นด้วย "ผ่าน พร้อม merge" **และ** ไม่มี commit ใหม่หลังคอมเมนต์นั้น (มี commit ใหม่ = ต้องให้ Claude ตรวจอีกรอบ)
   → merge แบบ squash → อัปเดต `CHANGELOG.md` → NetPED+ ดึงเองวันละครั้ง / กด "อัปเดตความรู้"

## ใช้กับ NetPED+
โฟลเดอร์ `playbooks/` ของ repo นี้ = `<DATA_DIR>/playbooks/` (ลิงก์ครั้งเดียว แล้ว `git pull` ก็ได้ของใหม่)
- Mac: `ln -s ~/git/netpedplus-knowledge/playbooks ~/NetPEDPlus/playbooks` (ย้ายโฟลเดอร์เดิมออกก่อนถ้ามี)
- Windows (cmd): `mklink /J "%LOCALAPPDATA%\Programs\NetPEDPlus\playbooks" "C:\git\netpedplus-knowledge\playbooks"`

## ห้าม
- ข้อมูลลูกค้า (IP, hostname, config, ชื่อหน่วยงาน, รหัส) / คู่มือ PDF ของผู้ผลิต / ไฟล์ `.netpedkb` / กุญแจ หรือ token
- แก้ไฟล์ของ playbook ที่มากับโปรแกรม (ทำไฟล์ใหม่แทน)

## ประหยัด token ของ Claude
- PR ละ 1 เรื่อง (1 ไฟล์ หรือไม่กี่หัวข้อ) / ตารางคำสั่ง → URL ครบในคำอธิบาย PR / ผล `check_playbook.py` แปะใน PR
- ไม่ต้องให้ Claude อ่านทั้ง repo — ส่งแค่เลข PR
