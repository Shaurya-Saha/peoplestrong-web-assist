# -*- coding: utf-8 -*-

import os

import chromadb
import fitz
import gradio as gr
from PIL import Image
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from openai import OpenAI

import prompt

CSS = """
.gr-label {
    height: 800px;  /* Limiting height */
    overflow-y: auto;   /* Adding vertical scrollbar */
}
"""

vectorstore_embedding_function = None
vectorstore_client = None
vectorstore_collection = None
model = None


def chat_function(user_question, chat_history):
    document_segments = vectorstore_collection.query(query_texts=[user_question], n_results=10,
                                                     include=['documents', 'distances', 'metadatas'])
    knowledge_base = "\n\n".join([x for x in document_segments["documents"][0]])
    metadatas = [x for x in document_segments["metadatas"][0]]

    references = {}
    for metadata in metadatas:
        reference_label = metadata["source"]
        reference_label = "/".join(reference_label.split("/")[-2:])
        reference_label = reference_label + ", Page No: " + str(metadata["page"] + 1)
        references[reference_label] = 1

    chatgpt_input_messages = [
        {
            "role": "system",
            "content": prompt.RAG_SUMMARIZATION_PROMPT_TEMPLATE.format(context=knowledge_base)
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    response = model.chat.completions.create(
        messages=chatgpt_input_messages,
        model="gpt-4o",
        temperature=0.0
    )

    chat_history.append((user_question, response.choices[0].message.content))

    return None, chat_history, references, None


def clearchat():
    return None, None, None, None, None, None, None, None, None


def showpage(evt: gr.SelectData):
    file_name = evt.value.split(", Page No: ")[0]
    page_number = evt.value.split(", Page No: ")[1]
    doc = fitz.open(file_name)
    page = doc[int(page_number) - 1]
    pix = page.get_pixmap()
    image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    return image


with gr.Blocks(css=CSS) as api_demo_ui:
    gr.Markdown("Medical Assistant | CWD: {}".format(os.getcwd()))
    with gr.Tabs() as hztab:
        with gr.TabItem("Medical Assistant"):
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        user_input = gr.Textbox(show_label=False, scale=2)
                        clear_button = gr.Button("🗑️  Clear", scale=1)
                    chatbot = gr.Chatbot(height=600)
                    references = gr.Label(elem_classes=["gr-label"], label="Reference Pages")
                with gr.Column():
                    image_reference = gr.Image(elem_id="imageref", sources=[], label="Reference View")

    user_input.submit(fn=chat_function,
                      inputs=[user_input, chatbot],
                      outputs=[user_input, chatbot, references, image_reference])

    clear_button.click(fn=clearchat, inputs=[],
                       outputs=[user_input, chatbot, references, image_reference])

    references.select(fn=showpage, inputs=[], outputs=[image_reference])

if __name__ == "__main__":
    vectorstore_embedding_function = OpenAIEmbeddingFunction(model_name="text-embedding-3-large",
                                                             api_key=os.environ.get('OPENAI_API_KEY'))
    vectorstore_client = chromadb.PersistentClient(path="vectorstore")
    vectorstore_collection = vectorstore_client.get_collection(name="embedding_db",
                                                               embedding_function=vectorstore_embedding_function)
    model = OpenAI()

    api_demo_ui.launch(server_name="0.0.0.0")
