---
id: sophos-sfos-21-ransomware-response
title: Sophos XGS (SFOS 21.5) Ransomware Response: กัก/บล็อก IOC
families: sophos_sfos
triggers: sophos ransomware, sophos quarantine infected, sophos active threat response, sophos block ioc, sophos third party threat feed, sophos application filter block, sophos block SMB RDP, sophos log search ransomware, sophos firewall rule block, sophos log viewer search, sophos ban host, sophos ip block
versions: SFOS 21.5.x
sources: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/ConfigureFeeds/ThirdPartyThreatFeeds/ConfigureThirdPartyThreatFeeds/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Logs/LogViewer/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Applications/ApplicationFilter/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/RulesAndPolicies/FirewallRules/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Applications/HowToArticles/BlockApplicationsUsingApplicationFilter/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/syslog/index.html
---

# Sophos XGS (SFOS 21.5) Ransomware Response: กัก/บล็อก IOC

คำค้น: sophos ransomware, sophos quarantine infected, sophos active threat response, sophos block ioc, sophos application filter, sophos block SMB RDP, sophos log search
อาการ: ต้องรับมือเหตุ ransomware บน Sophos XGS (SFOS 21.5) — กักเครื่องที่ติดเชื้อ, บล็อก IOC, บล็อกแอป remote access/ทังเนล, บล็อก SMB/RDP ข้ามโซนเร่งด่วน, และค้นย้อนหลังใน log

---

## 1. กักเครื่องที่สงสัยว่าติด ransomine ทันที (Ban IP / Block Host)

คำค้น: sophos ban host, sophos active threat response quarantine, sophos block ip, sophos block host, sophos block firewall rule
อาการ: พบเครื่องต้องสงสัยว่าติดเชื้อ ต้องบล็อก traffic จาก IP นั้นทันที

ตรวจใน GUI:
- **Rules and policies** → **Firewall rules** — ดูรายการ firewall rules
- **Active threat response widget** — ดู compromised hosts ที่แสดง

วิธีแก้:
- **สร้าง Firewall Rule Block (เร็วที่สุด):**
  1. ไปที่ **Rules and policies** → **Firewall rules** → **Add firewall rule** → **New firewall rule**
  2. ตั้งค่า:
     - **Rule name:** `BLOCK-INFECTED-HOST`
     - **Rule position:** **Top** (วางบนสุด — สำคัญมาก!)
     - **Source zones:** เลือกทุก zone ที่เกี่ยวข้องกับเครื่องที่ติดเชื้อ หรือเลือกเฉพาะ zone
     - **Source networks and devices:** สร้าง Host / เลือก IP ของเครื่องที่ติดเชื้อ
     - **Destination zones:** Any
     - **Destination networks:** Any
     - **Services:** Any
     - **Action:** **Drop**
  3. คลิก **Save**
- **Block ผ่าน Active Threat Response Widget:**
  1. ไปที่ **Active threat response widget** (หน้าแรก)
  2. ใน section ที่แสดง compromised host → Right-click IP → เลือก **Block**
  3. สร้าง firewall rule เพื่อ block IP นั้น (อัตโนมัติหรือแมนนวล)
- **Block ทั้งหมดจาก subnet:** หากไม่แน่ใจ IP ที่แน่ — block ทั้ง subnet
  - สร้าง Address/Network object สำหรับ subnet
  - สร้าง firewall rule block → Source = subnet → Position = Top

ที่มา: [Firewall rules — Sophos Firewall 21.5 Admin Help](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/RulesAndPolicies/FirewallRules/index.html), [Active threat response — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/index.html)

---

## 2. บล็อก IOC จากแหล่งภายนอก (Third-Party Threat Feeds)

คำค้น: sophos third party threat feed, sophos active threat response configure, sophos ioc block external, sophos threat indicator
อาการ: ต้องโหลดรายชื่อ IoC จากภายนอกมาบล็อกอัตโนมัติ

ตรวจใน GUI:
- **Active threat response** → **Third-party threat feeds** — ดูสถานะ feeds
- **Active threat response** → **Threat indicators** — ดูรายการ indicators

วิธีการ:
- **เพิ่ม Third-Party Threat Feed:**
  1. ไปที่ **Active threat response** → **Third-party threat feeds** → **Add**
  2. ตั้งค่า:
     - **Name:** ชื่อ feed (เช่น `Malware-IPs`, `C2-Domains`)
     - **Action:** **Block** (log และ block) หรือ **Monitor** (log เท่านั้น)
     - **Position:** **Top** (สำคัญ — feed ต้องอยู่ก่อน allow rule)
     - **Indicator type:** เลือกประเภท — **IPv4 address** / **Domain** / **URL** (ต้องแยก feed ต่อประเภท)
     - **URL:** กรอก URL ของ threat feed file (plain-text, indicator ต่อบรรทัด)
     - **Polling interval:** เลือก interval สำหรับ sync (แนะนำ 15 นาที — 6 ชั่วโมง)
  3. คลิก **Save**

- **ตรวจว่าโหลดสำเร็จ:**
  - ไปที่ **Active threat response** → **Third-party threat feeds**
  - ดูสถานะ — ต้องเห็นจำนวน indicators ที่โหลดแล้ว
  - ไปที่ **Active threat response** → **Threat indicators** — ดูรายการ indicators
  - ไปที่ **Log viewer** → เลือก **Active threat response** module — ดูว่ามีการ block แล้วหรือไม่

- **ตัวอย่างแหล่ง Threat Feed ฟรี:**
  - IP addresses: `https://rules.emergingthreats.net/blockrules/compromised-ips.txt`
  - Domains: `https://osint.digitalside.it/Threat-Intel/lists/latestdomains.txt`
  - URLs: `https://urlhaus.abuse.ch/downloads/text/`

ที่มา: [Configure third-party threat feeds — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/ConfigureFeeds/ThirdPartyThreatFeeds/ConfigureThirdPartyThreatFeeds/index.html), [FAQ — Active threat response](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/FAQ/index.html)

---

## 3. บล็อกแอป Remote Access / Tunnel / ส่งไฟล์ออก (Application Filter)

คำค้น: sophos application filter block, sophos block ScreenConnect ngrok, sophos block Cloudflare tunnel, sophos block MEGA, sophos block remote access
อาการ: ต้องบล็อกแอป remote control / ทังเนล / cloud storage ที่ผู้ไม่ประสงค์ดีใช้ส่งข้อมูลออก

ตรวจใน GUI:
- **Applications** → **Application filter** — ดูรายการ application filter policies
- **Log viewer** → **Application filter** — ดูว่ามีการ block application แล้วหรือไม่

วิธีการ:
- **สร้าง Application Filter Policy:**
  1. ไปที่ **Applications** → **Application filter** → **Add**
  2. ตั้งค่า:
     - **Name:** เช่น `BLOCK-REMOTE-ACCESS`
     - **Template:** เลือก **Allow All** (เริ่มจาก policy ว่าง แล้วเพิ่ม rule block)
  3. คลิก **Save**
- **เพิ่ม Rule Block Remote Access / Tunnel:**
  1. เปิด policy ที่สร้าง → คลิก **Edit**
  2. คลิก **Add** → เลือก **Select All**
  3. เลือก **Category: Remote Control** → **Action: Deny** → **Schedule: All the time** → **Save**
  4. เพิ่ม rule → **Category: Proxy and Tunnel** → **Action: Deny** → **Save** (ครอบคลุม ngrok, Cloudflare Tunnel, HTTP Tunnel)
  5. เพิ่ม rule → **Category: File Transfer** → **Action: Deny** → **Save** (ครอบคลุม MEGA, Dropbox, Google Drive)
  6. คลิก **Save** เพื่อ save policy
- **ผูกกับ Firewall Rule:**
  1. ไปที่ **Rules and policies** → **Firewall rules** → เลือก rule LAN → WAN (หรือ rule ที่ตรงกับ traffic ที่ต้องการ)
  2. เปิด **Other security features** → เลือก **Identify and control applications (App Control)** → เลือก policy `BLOCK-REMOTE-ACCESS`
  3. คลิก **Save**

ที่มา: [Application filter — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/help/en-us/webhelp/onlinehelp/AdministratorHelp/Applications/ApplicationFilter/index.html), [Block applications using the application filter](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Applications/HowToArticles/BlockApplicationsUsingApplicationFilter/index.html)

### 3.1 ใช้ Predefined Template เร็ว

หากต้องการบล็อกด่วน:
- ใช้ template **Block filter avoidance apps** — บล็อก proxy/tunnel/bypass apps
- ใช้ template **Block generally unwanted apps** — บล็อก file transfer, proxy/tunnel, risk-prone, P2P
- ใช้ template **Block high risk (Risk Level 4 and 5) apps** — บล็อกแอปที่เสี่ยงสูง
- นำ policy template ที่สร้างไปผูกกับ firewall rule เหมือนขั้นตอนด้านบน

ที่มา: [Application filter — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/help/en-us/webhelp/onlinehelp/AdministratorHelp/Applications/ApplicationFilter/index.html)

---

## 4. บล็อก SMB / RDP / WinRM ข้ามโซน (East-West) เร่งด่วน

คำค้น: sophos block SMB RDP, sophos block east-west, sophos firewall rule block service, sophos service SMB RDP
อาการ: ransomware ขยายผ่าน SMB/RDP ข้าม zone → ต้องบล็อกเร่งด่วน

ตรวจใน GUI:
- **Network** → **Network objects** → **Services** — ดู service objects
- **Rules and policies** → **Firewall rules** — ดู firewall rules

วิธีการ:
- **สร้าง Service Object สำหรับ SMB/RDP:**
  1. ไปที่ **Network** → **Network objects** → **Services** → **Add**
  2. ตั้งค่า service สำหรับแต่ละ port:
     - **Name:** `SMB-139`, **Protocol:** TCP, **Port:** 139
     - **Name:** `SMB-445`, **Protocol:** TCP, **Port:** 445
     - **Name:** `RDP-3389`, **Protocol:** TCP, **Port:** 3389
     - **Name:** `WinRM-5985`, **Protocol:** TCP, **Port:** 5985
  3. คลิก **Save**
- **สร้าง Firewall Rule Block:**
  1. ไปที่ **Rules and policies** → **Firewall rules** → **Add firewall rule** → **New firewall rule**
  2. ตั้งค่า:
     - **Rule name:** `BLOCK-SMB-RDP-EAST-WEST`
     - **Rule position:** **Top** (สำคัญ — rule ต้องอยู่ก่อน allow rule)
     - **Source zones:** zone ที่ต้องการ block (เช่น LAN → Server)
     - **Source networks:** Any
     - **Destination zones:** zone ที่ต้องการ block (เช่น Server)
     - **Destination networks:** Any
     - **Services:** เลือก service `SMB-139`, `SMB-445`, `RDP-3389`, `WinRM-5985`
     - **Action:** **Drop**
  3. คลิก **Save**

ที่มา: [Firewall rules — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/RulesAndPolicies/FirewallRules/index.html)

อ้างอิง playbook: `sophos-sfos-21-ips-hardening-syslog` สำหรับ zone-based policy

---

## 5. ค้นย้อนหลังใน Log ว่าเครื่องนั้นคุยกับใคร

คำค้น: sophos log viewer search, sophos log search ransomware, sophos firewall log, sophos log viewer, sophos log search source ip
อาการ: ต้องสืบสวนว่าเครื่องที่ติด ransomware คุยกับ IP/Domain ใดบ้าง (C2, ผู้แพร่กระจาย, ผู้ถูก infect ต่อ)

ตรวจใน GUI:
- **Log viewer** → เลือก **Firewall** module — ดู firewall logs
- คลิก **Add filter** → **src_ip** — กรองตาม source IP

วิธีตรวจใน Log Viewer:
- **เปิด Log viewer:** คลิก **Log viewer** ที่มุมบนขวาของหน้าเว็บ admin
- **เลือก Module:** เลือก **Firewall** ใน module selector
- **Filter by Source IP:**
  1. คลิก **Add filter** → เลือก **src_ip** → ใส่ IP ของเครื่องที่ติดเชื้อ
  2. คลิก **Apply**
  3. ดูผลลัพธ์ — จะเห็นรายการ traffic ทั้งหมดของเครื่องนั้น (source → destination, port, service, matching rule)
- **Filter by Time:** เลือก time range (เช่น 24 ชม. ก่อนหน้าเหตุการณ์)
- **Filter by Destination IP:** หากทราบว่าเครื่องติดต่อ C2 IP ใด → filter dst_ip = นั้น
- **ตรวจ Detailed View:** คลิกที่แต่ละรายการ → ดูรายละเอียดเพิ่ม (DNS query, HTTP host, application)
- **ตรวจ Web Filter Logs:** ไปที่ Log viewer → เลือก **Web filter** — ดูว่าเครื่องนั้น access domain อะไร (อาจเจอ C2 domain)
- **ตรวจ Malware Logs:** ไปที่ Log viewer → เลือก **Malware** — ดูว่าพบ malware ใด

ที่มา: [Log viewer — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Logs/LogViewer/index.html), [Logs — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/help/en-us/webhelp/onlinehelp/AdministratorHelp/Logs/index.html)

วิธีตรวจใน FortiAnalyzer (หากต่อ Sophos Fusion / Syslog):
- หากตั้งค่า syslog forwarding → log จะไปเก็บที่ Sophos Fusion / FortiAnalyzer / syslog server
- สามารถสืบสวนเพิ่มเติมจาก centralized log viewer

หมายเหตุ: หาก log level ต่ำ — อาจไม่พบข้อมูลทั้งหมด — ให้เพิ่ม logging ใน firewall rule (เปิด Log firewall traffic) สำหรับเหตุการณ์ในอนาคต

---

## 6. สรุปลำดับการดำเนินการ (Quick Reference)

ตรวจใน GUI:
- **Rules and policies** → **Firewall rules** — ตรวจสอบ firewall rules
- **Active threat response** → ดู threat feeds
- **Applications** → **Application filter** — ตรวจสอบ app control
- **Log viewer** → เลือก **Firewall** — ตรวจสอบ logs

วิธีดำเนินการ:
1. **กักเครื่องทันที:** สร้าง Firewall Rule Block → Position = Top → Source = IP เครื่องที่ติดเชื้อ
2. **บล็อก IOC:** Active Threat Response → Third-party threat feeds → Add → Block → Position = Top
3. **บล็อก Remote Access/Tunnel:** Application Filter → Block Remote Control + Proxy/Tunnel + File Transfer → ผูกกับ firewall rule
4. **บล็อก SMB/RDP ข้ามโซน:** สร้าง Service (139, 445, 3389, 5985) → Firewall Rule Block → Position = Top
5. **สืบสวน Log:** Log viewer → Firewall → Filter src_ip = เครื่องที่ติดเชื้อ

ที่มา: [Firewall rules — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/RulesAndPolicies/FirewallRules/index.html)

---

คำค้น: sophos ransomware, sophos quarantine, sophos ban host, sophos active threat response, sophos third party threat feed, sophos application filter, sophos block SMB, sophos block RDP, sophos east-west, sophos log viewer, sophos firewall log
