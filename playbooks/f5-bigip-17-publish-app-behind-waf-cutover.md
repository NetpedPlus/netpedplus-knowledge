---
id: f5-bigip-17-publish-app-behind-waf-cutover
title: F5 BIG-IP 17.x — เผยแพร่แอปหลัง F5 (SNAT, XFF, จำกัด IP) ก่อน cutover
families: f5_tmsh
triggers: f5 snat, snat automap, x-forwarded-for, xff, asymmetric routing, one-armed, class match, data group, iRule จำกัด IP, cutover, publish app, waf, firewall snat
versions: BIG-IP 17.5.x
sources: https://my.f5.com/manage/s/article/K7820, https://my.f5.com/manage/s/article/K7336, https://my.f5.com/manage/s/article/K4816, https://my.f5.com/manage/s/article/K40243113, https://my.f5.com/manage/s/article/K20510467, https://my.f5.com/manage/s/article/K42075438
---

# F5 BIG-IP 17.x — เผยแพร่แอปหลัง F5 (SNAT, XFF, จำกัด IP) ก่อน cutover

---

## SNAT: ทำไมต้องมี และ server ตอบกลับทางไหน

คำค้น: f5 snat ทำไม, f5 asymmetric routing, f5 one-armed, f5 server ตอบกลับตรงไป client

ที่มา: K7820 (https://my.f5.com/manage/s/article/K7820) Applies to BIG-IP LTM มี 17.5.1, 17.5.0, 17.5.X

"You can also use a SNAT to ensure that response traffic is returned through the BIG-IP system without requiring other outbound non-load balanced traffic to also route through the BIG-IP system, and without requiring any changes in the router or server's configuration." — K7820

"SNAT is also a critical component in one-armed configurations, preventing the server from responding directly to the client." — K7820

"The SNAT translates the source IP address of the packet to the SNAT address so that the external device routes the reply packet back to the BIG-IP system." — K7820

"You can monitor the number of concurrent connections going through the SNAT by running the tmsh show /ltm snat command" — K7820

หมายเหตุ: ต้นฉบับเขียน tmsh show /ltm snat ในบล็อกด้านล่างใช้รูป show ltm snat ที่ NetPED+ รันได้ ไม่พบที่มา: คำว่า "asymmetric" ในต้นฉบับ K7820 (ข้อสรุปว่าไม่ทำ SNAT แล้ว backend ตอบกลับผ่าน gateway ของตัวเองอยู่ในหัวข้อหลักการออกแบบท้ายไฟล์)

คำสั่งตรวจ:
```
show ltm snat
```

---

## SNAT Automap เลือก IP อย่างไร

คำค้น: f5 snat automap เลือก self ip, f5 automap floating self ip, f5 automap egress vlan

ที่มา: K7336 (https://my.f5.com/manage/s/article/K7336) Applies to BIG-IP LTM มี 17.5.1, 17.5.0, 17.5.X

"The SNAT Automap feature selects a translation address from the available self IP address in the following order of preference:" — K7336, Topic

ลำดับตามต้นฉบับ K7336: (1) Floating self IP addresses on the egress VLAN (2) Floating self IP addresses on different VLANs (3) Non-floating self IP addresses on the egress VLAN (4) Non-floating self IP addresses on different VLANs

"However, depending on the network routing configuration, selection of a self IP other than the egress VLAN may cause traffic disruption." — K7336

"F5 recommends that you ensure that you have configured floating self IP addresses on all VLANs from which you expect SNAT traffic to egress." — K7336

ตรวจใน GUI: ไม่พบที่มาของเมนูใน K7336 ที่มาของ IP ที่ใช้แปลเป็นรายการ self IP ของ VLAN ขาออก

ไม่พบที่มา: K7336 ไม่ได้ระบุ source IP ของ health monitor ว่าใช้ self IP ตัวใด

---

## X-Forwarded-For ใน HTTP profile

คำค้น: f5 insert x-forwarded-for, f5 xff http profile, f5 xff ปลอม, f5 client ip ที่ server

ที่มา: K4816 (https://my.f5.com/manage/s/article/K4816) และ K40243113 (https://my.f5.com/manage/s/article/K40243113) Applies to BIG-IP LTM ทั้ง 2 มี 17.5.1, 17.5.0, 17.5.X

"When the BIG-IP system translates the source IP address of the incoming packet to the SNAT address, the web server sees the request as originating from the SNAT address, not the original client IP address." — K4816

"The BIG-IP system inserts only a single HTTP X-Forwarded-For header. If there is an existing X-Forwarded-For header in the request, the BIG-IP appends the client IP address to the end." — K4816

ตัวอย่างในต้นฉบับ K4816: X-Forwarded-For: 192.0.2.1, 198.51.100.1

"Note: In BIG-IP 13.0.0 and earlier, if there is an existing X-Forwarded-For header in the request, the system appends a new X-Forwarded-For header." — K4816

"Note: You can insert HTTP headers in HTTPS traffic only if the client connects to a BIG-IP virtual server configured with a Client SSL profile." — K4816

ตรวจใน GUI: Local Traffic > Profiles จากนั้น For Services เลือก HTTP แล้วเปิด profile ดูตัวเลือก Insert X-Forwarded-For (ที่มา K4816)

ไม่พบที่มา: ประโยคใน K4816 และ K40243113 ที่บอกว่า profile ลบค่า X-Forwarded-For ที่ client ส่งมา (ต้นฉบับบอกว่าต่อท้าย) และ iRule ที่ remove แล้ว insert ไม่มีประโยคใน PDF ที่อ่าน

---

## จำกัด IP ด้วย iRule และ data group

คำค้น: f5 irule class match, f5 data group ip, f5 ip client_addr, f5 จำกัด ip virtual server

ที่มา: K20510467 (https://my.f5.com/manage/s/article/K20510467) Applies to BIG-IP LTM มี 17.5.0, 17.5.X และ K42075438 (https://my.f5.com/manage/s/article/K42075438) Applies to BIG-IP LTM มี 17.5.1, 17.5.0, 17.5.X

"The IP::client_addr command returns the source IP address of the client." — K20510467
"The class match command searches the entries in a data group." — K20510467

"if { [class match [IP::client_addr] equals internal_IP] } {" — K20510467, ตัวอย่างใน iRule

"You can restrict access to a virtual server based on the IP address of the client." — K42075438, Description

"If you want to allow access only from a specific IP address or network, you can configure the Source Address setting for the virtual server with the allowed IP addresses." — K42075438

"You can use iRules to restrict virtual server access based on the client IP address." — K42075438

ตรวจใน GUI: ไม่พบที่มาของเมนูตรวจ iRule และ data group ในไฟล์ที่ใช้ในหัวข้อนี้

---

## หลักการออกแบบจากประสบการณ์ของ Nut (ไม่ใช่ประโยคของ F5)

คำค้น: f5 snat asymmetric ไม่ผ่าน f5, f5 xff ปลอม, f5 firewall snat irule admin fail-open, f5 ทดสอบ vs ก่อน cutover

ที่มา: ประสบการณ์ของ Nut ไม่ใช่เอกสารของ F5 และยังไม่มีลิงก์ของ vendor รองรับ

ข้อความในหัวข้อนี้ไม่ได้มาจากประโยคของ F5 และ Nut ต้องยืนยันก่อนใช้งานจริง

- ถ้า VS กับ backend อยู่คนละ VLAN ที่ F5 มี self IP ทั้งคู่ และไม่ทำ SNAT backend จะตอบกลับผ่าน gateway ของตัวเอง ไม่ผ่าน F5 ทำให้ routing ไม่สมมาตรและ connection ใช้ไม่ได้
- Insert X-Forwarded-For ใน HTTP profile ไม่ลบ X-Forwarded-For ที่ client ส่งมา จึงถูกปลอมได้ iRule ที่ remove แล้ว insert ปลอดภัยกว่า
- ถ้า firewall ด้านหน้าทำ SNAT ขาเข้า และใช้ iRule จำกัด admin ตาม IP ผู้ใช้ internet ทุกคนจะถูกมองเป็น IP ภายใน ทำให้ admin เปิดออก internet (fail-open) วิธีแก้คือปิด NAT ใน policy ของ VIP ห้ามแก้ด้วยการใส่ IP หลัง SNAT ลงใน data group
- ทดสอบ VS ก่อน cutover ด้วย curl --resolve host:443:VIP หรือไฟล์ hosts และเพื่อจำลองว่ามาจากภายนอก ให้เอา subnet ของเครื่องทดสอบออกจาก data group ชั่วคราว ไม่มีเมนู "Test with different IP address"

ตรวจใน GUI: ไม่มี หัวข้อนี้เป็นหลักการออกแบบ ไม่ใช่ขั้นตอนตรวจ

---

ไม่พบที่มา
- ASM: wildcard URL แบบ [HTTP] เทียบ [HTTPS] (Differentiate between HTTP and HTTPS URLs) ไม่พบคู่มือ 17.5.x ที่เปิดอ่านได้
- ASM: ลำดับ Wildcards Order ของ URL ไม่พบที่มา
- ASM: File type, URL length, Request length และ violation "Request length exceeds defined buffer size" ไม่พบที่มา ห้ามตอบเป็นตัวเลข KB หรือ MB
- วิธีทดสอบ VS ก่อน cutover ไม่พบใน K-article ที่อ่าน
