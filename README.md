## Team Members: **Mohame**, **Nupur** & **Sara**

## Weekly Deliverables (Due Every Week)

**Figma Design File Link for Wireframes/Mockups:**

- [Web Project #2 - LIA Figma Design](https://www.figma.com/design/OUn3ckswZjNYYeKFZrAPFa/Web-Project-%232---LIA?t=bEQGchvMzCbPPf7r-0)

## Deliverables for Week 1:

- [Request for Proposal (RFP)](docs/rfp.md)
- [Proposal](docs/proposal.md)

## Deliverables for Week 2:

- [Visual Guidelines](https://www.figma.com/design/OUn3ckswZjNYYeKFZrAPFa/Web-Project-%232---LIA?t=bEQGchvMzCbPPf7r-0) _(Figma design file link)_

- [Data Model (ER Diagram)](docs/InSync-DB.png)

## **Installation Steps**

### Quick Install Guide for Viewing the "Insync Platform" Project

Follow these simple steps to get the "Insync Platform" running in your browser.

### 1. Clone the Repository:

Open your command line (Terminal or Command Prompt) and run:

```bash
git clone https://github.com/582-41W-VA/InSync.git
```

Then, navigate to the project directory by running:

```bash
cd InSync
```

### 2. Install uv:

Depending on your operating system, use the following commands to install uv.

In your (Terminal or Command Prompt) run:

#### Windows:

```bash
scoop install uv
```

#### Mac:

```bash
brew install uv
```

### 3. Install Python

The "Insync Platform" project requires Python to run. Python also includes a database called SQLite, which the project uses for now, so you won’t need to worry about setting up any external databases.

- Download Python from [here](https://www.python.org/downloads/), or use your system's package manager.

To check if Python is installed, open your command line (Terminal or Command Prompt) and run:

```bash
python3 --version
```

You should see something like:

```bash
Python 3.x.y
```

### 4. Run the Project Server

To start the "Insync Platform" and view it in your browser, run:

```bash
uv run manage.py runserver
```

You should see an output like this:

```bash
...
Starting development server at http://127.0.0.1:8000/
```

### 5. View the Project in Your Browser

1. Open your web browser.
2. Go to http://127.0.0.1:8000/.
3. You should see the "Insync Platform" homepage with all the features accessible through the web interface.

### 6. Access the Django Admin Panel:

To access the admin panel, you’ll need to create a superuser account (which has full admin access).

**Create a Superuser Account**

In your command line, run:

```bash
uv run manage.py createsuperuser
```

You'll be prompted to enter some details for your superuser account, such as:

- Username (e.g., admin)
- Email address (e.g., admin@example.com)
- Password (you'll need to enter this twice)

Once the superuser is created, you'll be able to log in at http://127.0.0.1:8000/admin/.

## You're All Set!

Enjoy using the "Insync Platform"!
