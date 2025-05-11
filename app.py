#!/usr/bin/env python3
import gradio as gr
from PIL import Image
import requests
from scanreads.reader import Reader


def get_image(url) -> Image.Image:
    """
    Convert the URL to an Image.
    """
    return Image.open(requests.get(url, stream=True).raw)


def read_image(image: Image.Image):
    """
    Read the image and return the title, author, publisher, and recommendations.
    """
    reader = Reader("api_key")
    response = reader(image)
    author = response["author"]
    title = response["title"]
    publisher = response["publisher"]
    images = [get_image(rec['image']) for rec in response["recommendations"]]
    authors = [rec['author'] for rec in response["recommendations"]]
    titles = [rec['title'] for rec in response["recommendations"]]
    return title, author, publisher, *images, *titles, *authors


def main():
    """
    Main function to run the Gradio app.
    """
    with gr.Blocks() as block:
        with gr.Column():
            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(
                        type='pil', label="Input Image", height=300)
                    submit_btn = gr.Button("Submit")
                with gr.Column():
                    title = gr.Textbox(
                        label="Book Title")
                    author = gr.Textbox(
                        label="Author")
                    publisher = gr.Textbox(
                        label="Publisher")
            with gr.Row():
                gr.HTML("<h1><center>Book recommendations</center></h1>")
            with gr.Row():
                images = []
                titles = []
                authors = []
                for i in range(5):
                    with gr.Column():
                        gr.HTML(f"<center>Top {i+1}</center>")
                        images.append(
                            gr.Image(label=f"Book cover", height=200))
                        titles.append(gr.Textbox(
                            label=f"Book Title"))
                        authors.append(gr.Textbox(
                            label=f"Book Author"))

        submit_btn.click(
            fn=read_image,
            inputs=[input_image],
            outputs=[title, author, publisher, *images, *titles, *authors],
        )
    block.queue(max_size=1).launch(show_api=False)


if __name__ == "__main__":
    main()
