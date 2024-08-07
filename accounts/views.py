from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required  # Make sure this line is present

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        # This is triggered only if the form is invalid
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Optionally add more context here
        return context
    

@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')

