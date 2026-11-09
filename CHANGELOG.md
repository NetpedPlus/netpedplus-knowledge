# CHANGELOG
- 2026-10-31 สร้าง repo, GUIDE.md, tools/check_playbook.py
- 2026-10-31 PR #1 Huawei AC radio / roaming (Claude ตัดส่วนที่ยืนยันไม่ได้), เพิ่ม LESSONS.md + กฎหลักฐานต่อคำสั่ง
- 2026-10-31 เพิ่ม EXISTING_TOPICS.md (หัวข้อที่มากับโปรแกรม) + กฎห้ามซ้ำ / PR #3 Aruba merged / PR #4, #5 ปิด (ซ้ำ)
- 2026-10-31 PR #6 FortiGate 7.4 SSL Deep Inspection / Certificate / Exemption merged (squash) — เพิ่ม LESSONS.md ข้อ 11
- 2026-10-31 PR #7 Huawei Port Mirroring (observe-port) merged (squash) — เพิ่ม LESSONS.md ข้อ 12
- 2026-10-31 PR #8 Huawei ACL / traffic-filter merged (squash) — เพิ่ม LESSONS.md ข้อ 13
- 2026-10-31 PR #9 FortiGate 7.4 Traffic Shaping / QoS merged (squash) — เพิ่ม LESSONS.md ข้อ 14, 15, 16
|- 2026-10-31 PR #10 H3C S6520X Comware 7 IRF/BAGG/VLAN merged (squash)
|- 2026-10-31 PR #11 Cisco Catalyst 9300X IOS-XE StackWise/Port-channel/VLAN merged (squash)
|- 2026-10-31 PR #12 TP-Link Omada SX6632YF MSTP/LAG/VLAN merged (squash) — แก้ CLI reference ลวง (รายงานว่ามี แต่ไม่มีในไฟล์)
|- 2026-10-31 PR #13 FortiAnalyzer 150G FAZ log ไม่เข้า/disk เต็ม/ADOM merged (squash) — families ไม่ใช่ fortinet_fortios (ต้องไม่ใส่), execute add/clear/disk-quota เป็น config ไม่อยู่ในบล็อกคำสั่งตรวจ
|- 2026-10-31 PR #14 Cisco C1300 Stack/Port-channel/VLAN merged (squash) — PR ดีที่สุดใน repo: ทุกคำสั่งมีลิงก์ CLI Guide จริงทุกหน้า, syntax C1300 จริง, families ถูก cisco_sb
|- 2026-11-01 PR #26 Sophos XGS / IPS / Hardening / Syslog merged (squash) — IPS / Hardening / Syslog 3 topics, แก้ 4 rounds
|- 2026-11-01 PR #27 FortiGate 7.4 + Sophos XGS Ransomware Response merged (squash) — แก้ 4 rounds (15 + 3 + 2 + 2 ข้อ)
|- 2026-11-01 PR #28 F5 BIG-IP 17.x ประเมินผลกระทบช่องโหว่ + อัปเกรดบนคู่ HA merged (squash) — แก้ 4 rounds (5 + 2 + 2 + 2 ข้อ)
|- 2026-10-31 check_playbook.py: ERROR อัตโนมัติ (ไม่มีคำสั่งตรวจ / บล็อกโค้ดอื่น / ตัวอย่าง output / อักษรจีน / commit ใน Huawei S) + ล้างตัวอย่าง output / commit ที่ค้างใน port-mirroring, ACL
|- 2026-11-08 PR #45 f5-bigip-17-pre-upgrade-check-ha merged (squash) — show cm failover-status, show sys software status, list sys provision + หมายเหตุ UCS
|- 2026-11-09 PR #47 f5-bigip-17-ha-upgrade-procedure merged (squash) — license, install image, monitor install, upgrade HA standby-first, post-install, sync-status
|- 2026-11-09 PR #48 f5-bigip-17-ucs-restore-master-key merged (squash) — แก้ที่มา UCS 16.0 -> 13.1.0 (2 บรรทัด)
|- 2026-11-09 PR #49 f5-bigip-17-ha-upgrade-procedure merged (squash) — เพิ่มหมายเหตุ "ไม่พบขั้นตอน rollback" ใน section 5
|- 2026-11-09 PR #50 f5-bigip-17-ha-config-sync merged (squash) — show cm sync-status, list cm device-group, list cm device
|- 2026-11-09 PR #51 f5-bigip-17-ha-failover merged (squash) — show sys failover, run sys failover standby (sys_failover.html)
|- 2026-11-09 PR #52 merged (squash) — อัปเดตหมายเหตุ "ไม่พบที่มา" ใน ha-upgrade-procedure และ ha-config-sync ให้ชี้ไปที่ ha-failover
|- 2026-11-09 PR #53 f5-bigip-17-ucs-backup merged (squash) — list ucs, save sys ucs (ไม่เข้ารหัส/เข้ารหัส), คำแนะนำเก็บ passphrase
|- 2026-11-09 PR #54 f5-bigip-17-ltm-pool-member-status merged (squash) — show/list ltm pool และ node, state user-down/user-up, session user-disabled
|- 2026-11-09 PR #55 merged (squash) — ย้าย f5-bigip-17-security-upgrade-assessment-ha ไป archive/ (ที่มา my.f5.com ตรวจไม่ได้)
