from .forms import messageForm

def message_form_processor(request):
    return {'MessageForm': messageForm()}
