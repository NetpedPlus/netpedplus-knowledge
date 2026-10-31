# หัวข้อที่มีอยู่แล้ว (playbook ที่มากับโปรแกรม NetPED+) — ห้ามทำซ้ำ

เลือกเรื่องใหม่ต้องไม่ซ้ำกับรายการนี้ และไม่ซ้ำกับไฟล์ใน `playbooks/` ของ repo นี้ (ถ้าอยากเติมเรื่องเดิมให้ละเอียดขึ้น ให้เปิด Issue ถามก่อน)
ไฟล์นี้สร้างจากโค้ดโปรแกรม — Claude อัปเดตเมื่อโปรแกรมเพิ่ม playbook

## F5 BIG-IP (TMOS 17.x, tmsh)
`f5-bigip-17` · families: f5_tmsh · versions: BIG-IP 17.1 / 17.5 (คำสั่ง tmsh ด้านล่างใช้ได้ตั้งแต่ 15.x)

- สุขภาพเครื่อง / license / ทรัพยากร
- HA / failover / config sync
- Virtual server / pool / monitor (เว็บเข้าไม่ได้)
- Network: interface / VLAN / self IP / route / trunk
- ICAP (ส่งไฟล์ไปสแกน เช่น Kaspersky Scan Engine)
- ตรวจความปลอดภัยของระบบ (advisory / CVE)
- Certificate หมดอายุ / SSL handshake ล้ม
- ASM / WAF บล็อกผู้ใช้ปกติ (false positive)
- iRule error / connection ถูก reset
- SNAT port หมด / connection limit
- อัปเกรด / volume / สำรอง
- Persistence (ผู้ใช้ถูกส่งไป server เดิม / ไม่กระจาย / session หลุดเมื่อสลับ server)
- Server ปลายทางไม่เห็น IP จริงของผู้ใช้ (X-Forwarded-For / SNAT)
- เก็บข้อมูลส่ง F5 support (qkview)
- CPU / หน่วยความจำสูง (control plane / TMM)
- SSL handshake ล้ม / connection ถูก reset (RST): วิธีหาสาเหตุ
- Pool member ถูก monitor ตั้งเป็น down ทั้งที่ server ปกติ
- เปลี่ยน hostname ของเครื่องที่ทำ HA (Active / Standby) โดยไม่รื้อ HA
- เปลี่ยน device name (ชื่อใน Device Management) ของคู่ HA: ต้องรื้อ device trust
- F5 HA กรณีแย่ที่สุด: Active-Active / sync ผิดทิศ / trust หาย / ต้อง restore UCS
- ASM ไม่ส่งไฟล์ไปสแกนไวรัส (ICAP เช่น Kaspersky) แบบ Integrated Services

## F5 BIG-IP 17.x สร้างระบบ (LTM + SSL + ASM)
`f5-ltm-asm-build` · families: f5_tmsh · versions: BIG-IP 17.1 / 17.5 (หลักการเดียวกันตั้งแต่ 15.x)

- ภาพรวม: สร้างเว็บผ่าน F5 ต้องทำอะไรบ้าง เรียงลำดับ
- สร้าง Node / Pool / เลือกวิธีกระจายโหลด (load balancing method)
- สร้าง Health Monitor แบบกำหนดเอง (HTTP / HTTPS send / receive)
- Virtual Server แต่ละชนิด (Standard / Performance L4 / Forwarding / ...) เลือกใช้ตอนไหน
- สร้าง Virtual Server แบบ Standard (HTTPS) และปัญหาที่ VS ขึ้น offline / ไม่ตอบ
- SNAT: Automap / SNAT pool / ไม่ทำ SNAT (server ตอบกลับไม่ผ่าน F5)
- Profiles ที่ใช้คู่ VS: tcp / http / OneConnect / X-Forwarded-For / compression
- SSL แต่ละแบบ: Offload (Termination) / Re-encryption (Bridging) / Passthrough เลือกยังไง
- Import certificate / key / chain (PEM หรือ PKCS12) และสร้าง client-ssl profile
- Server SSL profile (re-encrypt ไป server) และปัญหาฝั่ง server
- ติด cert ใหม่แล้วไม่ขึ้น / browser เตือน: chain ไม่ครบ, key ไม่ตรง, SNI, หมดอายุ
- Redirect HTTP เป็น HTTPS และ iRule / LTM policy ที่ใช้บ่อย
- สร้าง ASM / Advanced WAF security policy และผูกกับ Virtual Server
- ASM จาก Transparent ไป Blocking: learning, staging, Enforcement Readiness, ปรับ false positive
- ส่วนเสริมของ WAF: Bot Defense / DoS / IP Intelligence / Logging profile

## F5 BIG-IP 17.x งานระบบจริง (เครื่องใหม่ / HA / ASM ขั้นสูง / TLS / Monitoring)
`f5-ops-advanced` · families: f5_tmsh · versions: BIG-IP 17.1 / 17.5 (หลักการเดียวกันตั้งแต่ 14.x)

- เตรียมเครื่องใหม่: license / provisioning / management / VLAN / self IP / gateway
- Trunk / LACP ต่อกับ switch (port-channel / Eth-Trunk)
- Self IP แบบ floating / non-floating และ Port Lockdown
- สร้าง HA แบบ Active / Standby ตั้งแต่ต้น (device trust, ConfigSync, failover, device group)
- ASM ในคู่ HA: sync policy / signature ระหว่างเครื่อง
- ทยอยขึ้น Blocking ทีละ application: checklist ก่อนขึ้น / หลังขึ้น / ถอยกลับ
- Attack signature: signature set, staging, เปิด / ปิดเฉพาะตัว และอัปเดต (Live Update)
- ASM entity: URL / parameter / file type / JSON content profile (API, อัปโหลดไฟล์)
- Brute force ป้องกันหน้า login (Login Page + Brute Force Attack Prevention)
- Data Guard: ปิดบังข้อมูลสำคัญในหน้าเว็บ (บัตรเครดิต / เลขบัตร / pattern เอง)
- สำรอง / ย้าย / เทียบ ASM policy: Export / Import / Policy Diff
- TLS hardening: cipher rule / cipher group / ปิด TLS เก่า / HSTS
- ส่ง log ออก: remote syslog ของระบบ และ high-speed logging (ASM / SIEM เช่น QRadar)
- SNMP: ให้ระบบ monitor (Zabbix / PRTG) อ่านค่า และส่ง trap
- AVR (Analytics): ดูสถิติเว็บ ช้าตรงไหน / URL ไหนโดนเยอะ

## FortiGate (FortiOS 7.4)
`fortigate-74` · families: fortinet_fortios · versions: FortiOS 7.4.x (ทดสอบตามเอกสาร 7.4; 7.2 ใช้ได้เกือบทั้งหมด ยกเว้นตัวกรอง IKE debug)

- สุขภาพเครื่อง / HA
- Interface / LAG / ลิงก์
- เส้นทาง / routing protocol
- traffic ไม่ผ่าน: policy lookup และ debug flow
- IPsec VPN (site-to-site)
- SD-WAN / health check
- เวลา / NTP / license / FortiGuard
- Conserve mode / หน่วยความจำเต็ม
- HA ประวัติการสลับ / split brain
- ส่ง log ไป FortiAnalyzer / syslog ไม่ได้
- FortiGuard / web filter / license
- เข้าหน้าจัดการ (GUI / SSH) ไม่ได้
- NAT / IP pool เต็ม
- อัปเกรด firmware / สำรอง config
- SSL VPN ผู้ใช้ต่อไม่ได้ / หลุด / ช้า
- VIP / port forward (เปิดบริการจากภายนอก) ใช้ไม่ได้
- DHCP server บน FortiGate
- CPU / หน่วยความจำสูง (ขั้นตอนตาม Fortinet)
- FSSO (ผู้ใช้ AD) ไม่ขึ้นชื่อ / policy ตามกลุ่มไม่ทำงาน
- LDAP / AD ยืนยันตัวตนไม่ผ่าน (admin, SSL VPN, firewall auth)
- BGP neighbor ไม่ขึ้น / หลุดเป็นรอบ (flap)
- debug flow: แปลข้อความ drop แล้วแก้ (ตาม Fortinet)
- IPsec: อ่านข้อความใน IKE debug (ตาม Fortinet)

## Huawei Wireless AC (AC6000 / AirEngine 9700)
`huawei-ac-wlan` · families: huawei_ac · versions: WLAN AC V200R019C00 ขึ้นไป (AC6005 / AC6508 / AC6605 / AC6805 / AC6800V / AirEngine 9700)

- AP ไม่ online / สถานะไม่ใช่ normal
- AP หลุดเอง / ขึ้นลงบ่อย
- ผู้ใช้ (STA) เชื่อมต่อ Wi-Fi ไม่ได้
- ผู้ใช้ต่อ Wi-Fi ได้แต่ไม่ได้ IP / ใช้งานไม่ได้
- ยืนยันตัวตน 802.1X / Portal ไม่ผ่าน (RADIUS)
- AC สำรอง (HSB / hot standby) ไม่ sync / สลับเครื่อง
- license / จำนวน AP
- อัปเกรด AC / AP
- AP หลุดเพราะ heartbeat timeout (Echo timeout): ขั้นตอนตาม Huawei
- RADIUS ยืนยันตัวตนไม่ผ่าน (NCE / NPS เป็น RADIUS): ไล่ฝั่ง AC ทีละขั้นตาม Huawei
- ผู้ใช้ Wi-Fi หลุดเอง: ไล่ตามเหตุผลที่ AC บันทึก
- Wi-Fi ช้า / ความเร็วเชื่อมต่อต่ำ: ขั้นตอนตาม Huawei
- คลื่นรบกวน / ช่องสัญญาณชน / hidden node: ขั้นตอนตาม Huawei

## Huawei S12700E / S5731 (VRP V200)
`huawei-vrp-switch` · families: huawei_vrp_s · versions: VRP V200R019C00 – V200R025C00

- สุขภาพเครื่อง: CPU / memory / พัดลม / power / อุณหภูมิ
- Interface down / flap / CRC / error-down
- Eth-Trunk / LACP
- VLAN / MAC / ARP (เครื่องปลายทางใช้งานไม่ได้)
- Loop / broadcast storm / STP / MAC flapping
- OSPF neighbor ไม่ขึ้น / หลุด
- BGP peer ไม่ขึ้น / route ไม่มา
- เส้นทาง / ping / traceroute
- Stack: CSS (S12700E) / iStack (S5731)
- 802.1X / MAC / Portal / RADIUS (NAC)
- Log และหลักฐานสำหรับเปิดเคส
- PoE: AP / กล้อง / IP phone ไม่ติด (S5731-H48P4XC เป็นรุ่น PoE)
- VRRP: gateway สำรองไม่ทำงาน / สลับไปมา
- เข้า SSH / จัดการเครื่องไม่ได้
- SNMP / ระบบ monitor (เช่น Zabbix) ดึงค่าไม่ได้
- เวลา / NTP
- DHCP snooping / relay / IP ชนกัน
- MTU / packet ใหญ่ผ่านไม่ได้
- อัปเกรด / แพตช์ / ไฟล์ระบบ
- CPU สูง / ARP attack / packet ขึ้น CPU มากเกิน (cpu-defend)
- MAC flapping / loop: ขั้นตอนตาม Huawei
- RADIUS ยืนยันตัวตนไม่ผ่าน (เช่น NCE / NPS เป็น RADIUS): ไล่ฝั่งอุปกรณ์ทีละขั้นตาม Huawei
- Stack / CSS ตั้งไม่ขึ้น หรือสมาชิกไม่เข้า stack: ขั้นตอนตาม Huawei
- การ์ด / subcard / MPU / LPU ไม่ register (Unregistered / Abnormal)
- SSH เข้า switch ไม่ได้: ขั้นตอนตาม Huawei
- OSPF neighbor ไม่ขึ้น: ไล่ตามสถานะที่ค้าง (ขั้นตอนตาม Huawei)
- Interface ไม่ up (พอร์ตทองแดง / ทั่วไป): ขั้นตอนตาม Huawei
- Interface ไม่ up (พอร์ตแสง / SFP): ขั้นตอนตาม Huawei
- ping ไม่ผ่าน: ไล่ทีละชั้นตาม Huawei

## Huawei iMaster NCE-Campus / CampusInsight
`imaster-nce-campus` · families: vendor: Huawei · versions: iMaster NCE-Campus V300R0xx + CampusInsight (บน FusionInsight)

- บริการของ NCE / Insight ล่ม หรือหน้าเว็บใช้ไม่ได้
- CampusInsight ไม่มีข้อมูลเข้า dashboard / ZooKeeper AuthFailed
- อุปกรณ์ offline ใน NCE / จัดการอุปกรณ์ไม่ได้
- ผู้ใช้ยืนยันตัวตนไม่ผ่าน (NCE เป็น RADIUS / authentication)
- สำรองข้อมูล NCE / Insight
- certificate / license ของ NCE ใกล้หมดอายุ
- AP ขึ้น / ลงบ่อย หรือผู้ใช้ Wi-Fi หลุด (ดูจาก NCE / Insight)
- เพิ่ม / อัปเกรดระบบ NCE (เตรียมก่อนทำ)
- NCE เป็น RADIUS แล้วผู้ใช้ยืนยันตัวตนไม่ผ่าน / หลุดเพราะ accounting
- CampusInsight ได้ข้อมูลจากไหน (ใช้ไล่ "dashboard ว่างบางส่วน")
- อุปกรณ์ / AP ขึ้น NCE ไม่ได้ (ลงทะเบียน / cloud-mng / NETCONF)

## Kaspersky Scan Engine (ICAP mode)
`kaspersky-scan-engine` · families: vendor: Kaspersky · versions: Kaspersky Scan Engine 2.x บน Linux (ICAP mode)

- บริการ ICAP ไม่ทำงาน / F5 ส่งไฟล์ไปสแกนไม่ได้
- ทดสอบว่าตรวจจับได้จริง (EICAR)
- ฐานข้อมูลไวรัส / license
- log ของ scan engine
- สแกนช้า / ไฟล์ใหญ่ timeout / อัปโหลดล้มผ่าน F5
- false positive (ไฟล์ปกติถูกบล็อก)
- พฤติกรรมของ ICAP ที่ควรรู้ตอนไล่ปัญหากับ F5 / proxy

## Palo Alto (PAN-OS) — ตรวจอย่างเดียว
`paloalto-panos` · families: paloalto_panos · versions: PAN-OS 10.1 – 11.x (คำสั่ง operational mode)

- สุขภาพเครื่อง / HA
- traffic ไม่ผ่าน / ถูก drop
- เส้นทาง
- IPsec VPN กับปลายทางต่างยี่ห้อ (เช่น FortiGate)
- GlobalProtect (ผู้ใช้ VPN)
- commit / งานค้าง / ประวัติการเปลี่ยนแปลง
- User-ID / ระบุชื่อผู้ใช้ไม่ได้
- หาว่าเครื่องหนึ่งมี session อะไรอยู่
- license / dynamic update / พื้นที่ดิสก์
- NAT ไม่ตรงตามที่คาด / IP pool ของ NAT เต็ม
- GlobalProtect: ผู้ใช้ต่อไม่ได้ / ผ่าน portal แต่ไม่ผ่าน gateway
- IPsec: อ่าน error ใน ikemgr log
- traffic ของคู่ IP เดียวไม่ผ่าน: ดู global counter เฉพาะ flow นั้น (packet filter)

## IBM QRadar SIEM 7.5
`qradar-75` · families: vendor: IBM · versions: QRadar 7.5.0 (Update Packages / Patch)

- log source หยุดส่ง / "Device Stopped Sending Events"
- event เป็น Unknown / parse ผิด / log source ผิด DSM
- EPS / license / event ถูกทิ้ง
- สุขภาพระบบ / เวอร์ชัน / บริการ
- offense / กฎ (rule) ไม่ทำงานหรือเตือนมากเกิน
- disk เต็ม / retention
- อีเมลแจ้งเตือนไม่ส่ง
- managed host / deploy changes ล้ม
- WinCollect / log จาก Windows ไม่เข้า
- อัปเดต / แพตช์ QRadar
- ค้นด้วย AQL (Log Activity > Advanced Search)
- แจ้งเตือน "Events routed directly to storage" (38750088)
- แจ้งเตือน "Expensive custom rules found in CRE" (38750120)

## Routing ข้ามอุปกรณ์ (Huawei / FortiGate / Palo Alto)
`routing-concepts` · families: huawei_vrp_s, huawei_ce, fortinet_fortios, paloalto_panos · versions: Huawei VRP V200, FortiOS 7.4, PAN-OS 10.1 – 11.x

- route ขาไป / ขากลับไม่ตรงกัน (asymmetric) ผ่าน firewall
- MTU / MSS ในเส้นทางที่มี tunnel (IPsec / GRE / PPPoE)
- default route / เส้นทางสำรองไม่สลับเมื่อเส้นหลักล่ม
- redistribute / route loop / route แกว่ง
- PBR / policy route บังคับเส้นทางผิด
- ECMP / ใช้หลายเส้นพร้อมกัน

## Sophos Firewall (SFOS) / XGS
`sophos-sfos-21` · families: sophos_sfos · versions: SFOS 20.0 – 21.5 (บางหัวข้ออ้างบทความของ SFOS 22 ที่ใช้คำสั่งชุดเดียวกัน)

- สุขภาพเครื่อง / CPU / RAM / disk / เวอร์ชัน
- HA (Active-Passive) สถานะ / สลับเครื่อง / sync
- IPsec site-to-site ไม่ขึ้น / หลุด
- traffic ไม่ผ่าน / ถูก drop / ไม่รู้ว่าตรง rule ไหน
- routing / SD-WAN route / ลำดับความสำคัญของ route
- เข้า Web Admin / SSH ไม่ได้
- DNS / ping / ทดสอบจากตัว firewall
- Web filter / proxy / antivirus บล็อกผิด หรือขึ้น Unscannable
- ผู้ใช้ขึ้น Unidentified / AD SSO (STAS) / authentication
- SSL VPN / remote access
- DHCP บน firewall
- อัปเกรด firmware / สำรองข้อมูล
- เปิดบริการ (DNAT / server ภายใน) จากภายนอกไม่ได้
- SSL VPN remote access: ต่อไม่ได้ / ต่อได้แต่ใช้งานไม่ได้ / หลุดบ่อย
- STAS (AD SSO) ผู้ใช้ไม่ถูกระบุ / หายเป็นช่วง: เช็กลิสต์ตาม Sophos
- IPsec: ข้อความใน log แปลว่าอะไร / ต่อได้แต่ traffic หยุด (ตาม Sophos)

## Windows Server — Active Directory / DNS / DHCP / NPS
`windows-ad-dhcp-dns` · families: vendor: Microsoft, Windows · versions: Windows Server 2016 / 2019 / 2022 (PowerShell 5.1)

- Domain controller / replication
- บัญชีถูกล็อก / ล็อกอินไม่ผ่าน
- DNS ไม่ resolve / resolve ผิด
- DHCP ไม่แจก IP / scope เต็ม
- NPS (RADIUS สำหรับ 802.1X / VPN) ปฏิเสธผู้ใช้
- เวลาไม่ตรง (Kerberos / ล็อกอินล้มทั้งองค์กร)
- GPO ไม่มีผลกับเครื่อง / ผู้ใช้
- DHCP failover / server สองตัว
- FSMO / DC ตัวหลักหาย
- DNS record เก่าค้าง / ชื่อชี้ IP เก่า (aging / scavenging)
- AD replication error 1722 (The RPC server is unavailable)
- AD replication error อื่นที่พบบ่อย (8524, 8453, 8614, 1908, 1396, -2146893022)
- NPS ปฏิเสธ / ไม่มี log เลย: ขั้นตอนตาม Microsoft
