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
|- 2026-10-31 check_playbook.py: ERROR อัตโนมัติ (ไม่มีคำสั่งตรวจ / บล็อกโค้ดอื่น / ตัวอย่าง output / อักษรจีน / commit ใน Huawei S) + ล้างตัวอย่าง output / commit ที่ค้างใน port-mirroring, ACL
