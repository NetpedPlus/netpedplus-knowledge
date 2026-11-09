---
id: f5-bigip-17-ssl-handshake-troubleshooting
title: SSL Handshake Fail — Troubleshooting
families: f5_tmsh
triggers: f5 SSL handshake fail, f5 handshake failure, f5 no shared ciphers, f5 SSL/TLS negotiation failure
versions: BIG-IP 17.5.x
sources: https://my.f5.com/manage/s/article/K15292, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_profile_client-ssl.html
---

# SSL Handshake Fail — Troubleshooting

ที่มา: K15292 (https://my.f5.com/manage/s/article/K15292 — Applies to: BIG-IP LTM 17.5.1, 17.5.0) และ tmsh reference v17.0.0 (ltm_profile_client-ssl.html)

## 1. ตรวจ pool และ monitor status

คำค้น: f5 SSL handshake fail, f5 show ltm virtual, f5 list ltm virtual

ที่มา: https://my.f5.com/manage/s/article/K15292 (Negotiation stage), https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_virtual.html

อาการ: SSL/TLS handshake ล้มเหลวระหว่าง negotiation stage เมื่อ client และ server ไม่ตกลง protocol/cipher ที่ใช้ร่วมกันได้

"If the client and server do not agree on the complete list of options, the handshake will fail, often with very little diagnostic data." — K15292, Negotiation stage

"If the server does not support the ciphers from the client's list, the connection is terminated." — K15292, Negotiation stage

คำสั่งตรวจ:
```
show ltm virtual
list ltm virtual
```

---

## 2. ตรวจ log / SSL handshake failure messages

คำค้น: f5 SSL handshake failure log, f5 /var/log/ltm, f5 ssl error log

ที่มา: https://my.f5.com/manage/s/article/K15292 (Reviewing log messages related to SSL handshake failures, Enabling SSL debug logging)

"Beginning in 12.0.0, the BIG-IP system automatically logs SSL handshake failure information through standard logging; the use of debug logging for SSL handshake failures is not required." — K15292, Enabling SSL debug logging section

ตาราง SSL message / Description (K15292, Reviewing log messages related to SSL handshake failures section):

| SSL message | Description |
|---|---|
| 01260014:3: Cipher <cipher> negotiated is not configured in profile <profile_name> | The cipher negotiated by the client and server is not supported in one of the SSL profiles |
| 01260026:4: No shared ciphers between SSL peers <client_IP>:<server_IP> | None of the SSL ciphers sent by the client match the configured ciphers in the Client SSL profile. This error can occur when an older SSL client using a less secure cipher attempts to connect to the virtual server |

ตัวอย่าง log 01260009:7 — Unsupported version:

"The client and server unsuccessfully negotiate the protocol version: debug tmm3[9261]: 01260009:7: Connection error: ssl_hs_rxhello:4409: unsupported version (70)" — K15292, Enabling SSL debug logging section

ตัวอย่าง log 01260009:7 — No shared ciphers:

"The client and server unsuccessfully negotiate a cipher: debug tmm1[9261]: 01260009:7: Connection error: ssl_select_suite:4133: no shared ciphers (40)" — K15292, Enabling SSL debug logging section

คำสั่งตรวจ:
```
tail -f /var/log/ltm
```

---

## 3. ทดสอบการเชื่อมต่อ SSL

คำค้น: f5 openssl s_client, f5 ssldump, f5 SSL connection test

ที่มา: https://my.f5.com/manage/s/article/K15292 (Testing SSL connections, Packet tracing using the ssldump utility)

"To test SSL connections for the virtual server, use the following command syntax: openssl s_client -connect <virtual_server>:<port>" — K15292, Testing SSL connections (using s_client) section

"The ssldump utility is a protocol analyzer for SSL that identifies TCP connections from a chosen packet trace or network interface and attempts to interpret the packets as SSL traffic. When the ssldump utility identifies SSL traffic, it decodes the records and displays them in text to standard output." — K15292, Packet tracing using the ssldump utility section

หมายเหตุ: openssl s_client และ ssldump เป็นคำสั่ง bash ที่ต้องใช้ placeholder จึงไม่ได้นำมาใส่ในบล็อกคำสั่งตรวจ

คำสั่งตรวจ:
```
(no tmsh command - bash utilities openssl s_client / ssldump only)
```

---

## 4. ตรวจ Cipher ใน Client SSL profile

คำค้น: f5 client-ssl profile, f5 cipher configuration, f5 list ltm profile client-ssl

ที่มา: https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_profile_client-ssl.html (DESCRIPTION, OPTIONS → ciphers, OPTIONS → cipher-group)

"Client-side profiles allow the traffic management system to handle authentication and encryption tasks for any SSL connection coming into a traffic management system from a client system." — ltm_profile_client-ssl.html, DESCRIPTION section

tmsh reference `ltm_profile_client-ssl.html` WRITE section มี `ciphers [name | none]` และ `cipher-group [name | none]`
DISPLAY section เขียนชื่อคำสั่งแบบละ module: `list client-ssl` และ `show client-ssl` (คำสั่งเต็ม: `list ltm profile client-ssl`, `show ltm profile client-ssl`)

"Specifies a cipher name. The default value is DEFAULT, which uses the default ciphers." — ltm_profile_client-ssl.html, OPTIONS section → ciphers

"Specifies a cipher group. If the cipher group is not blank or none, the ciphers string will be used." — ltm_profile_client-ssl.html, OPTIONS section → cipher-group

คำสั่งตรวจ:
```
list ltm profile client-ssl
show ltm profile client-ssl
```

---

## ไม่พบที่มา

คำค้น: f5 cipher configuration, f5 Server SSL profile, f5 certificate expiry

ที่มา: —

คำสั่งตรวจ:
```
(no tmsh command - bash utilities openssl s_client / ssldump only)
```

การแก้ cipher ใน Client SSL profile — ตรวจ ltm_profile_client-ssl.html แล้วมีแค่ `ciphers [name | none]` และ `cipher-group [name | none]` แต่ไม่มีคำแนะนำว่าตั้งค่าอย่างไรจึงจะแก้ปัญหา
Server SSL profile handshake กับ pool member — ไม่พบแหล่งที่มา
ใบรับรองหมดอายุ/ไม่ตรง — ไม่พบแหล่งที่มา
