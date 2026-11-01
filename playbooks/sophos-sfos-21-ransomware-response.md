---
id: sophos-sfos-21-ransomware-response
title: Sophos XGS (SFOS 21.5) Ransomware Response: กัก/บล็อก IOC
families: sophos_sfos
triggers: sophos ransomware, sophos quarantine infected, sophos active threat response, sophos block ioc, sophos third party threat feed, sophos application filter block, sophos block SMB RDP, sophos log search ransomware, sophos firewall rule block, sophos log viewer search, sophos ban host, sophos ip block
versions: SFOS 21.5.x
sources: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/ConfigureFeeds/ThirdPartyThreatFeeds/ConfigureThirdPartyThreatFeeds/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Logs/LogViewer/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Applications/ApplicationFilter/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/RulesAndPolicies/FirewallRules/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Applications/HowToArticles/BlockApplicationsUsingApplicationFilter/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/Requirements/ConfigureLogs/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/help/en-us/webhelp/onlinehelp/AdministratorHelp/HostsAndServices/Services/ServiceAdd/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/syslog/index.html
---

# Sophos XGS (SFOS 21.5) Ransomware Response: กัก/บล็อก IOC

คำค้น: sophos ransomware, sophos quarantine infected, sophos active threat response, sophos block ioc, sophos application filter, sophos block SMB RDP, sophos log search
อาการ: ต้องรับมือเหตุ ransomware บน Sophos XGS (SFOS 21.5) — กักเครื่องที่ติดเชื้อ, บล็อก IOC, บล็อกแอป remote access/tunnel, บล็อก SMB/RDP/WinRM ข้ามโซนเร่งด่วน, และค้นย้อนหลังใน log

---

## 1. กักเครื่องที่สงสัยว่าติด ransomware ทันที (Ban IP / Block Host)

คำค้น: sophos ban host, sophos block ip, sophos block host, sophos block firewall rule
อาการ: พบเครื่องต้องสงสัยว่าติดเชื้อ ต้องบล็อก traffic จาก IP นั้นทันที

**ข้อควรรู้:** Firewall กักได้เฉพาะ traffic ที่ผ่าน firewall เท่านั้น — หากเครื่องอยู่ใน subnet/VLAN เดียวกัน คุยกันตรงผ่าน switch (SMB/RDP ภายในวงเดียวกัน) firewall บล็อกไม่ได้ ต้องตัดที่ switch port / NAC / EDR พร้อมกัน

ตรวจใน GUI:
- **Rules and policies** → **Firewall rules** — ดูรายการ firewall rules

วิธีแก้:
- **สร้าง Firewall Rule Block (เร็วที่สุด):**
  1. ไปที่ **Rules and policies** → **Firewall rules** → **Add firewall rule** → **New firewall rule**
  2. ตั้งค่า:
     - **Rule name:** `BLOCK-INFECTED-HOST`
     - **Rule position:** **Top** (วางบนสุด — สำคัญมาก!)
     - **Source zones:** เลือก zone ที่เกี่ยวข้องกับเครื่องที่ติดเชื้อ
     - **Source networks and devices:** สร้าง Host → ใส่ IP ของเครื่องที่ติดเชื้อ
     - **Destination zones:** Any
     - **Destination networks:** Any
     - **Services:** Any
     - **Action:** **Drop**
  3. คลิก **Save**
- **Block ทั้งหมดจาก subnet:** หากไม่แน่ใจ IP ที่แน่ — block ทั้ง subnet
  - สร้าง Address/Network object สำหรับ subnet
  - สร้าง firewall rule block → Source = subnet → Position = Top

ที่มา: [Firewall rules — Sophos Firewall 21.5 Admin Help](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/RulesAndPolicies/FirewallRules/index.html), [Active threat response — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/index.html)

---

## 2. บล็อก IOC จากแหล่งภายนอก (Third-Party Threat Feeds)

คำค้น: sophos third party threat feed, sophos active threat response configure
อาการ: ต้องโหลดรายชื่อ IoC จากภายนอกมาบล็อกอัตโนมัติ

ตรวจใน GUI:
- **Protect** → **Active threat response** → **Third-party threat feeds** — ดูสถานะ feeds

วิธีการ:
- **เปิด Log ก่อน (สำคัญ):** ไปที่ **System services** → **Log settings** → เปิด **Active threat response** สำหรับ Local reporting (และ Syslog หากมี)
- **เพิ่ม Third-Party Threat Feed:**
  1. ไปที่ **Protect** → **Active threat response** → **Third-party threat feeds** → **Add**
  2. ตั้งค่า:
     - **Name:** ชื่อ feed (เช่น `Malware-IPs`)
     - **Action:** **Block** (log+block) หรือ **Monitor** (log เท่านั้น) — แนะนำเริ่มที่ Monitor ก่อนเพื่อตรวจ false positive
     - **Position:** **Top** — feed ต้องอยู่ก่อน allow rule
     - **Indicator type:** **IPv4 address** / **Domain** / **URL** (แยก feed ต่อประเภท)
     - **URL:** กรอก URL ของ threat feed file (plain-text, indicator ต่อบรรทัด) — ต้องเป็น HTTPS โดยตรง (redirect 302 = Connection error)
     - **Polling interval:** 15 นาที — 6 ชั่วโมง
  3. คลิก **Save**

ที่มา: [Configure third-party threat feeds — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/ConfigureFeeds/ThirdPartyThreatFeeds/ConfigureThirdPartyThreatFeeds/index.html), [Logs and alerts for Active threat response — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/Requirements/ConfigureLogs/index.html)

---

## 2.1 ตรวจว่าโหลด Feed สำเร็จ + คำเตือน

คำค้น: sophos threat feed verify, sophos feed success status, sophos threat indicator
อาการ: ต้องตรวจว่า threat feed โหลดสำเร็จ และรู้ขีดจำกัดของสถานะ Success

ตรวจใน GUI:
- **Protect** → **Active threat response** → **Threat indicators** — ดูจำนวน indicators ที่โหลดแล้ว
- **Log viewer** → **Active threat response** — ดูว่ามีการ block แล้วหรือไม่

คำเตือนและหมายเหตุ:
- **สถานะ "Success" ยืนยันแค่ดึงไฟล์ได้** ไม่ได้ยืนยันว่ามี traffic match กับ IoC ใน feed
- **Feed ฟรี:** หากใช้ feed ฟรี (เช่น emergingthreats, osint.digitalside.it, urlhaus) ต้องตรวจ false positive และเงื่อนไขการใช้งานของผู้ให้ feed ก่อนตั้ง Block
- แนะนำเริ่มที่ **Monitor** ก่อน แล้วค่อยเปลี่ยนเป็น **Block** เมื่อมั่นใจว่า feed น่าเชื่อถือ

ที่มา: [FAQ — Active threat response](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/ActiveThreatResponse/FAQ/index.html), [Logs — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/help/en-us/webhelp/onlinehelp/AdministratorHelp/Logs/index.html)

---

## 3. บล็อกแอป Remote Access / Tunnel / ส่งไฟล์ออก (Application Filter)

คำค้น: sophos application filter block, sophos block ScreenConnect ngrok, sophos block MEGA
อาการ: ต้องบล็อกแอป remote control / tunnel / cloud storage ที่ผู้ไม่ประสงค์ดีใช้ส่งข้อมูลออก

ตรวจใน GUI:
- **Applications** → **Application filter** — ดูรายการ application filter policies

วิธีการ:
- **สร้าง Application Filter Policy:**
  1. ไปที่ **Applications** → **Application filter** → **Add**
  2. ตั้งค่า: **Name:** เช่น `BLOCK-REMOTE-ACCESS`, **Template:** เลือก **Allow All**
  3. คลิก **Save**
- **เพิ่ม Rule Block Remote Access:**
  1. เปิด policy → คลิก **Edit** → คลิก **Add** → **Select All**
  2. **Category: Remote Access** (AnyDesk, VNC, QQ Remote Access) → **Deny** → **Save**
- **เพิ่ม Rule Block Proxy and Tunnel:**
  1. **Add** → **Category: Proxy and Tunnel** (ngrok, Cloudflare Tunnel, OpenVPN) → **Deny** → **Save**
- **ผูกกับ Firewall Rule:**
  1. ไปที่ **Rules and policies** → **Firewall rules** → เลือก rule LAN → WAN
  2. เปิด **Other security features** → **Identify and control applications (App Control)** → เลือก policy
  3. คลิก **Save**

ที่มา: [Application filter — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/help/en-us/webhelp/onlinehelp/AdministratorHelp/Applications/ApplicationFilter/index.html), [Block applications using the application filter](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Applications/HowToArticles/BlockApplicationsUsingApplicationFilter/index.html)

---

## 3.1 บล็อก File Transfer / Storage + Predefined Template

คำค้น: sophos file transfer block, sophos storage backup block, sophos predefined template
อาการ: ต้องบล็อก file transfer และ cloud storage เพื่อป้องกันข้อมูลออก

ตรวจใน GUI:
- **Applications** → **Application filter** → ดู policy ที่สร้าง → คลิก **Edit** เพื่อดู rule ที่เพิ่ม

วิธีการ (File Transfer/Storage):
- เพิ่ม rule → **Category: File Transfer** หรือ **Category: Storage and Backup** → **Deny** → **Save**
- ผูกกับ firewall rule เหมือนขั้นตอนด้านบน

ใช้ Predefined Template เร็ว:
- **Block filter avoidance apps** — บล็อก proxy/tunnel/bypass apps
- **Block generally unwanted apps** — บล็อก file transfer, proxy/tunnel, risk-prone, P2P
- **Block high risk (Risk Level 4 and 5) apps** — บล็อกแอปที่เสี่ยงสูง
- นำ policy template ที่สร้างไปผูกกับ firewall rule เหมือนขั้นตอนด้านบน

ที่มา: [Application filter — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/help/en-us/webhelp/onlinehelp/AdministratorHelp/Applications/ApplicationFilter/index.html)

---

## 4. บล็อก SMB / RDP / WinRM ข้ามโซน (East-West) เร่งด่วน

คำค้น: sophos block SMB RDP, sophos block east-west, sophos service SMB RDP
อาการ: ransomware ขยายผ่าน SMB/RDP ข้าม zone → ต้องบล็อกเร่งด่วน

ตรวจใน GUI:
- **Hosts and services** → **Services** — ดู service objects
- **Rules and policies** → **Firewall rules** — ดู firewall rules

วิธีการ:
- **สร้าง Service Object สำหรับ SMB/RDP/WinRM:**
  1. ไปที่ **Hosts and services** → **Services** → **Add**
  2. ตั้งค่า service:
     - **SMB-139:** TCP Port 139
     - **SMB-445:** TCP Port 445
     - **RDP-3389:** TCP Port 3389
     - **WinRM-5985:** TCP Port 5985
     - **WinRM-5986:** TCP Port 5986
  3. คลิก **Save**
- **สร้าง Firewall Rule Block:**
  1. ไปที่ **Rules and policies** → **Firewall rules** → **Add firewall rule** → **New firewall rule**
  2. ตั้งค่า:
     - **Rule name:** `BLOCK-SMB-RDP-EAST-WEST`
     - **Rule position:** **Top**
     - **Source zones:** zone ที่ต้องการ block (เช่น LAN → Server)
     - **Destination zones:** zone ที่ต้องการ block (เช่น Server)
     - **Services:** เลือก service `SMB-139`, `SMB-445`, `RDP-3389`, `WinRM-5985`, `WinRM-5986`
     - **Action:** **Drop**
  3. คลิก **Save**

ที่มา: [Firewall rules — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/RulesAndPolicies/FirewallRules/index.html), [Add service — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/help/en-us/webhelp/onlinehelp/AdministratorHelp/HostsAndServices/Services/ServiceAdd/index.html)

อ้างอิง playbook: `sophos-sfos-21-ips-hardening-syslog` สำหรับ zone-based policy

---

## 5. ค้นย้อนหลังใน Log ว่าเครื่องนั้นคุยกับใคร

คำค้น: sophos log viewer search, sophos log search ransomware, sophos firewall log, sophos log viewer
อาการ: ต้องสืบสวนว่าเครื่องที่ติด ransomware คุยกับ IP/Domain ใดบ้าง (C2, ผู้แพร่กระจาย, ผู้ถูก infect ต่อ)

ตรวจใน GUI:
- **Log viewer** → เลือก **Firewall** module — ดู firewall logs
- คลิก **Add filter** → **src_ip** — กรองตาม source IP

วิธีตรวจใน Log Viewer:
- **เปิด Log viewer:** คลิก **Log viewer** ที่มุมบนขวาของหน้าเว็บ admin
- **เลือก Module:** เลือก **Firewall** ใน module selector
- **Filter by Source IP:** คลิก **Add filter** → เลือก **src_ip** → ใส่ IP ของเครื่องที่ติดเชื้อ → **Apply**
- ดูผลลัพธ์ — จะเห็นรายการ traffic ทั้งหมดของเครื่องนั้น (source → destination, port, service, matching rule)
- **Filter by Time:** เลือก time range (เช่น 24 ชม. ก่อนหน้าเหตุการณ์)
- **Filter by Destination IP:** หากทราบ C2 IP → filter dst_ip = นั้น
- **ตรวจ Detailed View:** คลิกที่แต่ละรายการ → ดู DNS query, HTTP host, application
- **ตรวจ Web Filter Logs:** เลือก **Web filter** — ดูว่าเครื่อง access domain อะไร (อาจเจอ C2)
- **ตรวจ Malware Logs:** เลือก **Malware** — ดูว่าพบ malware ใด
- **ตรวจ Active threat response Logs:** เลือก **Active threat response** — ดู block IoC

ที่มา: [Log viewer — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Logs/LogViewer/index.html), [Logs — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/help/en-us/webhelp/onlinehelp/AdministratorHelp/Logs/index.html)

วิธีตรวจใน Syslog server / SIEM (หากต่อ):
- หากตั้งค่า syslog forwarding → log จะไปเก็บที่ syslog server / SIEM ที่รับ log
- สามารถสืบสวนเพิ่มเติมจาก centralized log viewer

หมายเหตุ: หาก log level ต่ำ — อาจไม่พบข้อมูลทั้งหมด — ให้เพิ่ม logging ใน firewall rule (เปิด Log firewall traffic) สำหรับเหตุการณ์ในอนาคต

---

## 6. สรุปลำดับการดำเนินการ (Quick Reference)

ตรวจใน GUI:
- **Rules and policies** → **Firewall rules** — ตรวจสอบ firewall rules
- **Protect** → **Active threat response** → ดู threat feeds
- **Applications** → **Application filter** — ตรวจสอบ app control
- **Log viewer** → เลือก **Firewall** — ตรวจสอบ logs

วิธีดำเนินการ:
1. **กักเครื่องทันที:** สร้าง Firewall Rule Block → Position = Top → Source = IP เครื่องที่ติดเชื้อ
2. **บล็อก IOC:** Protect → Active threat response → Third-party threat feeds → Add → Block/Monitor → Position = Top
3. **บล็อก Remote Access/Tunnel:** Application Filter → Block Remote Access + Proxy and Tunnel → ผูกกับ firewall rule
4. **บล็อก SMB/RDP/WinRM ข้ามโซน:** สร้าง Service (139, 445, 3389, 5985, 5986) → Firewall Rule Block → Position = Top
5. **สืบสวน Log:** Log viewer → Firewall → Filter src_ip = เครื่องที่ติดเชื้อ

ที่มา: [Firewall rules — Sophos Firewall 21.5](https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/RulesAndPolicies/FirewallRules/index.html)

---

คำค้น: sophos ransomware, sophos quarantine, sophos ban host, sophos active threat response, sophos third party threat feed, sophos application filter, sophos block SMB, sophos block RDP, sophos east-west, sophos log viewer, sophos firewall log
