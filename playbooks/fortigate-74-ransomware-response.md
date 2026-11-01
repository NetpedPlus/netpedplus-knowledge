---
id: fortigate-74-ransomware-response
title: FortiGate 7.4 Ransomware Response: Gwarg/กัก/บล็อก IOC
families: fortinet_fortios
triggers: fortigate ransomware, fortigate quarantine infected, fortigate ban ip, fortigate ioc block, fortigate threat feed, fortigate application control remote access, fortigate block SMB RDP, fortigate east-west urgent, fortigate log search ransomware, fortigate compromised host, fortigate malware hash feed, fortigate automation stitch quarantine
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/9463/threat-feeds, https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/570050/ip-ban, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/637981/fortigate-quarantine-webhook-setup-example, https://docs.fortinet.com/document/fortigate/7.4.11/cli-reference/448397853/diagnose-user, https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/302748/application-control, https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/49251/ip-ban-using-security-profiles, https://docs.fortinet.com/document/fortigate/7.4.8/administration-guide/881990/default-automation-stitches, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/51460/actions, https://docs.fortinet.com/document/fortigate/7.4.12/administration-guide/913906/malware-hash-threat-feed
---

# FortiGate 7.4 Ransomware Response: Gwarg/กัก/บล็อก IOC

คำค้น: fortigate ransomware, fortigate quarantine infected, fortigate ban ip, fortigate ioc block, fortigate threat feed, fortigate block SMB RDP, fortigate log search
อาการ: ต้องรับมือเหตุ ransomware บน FortiGate 7.4 — กักเครื่องที่ติดเชื้อ, บล็อก IOC, บล็อกแอป remote access/ทังเนล, บล็อก SMB/RDP ข้ามโซนเร่งด่วน, และค้นย้อนหลังใน log

---

## 1. กักเครื่องที่สงสัยว่าติด ransomine ทันที (IP Ban / Quarantine)

คำค้น: fortigate ban ip, fortigate quarantine infected host, fortigate diagnose user banned-ip, fortigate quarantine webhook
อาการ: พบเครื่องต้องสงสัยว่าติดเชื้อ ต้องบล็อก traffic จาก IP นั้นทันที

คำสั่งตรวจ:
```
diagnose user banned-ip list
diagnose user quarantine list
```
อ่านผล:
- ต้องเห็นรายการ IP ที่ถูก ban พร้อม IP, created date, expires date, cause (admin/av/dos/ips)
- หากไม่พบ = ยังไม่ได้ ban เครื่องนั้น
ที่มา: [diagnose user — FortiOS 7.4.11 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.11/cli-reference/448397853/diagnose-user)

วิธีแก้:
- **Ban จาก CLI (เร็วที่สุด):** `diagnose user quarantine add src4 <IP-CLIENT> <expiry-seconds> admin` เช่น `diagnose user quarantine add src4 10.0.0.23 86400 admin` (ban 24 ชม.)
- **Ban แบบถาวร (ไม่หมดอายุ):** `diagnose user banned-ip add src4 <IP-CLIENT> admin`
- **ตรวจรายการที่ ban:** `diagnose user quarantine list` หรือ `diagnose user banned-ip list`
- ** Unblock (ยกการ ban):** `diagnose user quarantine delete src4 <IP-CLIENT>`
- **Unban แบบถาวร:** `diagnose user banned-ip delete <IP-CLIENT>`
- **View จาก GUI:** FortiView → Sources → Right-click IP → Ban IP (ระบุ duration)
- **อัตโนมัติด้วย Automation Stitch:** หากตั้งค่า automation stitch แล้ว (อ้างอิง playbook `fortigate-74-dos-reputation` สำหรับ automation stitch สำหรับ Compromised Host) FortiGate จะ ban IP อัตโนมัติเมื่อตรวจพบ IoC
- หมายเหตุ: `diagnose user quarantine` ใช้ใน FortiOS 7.x — 7.2+ ใช้ `diagnose user banned-ip` เพิ่มเติม

---

## 2. บล็อก IOC จากแหล่งภายนอก (Threat Feed)

คำค้น: fortigate threat feed, fortigate external block list, fortigate malware hash feed, fortigate threat feed config
อาการ: ต้องโหลดรายชื่อ IoC (IP/Domain/Hash) จากแหล่งภายนอกมาบล็อกอัตโนมัติ

### 2.1 IP Address Threat Feed

คำสั่งตรวจ:
```
diagnose fbtest threat-feed
```
อ่านผล:
- ต้องเห็นรายการ threat feeds ที่โหลดสำเร็จ พร้อมจำนวน indicators

วิธีการ:
- **เพิ่ม External Threat Feed:** Security Fabric → External Connectors → Threat Feeds → เลือกประเภท IP → Create New
- **ตั้งค่า URL:** กรอก URL ของ threat feed ที่ host plain-text file (IP ต่อบรรทัด)
- **Update Method:** เลือก External Feed และตั้ง polling interval
- **นำไปใช้กับ Policy:** สร้าง IPv4 Policy → Destination = Threat Feed ที่เพิ่ม → Action = Deny
- **ตรวจว่าโหลดสำเร็จ:** System → FortiGuard → Threat Feed Status หรือ `diagnose fbtest threat-feed`

ที่มา: [Threat feeds — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/9463/threat-feeds)

### 2.2 Malware Hash Threat Feed

วิธีการ:
- **เพิ่ม Malware Hash Feed:** Security Fabric → External Connectors → Malware Hash → Create New
- **ตั้งค่า URL:** เช่น S3 bucket ของ malware hash หรือแหล่งที่ host ไฟล์ hash (MD5/SHA1/SHA256 ต่อบรรทัด)
- **นำไปใช้กับ AV Profile:** Security Profiles → AntiVirus → Edit → เปิด Use external malware block list → เลือก feed ที่เพิ่ม
- **นำไปใช้กับ Policy:** ผูก AV profile กับ firewall policy
- **ตรวจว่าโหลดสำเร็จ:** Security Profiles → AntiVirus → ดูว่า external malware block list ถูกเลือกแล้ว

ที่มา: [Malware hash threat feed — FortiOS 7.4.12 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.12/administration-guide/913906)

---

## 3. บล็อกแอป Remote Access / Tunnel / ส่งไฟล์ออก (Application Control)

คำค้น: fortigate application control block, fortigate block ScreenConnect ngrok, fortigate block Cloudflare tunnel, fortigate block MEGA, fortigate application control remote access
อาการ: ต้องบล็อกแอป remote control / ทังเนล / cloud storage ที่ผู้ไม่ประสงค์ดีใช้ส่งข้อมูลออก

คำสั่งตรวจ:
```
get application list
get application control sensor
```
อ่านผล:
- ต้องเห็น application list และ sensor ที่สร้าง → action = block สำหรับ remote access, tunnel, file transfer

วิธีการ:
- **เพิ่ม Application List:** Security Profiles → Application List → Create New → เพิ่ม signature ที่ต้องการ block
- **เลือก Category "Remote Access":** Category Remote Access รวม TeamViewer, AnyDesk, ScreenConnect, RustDesk
- **เลือก Category "Tunnel" (proxy & tunnel):** รวม ngrok, Cloudflare Tunnel, OpenVPN, HTTP Tunnel
- **เลือก Category "File Transfer":** รวม MEGA, Dropbox, Google Drive (ใช้ส่งข้อมูลออก)
- **ผูกกับ Policy:** Security Profiles → Application Control → เลือก profile ที่สร้าง → ผูกกับ firewall policy
- **ตั้ง Action = Block:** สำหรับ remote access, tunnel, file transfer

ที่มา: [Application control — FortiOS 7.4.0 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/302748)

อ้างอิง playbook: `fortigate-74-security-profiles` สำหรับรายละเอียดการสร้าง Application list, Profile group, และผูกกับ policy

### 3.1 เพิ่ม Quarantine Override (บล็อกยาว)

วิธีการ:
- **ตั้งค่า Quarantine ใน Application Control:** เมื่อ match application ที่ block → ban IP ชั่วคราว
- **CLI:** `config application list`, `edit "<list-name>"`, `config entries`, `edit <id>`, `set quarantine attacker`, `set quarantine-expiry <seconds>`, `next`, `end`, `next`, `end`
- **ตรวจ:** User & Devices → Quarantine — ดูรายการ quarantined users

---

## 4. บล็อก SMB / RDP / WinRM ข้ามโซน (East-West) เร่งด่วน

คำค้น: fortigate block SMB RDP, fortigate block east-west ransomware, fortigate service SMB RDP, fortigate urgent block SMB
อาการ: ransomware ขยายผ่าน SMB/RDP/WiNRm ข้าม zone → ต้องบล็อกเร่งด่วน

คำสั่งตรวจ:
```
show firewall policy
show firewall service custom
```
อ่านผล:
- ต้องเห็น policy ที่ block SMB/RDP ที่วางบนสุด (policy-id ต่ำ)
- ต้องเห็น custom service สำหรับ port 139, 445, 3389, 5985

วิธีการ:
- **สร้าง Service Object สำหรับ SMB/RDP/WinRM:**
  - SMB: `config firewall service custom`, `edit "SMB-RDP-URGENT"`, `set protocol 6 TCP`, `config port`, `edit 1`, `set port-range 139 139`, `next`, `edit 2`, `set port-range 445 445`, `next`, `edit 3`, `set port-range 3389 3389`, `next`, `edit 4`, `set port-range 5985 5985`, `next`, `end`, `next`, `end`
  - หรือแยกเป็น service object แยกกัน: `SMB-139`, `SMB-445`, `RDP-3389`, `WinRM-5985`
- **สร้าง Policy Block ข้ามโซน (วางบนสุด):** `config firewall policy`, `edit 0`, `set name "BLOCK-SMB-RDP-EW"`, `set srcintf "<src-zone>"`, `set dstintf "<dst-zone>"`, `set srcaddr "all"`, `set dstaddr "all"`, `set service "SMB-139" "SMB-445" "RDP-3389" "WinRM-5985"`, `set action deny`, `set logtraffic all`, `next`, `end`
- **วาง policy ไว้บนสุดของรายการ:** policy ที่สร้างด้วย `edit 0` จะอยู่ด้านบนสุด
- **ตรวจ:** `diagnose flow filter clear` → `diagnose flow filter dst <IP>` → `diagnose flow search` — ดูว่า traffic SMB/RDP ถูก block แล้ว

อ้างอิง playbook: `fortigate-74-segmentation-east-west` สำหรับ zone-based policy

ที่มา: [Firewall policy — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/656084/firewall-policy)

---

## 5. ค้นย้อนหลังใน Log ว่าเครื่องนั้นคุยกับใคร

คำค้น: fortigate log search ransomware, fortigate fortiview, fortigate session search, fortigate log search, fortianalyzer log
อาการ: ต้องสืบสวนว่าเครื่องที่ติด ransomware คุยกับ IP/Domain ใดบ้าง (C2, ผู้แพร่กระจาย, ผู้ถูก infect ต่อ)

คำสั่งตรวจ:
```
diagnose flow filter clear
diagnose flow filter dst <IP>
diagnose flow search
show log setting
```
อ่านผล:
- ต้องเห็น log device = local/fortianalyzer/remote
- ต้องเห็น log traffic = all/audit ใน policy ที่เกี่ยวข้อง
- หาก log device = none = ไม่มี log เก็บไว้

วิธีตรวจใน FortiGate (Log Viewer / FortiView):
- **FortiView → Sources:** ดู source IP → เลือก IP ของเครื่องที่ติดเชื้อ → ดู destination IP / Application / Service ที่คุยด้วย
- **FortiView → Top Talkers:** ดู traffic volume ของเครื่องที่ติดเชื้อ
- **FortiView → Top Applications:** ดูว่าเครื่องใช้แอปอะไร (อาจเจอ remote access / file transfer)
- **Log & Report → Firewall Log:** Filter โดย srcip = IP ของเครื่องที่ติดเชื้อ → ดูทุก destination และ service ที่คุย
- **Log & Report → Intrusion Log:** Filter โดย srcip — ดูว่าถูก IPS block อะไร
- **Log & Report → Event Log:** Filter โดย loglevel = warning/error — ดูเหตุการณ์สำคัญ

ที่มา: [Firewall policy — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/656084/firewall-policy)

วิธีตรวจใน FortiAnalyzer (หากต่อแล้ว):
- **Log View → Firewall:** Filter source = IP ของเครื่องที่ติดเชื้อ
- **Log View → Intrusion:** Filter source = IP — ดู IPS alerts
- **FortiView → Network:** ดู topology ของเครื่องที่ติดเชื้อ
- **รายงาน:** สามารถสร้างรายงานสรุป traffic ของเครื่องนั้น

หมายเหตุ: หากไม่มี FortiAnalyzer หรือ log level ต่ำ → ข้อมูลอาจไม่ครบ — ให้ตรวจ FortiView เป็นหลัก

---

## 6. สรุปลำดับการดำเนินการ (Quick Reference)

คำสั่งตรวจ:
```
diagnose user quarantine list
diagnose flow filter clear
get application control sensor
```
อ่านผล:
- ต้องเห็น quarantine list, flow status, และ application control sensor ที่ตั้งค่าแล้ว

วิธีดำเนินการ:
1. **กักเครื่องทันที:** `diagnose user quarantine add src4 <IP> <expiry> admin` (หรือ ban แบบถาวรด้วย `banned-ip`)
2. **บล็อก IOC:** เพิ่ม Threat Feed → ผูกกับ Policy → Action = Deny
3. **บล็อก Remote Access/Tunnel:** Application Control → Block Category Remote Access + Tunnel + File Transfer
4. **บล็อก SMB/RDP ข้ามโซน:** สร้าง Service + Policy Block → วางบนสุด
5. **สืบสวน Log:** FortiView + Firewall Log — filter srcip = เครื่องที่ติดเชื้อ
6. **ตรวจสอบ Automation Stitch:** หากตั้งค่า Compromised Host → IP Ban แล้ว (อัตโนมัติ)

ที่มา: [diagnose user — FortiOS 7.4.11 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.11/cli-reference/448397853/diagnose-user)

---

คำค้น: fortigate ransomware, fortigate quarantine, fortigate ban ip, fortigate ioc, fortigate threat feed, fortigate malware hash, fortigate application control, fortigate block SMB, fortigate block RDP, fortigate east-west, fortigate log search, fortigate fortiview, fortigate compromised host
