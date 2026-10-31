---
id: fortigate-ha-sync-ips
title: FortiGate — HA Sync ไม่ผ่าน / IPS Fail Open
families: fortinet_fortios
triggers: fortigate, fortiGate, fortios, HA sync not through, ha session sync not working, config sync not through, IPS fail open, IPS security profile not applied, session pickup
vendor: Fortinet
versions: FortiOS 7.6, 8.0
sources: https://docs.fortinet.com/document/fortigate/8.0.0/cli-reference/857448677/config-system-ha
---
# FortiGate — HA Sync ไม่ผ่าน / IPS Fail Open

## HA Sync ไม่ผ่าน (Config Sync / Session Sync ไม่ทำงาน)
คำค้น: HA sync not through, HA session sync not working, HA sync not working, config sync not through, config sync not working, HA sync, HA configuration out of sync, session pickup not working, ses_pickup, HA failover, ha failover not working, check-ha-sync, get system ha status, execute ha failover, checksum mismatch
อาการ: Config Sync ไม่ผ่านระหว่าง primary/secondary, Configuration Status ไม่เป็น in-sync, ses_pickup disable, HA failover แล้ว session ต้องสร้างใหม่หมด, Configuration Status แสดง out-of-sync, HA Heartbeat ไม่ผ่าน
คำสั่งตรวจ:
```
get system ha status
get system status
```
อ่านผล:
- `get system ha status`: ดู **HA Health Status** — ต้องเป็น **OK**, ดู **ses_pickup** — ต้องเป็น **enable**, ดู **Configuration Status** — ต้องแสดง **in-sync** สำหรับทุก unit
- `get system status`: ดู model, version, serial number — primary และ secondary ต้อง version ตรงกัน
สาเหตุที่พบบ่อย:
1. HA Version ไม่ตรงกัน — primary กับ secondary ใช้ firmware version ไม่ตรงกัน
2. ses_pickup disable — ต้อง enable session pickup
3. HBDEV ไม่ผ่าน — heartbeat interface มีปัญหา
4. Config mismatch — configuration checksum ไม่ตรงกัน
5. Certificate Bundle version ไม่ตรง — CA bundle ไม่ตรงกัน → config sync ล้มเหลวแบบ invisible
6. Disk ไม่ match — disk size/status ไม่ตรง (แสดง Need format)
วิธีแก้:
- Enable session pickup: `config system ha` → `set session-pickup enable` → `end`
- Enable session-pickup-connectionless: `config system ha` → `set session-pickup-connectionless enable` → `end`
- Upgrade firmware ให้ version ตรงกันทั้งสอง unit
- ตรวจ certificate: `diagnose autoupdate versions | grep Certificate -A6`
- ตรวจ disk: `diagnose hardware device disk`
-  Force resync: `execute ha synchronize start` (ผ่าน CLI)
- Manual sync: ผ่าน GUI → System → HA → เลือก unit → Force resync
- ตรวจ certificate bundle version ให้ตรงกัน
ที่มา: config system ha (FortiOS 8.0) https://docs.fortinet.com/document/fortigate/8.0.0/cli-reference/857448677/config-system-ha

## IPS Fail Open / IPS ไม่สแกน traffic หลัง HA Failover
คำค้น: IPS fail open, IPS not applied, IPS security profile not working, IPS failover, ICCP, IPS session pickup, HA failover IPS, ha-session-pickup, connectivity security, IPS scanning, IPS engine not running
อาการ: IPS ไม่สแกน traffic หลัง HA failover, security profile ไม่ทำงาน, ICCP session ขาดหาย, IPS scanning not through, IPS fail open หลัง failover, HA failover แล้ว traffic bypass IPS
คำสั่งตรวจ:
```
get system ha status
get ips settings
```
อ่านผล:
- `get system ha status`: ดู ses_pickup ต้องเป็น **enable** — ถ้า disable หลัง failover IPS session จะต้องสร้างใหม่
- `get ips settings`: ดู ha-session-pickup — **security** = prioritize complete inspection, **connectivity** = prioritize session continuity
- ตรวจ IPS session: `diagnose ips session list`
สาเหตุที่พบบ่อย:
1. ses_pickup disable — หลัง failover IPS ต้อง restart scan จากศูนย์
2. ha-session-pickup = connectivity — ไม่ inspect traffic ใหม่หลัง failover
3. ICCP session cache หาย — primary ใหม่ไม่ได้ cache ICCP session
4. IPS engine ไม่ทำงาน — IPS engine crash หลัง failover
วิธีแก้:
- Enable session pickup: `config system ha` → `set session-pickup enable` → `end`
- Set ha-session-pickup = security: `config ips settings` → `set ha-session-pickup security` → `end`
- Force resync: `execute ha synchronize start`
- Restart IPS engine: `diagnose test application ipsmonitor 97` (start) / `98` (stop) / `99` (restart all)
- ตรวจ IPS debug: `diagnose ips debug enable all` / `diagnose debug enable`
ที่มา: session-pickup (FortiOS 8.0) https://docs.fortinet.com/document/fortigate/8.0.0/administration-guide/955521/session-pickup
