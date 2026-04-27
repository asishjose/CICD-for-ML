from pathlib import Path

import gradio as gr
import skops.io as sio


MODEL_PATH = Path(__file__).resolve().parents[1] / "Model" / "drug_pipeline.skops"
TRUSTED_TYPES = sio.get_untrusted_types(file=MODEL_PATH)
pipe = sio.load(MODEL_PATH, trusted=TRUSTED_TYPES)


def predict_drug(age, sex, blood_pressure, cholesterol, na_to_k_ratio):
    """Predict the drug label from patient features."""
    features = [age, sex, blood_pressure, cholesterol, na_to_k_ratio]
    predicted_drug = pipe.predict([features])[0]
    return f"Predicted Drug: {predicted_drug}"


inputs = [
    gr.Slider(15, 74, step=1, label="Age"),
    gr.Radio(["M", "F"], label="Sex"),
    gr.Radio(["HIGH", "LOW", "NORMAL"], label="Blood Pressure"),
    gr.Radio(["HIGH", "NORMAL"], label="Cholesterol"),
    gr.Slider(6.2, 38.2, step=0.1, label="Na_to_K"),
]

examples = [
    [30, "M", "HIGH", "NORMAL", 15.4],
    [35, "F", "LOW", "NORMAL", 8.0],
    [50, "M", "HIGH", "HIGH", 34.0],
]


title = "Drug Classification"
description = "Enter the patient details to predict the drug type."
article = (
    "This app is part of the Beginner's Guide to CI/CD for Machine Learning. "
    "It shows how to automate training, evaluation, and deployment with GitHub Actions."
)


demo = gr.Interface(
    fn=predict_drug,
    inputs=inputs,
    outputs=gr.Textbox(label="Prediction"),
    examples=examples,
    title=title,
    description=description,
    article=article,
    theme=gr.themes.Soft(),
)


if __name__ == "__main__":
    demo.launch(share=True)
