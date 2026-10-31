---
id: fortianalyzer-150g-log-disk-adom
title: FortiAnalyzer 150G (7.4) — log ไม่เข้า / disk เต็ม / ADOM
families: fortinet_fortios
triggers: fortianalyzer, faz, faz-150g, adom, logd
vendor: Fortinet
versions: FortiAnalyzer 7.4.x
sources: https://docs.fortinet.com/document/fortianalyzer/7.4.7/administration-guide/155934/log-and-file-storage, https://docs.fortinet.com/document/fortianalyzer/7.4.8/administration-guide/743670, https://docs.fortinet.com/document/fortianalyzer/7.4.0/cli-reference/425935/log, https://docs.fortinet.com/document/fortianalyzer/7.4.1/administration-guide/62269/log-storage-information, https://docs.fortinet.com/document/fortianalyzer/7.4.2/administration-guide/667061/creating-adoms
---
# FortiAnalyzer 150G (7.4) — log ไม่เข้า / disk เต็ม / ADOM

## log ไม่เข้า FAZ | ตรวจ ADOM, device, log status
คำค้น: log not receiving, logd, log device, device log status, log source, FAZ log not receiving, log collection, log forwarder
อาการ: log ไม่เข้า FAZ, ต้องการตรวจ device log status, ต้องการตรวจ ADOM, ต้องการตรวจ logd service
คำสั่งตรวจ:
```
execute log device logstore list
execute log device vdom list <Device Name>
```
ตรวจใน GUI:
1. **Log & Event → Device Management**: ดู device status — "Managed" หรือ "Unmanaged"
2. **Log & Event → Log View → Select Device**: เลือก device → ดู log ที่เข้าจริง → filtrate ตาม time range
3. **Log & Event → Log View → Select FAZ**: ดู log local ของ FAZ เอง
4. **System Settings → ADOM**: เข้า ADOM ของ device → ตรวจสอบ device ว่าอยู่ใน ADOM ไหน
5. **System Settings → ADOM → Edit ADOM → Device**: ดู list device ใน ADOM — หา device ที่ไม่มีอยู่
สาเหตุที่พบบ่อย:
1. Device ไม่ได้ assign เข้า ADOM — ต้องเพิ่ม device เข้า ADOM
2. ADOM type ผิด — ADOM ต้องตรงกับ device type (FortiGate = Security Fabric ADOM)
3. logd service หยุด — ต้อง restart
วิธีแก้ (GUI):
1. เพิ่ม device เข้า ADOM: **System Settings → ADOM → เลือก ADOM → Edit → Devices → Add** → เลือก device → OK
2. ตรวจ logd: **Log & Event → FortiView → FortiView Logs** — ถ้า log ไม่แสดง = logd มีปัญหา
3. CLI: `execute log device logstore list` — ดู log directory ของ device
ที่มา: FortiAnalyzer 7.4 Log and File Storage https://docs.fortinet.com/document/fortianalyzer/7.4.7/administration-guide/155934/log-and-file-storage + FortiAnalyzer 7.4 Creating ADOMs https://docs.fortinet.com/document/fortianalyzer/7.4.2/administration-guide/667061/creating-adoms

## disk เต็ม / จัดการ quota FAZ | ตรวจและปรับ log storage policy
คำค้น: disk full, disk quota, log storage policy, adom disk quota, logd storage, data policy, analytics, archive, automatic deletion
อาการ: disk เต็ม, ต้องการดู disk usage, ต้องการปรับ log storage policy, ต้องการดู adom disk quota
คำสั่งตรวจ:
```
execute log adom disk-quota <adom_name> <value>
execute log device disk-quota <device_id> <value>
execute log device logstore list
```
ตรวจใน GUI:
1. **System Settings → Storage Info**: ดู disk utilization — Analytics/Archive usage, Max Storage, Config Days
2. **System Settings → ADOM → Edit ADOM**: ดู log storage policy — Keep Logs for Analytics/Archive, Allocated, Alert and Delete When Usage Reaches
3. **System Settings → Dashboard → Storage**: ดู storage overview — disk health, RAID status, total/free space
สาเหตุที่พบบ่อย:
1. Data Policy set Analytics นานเกินไป — logs ค้างใน SQL database
2. Archive retention ไม่ตั้ง — archived log files สะสมไม่ delete
3. Alert and Delete When Usage Reaches ไม่ตั้ง — FAZ ไม่ delete log อัตโนมัติเมื่อ disk เต็ม
4. Device log directory สะสม (logstore) — ต้อง clear leftover log directory
วิธีแก้ (GUI):
1. ลด Analytics retention: **System Settings → ADOM → Edit ADOM → Data Policy → Keep Logs for Analytics** → set เป็น 7-30 days → OK
2. ตั้ง Archive retention: **Data Policy → Keep Logs for Archive** → set ตาม compliance (เช่น 90 days) → OK
3. ตั้ง auto delete: **Disk Utilization → Alert and Delete When Usage Reaches** → set เป็น 90% → OK
4. CLI: `execute log device logstore clear <device_id>` — ลบ leftover log directory
5. CLI: `execute log adom disk-quota <adom_name> <value>` — ปรับ ADOM disk quota (MB)
ที่มา: FortiAnalyzer 7.4 Configuring Log Storage Policy https://docs.fortinet.com/document/fortianalyzer/7.4.8/administration-guide/743670 + FortiAnalyzer 7.4 Log Storage Information https://docs.fortinet.com/document/fortianalyzer/7.4.1/administration-guide/62269/log-storage-information + CLI Reference https://docs.fortinet.com/document/fortianalyzer/7.4.0/cli-reference/425935/log#log16

## ADOM ไม่สร้าง / device ไม่เข้า ADOM | ตรวจ ADOM management
คำค้น: adom not creating, adom error, device not adding to adom, adom type, adom device mode, adom device mode advanced
อาการ: ไม่สร้าง ADOM ได้, device ไม่เข้า ADOM, ต้องการดู adom type, ต้องการดู adom device mode
คำสั่งตรวจ:
```
execute log device vdom list <Device Name>
execute log device vdom add <Device Name> <ADOM> <VDOM>
```
ตรวจใน GUI:
1. **System Settings → ADOM**: ดู list ADOMs — ADOM names, types, device count
2. **System Settings → ADOM → Create New**: ตรวจขั้นตอนการสร้าง ADOM ใหม่
3. **System Settings → ADOM → Edit → Device Type**: ตรวจ device type ของ ADOM
4. **Log & Event → Device Management → Devices**: ดู list devices — หา device ที่ไม่ได้ assign เข้า ADOM
สาเหตุที่พบบ่อย:
1. ADOM limit เต็ม — FAZ 150G มี max ADOM limit ขึ้นกับ license
2. Device ถูก assign อยู่แล้วใน ADOM อื่น — device อยู่ได้แค่ใน ADOM เดียว
3. ADOM type ผิด — Device type ต้องตรงกับ ADOM type (FortiGate → Security Fabric ADOM)
4. Advanced device mode ปิด — ต้อง enable เพื่อ add individual VDOM เข้า ADOM คนละตัว
วิธีแก้ (GUI):
1. ลบ unused ADOM: **System Settings → ADOM → Select unused ADOM → Delete** → OK
2. Assign device ใหม่: **System Settings → ADOM → Edit → Devices → Add** → เลือก device
3. Enable advanced device mode: **System Settings → ADOM → Edit → Advanced Device Mode → Enable** → OK
4. CLI: `execute log device vdom list <Device Name>` — ตรวจ VDOM ของ device
5. CLI: `execute log device vdom add <Device Name> <ADOM> <VDOM>` — เพิ่ม VDOM เข้า ADOM
ที่มา: FortiAnalyzer 7.4 Creating ADOMs https://docs.fortinet.com/document/fortianalyzer/7.4.2/administration-guide/667061/creating-adoms + CLI Reference https://docs.fortinet.com/document/fortianalyzer/7.4.0/cli-reference/425935/log#log5
