---
id: f5-bigip-17-log-files
title: F5 BIG-IP 17.x — ดู log และตรวจ remote syslog
families: f5_tmsh
triggers: f5 log, var log ltm, show sys log, remote syslog, syslog-ng, log filter, ไม่เห็น log, ส่ง log ไม่ไป
versions: BIG-IP 17.5.x
sources: https://my.f5.com/manage/s/article/K16197, https://my.f5.com/manage/s/article/K86480148, https://my.f5.com/manage/s/article/K000152709, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_log.html
---

# F5 BIG-IP 17.x — ดู log และตรวจ remote syslog

---

## ไฟล์ log ชนิดต่างๆ และการดูด้วย tmsh

คำค้น: f5 log files var log ltm, f5 show sys log ltm, f5 show log range, f5 log audit tmm

ที่มา: K16197 (https://my.f5.com/manage/s/article/K16197) Applies to BIG-IP LTM มี 17.5.1, 17.5.0, 17.5.X และ tmsh reference (latest) (https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_log.html)

"By default, the BIG-IP system logs events locally and stores messages in the /var/log directory." — K16197, Local logging

ตารางชนิด log ตามต้นฉบับ K16197 (Type = Log file): audit = /var/log/audit, boot = /var/log/boot.log, cron = /var/log/cron, daemon = /var/log/daemon.log, dmesg = /var/log/dmesg, GSLB = /var/log/gtm, httpd = /var/log/httpd/httpd_errors, kernel = /var/log/kern.log, local traffic = /var/log/ltm, mail = /var/log/maillog, monitor = /var/log/ltm และ /var/log/monitors/*, sync = /var/log/nsyncd.log, packet filter = /var/log/pktfilter, security = /var/log/secure, system = /var/log/messages, TMM = /var/log/tmm, user = /var/log/user.log, webui = /var/log/webui.log

"The local traffic messages pertain specifically to the BIG-IP local traffic management events." — K16197, ตาราง BIG-IP log types

"log - Displays various system log files." — sys_log.html, NAME
"You can use the log component to display various logs." — sys_log.html, DESCRIPTION
"show log" — sys_log.html, DISPLAY

"show /sys log <log>" — K16197, Use tmsh to review log files
"show /sys log ltm range now-3d" — K16197
"show /sys log ltm lines 10000" — K16197

"Note: To conserve system resources, tmsh limits the maximum line count to 10,000 by default." — K16197

หมายเหตุละ module: หน้า tmsh เขียน show log ละ module ต้นฉบับ K16197 เขียน show /sys log ในบล็อกด้านล่างใช้รูป show sys log ที่ NetPED+ รันได้ (ตรงกับ playbook f5-bigip-17-ssl-handshake-troubleshooting)

คำสั่งตรวจ:
```
show sys log ltm
show sys log ltm range now-3d
show sys log ltm lines 10000
```

---

## ตรวจ remote syslog เมื่อ log ไม่ถึงเซิร์ฟเวอร์ปลายทาง

คำค้น: f5 remote syslog ไม่ได้ log, f5 list sys syslog, f5 syslog-ng local-ip, f5 log ไม่ส่ง

ที่มา: K86480148 (https://my.f5.com/manage/s/article/K86480148), K000159713 (https://my.f5.com/manage/s/article/K000159713), K000162023 (https://my.f5.com/manage/s/article/K000162023) Applies to BIG-IP LTM ทั้ง 3 มี 17.5.1, 17.5.0, 17.5.X

"Log messages from your BIG-IP system are not visible on the remote syslog server." — K86480148, Symptoms

"Display the BIG-IP syslog configuration by typing the following command:" — K86480148
"tmsh list sys syslog" — K86480148

"Note: The remote port will not be displayed in the remote-servers section if port 514 is configured." — K86480148

"The remote syslog configuration contained an invalid local-ip parameter that referenced an IP address that was not present on the system." — K000159713, Cause

"A race condition where syslog-ng may start before routing tables are fully populated after a reboot or upgrade, causing it to bind to an incorrect source IP." — K000162023, Cause

หมายเหตุ: คำสั่งแก้ไข (modify sys syslog, save sys config, bigstart restart syslog-ng) ในต้นฉบับไม่ใส่ในบล็อกตรวจ เพราะเป็นการเปลี่ยนค่า

คำสั่งตรวจ:
```
list sys syslog
```

---

## ตรวจ log filter ที่ทำให้ไม่เห็น log

คำค้น: f5 ไม่เห็น log, f5 list sys log-config filter, f5 log filter restrictive

ที่มา: K000152709 (https://my.f5.com/manage/s/article/K000152709) Applies to BIG-IP LTM มี 17.5.1, 17.5.0, 17.5.X

"Review current log filter configurations:" — K000152709, Recommended Actions
"tmsh list sys log-config filter" — K000152709
"Look for any custom filters with restrictive settings." — K000152709

คำสั่งตรวจ:
```
list sys log-config filter
```

---

ไม่พบที่มา
- ไม่ใส่คำสั่ง delete sys log-config filter และ cat/less (bash) จาก K000152709 และ K16197
