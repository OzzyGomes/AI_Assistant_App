<!DOCTYPE html>
<html>
<body>
    <h1>AI Personal Assistant by Ozzy and OpenAI 1.0</h1>

<h2>Overview</h2>
<p>The AI Personal Assistant is a Python desktop application that uses the OpenAI API to provide conversational AI capabilities. It allows you to interact with the OpenAI GPT-3 model by entering prompts and receiving responses. This README provides an overview of the code and how to use the application.</p>

<h2>Table of Contents</h2>
<ul>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
</ul>

<h2>Prerequisites</h2>
<p>Before using this application, you need to have the following prerequisites:</p>
<ol>
    <li>Python 3.x</li>
    <li>The <code>PyQt6</code> library</li>
    <li>An OpenAI API key</li>
</ol>

<h2>Installation</h2>
<ol>
    <li>Clone the repository or download the source code to your local machine.</li>
    <li>Install the required libraries by running the following command:
        <pre><code>pip install PyQt6</code></pre>
    </li>
    <li>Create a configuration file named <code>password_manager.ini</code> in the same directory as the code and add your OpenAI API key to it:
        <pre><code>[openai]
API_KEY = your-api-key-here
</code></pre>
    </li>
    <li>Run the application by executing the following command:
        <pre><code>python your_app_file.py</code></pre>
    </li>
</ol>

<h2>Usage</h2>
<ol>
    <li>Launch the application by running the script, and you'll be presented with a window containing the AI Personal Assistant.</li>
    <li>You can interact with the AI Personal Assistant in the following way:
        <ul>
            <li>Enter a prompt in the "Prompt" textbox.</li>
            <li>Adjust the "Max Token," "Temperature," and "Presence Penalty" settings using sliders.</li>
            <li>Click the "Submit" button to send your prompt to the OpenAI API.</li>
            <li>The response from the API will be displayed in the "Output" textbox.</li>
        </ul>
    </li>
    <li>You can also save the conversation by selecting "File" in the menu bar and choosing "Save Output."</li>
    <li>If you need to have multiple conversations simultaneously, you can click the "+" button on the tab bar to add a new conversation tab.</li>
</ol>

<h2>Features</h2>
<ul>
    <li>Interactive user interface for communicating with the OpenAI GPT-3 model.</li>
    <li>Customizable settings for controlling the response generation.</li>
    <li>Ability to save conversation transcripts to a file.</li>
    <li>Supports multiple conversation tabs for concurrent interactions.</li>
</ul>

<h2>Contributing</h2>
<p>If you want to contribute to this project, please follow these steps:</p>
<ol>
    <li>Fork the repository.</li>
    <li>Create a new branch for your feature or bug fix: <code>git checkout -b feature/your-feature-name</code> or <code>git checkout -b bugfix/your-bug-fix</code>.</li>
    <li>Make your changes and commit them: <code>git commit -m 'Add some feature'</code>.</li>
    <li>Push to your fork: <code>git push origin feature/your-feature-name</code>.</li>
    <li>Create a pull request.</li>
</ol>

<h2>License</h2>
<p>This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for details.</p>
</body>
</html>

