---
id: f5-bigip-17-ssl-certificate-expiry
title: F5 BIG-IP 17.x — ตรวจวันหมดอายุใบรับรอง SSL
families: f5_tmsh
triggers: certificate expired, ใบรับรองหมดอายุ, ssl certificate expiration, cert expiry, check-cert
versions: BIG-IP 17.5.x
sources: https://my.f5.com/manage/s/article/K14318 (Monitoring SSL certificate expiration on the BIG-IP system), https://my.f5.com/manage/s/article/K000161643 (Overview of BIG-IP certificate renewal with keymgmtd), https://my.f5.com/manage/s/article/K000159955 (SSL certificate intermittently appears expired after renewal), https://my.f5.com/manage/s/article/K15462 (Managing SSL certificates for BIG-IP systems using tmsh)
---

# F5 BIG-IP 17.x — ตรวจวันหมดอายุใบรับรอง SSL

## ตรวจวันหมดอายุของใบรับรอง SSL ใน GUI และ check-cert

คำค้น: f5 certificate expiration, f5 ssl certificate list, f5 check-cert, f5 show sys crypto cert, f5 show sys crypto cert-order-manager, f5 show cm sync-status

ที่มา: https://my.f5.com/manage/s/article/K14318 (Monitoring SSL certificates using Configuration utility and tmsh), https://my.f5.com/manage/s/article/K000161643, https://my.f5.com/manage/s/article/K000159955, https://my.f5.com/manage/s/article/K15462 (View properties of an SSL certificate), https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_crypto_check-cert.html

"Performing the following procedure should not have a negative impact on your system." — K14318, Impact of procedure

"Go to System > Certificate Management > Traffic Certificate Management > SSL Certificate List." — K14318, BIG-IP 13.0.0 and later

"Under Expiration, look for the following SSL certificate expiration indicators: Red exclamation icons indicate expired certificates, yellow exclamation icons indicates expiration within 30 days." — K14318, Expiration indicators

"The check-cert command checks for SSL certificates that have expired or will expire within 30 days." — K14318, Monitoring the expiration of SSL certificates using tmsh

"The system prints expiration information to the screen and logs it to the /var/log/ltm file, for up to five expired certificates." — K14318, Monitoring the expiration of SSL certificates using tmsh

"The check-cert command automatically runs on a weekly schedule; the system calls the command from the /etc/cron.weekly/5checkcert file." — K14318, Monitoring the expiration of SSL certificates using tmsh

"run /sys crypto check-cert" — K14318, Monitoring the expiration of SSL certificates using tmsh (วางเอง)

"run /sys crypto check-cert verbose enabled" — K14318, Viewing the expiration dates of all SSL certificates using tmsh (วางเอง)

"To view the SSL certificate properties, use the following command syntax:" — K15462, View properties of an SSL certificate
list sys crypto cert <cert name> — K15462, View properties of an SSL certificate (ข้อความธรรมดา)

ตรวจใน GUI: System > Certificate Management > Traffic Certificate Management > SSL Certificate List

## ใบรับรองต่ออายุอัตโนมัติด้วย keymgmtd

คำค้น: f5 certificate auto-renewal, f5 keymgmtd, f5 cert-order-manager, f5 certificate mismatch key

ที่มา: https://my.f5.com/manage/s/article/K000161643 (Overview of BIG-IP certificate renewal with keymgmtd)

"Certificate auto-renewal starts 14 days prior to expiry with tiered retries that never give up." — K000161643, Topic

"Manually imported certificates: you must track and rotate these yourself." — K000161643, Topic

"Failed to install certificate due to mismatch of the certificate with key" — K000161643, Certificate and private key verification

"To show counts of successful, failure and pending orders, enter tmsh show sys crypto cert-order-manager." — K000161643, Topic, footnote 1

ตรวจใน GUI: Big-IP GUI -> System -> Certificate Management

คำสั่งตรวจ:
```
show sys crypto cert-order-manager
```

## หลังต่ออายุแล้วยังขึ้นหมดอายุเป็นพัก ๆ (HA ไม่ sync)

คำค้น: f5 certificate appears expired after renewal, f5 HA sync certificate, f5 changes pending, f5 show cm sync-status

ที่มา: https://my.f5.com/manage/s/article/K000159955 (SSL certificate intermittently appears expired after renewal on a BIG-IP virtual server), https://my.f5.com/manage/s/article/K14624

"The root cause is unsynchronized certificate configuration between the active and standby BIG-IP LTM devices." — K000159955, Cause

"Check for \"Changes Pending\" status, which indicates unsynchronized configuration." — K000159955, Recommended Actions

tmsh reference บทความเขียนคำสั่ง tmsh show /cm sync-status คำสั่งเต็มคือ show cm sync-status

คำสั่งตรวจ:
```
show cm sync-status
```

ขั้นตอน config-sync จริงดูที่ playbook f5-bigip-17-ha-config-sync

ไม่พบที่มา — ตรวจ K14318, K000161643, K000159955, K15462, sys_crypto_check-cert.html, sys_crypto_cert.html แล้วไม่พบ:
คำสั่ง list/show ใบรับรองทั้งหมดที่ไม่มี placeholder — ตรวจ sys_crypto_cert.html แล้วไม่มี DISPLAY section
ขั้นตอนต่ออายุ/สร้างใบรับรองใหม่ — ตรวจแล้วเป็นการแก้ไข ไม่ใช่การตรวจ
K15288 (แจ้งเตือนอีเมลล่วงหน้า) — ตรวจแล้วไม่พบในเอกสารชุดนี้
