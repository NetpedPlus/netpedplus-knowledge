---
id: f5-bigip-17-cpu-memory
title: F5 BIG-IP 17.x — ตรวจ CPU และ Memory
families: f5_tmsh
triggers: f5 cpu memory high, f5 tmm memory usage, f5 system resource threshold, f5 bigip cpu memory critical, f5 tmm cpu
versions: BIG-IP 17.5.x
sources: https://my.f5.com/manage/s/article/K000152888, https://my.f5.com/manage/s/article/K15468, https://my.f5.com/manage/s/article/K16419, https://my.f5.com/manage/s/article/K000151935, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_memory.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_tmm-info.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_cpu.html
---

# F5 BIG-IP 17.x — ตรวจ CPU และ Memory

---

## 1. ตรวจเกณฑ์ CPU และ Memory (threshold)

คำค้น: f5 cpu memory threshold, f5 tmm memory utilization, f5 swap usage percentage, f5 bigip resource utilization normal medium critical

อาการ: ตรวจทรัพยากร CPU และ Memory ว่าเกินเกณฑ์ Normal / Medium / Critical หรือไม่

"Below table shows the normal, medium and critical utilization percentage for device resources, especially the CPU and Memory." — K000152888, Recommended Actions

| Resource | Normal (<) | Medium (approx.) | Critical |
|---|---|---|---|
| TMM CPU Utilization (%) | 70 | 70-85 | 85 |
| Total CPU Utilization (%) | 70 | 70-90 | 90 |
| TMM Memory Utilization (%) | 85 | 80-95 | 95 |
| Swap Usage (%) | 10 | 10-50 | 50 |

ที่มา: K000152888 (https://my.f5.com/manage/s/article/K000152888), Recommended Actions — หมายเหตุ: PDF ไม่แสดงสัญลักษณ์ ≥/≤ ในหัวคอลัมน์ Normal และ Critical

"Normal Utilization: System is operating optimally." — K000152888, Recommended Actions
"Medium Utilization: Resource usage is approaching upper limits; monitor closely and consider optimization." — K000152888, Recommended Actions
"Critical Utilization: Immediate action recommended to prevent performance degradation." — K000152888, Recommended Actions

"Short spikes are normal under load, but sustained high CPU can indicate a problem and may warrant investigation." — K000152888, Additional Information
"It is normal for a Linux system, including the BIG-IP system, to use swap." — K000152888, Additional Information

"High swap usage may be a sign that the system is experiencing memory pressure." — K16419, Swap memory usage

"However, the BIG-IP system may experience high swap usage under normal operating conditions, especially in later versions." — K16419, Swap memory usage

หมายเหตุ: แถว TMM Memory ในตารางต้นฉบับมีช่วงซ้อนกัน — Normal < 85 กับ Medium 80-95 (ช่วง 80-85 ซ้อนกัน)

"cpu - Displays statistics about the Traffic Management Microkernel (TMM) service, specifically, CPU cycles." — sys_cpu.html, NAME section
"You can use the cpu component to display the CPU cycles for the system." — sys_cpu.html, DESCRIPTION section
"show cpu" — sys_cpu.html, DISPLAY section — หมายเหตุละ module: tmsh reference เขียนรูป "show cpu" โดยละ module คำสั่งเต็มที่ใช้ตรวจคือ show sys cpu

คำสั่งตรวจ:
```
show sys cpu
show sys memory
```

---

## 2. ตรวจ TMM CPU usage

คำค้น: f5 tmm cpu usage, f5 show sys tmm-info, f5 bigip tmm cpu statistics

อาการ: ตรวจ TMM CPU usage แบบละเอียด

"Performing the following procedure should not have a negative impact on your system." — K15468, "Use the Configuration utility to view TMM CPU usage"

ที่มา: K15468 (https://my.f5.com/manage/s/article/K15468), tmsh reference (latest) (sys_tmm-info.html)

เมนู GUI: "Go to Statistics (in versions prior to 11.1.0, select Overview) > Performance Reports." — K15468, "Use the Configuration utility to view TMM CPU usage"
"Select the System menu or the All menu." — K15468, "Use the Configuration utility to view TMM CPU usage"
"Scroll down to System CPU Usage and select View Detailed Graph." — K15468, "Use the Configuration utility to view TMM CPU usage"

"The Traffic Management Microkernel (TMM) processes all load-balanced traffic on the BIG-IP system." — K15468, Topic
"CPU resources are explicitly provisioned in the BIG-IP configuration." — K15468, CPU usage on single CPU, single core systems

"tmm-info - Displays information about the Traffic Management Microkernel (tmm) daemon." — sys_tmm-info.html, NAME section
"You can use the tmm-info component to display information about the tmm daemon." — sys_tmm-info.html, DESCRIPTION section
"show tmm-info" — sys_tmm-info.html, DISPLAY section — หมายเหตุละ module: tmsh reference เขียนรูป "show tmm-info" โดยละ module คำสั่งเต็มที่ใช้ตรวจคือ show sys tmm-info

หมายเหตุ: ต้นฉบับ K15468 เขียนว่า "show /sys tmm-info" แต่หน้า tmsh reference มี DISPLAY เป็น "show tmm-info" (ไม่มี /sys) คำสั่งเต็มที่ใช้ตรวจคือ show sys tmm-info

คำสั่งตรวจ:
```
show sys tmm-info
```

---

## 3. ตรวจ Memory usage

คำค้น: f5 show sys memory, f5 tmm memory usage, f5 bigip memory statistics, f5 bigip memory utilization

อาการ: ตรวจ TMM memory, Other memory, Swap usage

ที่มา: K16419 (https://my.f5.com/manage/s/article/K16419), K000151935 (https://my.f5.com/manage/s/article/K000151935), tmsh reference (latest) (sys_memory.html)

"TMM runs as a real-time user process within the Linux host operating system." — K16419, Description
"The BIG-IP system statically assigns memory resources to TMM and potentially to other module-related processes, depending on module provisioning." — K16419, Description

"The BIG-IP system assigns a dedicated pool of memory to each TMM process. TMM memory is not available for the Linux kernel to reassign to other host processes. The system never considers TMM memory as available. TMM memory cannot be swapped to disk." — K16419, TMM memory usage

"It is normal for a Linux system, including the BIG-IP system, to use swap. The Linux kernel sometimes prefers to swap idle processes' memory to disk so that more physical memory is available for more active processes, buffers, and caches." — K16419, Swap memory usage

"High swap usage may be a sign that the system is experiencing memory pressure." — K16419, Swap memory usage

"Statistics > Module Statistics > Memory" — K16419, "Understanding BIG-IP memory statistics"
"tmsh show /sys memory" — K16419, "Understanding BIG-IP memory statistics"

"The tmsh show /sys memory command output displays information about BIG-IP memory allocation." — K000151935, Description

"Use tmsh commands (e.g. show sys memory, show sys tmm-info) at the first instance, and only use tmctl when you require further details in advanced troubleshooting." — K000151935, Recommendations

"show memory" — sys_memory.html, DISPLAY section — หมายเหตุละ module: tmsh reference เขียนรูป "show memory" โดยละ module คำสั่งเต็มที่ใช้ตรวจคือ show sys memory

หมายเหตุ: ต้นฉบับ K16419, K000151935 เขียนว่า "show /sys memory" แต่หน้า tmsh reference มี DISPLAY เป็น "show memory" (ไม่มี /sys) คำสั่งเต็มที่ใช้ตรวจคือ show sys memory

คำสั่งตรวจ:
```
show sys memory
```

---

ไม่พบที่มา
- ตรวจ K000152888, K15468, K16419, K000151935 แล้วไม่พบ: ขั้นตอนแก้ไข/จัดการเมื่อ CPU หรือ Memory เกินเกณฑ์ Critical
