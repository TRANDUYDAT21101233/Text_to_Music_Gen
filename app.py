import gradio as gr
from logics.models import unload_vc_model, unload_acestep_model
from logics.ui import create_voice_conversion_ui, create_text2music_ui



def handle_tab_selection(selected_tab: gr.SelectData):
    if selected_tab.index == 0:
        print("➡️ Switched to Voice Conversion tab.")
        unload_acestep_model()
    elif selected_tab.index == 1:
        print("➡️ Switched to Text-to-Music tab.")
        unload_vc_model()

def main():
    with gr.Blocks(title="Unified Music AI Suite") as demo:
        # gr.Markdown("<h1>🎶 Unified Music AI Suite 🎶</h1>")

        with gr.Tabs() as tabs:
            # with gr.TabItem("Music Voice Conversion", id=0):
            #     create_voice_conversion_ui()
            with gr.TabItem("Text to Music", id=0):
                create_text2music_ui()

        tabs.select(fn=handle_tab_selection, inputs=None, outputs=None)

    demo.launch(server_name="localhost", server_port=7860)

if __name__ == "__main__":
    main()