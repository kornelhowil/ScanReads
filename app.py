#!/usr/bin/env python3
import gradio as gr
from PIL import Image
import requests
from scanreads import ScanreadsReader


def get_image(url) -> Image.Image:
    """
    Convert the URL to an Image.
    """
    return Image.open(requests.get(url, stream=True).raw)


def read_image(image: Image.Image, gemini_api_key: str) -> tuple:
    """
    Read the image and return the title, author, publisher, and recommendations.
    """
    reader = ScanreadsReader(gemini_api_key)
    r = reader(image)
    book_info = [r["title"], r["author"], r["publisher"],
                 r["about_book"], r["about_author"]]
    images = [get_image(rec['image']) for rec in r["recommendations"]]
    authors = [rec['author'] for rec in r["recommendations"]]
    titles = [rec['title'] for rec in r["recommendations"]]
    return *book_info, *images, *titles, *authors


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
                    gemini_api_key = gr.Textbox(
                        label="Gemini API Key", type="password")
                    submit_btn = gr.Button("Submit")
                with gr.Column():
                    book_info = []
                    book_info.append(gr.Textbox(label="Book Title"))
                    book_info.append(gr.Textbox(label="Author"))
                    book_info.append(gr.Textbox(label="Publisher"))
                    book_info.append(gr.Textbox(label="About Book"))
                    book_info.append(gr.Textbox(label="About Author"))
            with gr.Row():
                gr.HTML("<h1><center>Book recommendations</center></h1>")
            with gr.Row():
                images = []
                titles = []
                authors = []
                for i in range(3):
                    with gr.Column("70%"):
                        gr.HTML(f"<center>Top {i+1}</center>")
                        images.append(
                            gr.Image(label=f"Book cover", height=200))
                        titles.append(gr.Textbox(
                            label=f"Book Title"))
                        authors.append(gr.Textbox(
                            label=f"Book Author"))

        submit_btn.click(
            fn=read_image,
            inputs=[input_image, gemini_api_key],
            outputs=[*book_info, *images, *titles, *authors],
        )
    block.queue(max_size=1).launch(show_api=False)


if __name__ == "__main__":
    main()
