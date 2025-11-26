# Job Tracker App: Your Simple Guide to Setup and Launch

This guide will help you get the Job Tracker application up and running on your computer. This app helps you keep track of your job applications.

### Part 1: What You Need (Tools to Install First)

Before we start, you'll need to install a few essential tools on your computer. Think of these as the basic ingredients for our project:

1.  **Git (Optional, for cloning the project):**
    *   **What it is:** Git is a tool that helps you download and manage project files from the internet. While recommended for version control, you can also download the project as a ZIP file if you prefer.
    *   **How to get it (if you choose to install Git):**
        *   Open your web browser and go to: [https://git-scm.com/downloads](https://git-scm.com/downloads)
        *   Download the version for your computer (Windows or Mac).
        *   Follow the installation steps. You can usually just click "Next" through most of the options.

2.  **Python (the language the app is built with):**
    *   **What it is:** Python is a programming language that makes this app work.
    *   **How to get it:**
        *   Open your web browser and go to: [https://www.python.org/downloads/](https://www.python.org/downloads/)
        *   Download the *latest stable version* of Python (e.g., Python 3.x.x).
        *   **Important for Windows:** During installation, make sure to check the box that says "Add Python to PATH" or "Add Python 3.x to PATH". This is very important!
        *   Follow the installation steps.

3.  **MongoDB Compass (to see and manage your job data):**
    *   **What it is:** This is a friendly tool that lets you look at and manage the job application data stored in the database.
    *   **How to get it:**
        *   Open your web browser and go to: [https://www.mongodb.com/products/compass](https://www.mongodb.com/products/compass)
        *   Download and install MongoDB Compass for your operating system.

### Part 2: Step-by-Step Guide to Launch the Project

Now that you have the tools, let's get the app running!

#### **Step 1: Get the Project Files**

1.  **Open your Terminal (Mac/Linux) or Command Prompt (Windows):**
    *   **Mac/Linux:** Search for "Terminal" in your applications.
    *   **Windows:** Search for "Command Prompt" or "CMD".

2.  **Download the project files:**
    *   **Option 1: Clone with Git (Recommended if you have Git installed)**
        In the Terminal/Command Prompt, type the following command and press Enter:

        ```bash
        git clone https://github.com/YOUR_USERNAME/job_tracker.git
        ```

        *(Replace `YOUR_USERNAME` with the actual GitHub username if you have a fork, otherwise you can use the original repo's URL.)*

    *   **Option 2: Download as ZIP**
        Go to the GitHub repository page (e.g., `https://github.com/YOUR_USERNAME/job_tracker`), click on the green "Code" button, and select "Download ZIP". Extract the contents of the ZIP file to your desired location.

    *   This will create a folder named `job_tracker` on your computer (or extract it to a folder of that name if you downloaded the ZIP).

3.  **Go into the project folder:**
    *   Type this command and press Enter:

        ```bash
        cd job_tracker
        ```

#### **Step 3: Set Up the Application**

This part sets up a special isolated environment for your app and installs its specific needs.

**For macOS/Linux Users:**

1.  **Create an isolated environment:**

    ```bash
    python3 -m venv venv
    ```

2.  **Activate this environment:**

    ```bash
    source venv/bin/activate
    ```

3.  **Install app's requirements:**

    ```bash
    pip install -r Job_Tracker_App/backend/requirements.txt
    ```

**For Windows Users:**

1.  **Create an isolated environment:**

    ```bash
    python -m venv venv
    ```

2.  **Activate this environment:**

    ```bash
    .\venv\Scripts\activate
    ```

3.  **Install app's requirements:**

    ```bash
    pip install -r Job_Tracker_App\backend\requirements.txt
    ```

#### **Step 4: Connect to the Database (MongoDB)**

This app stores your job application data in a database called MongoDB. Here's how to ensure it can connect:

1.  **Open the `app.py` file:**
    *   Using a text editor (like VS Code, Notepad, or TextEdit), open the file located at: `job_tracker/Job_Tracker_App/backend/app.py`
    *   Look for a line that starts with `Connection_String = "mongodb+srv://..."`. It should look similar to this:

        ```python
        Connection_String = "mongodb+srv://<username>:<password>@cluster0.digxvgs.mongodb.net/"
        ```

2.  **Set up your own MongoDB Atlas account (if you haven't already):**
    *   This project uses a cloud-based MongoDB database. You'll need to create a free account at [https://cloud.mongodb.com/](https://cloud.mongodb.com/).
    *   Once you have an account, create a new "Cluster" (it's like your personal database server in the cloud).
    *   You'll then get your *own* connection string and create your *own* database username and password.

3.  **Update the `Connection_String`:**
    *   In the `app.py` file, replace `<username>:<password>` in the `Connection_String` with the actual username and password you created for your MongoDB Atlas account.
    *   **Example:** If your username is `myjobuser` and password is `secure123`, it would look like:

        ```python
        Connection_String = "mongodb+srv://myjobuser:secure123@cluster0.digxvgs.mongodb.net/"
        ```

    *   **Save the `app.py` file.**

4.  **Connect with MongoDB Compass (Optional, but Recommended):**
    *   Open the MongoDB Compass application you installed earlier.
    *   Click on "Connect" and then "Connect to..." (or look for a "New Connection" button).
    *   Paste your updated `Connection_String` (the one from `app.py` with your username and password) into the "URI" field.
    *   Click "Connect".
    *   If successful, you should see a database named `jobTracker` and inside it, a collection (table) called `applications`. This is where your job data will be stored!

#### **Step 5: Launch the Application!**

Finally, let's get the web app running!

1.  **Go to the backend folder (if you're not already there):**
    *   In your Terminal/Command Prompt (where you activated the environment), type:
        *   **For macOS/Linux:**

            ```bash
            cd Job_Tracker_App/backend
            ```

        *   **For Windows:**

            ```bash
            cd Job_Tracker_App\backend
            ```

    *   *(Make sure you are in the `backend` folder, not just `job_tracker`.)*

2.  **Run the application:**
    *   Type this command and press Enter:

        ```bash
        flask run
        ```

3.  **Open the app in your web browser:**
    *   After running the command, you'll see a message like `* Running on http://127.0.0.1:5000/`.
    *   Open your web browser (Chrome, Firefox, Safari, Edge) and go to that address:

        ```
        http://127.0.0.1:5000/
        ```

    *   You should now see your Job Tracker application!

---

### Part 3: Features and How to Utilize

This section highlights the key features of the Job Tracker App and guides you on how to use them effectively. Screenshots will be added here to visually explain each feature.

#### 1. Submitting a New Job Application

*   **Description:** This feature allows you to input details for a new job application, including position, company, description, contact, source, application date, status, notes, and an optional resume upload.
*   **How to Utilize:** Navigate to the home page (`/`) to access the submission form. Fill in the required fields (marked with `*`) and select the appropriate application status. You can also upload your resume in PDF format.

    <!-- Screenshot: Job Submission Form -->
    ![Job Submission Form Screenshot](Job_Tracker_App/home.png)

#### 2. Viewing and Managing Job Applications

*   **Description:** This feature displays all your submitted job applications in a table format, allowing you to view, edit, or delete them. It also provides filtering by status and sorting options.
*   **How to Utilize:** Click on the "View Jobs" button (or navigate to `/view`). You can:
    *   **Sort:** Use the "Sort by" dropdown to organize applications by Position, Company Name, or Application Date.
    *   **Filter by Status:** Click on the status buttons (e.g., "Applied", "Interview") to filter the list and see only applications with that status. The numbers next to each status show the count of applications.
    *   **View Details:** Click "View More" for truncated descriptions.
    *   **View Resume:** Click "View" in the Resume column to open the uploaded PDF.
    *   **Edit Application:** Click "Edit" to modify an existing job application.
    *   **Delete Application:** Click "Delete" to remove a single application.
    *   **Delete Multiple:** Select multiple jobs using the checkboxes and click "Delete Selected" to remove them in bulk.

    <!-- Screenshot: Job Applications List View -->
    ![Job Applications List View Screenshot](path/to/your/list_view_screenshot.png)

---

That's it! You've successfully set up and launched the Job Tracker app. If you encounter any issues, double-check each step, especially the `Connection_String` in `app.py` and the virtual environment activation.

