import gradio as gr
from crew import AIResearchCrew


def run_research(topic, month, year):

    inputs = {
        "topic": topic,
        "month": month,
        "year": year
    }

    result = AIResearchCrew().crew().kickoff(
        inputs=inputs
    )

    return str(result)


with gr.Blocks(title="AI Research Agent") as app:

    gr.Markdown(
        """
        # 🔬 AI Research Agent

        **Researcher → Analyst → Reviewer**

        Generate an AI research report for a specific month.
        """
    )

    with gr.Row():

        topic = gr.Textbox(
            label="Research Topic",
            placeholder="e.g. RAG, AI Agents, LLMs"
        )

        month = gr.Dropdown(
            choices=[
                "January", "February", "March",
                "April", "May", "June",
                "July", "August", "September",
                "October", "November", "December"
            ],
            label="Month",
            value="September"
        )

        year = gr.Number(
            label="Year",
            value=2026,
            precision=0
        )

    run_button = gr.Button(
        "🚀 Run Research",
        variant="primary"
    )

    report = gr.Markdown(
        label="Research Report"
    )

    run_button.click(
        fn=run_research,
        inputs=[topic, month, year],
        outputs=report
    )


app.launch()