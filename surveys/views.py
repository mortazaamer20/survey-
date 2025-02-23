from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Survey, Question, Response, Answer

def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, 'surveys/survey_list.html', {'surveys': surveys})

def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    responses = survey.responses.all()
    return render(request, 'surveys/survey_detail.html', {"survey": survey, "responses": responses})

# def submit_response(request, survey_id):
#     if request.method == 'POST':
#         survey = get_object_or_404(Survey, id=survey_id)
#         questions = survey.questions.all()
#         response = Response.objects.create(survey=survey)
        
#         # Loop through the questions and create answers.
#         for question in questions:
#             answer_text = request.POST.get(f'question_{question.id}', '')
#             Answer.objects.create(response=response, question=question, text=answer_text)
#             # Save first answer as "username" if not already set.
#             if not response.first_answer:
#                 response.first_answer = answer_text
#                 response.save()
        
#         return redirect('thank_you')
#     return redirect('survey_detail', survey_id=survey_id)

def submit_response(request, survey_id):
    if request.method == 'POST':
        survey = get_object_or_404(Survey, id=survey_id)
        questions = survey.questions.all()
        
        # Get the color from the form; default to "#ff6f61" if not provided
        chosen_color = request.POST.get('color', '#ff6f61')
        
        # Create the Response including the chosen color
        response = Response.objects.create(survey=survey, text_color=chosen_color)
        
        # Process each question's answer
        for question in questions:
            answer_text = request.POST.get(f'question_{question.id}', '')
            Answer.objects.create(response=response, question=question, text=answer_text)
            if not response.first_answer:
                # The first answer will be stored as the username
                response.first_answer = answer_text
                response.save()
        
        return redirect('thank_you')
    
    return redirect('survey_detail', survey_id=survey_id)




def thank_you(request):
    return render(request, 'surveys/thank_you.html')

# This view is for admins only to see responses (Instagram-like comments)
@staff_member_required
def admin_response_list(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    responses = Response.objects.filter(survey=survey)
    
    # If the request asks for a partial, render only the partial template.
    if request.GET.get('partial'):
        return render(request, 'surveys/partials/admin_response_list.html', {'responses': responses})
    
    # Otherwise, render the full admin response page.
    return render(request, 'surveys/admin_response_list.html', {'survey': survey, 'responses': responses})


# (Optional) If you still want a public responses view via HTMX
def response_list(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    responses = Response.objects.filter(survey=survey)
    return render(request, 'surveys/partials/response_list.html', {'responses': responses})
