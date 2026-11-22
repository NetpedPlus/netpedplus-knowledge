---
id: fortianalyzer-150g-log-disk-adom
title: FortiAnalyzer 150G (7.4) — log ไม่เข้า / disk เต็ม / ADOM
families:
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
1. **Device Manager**: device ที่ส่ง log มาแต่ยังไม่ Authorize จะอยู่ในรายการ Unauthorized — log จะไม่ถูกเก็บจนกว่าจะ Authorize
2. **Log & Event → Log View → Select Device**: เลือก device → ดู log ที่เข้าจริง → filtrate ตาม time range
3. **Log & Event → Log View → Select FAZ**: ดู log local ของ FAZ เอง
4. **System Settings → ADOM**: เข้า ADOM ของ device → ตรวจสอบ device ว่าอยู่ใน ADOM ไหน
5. **System Settings → ADOM → Edit ADOM → Device**: ดู list device ใน ADOM — หา device ที่ไม่มีอยู่
สาเหตุที่พบบ่อย:
1. Device ไม่ได้ assign เข้า ADOM — ต้องเพิ่ม device เข้า ADOM
2. Device ยังไม่ได้ Authorize ใน Device Manager (ขึ้นเป็น Unauthorized)
3. ฝั่ง FortiGate ยังไม่ได้ตั้งส่ง log มา FAZ หรือ traffic ถูกบล็อกระหว่างทาง → ดูหัวข้อฝั่ง FortiGate "ส่ง log ไป FortiAnalyzer / syslog ไม่ได้"
วิธีแก้ (GUI):
1. เพิ่ม device เข้า ADOM: **System Settings → ADOM → เลือก ADOM → Edit → Devices → Add** → เลือก device → OK
2. Authorize device: **Device Manager → Unauthorized → เลือก device → Authorize** → เลือก ADOM
3. CLI: `execute log device logstore list` — ดู log directory ของ device
ที่มา: FortiAnalyzer 7.4 Log and File Storage https://docs.fortinet.com/document/fortianalyzer/7.4.7/administration-guide/155934/log-and-file-storage + FortiAnalyzer 7.4 Creating ADOMs https://docs.fortinet.com/document/fortianalyzer/7.4.2/administration-guide/667061/creating-adoms

## disk เต็ม / จัดการ quota FAZ | ตรวจและปรับ log storage policy
คำค้น: disk full, disk quota, log storage policy, adom disk quota, logd storage, data policy, analytics, archive, automatic deletion
อาการ: disk เต็ม, ต้องการดู disk usage, ต้องการปรับ log storage policy, ต้องการดู adom disk quota
คำสั่งตรวจ:
```
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
1. ลด Analytics retention: **System Settings → ADOM → Edit ADOM → Data Policy → Keep Logs for Analytics** → ตั้งตาม policy ขององค์กร (สั้นลง = ใช้ disk น้อยลง) → OK
2. ตั้ง Archive retention: **Data Policy → Keep Logs for Archive** → ตั้งตาม compliance ขององค์กร → OK
3. ตั้ง auto delete: **Disk Utilization → Alert and Delete When Usage Reaches** → ตั้งเปอร์เซ็นต์ที่ต้องการ → OK
4. CLI: `execute log device logstore clear <device_id>` — ลบ log directory ที่ค้างของ device ที่ลบไปแล้ว (**ลบ log ถาวร** ตรวจด้วย `execute log device logstore list` ก่อน)
5. CLI: `execute log adom disk-quota <adom_name> <value>` — ปรับ ADOM disk quota (MB)
ที่มา: FortiAnalyzer 7.4 Configuring Log Storage Policy https://docs.fortinet.com/document/fortianalyzer/7.4.8/administration-guide/743670 + FortiAnalyzer 7.4 Log Storage Information https://docs.fortinet.com/document/fortianalyzer/7.4.1/administration-guide/62269/log-storage-information + CLI Reference https://docs.fortinet.com/document/fortianalyzer/7.4.0/cli-reference/425935/log#log16

## ADOM ไม่สร้าง / device ไม่เข้า ADOM | ตรวจ ADOM management
คำค้น: adom not creating, adom error, device not adding to adom, adom type, adom device mode, adom device mode advanced
อาการ: ไม่สร้าง ADOM ได้, device ไม่เข้า ADOM, ต้องการดู adom type, ต้องการดู adom device mode
คำสั่งตรวจ:
```
execute log device vdom list <Device Name>
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

## PSIRT พฤศจิกายน 2026: FG-IR-26-251, FG-IR-26-236, FG-IR-26-229 (FortiAnalyzer 7.4.0 ถึง 7.4.11)
คำค้น: fg-ir-26-251, fg-ir-26-236, fg-ir-26-229, cve-2026-126236, cve-2026-126184, psirt fortianalyzer, ช่องโหว่ fortianalyzer, faz 7.4.12, rpc-permit, json api, fortilogd
อาการ: 3 advisory ระดับ High (10 พ.ย. 2026) กระทบ FortiAnalyzer 7.4
คำสั่งตรวจ:
```
get system status
```
อ่านผล:
- ดูบรรทัด Version ถ้าอยู่ในช่วง "7.4.0 through 7.4.11" = อยู่ในข่ายทั้ง 3 advisory ทางแก้ของทั้งหมดคือ "Upgrade to 7.4.12 or above"
- FG-IR-26-251 "Improper neutralization of special elements used in an os command in GUI" (ต้องยืนยันตัวตน): "The vulnerability can be exploited via the JSON API if enabled (Disabled by default)"
- FG-IR-26-236 "Improper limitation of a pathname to a restricted directory" (ต้องยืนยันตัวตน)
- FG-IR-26-229 "Authentication bypass by spoofing" (ไม่ต้องยืนยันตัวตน): "fortilogd may allow an attacker to disrupt the HA state."
วิธีแก้:
- วางแผนอัปเกรดเป็น 7.4.12 ขึ้นไป
- FG-IR-26-251 ถ้า admin profile เปิด JSON API ไว้ ลดความเสี่ยงได้ด้วยการวางเองใน CLI: `config system admin profile` / `edit <profile name>` / `set rpc-permit none` / `end`
ระวัง: `set rpc-permit none` ตัดสิทธิ์ JSON API ของ profile นั้น ระบบที่เรียก API ของ FAZ ด้วย admin ใน profile นี้จะใช้ไม่ได้ การอัปเกรด firmware ทำให้เครื่อง reboot ต้องทำในช่วง maintenance
ที่มา: FortiGuard PSIRT FG-IR-26-251 https://fortiguard.fortinet.com/psirt/FG-IR-26-251 และ FG-IR-26-236 https://fortiguard.fortinet.com/psirt/FG-IR-26-236 และ FG-IR-26-229 https://fortiguard.fortinet.com/psirt/FG-IR-26-229 และ FortiAnalyzer 7.4.0 CLI Reference system status https://docs.fortinet.com/document/fortianalyzer/7.4.0/cli-reference/714660/system-status
