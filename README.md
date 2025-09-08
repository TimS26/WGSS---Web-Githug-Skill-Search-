🏗️ Developer Portfolio Web App

A lightweight, Flask-powered web application that lets developers create and showcase their portfolios with skill-based filtering and GitHub integration. Perfect for sharing your work in one centralized place. To sucsesfully run the prograam you shuld check out its structure.

Stucture:
C:your_porgect_name/
--------------------/static
---------------------------/style.css
---------------------------/styleD.css
---------------------------/placeholder.png
---------------------------/594de9ef-44c8-4833-be90-579a6a697fb8_Dummy_presentation.jpg
--------------------/templates
------------------------------/all_porfolios.html
------------------------------/create_portfolio.html
------------------------------/form.html
------------------------------/portfolio_detail.html
------------------------------/regiser.html
--------------------/main.py
--------------------/portfolios.db
  

🌟 Features

Create Portfolio: Add name, bio, GitHub & Telegram links, skills, and avatar.

Browse Portfolios: Filter portfolios by skills with emoji icons.

GitHub Integration: Display public GitHub repositories automatically.

Themes: Switch between dark and light modes via cookies.

Preloaded Demo: Comes with a sample portfolio for instant testing.

Database-backed: Stores data in SQLite for simplicity and reliability.

📸 Screenshots

All Portfolios Page


Portfolio Detail Page


Create Portfolio Page


🚀 Installation & Usage
# Clone the repository
git clone https://github.com/yourusername/portfolio-app.git
cd portfolio-app

# Install dependencies
pip install flask requests

# Run the app
python app.py


Open your browser and visit http://localhost:5000
.

⚠️ Known Limitations

GitHub API may fail due to rate limits on unauthenticated requests.

File uploads are minimally validated — not secure for production.

No full authentication: anyone can create/view portfolios.

Limited skill icons; unmatched skills default to a generic icon.

SQLite is single-threaded — not ideal for high-concurrency production.

💡 Future Improvements

Add full user authentication and authorization.

Secure avatar uploads with validation and storage.

Cache GitHub API calls to reduce rate-limit issues.

Paginate portfolios and GitHub repositories.

Expand skill icon support dynamically.

🌐 Tech Stack

Python 3

Flask

SQLite

HTML/CSS & Jinja2 Templates

Requests library for GitHub API

📬 Contributing

Feel free to fork this repo, create issues, or submit pull requests.
Let’s make developer portfolios more accessible and fun! 🚀
