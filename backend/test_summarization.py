from services.summarization_service import SummarizationService


text = """
Artificial intelligence is a branch of computer science that focuses on
creating systems capable of performing tasks that normally require human
intelligence. These tasks include learning, reasoning, problem solving,
understanding natural language, and recognizing patterns. Machine learning
is a major part of artificial intelligence and allows computers to learn
from data without being explicitly programmed for every task.
"""


try:

    summary = SummarizationService.summarize_text(text)

    print("\n========== SUMMARY ==========\n")
    print(summary)
    print("\n=============================\n")

except Exception as e:

    print("Summarization failed:")
    print(e)