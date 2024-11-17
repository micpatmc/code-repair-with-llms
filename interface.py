import gradio as gr
import os

import utils.interface_utils as iutils


session_restore = False
chatbot = gr.Chatbot(value=None, type="messages", show_label=True, show_share_button=False)  

# Create the Gradio interface
def create_interface():
    # Secondary Interface (chat and model selection) - initially hidden
    with gr.Blocks(css=iutils.custom_css()) as interface:
        with gr.Column():
            # Display the image in the top-right corner on the secondary page
            with gr.Row():
                gr.Markdown("")  # Filler to push logo to the right
                gr.Image("logo.png", label="Logo", show_download_button=False, show_fullscreen_button=False, show_label=False)

            # Chat Tab
            with gr.Tab("Chat"):
                choices = [file for file in os.listdir('./models')]
                gr.CheckboxGroup(["Bug Finding", "Pattern Matching", "Patch Generation", "Patch Validation"], label="Desired steps", select_all=True)
 
                model_dropdown = gr.Dropdown(
                    label="Model Selection",
                    choices=choices,
                    multiselect=False
                )

                # TODO: expecting a codebase
                with gr.Row():
                    file_input = gr.File(label="Upload Codebase/single file", file_types=[".py", ".java", ".c", ".cpp"])
                    file_content = gr.Code(label="File Contents", language="python", interactive=False, elem_classes=["fixed-height"])

                chatbot.render()
                with gr.Row():
                    with gr.Column(scale=10):
                        msg = gr.Textbox(label="Prompt", placeholder="Enter prompt")

                with gr.Row():
                    with gr.Column(min_width=0, scale=10):
                        submit_button = gr.Button("Submit Prompt")


            # Bug finding Tab
            with gr.Tab("Bug Finding"):
                with gr.Column():
                    model_dropdown = gr.Dropdown(
                        label="Model Selection",
                        choices=choices,
                        multiselect=False
                    )
                    bug_find_model_output = gr.Textbox(label="Output", interactive=False)
                    bug_find_code_output = gr.Code(label="File Contents", language="python", interactive=False, elem_classes=["fixed-height"])

            # Pattern Fixing Tab
            with gr.Tab("Pattern Fixing"):
                with gr.Column():
                    model_dropdown = gr.Dropdown(
                        label="Model Selection",
                        choices=choices,
                        multiselect=False
                    )
                    pattern_fix_model_output = gr.Textbox(label="Output", interactive=False)
                    pattern_fix_code_output = gr.Code(label="File Contents", language="python", interactive=False, elem_classes=["fixed-height"])

            # Patch Generation Tab
            with gr.Tab("Patch Generation"):
                with gr.Column():
                    model_dropdown = gr.Dropdown(
                        label="Model Selection",
                        choices=choices,
                        multiselect=False
                    )
                    patch_gen_model_output = gr.Textbox(label="Output", interactive=False)
                    patch_gen_code_output = gr.Code(label="File Contents", language="python", interactive=False, elem_classes=["fixed-height"])

            # Patch Validation Tab
            with gr.Tab("Patch Validation"):
                with gr.Column():
                    model_dropdown = gr.Dropdown(
                        label="Model Selection",
                        choices=choices,
                        multiselect=False
                    )
                    patch_val_model_output = gr.Textbox(label="Output", interactive=False)
                    patch_val_code_output = gr.Code(label="File Contents", language="python", interactive=False, elem_classes=["fixed-height"])
            
            file_input.change(fn=iutils.display_file_content, inputs=[file_input], outputs=[file_content])

    return interface

# Create the Gradio app
if __name__ == "__main__":
    # Launch the Gradio interface
    interface = create_interface()
    interface.launch(show_api=False)

