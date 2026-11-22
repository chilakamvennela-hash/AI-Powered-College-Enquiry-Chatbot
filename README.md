# AI-Powered College Enquiry Chatbot

An AI-powered college enquiry chatbot developed using Python, Flask, NLTK, Scikit-learn, SQLite, HTML, CSS and JavaScript.

This project is customized for **Sapthagiri NPS University (SNPSU)** to help students obtain information about admissions, eligibility, courses, fees, scholarships, hostel facilities, transportation, examinations, placements and other university-related enquiries.

The chatbot uses Natural Language Processing (NLP) techniques to understand different ways of asking questions and retrieve relevant answers from its knowledge base.

No paid APIs or API keys are required.

---

## 1. Project Objectives

The main objective of this project is to develop an interactive college enquiry chatbot that:

- Provides students with quick answers to common university-related questions.
- Understands different natural-language question variations.
- Reduces the need to manually search for basic college information.
- Provides a simple and user-friendly chat interface.
- Stores university information and chat history using SQLite.
- Works locally without requiring paid AI services.

## 2. Features

### College Enquiry Support

The chatbot supports the following enquiry categories:

- University information
- Admissions and application procedures
- Admission eligibility
- Courses and academic programmes
- Departments and schools
- Fee structure
- Examination information
- Scholarships and financial assistance
- Boys' and girls' hostel facilities
- Transportation facilities
- Library facilities
- Laboratory facilities
- Faculty information
- Placement and career support
- University contact information
- Frequently Asked Questions (FAQs)

### Chatbot Features

- Natural-language question understanding.
- TF-IDF-based text vectorization.
- Cosine similarity-based question matching.
- NLTK tokenization and stemming.
- Stopword removal.
- Multiple question patterns for each intent.
- Automatic fallback responses for unsupported questions.
- Greeting, thank-you and goodbye responses.
- Suggested questions for students.
- Animated typing indicator.
- Persistent chat history using SQLite.
- Clear Chat functionality.
- Automatic scrolling to the latest message.
- Responsive design for desktop and mobile screens.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.10 |
| Backend Framework | Flask |
| Natural Language Processing | NLTK |
| Machine Learning | Scikit-learn |
| Text Vectorization | TF-IDF |
| Similarity Measurement | Cosine Similarity |
| Database | SQLite |
| Frontend | HTML5 |
| Styling | CSS3 |
| Client-side Functionality | JavaScript |
| Development Environment | Visual Studio Code |

## 4. System Requirements

- Python 3.10 or newer
- Visual Studio Code (recommended)
- Web browser such as Google Chrome
- Internet connection for initial package installation

The application can answer questions locally after the required dependencies and database have been initialized.

## 5. Project Directory Structure

```text
college_enquiry_chatbot/
│
├── app.py
├── chatbot.py
├── database.py
├── train_model.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── dataset/
│   └── college_data.json
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

### File Descriptions

| File / Folder | Description |
|---|---|
| `app.py` | Flask application and API routes |
| `chatbot.py` | NLP preprocessing and question-matching logic |
| `database.py` | SQLite database creation and operations |
| `train_model.py` | Initializes the database and prepares the chatbot model |
| `requirements.txt` | Python dependency list |
| `README.md` | Project documentation |
| `.gitignore` | Excludes unnecessary files from Git |
| `dataset/college_data.json` | University information, intents, patterns and responses |
| `templates/index.html` | Chatbot web interface |
| `static/style.css` | Chatbot styling and responsive layout |
| `static/script.js` | Chat interaction and frontend functionality |

The SQLite database file, `college_chatbot.db`, is generated automatically and is not included in the GitHub repository.

## 6. Installation and Setup

Follow these steps to run the project on a Windows computer.

### Step 1: Clone or Download the Project

Open PowerShell and navigate to the project directory.

```powershell
cd path\to\college_enquiry_chatbot
```

### Step 2: Create a Virtual Environment

```powershell
py -3 -m venv venv
```

### Step 3: Activate the Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Required Dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: Initialize the Database and Prepare the Model

```powershell
python train_model.py
```

This initializes the SQLite database, prepares the NLTK stopwords and builds the TF-IDF question-matching model.

### Step 6: Start the Flask Application

```powershell
python app.py
```

### Step 7: Open the Chatbot

Open the following URL in your web browser:

**http://127.0.0.1:5000**

The chatbot interface will be displayed.

## 7. Python Dependencies

The project uses the following packages:

```text
Flask==3.1.1
nltk==3.9.1
scikit-learn==1.7.1
```

All dependencies can be installed using:

```powershell
pip install -r requirements.txt
```

## 8. How the Chatbot Works

The chatbot follows a retrieval-based Natural Language Processing approach.

### Step 1: User Input

The student enters a question through the chatbot interface.

Example:

"What courses are available at your university?"

### Step 2: Text Preprocessing

The application uses NLTK to:

- Tokenize the user input.
- Convert text into lowercase.
- Remove English stopwords when available.
- Apply Porter Stemming to reduce words to their root forms.

### Step 3: TF-IDF Vectorization

The stored example questions are converted into numerical vectors using Scikit-learn's `TfidfVectorizer`.

### Step 4: Cosine Similarity

The chatbot compares the user's question with the stored questions using cosine similarity.

### Step 5: Best Match Selection

The chatbot identifies the question with the highest similarity score.

If the score meets the configured threshold, the corresponding answer is returned.

The default similarity threshold is `0.22`, configured in `chatbot.py`.

### Step 6: Fallback Response

If no sufficiently relevant match is found, the chatbot displays a fallback response suggesting supported enquiry topics.

### Step 7: Store Conversation History

User messages and chatbot responses are stored in the SQLite database using the current browser session.

**Note:** This is a retrieval-based NLP chatbot. It does not use a generative Large Language Model (LLM).

## 9. Dataset and Knowledge Base

The university information and chatbot question patterns are maintained in:

```text
dataset/college_data.json
```

The dataset contains:

- University details.
- Intent categories.
- Multiple question patterns.
- Responses associated with each intent.

The current dataset is customized for Sapthagiri NPS University (SNPSU) and contains 19 intent categories.

### Adding New Questions

To improve the chatbot's ability to understand student enquiries:

1. Open `dataset/college_data.json`.
2. Locate the required intent.
3. Add additional question variations inside its `patterns` array.
4. Keep the response inside the `responses` array.
5. Save the JSON file.
6. Refresh the SQLite Q&A records before testing the updated patterns.

Example:

```json
{
  "tag": "courses",
  "patterns": [
    "what courses are available",
    "which programmes do you offer",
    "what can I study",
    "tell me about available courses"
  ],
  "responses": [
    "Sapthagiri NPS University offers undergraduate, postgraduate and doctoral programmes. Visit https://snpsu.edu.in/ for programme information."
  ]
}
```

**Important:** The `responses` value must always be a JSON array, even when there is only one response.

### Updating the SQLite Database

The application seeds the Q&A table when it is empty.

When changing the dataset in an existing installation:

1. Stop the Flask server.
2. Back up `college_chatbot.db`.
3. Refresh the Q&A records from the updated JSON dataset, or recreate the database if a complete reset is intended.
4. Run `python train_model.py` when initializing a recreated database.
5. Restart the Flask application.

Deleting the entire database recreates its tables and also removes previously stored chat history. Back up the database first if that history needs to be retained.

## 10. Database Structure

The application uses SQLite for local data storage.

The database contains three main tables.

### 1. college_info

Stores university information such as:

- University name
- Address
- Phone number
- Email address
- Website
- Office hours

### 2. qa

Stores question-and-answer information:

- ID
- Intent tag
- Question pattern
- Answer

### 3. chat_history

Stores chatbot conversations:

- ID
- Session ID
- Message role
- Message content
- Created timestamp

The database is automatically initialized by the application.

## 11. API Endpoints

The Flask backend provides the following API routes:

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Displays the chatbot interface |
| POST | `/api/chat` | Processes a user question and returns an answer |
| GET | `/api/history` | Retrieves the current session's chat history |
| POST | `/api/clear` | Clears the current session's chat history |
| GET | `/api/college` | Retrieves university information |

### Example Chat API Request

Endpoint:

```text
POST /api/chat
```

Request body:

```json
{
  "message": "What courses are available?"
}
```

The API returns the chatbot's answer in JSON format.

## 12. Testing and Validation

The chatbot has been tested using different question categories and natural-language variations.

### Functional Testing

- Greeting responses.
- University name enquiries.
- Admission procedures.
- Eligibility enquiries.
- Course information.
- Department information.
- Fee structure.
- Examination enquiries.
- Scholarship information.
- Hostel facilities.
- Transportation facilities.
- Library information.
- Laboratory facilities.
- Faculty enquiries.
- Placement and career support.
- University contact information.
- Frequently Asked Questions.
- Thank-you and goodbye responses.
- Fallback responses.

### NLP Testing

Different phrasings of student questions were tested to verify intent recognition.

Examples:

- "I want to join this university. What should I do?"
- "I have completed my 12th standard. Am I eligible to apply?"
- "I'm interested in studying engineering. What programmes can I choose from?"
- "How much money do I need to pay for my course?"
- "I cannot afford the full fees. Is there any financial assistance available?"
- "I am coming from another city. Can I stay on campus?"
- "Can I travel to the university using college buses?"
- "Will the university help me get a job after graduation?"

The question patterns were improved during testing to reduce incorrect intent matching.

### User Interface Testing

The following interface features were also tested:

- Suggested question buttons.
- Animated typing indicator.
- Chat history persistence.
- Clear Chat functionality.
- Automatic scrolling to the latest response.
- Mobile responsiveness.
- Desktop responsiveness.
- Proper display of long answers.

### Database Validation

The final Q&A database was checked against the JSON dataset.

The final database contains **155 Q&A records with zero duplicate questions**.

## 13. Running the Application

After completing installation and database initialization, use:

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

To stop the Flask development server, press:

```text
Ctrl + C
```

## 14. Limitations and Future Enhancements

The chatbot currently uses predefined question patterns and responses. Its accuracy depends on the quality of its knowledge base and the variety of question examples.

Possible future improvements include:

- Expand the university knowledge base.
- Add more natural-language question variations.
- Improve intent classification and confidence handling.
- Add an administrator dashboard for managing FAQs.
- Add additional language support.
- Improve reporting and analytics.
- Add more detailed university programme information.
- Deploy the application on a production web server.

## 15. Security and Deployment Notes

- The default Flask secret key is intended for local development only.
- Configure a strong `FLASK_SECRET_KEY` environment variable before deployment.
- Disable Flask debug mode in production.
- Use a production WSGI server when deploying publicly.
- Add authentication and rate limiting if the chatbot is exposed publicly.
- Do not publish private student information.
- Verify current admission, fee, scholarship, hostel and placement information before using the chatbot as an official university service.

## 16. University Website

**Sapthagiri NPS University**

Website: https://snpsu.edu.in/

Placement and career support: https://snpsu.edu.in/hrd

## 17. Conclusion

The AI-Powered College Enquiry Chatbot demonstrates how Natural Language Processing and machine-learning techniques can be used to create an interactive university enquiry system.

By combining Flask, NLTK, Scikit-learn, SQLite and a responsive web interface, the project provides students with a convenient way to access university-related information.

The project also demonstrates practical implementation of text preprocessing, TF-IDF vectorization, cosine similarity, database management and full-stack web application development.

---

**Project Name:** AI-Powered College Enquiry Chatbot

**Configured University:** Sapthagiri NPS University (SNPSU)

**Primary Technologies:** Python, Flask, NLTK, Scikit-learn, SQLite, HTML, CSS and JavaScript.