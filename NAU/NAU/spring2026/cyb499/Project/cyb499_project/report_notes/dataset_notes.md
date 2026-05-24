# Dataset Notes

Generated: `2026-04-29T19:33:06-07:00`
Seed: `499`

## Raw File Counts

- Benign JSON files scanned: 3
- Malicious JSON files scanned: 45
- Non-empty malicious JSON files scanned: 34

## Selected Row Counts

- Total rows: 100
- Benign rows: 50
- Malicious rows: 50

### By Label / Source Type

- `Malicious / Sysmon`: 26
- `Malicious / PowerShell`: 24
- `Benign / Sysmon`: 20
- `Benign / PowerShell`: 15
- `Benign / Security`: 15

### By Scenario (Malicious Only)

- `persistence_persist_download_execute`: 11
- `lateral_powershell_lateral_usingExcelAppObject`: 10
- `c2c_dns_https_largequeryvolume`: 9
- `credential-access-bruteforceCreds_singleActiveDirectory_viaLDAP`: 9
- `discovery_discover_system_language_withchcp`: 3
- `execution-app-uninstall-using-wmic`: 3
- `collection_compressData_lockwithpw_exfiltrationwinrar`: 2
- `defense_evasion_disable_windows_registry_tool`: 2
- `execute-powershell-script-via-word-dde`: 1

### By Source File

- `data/raw/benign/sysmon.json`: 20
- `data/raw/benign/powershell.json`: 15
- `data/raw/benign/security.json`: 15
- `data/raw/malicious/persistence_persist_download_execute_json/T1197-3_Microsoft-Windows-Sysmon_Operational.json`: 11
- `data/raw/malicious/lateral_powershell_lateral_usingExcelAppObject_Json/T1021.003-2_Windows PowerShell.json`: 9
- `data/raw/malicious/credential-access-bruteforceCreds_singleActiveDirectory_viaLDAP_json/T1110.001-2_Windows PowerShell.json`: 8
- `data/raw/malicious/c2c_dns_https_largequeryvolume_json/T1572-1_Windows PowerShell.json`: 7
- `data/raw/malicious/discovery_discover_system_language_withchcp_json/T1614.001-2_Microsoft-Windows-Sysmon_Operational.json`: 3
- `data/raw/malicious/execution-app-uninstall-using-wmic-json/T1047-10_Microsoft-Windows-Sysmon_Operational.json`: 3
- `data/raw/malicious/c2c_dns_https_largequeryvolume_json/T1572-1_Microsoft-Windows-Sysmon_Operational.json`: 2
- `data/raw/malicious/collection_compressData_lockwithpw_exfiltrationwinrar_json/T1560.001-2_Microsoft-Windows-Sysmon_Operational.json`: 2
- `data/raw/malicious/defense_evasion_disable_windows_registry_tool_json/T1112-10_Microsoft-Windows-Sysmon_Operational.json`: 2
- `data/raw/malicious/credential-access-bruteforceCreds_singleActiveDirectory_viaLDAP_json/T1110.001-2_Microsoft-Windows-Sysmon_Operational.json`: 1
- `data/raw/malicious/execute-powershell-script-via-word-dde-json/T1559.002-2_Microsoft-Windows-Sysmon_Operational.json`: 1
- `data/raw/malicious/lateral_powershell_lateral_usingExcelAppObject_Json/T1021.003-2_Microsoft-Windows-Sysmon_Operational.json`: 1

## Label Logic

- Benign rows are sampled only from `data/raw/benign` and are filtered toward routine Sysmon, Security, and PowerShell telemetry.
- Benign rows exclude the attack-specific keywords that drive malicious selection, so the benchmark does not label obvious attack-pattern strings as benign.
- Malicious rows are selected event by event. The script does not label an entire attack-scenario folder as malicious by default.
- Malicious selection requires direct attack evidence in the event itself or in a preserved `ParentCommandLine` field for a child event in the same execution chain.
- High-priority malicious evidence includes suspicious PowerShell content, `reg add` policy changes, `wmic` uninstall commands, `bitsadmin` download-and-notify chains, `WinRAR` archive creation, `chcp` discovery, DDE document launch, and Excel COM / copy-based lateral movement behavior.
- Background noise such as Microsoft Edge update activity and `SecurityHealthService.exe` is intentionally excluded unless a row also carries explicit attack evidence.

## Limitations

- This repository's benign side contains Sysmon, Security, and Windows PowerShell logs only; there are no benign Application or System JSON files to sample from.
- Some malicious PowerShell rows use normalized `EventData` text as `script_block_text` because the raw export does not always expose a dedicated `ScriptBlockText` field.
- Several malicious PowerShell rows come from different telemetry points around the same command, because the available event-level evidence is limited and the dataset target is fixed at 50 malicious rows.
- The benchmark is conservative by design: it aims to keep only events with explicit attack-relevant context rather than maximizing coverage of every scenario event.

## Output

- Dataset CSV: `data/processed/evaluation_dataset.csv`
