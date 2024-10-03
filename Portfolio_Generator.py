import google.generativeai as genai
import os
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_content(text):
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    template = PromptTemplate(input_variables=["input"], template="What is the summary of {input}?")
    chain = LLMChain(llm=model, prompt=template)
    response = chain.run(text)
    
    # Replace Markdown-like syntax with HTML
    
    response = response.replace('*',"")
    return response
    
def create_html(about_me, projects, skills, link):
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Portfolio</title>
        <style>
            body {{
                font-family: 'Times New Roman', Times, serif;
                margin: 0;
                padding: 0;
                background-image: url('https://images.unsplash.com/photo-1513530534585-c7b1394c6d51?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHByb2Zlc3Npb25hbCUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D');
                background-size: cover;
                background-position: center;
                color: #E0E0E0;
                height: 100vh; /* Full height */
                display: flex;
                flex-direction: column;
            }}
            header {{
                background-color: rgba(31, 31, 31, 0.8); /* Semi-transparent */
                padding: 20px 0;
                text-align: center;
                color: #E0E0E0;
            }}
            h1 {{
                margin: 0;
                font-size: 2.5em;
            }}
            .container {{
                width: 80%;
                max-height: 80vh; /* Limit height */
                margin: 20px auto;
                background-color: rgba(30, 30, 30, 0.8); /* Semi-transparent */
                padding: 20px;
                box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
                overflow-y: auto; /* Enable vertical scroll */
            }}
            h2 {{
                color: #BB86FC;
                border-bottom: 2px solid #BB86FC;
                padding-bottom: 5px;
            }}
            p {{
                line-height: 1.6;
            }}
            footer {{
                text-align: center;
                padding: 10px;
                background-color: rgba(31, 31, 31, 0.8); /* Semi-transparent */
                color: #E0E0E0;
                position: fixed;
                width: 100%;
                bottom: 0;
            }}
            .exit-button {{
                display: block;
                margin: 20px auto;
                padding: 10px 20px;
                background-color: #BB86FC;
                color: #E0E0E0;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1em;
            }}
        </style>
        <script>
            function showExitMessage() {{
                alert("Thanks for visiting!");
            }}
        </script>
    </head>
    <body>
        <header>
            <h1>My Portfolio</h1>
        </header>
        
        <div class="container">
            <h2>About Me</h2>
            <p>{about_me}</p>

            <h2>Projects</h2>
            <p>{projects}</p>

            <h2>Skills</h2>
            <p>{skills}</p>

            <h2>Link</h2>
            <p>{link}</p>
            
            <button class="exit-button" onclick="showExitMessage()">Exit</button>
        </div>
        
        <footer>
            <p>&copy; 2024 My Portfolio</p>
        </footer>
    </body>
    </html>
    """
    return html_template

def save_html(about_me, projects, skills, link):
    html_content = create_html(about_me, projects, skills, link)
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(html_content)
        messagebox.showinfo("Success", "Portfolio saved successfully!")

def generate_portfolio():
    about_me = about_me_input.get("1.0", tk.END).strip()
    projects = projects_input.get("1.0", tk.END).strip()
    skills = skills_input.get("1.0", tk.END).strip()
    link = link_input.get("1.0", tk.END).strip()

    if not about_me or not projects or not skills:
        messagebox.showwarning("Input Error", "Please fill in all the sections.")
        return

    generated_about_me = generate_content(about_me)
    generated_projects = generate_content(projects)
    generated_skills = generate_content(skills)
    generated_link = generate_content(link)

    save_html(generated_about_me, generated_projects, generated_skills, generated_link)

root = tk.Tk()
root.title("Portfolio Generator")
root.geometry("600x600")

about_me_label = tk.Label(root, text="About Me")
about_me_label.pack()
about_me_input = tk.Text(root, height=5, width=50)
about_me_input.pack()

projects_label = tk.Label(root, text="Projects")
projects_label.pack()
projects_input = tk.Text(root, height=5, width=50)
projects_input.pack()

skills_label = tk.Label(root, text="Skills")
skills_label.pack()
skills_input = tk.Text(root, height=5, width=50)
skills_input.pack()

link_label = tk.Label(root, text="Link")
link_label.pack()
link_input = tk.Text(root, height=5, width=50)
link_input.pack()

generate_button = tk.Button(root, text="Generate Portfolio", command=generate_portfolio)
generate_button.pack(pady=20)

root.mainloop()
