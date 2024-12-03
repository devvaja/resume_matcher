# resume_matcher
1. Clone The Project
   git colne https://github.com/devvaja/resume_matcher.git
   cd resume
2. Creating Virtual env
   python -m venv venv
   venv/Scripts/activate 
3. Installation
   pip install django
   install all required libraries from requirement.txt file
4. Import nltk
   import nltk
    # Set a custom NLTK data directory (make sure to adjust the path)
    nltk.data.path.append(r'\nltk_data')  # Change this to your desired path
    # Now try downloading stopwords again
    nltk.download('stopwords', download_dir=r'nltk_data')
5. Use spacy
   pip install spacy,
   python -m pip install en_core_web_md
6. make directory for storing all the fiels of resume and job description
   Data -> Resume -> Proceed-> Resume
   Data -> JobDescription -> Proceed-> JobDescription
7. Create utils.py, processor.py,parser.py file inside app
8. Run the server
   python manage.py runserver
