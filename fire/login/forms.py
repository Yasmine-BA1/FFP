from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    pseudo = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'pseudo',
                'name': 'pseudo',
                'placeholder': 'Pseudo',
                'class': "form-control shadow-lg p-6 mb-6 rounded",
                'style': "font-size: 20px; background-color: #DFD9DB;"
            }
        )
    )
    mot_de_passe = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'password',
                'name': 'password',
                'placeholder': 'Mot de passe',
                'class': "form-control shadow-lg p-6 mb-6 rounded",
                'style': "font-size: 20px; background-color: #DFD9DB;"
            }
        )
    )

    reset_password = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(),
        initial=False,
        label='Mot de passe oublié ?'
    )




    def is_valid(self, request):
        pseudo = self.data['pseudo']
        mot_de_passe = self.data['mot_de_passe']
        reset_password = self.cleaned_data['reset_password']

        if reset_password:
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                form.save(
                    request=request,
                    email_template_name='registration/password_reset_email.html'
                )
                return render(request, 'password_reset_done.html')
                
        if User.objects.filter(username=pseudo).exists():
            # Here, we assign the result of authenticate() to a variable
            user = authenticate(request, username=pseudo,
                                password=mot_de_passe)
            if user is None:
                self.add_error(
                    "mot_de_passe", "Les mots de passe ne correspondent pas.")
        else:
            self.add_error("pseudo", "Ce compte n'existe pas.")
        return super(LoginForm, self).is_valid()
