from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import pandas as pd

def file_upload_view(request):
    if request.method == 'POST' and request.FILES['uploaded_file']:
        uploaded_file = request.FILES['uploaded_file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        # Load the file into a DataFrame
        if filename.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        elif filename.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            return render(request, 'upload.html', {'error': 'Unsupported file format'})

        final_data = {}
        for _, row in data.iterrows():
            if row[3] in final_data:
                final_data[row[3]].append(row[2])
            else:
                final_data[row[3]] = [row[2]]

        final_output = []
        for key, value in final_data.items():
            final_output.append([value[0], key, len(value)])

        msg_html = render_to_string('summary.html', {'summary': final_output})

        subject, from_email, to = "Summary Report", "sharmayaman80@gmail.com", "sharmayaman80@gmail.com"
        text_content = "Summary:"
        html_content = msg_html
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return render(request, 'summary.html', {'summary': final_output})
    
    return render(request, 'upload.html')

