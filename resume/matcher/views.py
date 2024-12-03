# import os
# from django.shortcuts import render
# from django.core.files.storage import FileSystemStorage
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from pypdf import PdfReader
# from .parsers import ParseResume
# from .utils import read_single_pdf
#
#
# def home(request):
#     """Renders the upload resume form."""
#     return render(request, "upload.html")
#
# @csrf_exempt
# def upload_and_process_resume(request):
#     if request.method == "POST" and request.FILES.get("resume"):
#         # Save the uploaded file temporarily
#         resume_file = request.FILES["resume"]
#         fs = FileSystemStorage(location="/tmp")
#         file_path = fs.save(resume_file.name, resume_file)
#
#         try:
#             # Read and process the PDF
#             resume_text = read_single_pdf(os.path.join("/tmp", file_path))
#             parser = ParseResume(resume_text)
#             parsed_data = parser.get_JSON()
#
#             # Remove temporary file
#             os.remove(os.path.join("/tmp", file_path))
#
#             # Render results with annotated text
#             return render(request, "upload.html", {
#                 "resume_data": parsed_data["annotated_text"],
#                 "emails": parsed_data["emails"],
#                 "phones": parsed_data["phones"],
#                 "skills": parsed_data["skills"],
#             })
#         except Exception as e:
#             return JsonResponse({"error": f"Error processing the resume: {str(e)}"}, status=500)
#
#     return render(request, "upload.html")
#
# def read_pdf(file_path: str) -> str:
#     """Extract text from a PDF file."""
#     text = []
#     try:
#         pdf = PdfReader(file_path)
#         for page in pdf.pages:
#             text.append(page.extract_text())
#     except Exception as e:
#         print(f"Error reading PDF: {e}")
#     return " ".join(text)
#


import os

from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .forms import ResumeUploadForm
from .processor import ResumeProcessor  # Import the ResumeProcessor class

def upload_resume(request):
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = form.cleaned_data['resume']

            # Save the uploaded file temporarily
            fs = FileSystemStorage(location="Data/Resumes/")
            filename = fs.save(resume_file.name, resume_file)

            # Process the resume
            processor = ResumeProcessor(filename)
            if processor.process():
                return JsonResponse({"message": "Resume processed successfully."})
            else:
                return JsonResponse({"error": "Error processing the resume."}, status=400)
        else:
            return JsonResponse({"error": "Invalid form submission."}, status=400)

    # Render the upload page with the form
    form = ResumeUploadForm()
    return render(request, "upload.html", {"form": form})



from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .parsers import ParseResume
from .utils import generate_unique_id

# Define the paths for storing resumes
RESUME_UPLOAD_DIR = "Data/Resumes/"
PROCESSED_RESUME_DIR = "Data/Processed/Resumes/"

# Ensure directories exist
os.makedirs(RESUME_UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_RESUME_DIR, exist_ok=True)


@csrf_exempt
def upload_and_process_resume(request):
    """
    View to handle file upload and resume processing.
    """
    if request.method == "POST" and request.FILES.get("resume"):
        uploaded_file = request.FILES["resume"]
        fs = FileSystemStorage(location=RESUME_UPLOAD_DIR)

        # Save uploaded file
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = os.path.join(RESUME_UPLOAD_DIR, filename)

        try:
            # Process the uploaded resume
            with open(file_path, "rb") as f:
                pdf_content = f.read()

            from .utils import read_single_pdf  # Function to extract text from PDF
            resume_text = read_single_pdf(file_path)

            # Parse the resume
            parser = ParseResume(resume_text)
            parsed_data = parser.get_JSON()

            # Save processed data to a JSON file
            unique_id = parsed_data["unique_id"]
            output_file = os.path.join(PROCESSED_RESUME_DIR, f"Resume-{unique_id}.json")
            with open(output_file, "w") as json_file:
                import json
                json.dump(parsed_data, json_file, indent=4)

            # Clean up uploaded file
            os.remove(file_path)

            return JsonResponse(parsed_data, safe=False)
        except Exception as e:
            return JsonResponse({"error": f"Error processing the resume: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)