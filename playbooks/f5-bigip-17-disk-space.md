---
id: f5-bigip-17-disk-space
title: F5 BIG-IP 17.x — ตรวจพื้นที่ดิสก์ (diskmonitor)
families: f5_tmsh
triggers: disk space, diskmonitor, 011d0004, 011d005, 011d004, พื้นที่ดิสก์เต็ม, var เต็ม, volume group
versions: BIG-IP 17.5.x
sources: https://my.f5.com/manage/s/article/K14403, https://my.f5.com/manage/s/article/K8865, https://my.f5.com/manage/s/article/K60799644, https://my.f5.com/manage/s/article/K000148391, https://my.f5.com/manage/s/article/K000158919
---

# F5 BIG-IP 17.x — ตรวจพื้นที่ดิสก์ (diskmonitor)

---

## ข้อความ diskmonitor และการตรวจ

คำค้น: f5 diskmonitor, f5 011d0004, f5 disk partition has only free, f5 var เต็ม, f5 disk space

ที่มา: K14403 (https://my.f5.com/manage/s/article/K14403), K8865 (https://my.f5.com/manage/s/article/K8865), K60799644 (https://my.f5.com/manage/s/article/K60799644) (Applies to BIG-IP LTM มี 17.5.1, 17.5.0, 17.5.X ทั้ง 3 บทความ)

"The diskmonitor utility is a script that runs periodically on the BIG-IP system to monitor disk usage." — K8865

"Monitors BIG-IP disk usage limits and disk usage growth rates on selected volumes." — K8865, diskmonitor functions

"Note: By default, 10 percent or less disk space in the /var/log volume is considered critical." — K8865

"diskmonitor: 011d005: Disk partition shared has less than 30% free" — K14403, ตัวอย่างข้อความใน /var/log/ltm

"diskmonitor: 011d004: Disk partition shared has only 0% free" — K14403

"err diskmonitor: 011d0004: Disk partition var has only 0% free" — K60799644

"Available disk space on the BIG-IP system dropped below a critical threshold." — K60799644, Description

"To display a list of DiskMonitors and their settings, use the following command:" — K8865
"tmsh list sys db platform.diskmonitor.monitor.*" — K8865

หมายเหตุ: ต้นฉบับ F5 เขียนคำสั่งขึ้นต้นด้วย tmsh ในบล็อกด้านล่างใช้รูปที่รันใน tmsh คือไม่ใส่คำว่า tmsh นำหน้า ข้อความ log ดูได้ด้วย show sys log ltm (ที่มาของคำสั่ง: playbook f5-bigip-17-ssl-handshake-troubleshooting)

คำสั่งตรวจ:
```
list sys db platform.diskmonitor.monitor.*
show sys log ltm
```

---

## พื้นที่ว่างก่อนอัปเกรดและสาเหตุที่พบบ่อย

คำค้น: f5 free disk space upgrade, f5 list sys disk all-properties, f5 vg-free, f5 old ucs old software images

ที่มา: K000148391 (https://my.f5.com/manage/s/article/K000148391), K000158919 (https://my.f5.com/manage/s/article/K000158919) (Applies to BIG-IP LTM มี 17.5.1, 17.5.0, 17.5.X ทั้ง 2 บทความ)

"You will need to have minimum 15 GiB free space in the volume group to install the software image." — K000148391, Description

"You can check if your BIG-IP has enough diskspace using either of the below commands :" — K000148391, Recommended Actions
"# tmsh list sys disk all-properties" — K000148391
"# tmsh show sys software" — K000148391, Additional Information (ดูว่า boot location ใดมี Active เป็น yes)

"A common issue is caused by having too many old ucs archives, old software images, or too many old installed OS versions." — K000158919, Recommended Actions

หมายเหตุ: ต้นฉบับเขียน `# tmsh list sys disk all-properties` ในบล็อกด้านล่างใช้รูปที่รันใน tmsh

คำสั่งตรวจ:
```
list sys disk all-properties
show sys software
```

---

ไม่พบที่มา
- K14403 และ K000148391 มีคำสั่ง bash (df, du, lsof, vgs) ไม่ได้ใส่ในบล็อกตรวจ เพราะ NetPED+ รันได้เฉพาะ show/list
- ตรวจ K8865 แล้วไม่พบ: ค่า default ของเกณฑ์ว่างน้อยของแต่ละ partition นอกจากหมายเหตุ /var/log ข้างต้น
- ไม่ใส่วิธีลบไฟล์ ลบ boot location หรือ modify sys db เพราะเป็นการแก้ไข (ดูต้นฉบับที่ K14403 และ K33265170 ซึ่ง K33265170 ไม่ได้ตรวจ)
