# CYB 499 LLM Windows Event Log Benchmark

This project evaluates whether LLMs can classify structured Windows Event Log entries as Malicious or Benign.

## Goal

Build a clean event-level evaluation dataset from atomic-evtx JSON logs. The final dataset should support benchmarking two LLMs and two prompt styles:

1. OpenAI model GPT-5.4 api with direct classification prompt
2. OpenAI model GPT-5.4 api structured reasoning prompt
3. Llama-3.3-70B-Instruct via huggingface with direct classification prompt
4. Llama-3.3-70B-Instruct via huggingface with structured reasoning prompt

## Important dataset rule

Do not label every event inside an attack scenario folder as malicious. Attack folders contain both attack-relevant events and background system noise. Only events with clear attack-relevant evidence should be labeled Malicious.

Benign events should come from benign_activity_logs JSON files.

## Desired final dataset

Create `data/processed/evaluation_dataset.csv` with columns:

- sample_id
- label
- source_type
- attack_category
- scenario_name
- source_file
- provider
- channel
- event_id
- timestamp
- computer
- user
- image
- command_line
- parent_image
- target_object
- destination_ip
- destination_hostname
- query_name
- script_block_text
- event_summary
- label_reason

## Labeling guidance

Malicious examples may include:
- suspicious PowerShell execution
- encoded commands
- credential access logic
- LDAP brute force behavior
- WMIC execution
- registry modification for defense evasion
- archive creation with password protection
- suspicious DNS or network beacon-like behavior
- Office spawning PowerShell or script interpreters
- persistence download and execute behavior

Avoid labeling normal background events as malicious, including:
- Microsoft Edge updates
- SecurityHealthService activity
- generic conhost.exe events unless tied to suspicious parent/command line
- routine Windows service events

## Code style

Use Python scripts in `src/`.
Keep scripts simple and readable.
Include comments.
Do not require Jupyter notebooks.
Print summary counts after each script runs.