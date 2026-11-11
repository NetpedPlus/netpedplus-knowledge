---
id: f5-bigip-17-ssl-handshake-troubleshooting
title: F5 BIG-IP 17.x — SSL Handshake Fail
families: f5_tmsh
triggers: f5 ssl handshake fail, f5 handshake failure, f5 no shared ciphers
versions: BIG-IP 17.5.x
sources: https://my.f5.com/manage/s/article/K15292, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_profile_client-ssl.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_log.html
---

# F5 BIG-IP 17.x — SSL Handshake Fail

## ตรวจ cipher ใน Client SSL profile และสาเหตุช่วงเจรจา

คำค้น: f5 SSL handshake fail, f5 no shared ciphers, f5 cipher configuration, f5 client-ssl profile, f5 list ltm profile client-ssl, handshake ไม่ผ่าน, ssl ไม่ผ่าน, cipher ไม่ตรง, เปิด https ไม่ได้

ที่มา: https://my.f5.com/manage/s/article/K15292 (Negotiation stage), https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_profile_client-ssl.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_log.html

"If the client and server do not agree on the complete list of options, the handshake will fail, often with very little diagnostic data." — K15292, Negotiation stage

"If the server does not support the ciphers from the client's list, the connection is terminated." — K15292, Negotiation stage

"Client-side profiles allow the traffic management system to handle authentication and encryption tasks for any SSL connection coming into a traffic management system from a client system." — ltm_profile_client-ssl.html, DESCRIPTION section

tmsh reference `ltm_profile_client-ssl.html` DISPLAY section เขียนชื่อคำสั่งแบบละ module: `list client-ssl` และ `show client-ssl` (คำสั่งเต็ม: `list ltm profile client-ssl`, `show ltm profile client-ssl`)

"Specifies a cipher name. The default value is DEFAULT, which uses the default ciphers." — ltm_profile_client-ssl.html, OPTIONS section → ciphers

"Specifies a cipher group. If the cipher group is not blank or none, the ciphers string will be used." — ltm_profile_client-ssl.html, OPTIONS section → cipher-group

คำสั่งตรวจ:
```
list ltm profile client-ssl
show ltm profile client-ssl
```

---

## Log ของ SSL handshake failure

คำค้น: f5 SSL handshake fail, f5 log, f5 01260026, f5 01260014, f5 01260009, f5 show sys log ltm, log handshake, ssl ดู log ที่ไหน

ที่มา: https://my.f5.com/manage/s/article/K15292 (Reviewing log messages related to SSL handshake failures, Enabling SSL debug logging), https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_log.html

"Beginning in 12.0.0, the BIG-IP system automatically logs SSL handshake failure information through standard logging; the use of debug logging for SSL handshake failures is not required." — K15292, Enabling SSL debug logging section

ตาราง SSL message / Description (K15292, Reviewing log messages related to SSL handshake failures section):

| SSL message | Description |
|---|---|
| 01260014:3: Cipher <cipher> negotiated is not configured in profile <profile_name> | The cipher negotiated by the client and server is not supported in one of the SSL profiles |
| 01260026:4: No shared ciphers between SSL peers <client_IP>:<server_IP> | None of the SSL ciphers sent by the client match the configured ciphers in the Client SSL profile. This error can occur when an older SSL client using a less secure cipher attempts to connect to the virtual server |

The client and server unsuccessfully negotiate the protocol version:

"debug tmm3[9261]: 01260009:7: Connection error: ssl_hs_rxhello:4409: unsupported version (70)" — K15292, Enabling SSL debug logging section

The client and server unsuccessfully negotiate a cipher:

"debug tmm1[9261]: 01260009:7: Connection error: ssl_select_suite:4133: no shared ciphers (40)" — K15292, Enabling SSL debug logging section

หมายเหตุ: หน้า tmsh `sys_log.html` DISPLAY section เขียนชื่อคำสั่งแบบละ module: `show log` (คำสั่งเต็ม: `show sys log ltm` เพื่อแสดง LTM log)

"Displays a list of logs that you can view." — sys_log.html, EXAMPLES section

คำสั่งตรวจ:
```
show sys log ltm
```

ไม่พบที่มา — ตรวจ K15292, ltm_profile_client-ssl.html, sys_log.html แล้ว:
วิธีแก้ cipher ใน Client SSL profile — ไม่พบแหล่งที่มา
Server SSL profile handshake กับ pool member — ไม่พบแหล่งที่มา
ใบรับรองหมดอายุ/ไม่ตรง — ไม่พบแหล่งที่มา
K15292 มีหัวข้อทดสอบด้วย openssl s_client และ ssldump แต่ไม่ได้นำมาใส่ เพราะเป็นคำสั่ง bash
