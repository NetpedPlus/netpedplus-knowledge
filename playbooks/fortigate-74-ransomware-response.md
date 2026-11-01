---
id: fortigate-74-ransomware-response
title: FortiGate 7.4 Ransomware Response: กัก/บล็อก IOC
families: fortinet_fortios
triggers: fortigate ransomware, fortigate quarantine infected, fortigate ban ip, fortigate ioc block, fortigate threat feed, fortigate application control remote access, fortigate block SMB RDP, fortigate east-west urgent, fortigate log search ransomware, fortigate compromised host, fortigate malware hash feed, fortigate automation stitch quarantine
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/570050/ip-ban, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/637981/fortigate-quarantine-webhook-setup-example, https://docs.fortinet.com/document/fortigate/7.4.11/cli-reference/448397853/diagnose-user, https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/302748/application-control, https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/49251/ip-ban-using-security-profiles, https://docs.fortinet.com/document/fortigate/7.4.8/administration-guide/881990/default-automation-stitches, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/51460/actions, https://docs.fortinet.com/document/fortigate/7.4.12/administration-guide/913906/malware-hash-threat-feed, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/9463/threat-feeds, https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/116821/zone, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/876272/security-events-log-page, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/54688/debugging-the-packet-flow, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/656084/firewall-policy
---

# FortiGate 7.4 Ransomware Response: กัก/บล็อก IOC

คำค้น: fortigate ransomware, fortigate quarantine infected, fortigate ban ip, fortigate ioc block, fortigate threat feed, fortigate application control remote access, fortigate block SMB RDP, fortigate east-west urgent, fortigate log search ransomware
อาการ: ต้องรับมือเหตุ ransomware บน FortiGate 7.4 — กักเครื่องที่ติดเชื้อ, บล็อก IOC, บล็อกแอป remote access/tunnel, บล็อก SMB/RDP/WinRM ข้ามโซนเร่งด่วน, และค้นย้อนหลังใน log

---

## 1. กักเครื่องที่สงสัยว่าติด ransomware ทันที (IP Ban)

คำค้น: fortigate ban ip, fortigate quarantine infected host, fortigate diagnose user banned-ip
อาการ: พบเครื่องต้องสงสัยว่าติดเชื้อ ต้องบล็อก traffic จาก IP นั้นทันที

**ข้อควรรู้:** Firewall กักได้เฉพาะ traffic ที่ผ่าน firewall เท่านั้น — หากเครื่องอยู่ใน subnet/VLAN เดียวกัน คุยกันตรงผ่าน switch (SMB/RDP ภายในวงเดียวกัน) firewall บล็อกไม่ได้ ต้องตัดที่ switch port / NAC / EDR พร้อมกัน

คำสั่งตรวจ:
```
diagnose user banned-ip list
```
อ่านผล:
- ต้องเห็นรายการ IP ที่ถูก ban พร้อม IP, created date, expires date, cause (admin/av/dos/ips)
- หากไม่พบ = ยังไม่ได้ ban เครื่องนั้น
ที่มา: [diagnose user — FortiOS 7.4.11 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.11/cli-reference/448397853/diagnose-user)

วิธีแก้:
- **Ban จาก CLI (เร็วที่สุด):** `diagnose user banned-ip add src4 <IP> <expiry-seconds> admin` เช่น `diagnose user banned-ip add src4 10.0.0.23 86400 admin` (ban 24 ชม.)
- **ตรวจรายการที่ ban:** `diagnose user banned-ip list`
- **Unban:** `diagnose user banned-ip delete src4 <IP>`
- **ล้างทั้งหมด:** `diagnose user banned-ip clear`
- **View จาก GUI:** FortiView → Sources → Right-click IP → Ban IP (ระบุ duration)
- หมายเหตุ: FortiOS 7.2+ ใช้ `diagnose user banned-ip` เท่านั้น (7.0 ลงมาใช้ `diagnose user quarantine`)

---

## 2. บล็อก IOC จากแหล่งภายนอก (Threat Feed)

คำค้น: fortigate threat feed, fortigate external block list, fortigate malware hash feed
อาการ: ต้องโหลดรายชื่อ IoC (IP/Domain/Hash) จากแหล่งภายนอกมาบล็อกอัตโนมัติ

### 2.1 IP Address Threat Feed

ตรวจใน GUI:
- **Security Fabric → External Connectors → Threat Feeds** — ดูสถานะ feeds

วิธีการ:
- **เพิ่ม External Threat Feed:** Security Fabric → External Connectors → Threat Feeds → เลือกประเภท IP → Create New
- **ตั้งค่า URL:** กรอก URL ของ threat feed ที่ host plain-text file (IP ต่อบรรทัด)
- **Update Method:** เลือก External Feed และตั้ง polling interval
- **นำไปใช้กับ Policy:** สร้าง IPv4 Policy → Destination = Threat Feed ที่เพิ่ม → Action = Deny
- **ตรวจว่าโหลดสำเร็จ:** Security Fabric → External Connectors → เลือก connector → ดูจำนวน entries ที่โหลดแล้ว

ที่มา: [Threat feeds — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/9463/threat-feeds)

### 2.2 Malware Hash Threat Feed

ตรวจใน GUI:
- **Security Profiles → AntiVirus** — ดูว่า external malware block list ถูกเลือกแล้ว

วิธีการ:
- **เพิ่ม Malware Hash Feed:** Security Fabric → External Connectors → Malware Hash → Create New
- **ตั้งค่า URL:** เช่น S3 bucket ของ malware hash หรือแหล่งที่ host ไฟล์ hash (MD5/SHA1/SHA256 ต่อบรรทัด)
- **นำไปใช้กับ AV Profile:** Security Profiles → AntiVirus → Edit → เปิด Use external malware block list → เลือก feed ที่เพิ่ม
- **นำไปใช้กับ Policy:** ผูก AV profile กับ firewall policy

ที่มา: [Malware hash threat feed — FortiOS 7.4.12 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.12/administration-guide/913906)

---

## 3. บล็อกแอป Remote Access / Tunnel / ส่งไฟล์ออก (Application Control)

คำค้น: fortigate application control block, fortigate block ScreenConnect ngrok, fortigate block Cloudflare tunnel, fortigate block MEGA, fortigate application control remote access
อาการ: ต้องบล็อกแอป remote control / tunnel / cloud storage ที่ผู้ไม่ประสงค์ดีใช้ส่งข้อมูลออก

คำสั่งตรวจ:
```
show application list
```
อ่านผล:
- ต้องเห็น application list และ entry ที่สร้าง → action = block สำหรับ remote access, proxy, storage

วิธีการ:
- **เพิ่ม Application List:** Security Profiles → Application Control → Edit → เพิ่ม entry ที่ต้องการ block
- **เลือก Category "Remote.Access":** รวม TeamViewer, AnyDesk, ScreenConnect, RustDesk (FortiGuard category: Remote.Access)
- **เลือก Category "Proxy":** รวม ngrok, Cloudflare Tunnel, OpenVPN, HTTP Tunnel (FortiGuard category: Proxy)
- **เลือก Category "Storage.Backup":** รวม MEGA, Dropbox, Google Drive, OneDrive (FortiGuard category: Storage.Backup)
- **เลือก Category "Cloud.IT":** บางแอป cloud storage อยู่หมวดนี้
- **ผูกกับ Policy:** Security Profiles → Application Control → เลือก profile ที่สร้าง → ผูกกับ firewall policy
- **ตั้ง Action = Block:** สำหรับ remote access, proxy, storage

ที่มา: [Application control — FortiOS 7.4.0 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/302748), [Application Control Categories — FortiGuard](https://www.fortiguard.com/appcontrol/categories)

อ้างอิง playbook: `fortigate-74-security-profiles` สำหรับรายละเอียดการสร้าง Application list, Profile group, และผูกกับ policy

### 3.1 เพิ่ม Quarantine Override (บล็อกยาว)

วิธีการ:
- **ตั้งค่า Quarantine ใน Application Control:** เมื่อ match application ที่ block → ban IP ชั่วคราว
- **CLI:** `config application list`, `edit "<list-name>"`, `config entries`, `edit <id>`, `set quarantine attacker`, `set quarantine-expiry <seconds>`, `next`, `end`, `next`, `end`
- **ตรวจ:** `diagnose user banned-ip list` — ดูรายการ quarantined IP

---

## 4. บล็อก SMB / RDP / WinRM ข้ามโซน (East-West) เร่งด่วน

คำค้น: fortigate block SMB RDP, fortigate block east-west ransomware, fortigate service SMB RDP, fortigate urgent block SMB
อาการ: ransomware ขยายผ่าน SMB/RDP/WinRM ข้าม zone → ต้องบล็อกเร่งด่วน

**ข้อควรรู้:** Firewall กักได้เฉพาะ traffic ที่ผ่าน firewall เท่านั้น — หากเครื่องอยู่ใน subnet/VLAN เดียวกัน คุยกันตรงผ่าน switch (SMB/RDP ภายในวงเดียวกัน) firewall บล็อกไม่ได้ ต้องตัดที่ switch port / NAC / EDR พร้อมกัน

คำสั่งตรวจ:
```
show firewall policy
show firewall service custom
```
อ่านผล:
- ต้องเห็น policy ที่ block SMB/RDP ที่วางบนสุด (policy-id ต่ำ)
- ต้องเห็น custom service สำหรับ port 139, 445, 3389, 5985, 5986

วิธีการ:
- **สร้าง Service Object สำหรับ SMB/RDP/WinRM:** `config firewall service custom`, `edit "SMB-RDP-URGENT"`, `set tcp-portrange 139 445 3389 5985 5986`, `next`, `end` (รวม WinRM ทั้ง 5985 TCP และ 5986 TCP HTTPS)
- **สร้าง Policy Block ข้ามโซน (วางบนสุด):**
  1. หา policy-id บนสุด: `show firewall policy` → ดู policy-id ต่ำสุด (เช่น 5)
  2. ย้าย policy ปัจจุบันไปล่าง: `config firewall policy`, `edit 5`, `move 5 before 10`, `next`, `end` (ใช้เลข policy-id ที่มากกว่า)
  3. สร้าง policy ใหม่บนสุด: `config firewall policy`, `edit 5`, `set name "BLOCK-SMB-RDP-EW"`, `set srcintf "<src-zone>"`, `set dstintf "<dst-zone>"`, `set srcaddr "all"`, `set dstaddr "all"`, `set service "SMB-RDP-URGENT"`, `set action deny`, `set logtraffic all`, `next`, `end`
  4. หากต้องการให้อยู่บนสุดจริงๆ: ย้ายทุก policy ลงมา 1 ตำแหน่ง แล้วสร้าง policy-id 1 ใหม่
- **ตรวจว่า policy อยู่บนสุด:** `show firewall policy` — policy ที่ block SMB/RDP ต้องเป็น policy-id ต่ำสุด

อ้างอิง playbook: `fortigate-74-segmentation-east-west` สำหรับ zone-based policy

ที่มา: [Firewall policy — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/656084/firewall-policy)

---

## 5. ค้นย้อนหลังใน Log ว่าเครื่องนั้นคุยกับใคร

คำค้น: fortigate log search ransomware, fortigate fortiview, fortigate log search
อาการ: ต้องสืบสวนว่าเครื่องที่ติด ransomware คุยกับ IP/Domain ใดบ้าง (C2, ผู้แพร่กระจาย, ผู้ถูก infect ต่อ)

คำสั่งตรวจ:
```
diagnose sys session filter clear
diagnose sys session filter src 10.0.0.23
diagnose sys session list
show log setting
```
อ่านผล:
- ต้องเห็น session ที่ active ของเครื่องที่ติดเชื้อ
- ต้องเห็น log device = local/fortianalyzer/remote
- ต้องเห็น log traffic = all/audit ใน policy ที่เกี่ยวข้อง
- หาก log device = none = ไม่มี log เก็บไว้

ที่มา: [Security Events log page — FortiOS 7.4.0 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/876272/security-events-log-page)

วิธีตรวจใน FortiGate (Log Viewer / FortiView):
- **Log & Report → Forward Traffic:** Filter โดย srcip = IP ของเครื่องที่ติดเชื้อ → ดูทุก destination และ service ที่คุย
- **Log & Report → Security Events:** ดู UTM events (Application Control, IPS, AV)
- **FortiView → Sources:** ดู source IP → เลือก IP ของเครื่องที่ติดเชื้อ → ดู destination IP / Application / Service ที่คุยด้วย
- **FortiView → Top Applications:** ดูว่าเครื่องใช้แอปอะไร (อาจเจอ remote access / file transfer)

วิธีตรวจด้วย Debug Flow (ดูว่า traffic ผ่าน policy ไหน):
- `diagnose debug flow filter addr <IP>`
- `diagnose debug flow trace start 10`
- `diagnose debug enable`
- แล้ว reproduce traffic → ดูผล → `diagnose debug disable` → `diagnose debug reset`

ที่มา: [Debugging the packet flow — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/54688/debugging-the-packet-flow)

---

## 6. สรุปลำดับการดำเนินการ (Quick Reference)

คำสั่งตรวจ:
```
diagnose user banned-ip list
show firewall policy
show application list
```
อ่านผล:
- ต้องเห็น quarantine list, firewall policy, และ application list ที่ตั้งค่าแล้ว

วิธีดำเนินการ:
1. **กักเครื่องทันที:** `diagnose user banned-ip add src4 <IP> <expiry> admin`
2. **บล็อก IOC:** เพิ่ม Threat Feed → ผูกกับ Policy → Action = Deny
3. **บล็อก Remote Access/Tunnel/Storage:** Application Control → Block Category Remote.Access + Proxy + Storage.Backup
4. **บล็อก SMB/RDP/WinRM ข้ามโซน:** สร้าง Service (tcp-portrange 139 445 3389 5985 5986) + Policy Block → ย้ายมาบนสุด
5. **สืบสวน Log:** Log & Report → Forward Traffic / Security Events — filter srcip = เครื่องที่ติดเชื้อ
6. **ตรวจสอบ Automation Stitch:** หากตั้งค่า Compromised Host → IP Ban แล้ว (อ้างอิง: default automation stitches)

ที่มา: [diagnose user — FortiOS 7.4.11 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.11/cli-reference/448397853/diagnose-user), [Default automation stitches — FortiOS 7.4.8 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.8/administration-guide/881990)

---

คำค้น: fortigate ransomware, fortigate quarantine, fortigate ban ip, fortigate ioc, fortigate threat feed, fortigate malware hash, fortigate application control, fortigate block SMB, fortigate block RDP, fortigate east-west, fortigate log search, fortigate fortiview, fortigate compromised host
