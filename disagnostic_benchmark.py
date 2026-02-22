from openai import OpenAI
import csv
import json

# 1️⃣ Connect to Featherless
client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key="rc_75e9782ce9570cbed0c28488b94f595dacbabdf94b9647cb3aaabe566bcbb8a0"  # <-- replace with your Featherless key
)

# 2️⃣ Sample patient notes
samples = [
    "Patient reports fever of 102°F, sore throat, and headache for 3 days. Blood pressure 120/80, pulse 88.",
    "Patient complains of chest pain radiating to left arm, shortness of breath, and nausea. Vitals: BP 140/90, pulse 110.",
    "Patient has persistent cough, mild fever, and fatigue. Symptoms started 5 days ago."
]

# 3️⃣ Models to compare
models = [
    "Qwen/Qwen2.5-14B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Mistral-Instruct-7B"
]

# 4️⃣ Open CSV to save results
with open("diagnostic_benchmark.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Sample", "Model", "Response_JSON"])  # headers

    # 5️⃣ Loop through samples and models
    for sample in samples:
        for model in models:
            prompt = f"""
Please extract the following information from the patient note and return it as JSON:

1. Vitals (BP, Pulse, Temp, etc.)
2. Symptoms (list)
3. Diagnosis (brief)
4. ICD Code (suggested)
5. Patient Summary (plain language instructions)

Patient note:
{sample}

Return ONLY valid JSON.
"""
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a professional medical assistant."},
                    {"role": "user", "content": prompt}
                ],
            )

            result_text = response.choices[0].message.content.strip()
            
            # Optional: Try to parse JSON; if fails, save raw text
            try:
                parsed = json.loads(result_text)
                result_json = json.dumps(parsed)
            except:
                result_json = json.dumps({"raw_output": result_text})

            writer.writerow([sample, model, result_json])
            print(f"✅ Done for model {model} on sample: {sample[:30]}...")