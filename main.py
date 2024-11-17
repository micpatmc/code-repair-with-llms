import gradio
from ui.FrontPage import FrontPage

def main():
    front_page = FrontPage()
    front_page.page.launch()

if __name__ == "__main__":
    main()