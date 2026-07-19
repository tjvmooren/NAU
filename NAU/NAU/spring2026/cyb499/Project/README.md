# LLM-Based Security Event Classification

This project evaluates how effectively large language models can classify Windows security events as **benign** or **malicious**. It compares model choice and prompt structure using a repeatable Python-based evaluation pipeline.

The project was completed for **CYB 499 at Northern Arizona University**.

## Project Objective

Security analysts often review large volumes of Windows event data while trying to distinguish normal activity from behavior that may indicate an attack. This project explores whether large language models can assist with that task and how reliably their classifications perform against labeled data.

The evaluation focuses on two questions:

1. How accurately can an LLM classify Windows security events as benign or malicious?
2. Does a structured prompting approach improve performance compared with a direct prompt?

## Models and Prompting Approaches

The project compares four configurations:

- OpenAI model with direct prompting
- OpenAI model with structured prompting
- Qwen model with direct prompting
- Qwen model with structured prompting

Each configuration processes the same labeled event set so the results can be compared consistently.

## Data

The dataset contains benign and malicious Windows telemetry, including events from sources such as:

- Windows Security logs
- Sysmon logs
- PowerShell logs
- Attack-related event samples mapped to malicious behaviors

Relevant fields may include process images, command-line activity, users, computers, event identifiers and other security-event attributes.

## Evaluation Method

The pipeline:

1. Loads and normalizes raw Windows event data.
2. Builds a consistent evaluation dataset with known benign and malicious labels.
3. Sends each event to the selected model and prompting configuration.
4. Parses and validates the returned classification.
5. Compares predictions with the ground-truth labels.
6. Calculates performance metrics and generates confusion matrices.

The project measures:

- Accuracy
- Precision
- Recall
- F1 score
- True positives
- True negatives
- False positives
- False negatives

## Results

| Configuration | Accuracy | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| OpenAI — Direct | 83% | 100% | 66% | 0.795 |
| OpenAI — Structured | 86% | 100% | 72% | 0.837 |
| Qwen — Direct | 82% | 94.4% | 68% | 0.791 |
| Qwen — Structured | 79% | 85.4% | 70% | 0.769 |

Within this evaluation, the **OpenAI structured-prompt configuration produced the strongest overall result**, reaching 86% accuracy and an F1 score of approximately 0.84.

The results also show why accuracy alone is not enough for security analysis. False negatives are especially important because they represent malicious events that the model incorrectly classified as benign.

## Key Findings

- Prompt structure can materially affect model performance.
- The strongest configuration achieved high precision but still missed some malicious events.
- Different models did not respond to structured prompting in the same way.
- LLM output should be validated and measured rather than treated as inherently reliable.
- These systems are better suited to supporting analysts than replacing human review or established detection controls.

## Technologies Used

- Python
- pandas
- NumPy
- scikit-learn
- matplotlib
- OpenAI API
- Qwen
- JSON and CSV data processing

## Repository Contents

The project includes:

- Raw benign and malicious event data
- Data preparation and normalization scripts
- Model evaluation scripts
- Direct and structured prompt configurations
- Raw model outputs
- Calculated metrics in CSV and JSON formats
- Confusion-matrix visualizations

## Setup

Create and activate a Python virtual environment, then install the dependencies:

```bash
pip install -r requirements.txt
```

For OpenAI-based evaluations, create a local `.env` file and provide the required API key:

```env
OPENAI_API_KEY=your_api_key_here
```

Do not commit API keys, tokens or other credentials to the repository.

## Responsible Use

This project is an academic evaluation of AI-assisted security-event classification. Its output should not be used as the sole basis for incident response, access-control decisions or production security enforcement. Model predictions require validation through additional telemetry, established detection logic and human analysis.

## Author

**Tyler Vander Mooren**  
B.S. Cybersecurity, Northern Arizona University  
[GitHub Profile](https://github.com/tjvmooren)