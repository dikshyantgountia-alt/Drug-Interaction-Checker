from io import StringIO

import gradio as gr
import pandas as pd

MOCK_DATA = """Drug 1,Drug 2,Interaction Description
Aspirin,Warfarin,Increases the risk of bleeding when taken together.
Aspirin,Ibuprofen,May reduce the antiplatelet effect of Aspirin.
Metformin,Furosemide,Furosemide may increase blood glucose levels reducing Metformin's effect.
Simvastatin,Amlodipine,Increases the risk of muscle damage (myopathy).
Lisinopril,Spironolactone,Increases the risk of high potassium levels (hyperkalemia).
Warfarin,Paracetamol,Prolonged use may increase the anticoagulant effect of Warfarin.
Omeprazole,Clopidogrel,Reduces the effectiveness of Clopidogrel.
Digoxin,Furosemide,"Furosemide can lower potassium, increasing Digoxin toxicity risk."
Sertraline,Tramadol,Increases the risk of serotonin syndrome.
Metronidazole,Alcohol,"Causes a severe reaction: flushing, nausea, and rapid heartbeat."
"""

# The CSV text is embedded so the app runs as a single Python file.
df = pd.read_csv(StringIO(MOCK_DATA))
df["drug1_lower"] = df["Drug 1"].str.lower().str.strip()
df["drug2_lower"] = df["Drug 2"].str.lower().str.strip()


def check_interaction(drug_a: str, drug_b: str) -> str:
    """Look up a known pair in either input order."""
    drug_a = (drug_a or "").lower().strip()
    drug_b = (drug_b or "").lower().strip()

    if not drug_a or not drug_b:
        return "Please enter both drug names."

    match1 = df[(df["drug1_lower"] == drug_a) & (df["drug2_lower"] == drug_b)]
    match2 = df[(df["drug1_lower"] == drug_b) & (df["drug2_lower"] == drug_a)]
    result = pd.concat([match1, match2])

    if not result.empty:
        return result.iloc[0]["Interaction Description"]

    return (
        f"No known interaction found between '{drug_a}' and '{drug_b}' "
        "in this dataset. This does NOT mean it is safe - always check "
        "with a pharmacist or doctor."
    )


demo = gr.Interface(
    fn=check_interaction,
    inputs=[
        gr.Textbox(label="Drug 1", placeholder="e.g. Aspirin"),
        gr.Textbox(label="Drug 2", placeholder="e.g. Warfarin"),
    ],
    outputs=gr.Textbox(label="Interaction Result"),
    title="Drug Interaction Checker",
    description=(
        "Enter two drug names to check for a known interaction between them. "
        "This demonstration uses a small sample dataset and is not a substitute "
        "for advice from a pharmacist or doctor. A missing result does not mean "
        "a combination is safe."
    ),
)

if __name__ == "__main__":
    # Gradio creates a public, temporary share URL (typically available for 72 hours).
    demo.launch(share=True, debug=True)
