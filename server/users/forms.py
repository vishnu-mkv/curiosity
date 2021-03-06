from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, WriterApplication, EmailActivation, ForgotPasswordKey


# the forms data is a query dict and it is immutable
# use this method to change value
def reset_to_initial(form, key, value):
    form.data = form.data.copy()
    form.data[key] = value


def get_user_from_id(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None


class UserAdminCreateForm(forms.ModelForm):
    password2 = forms.CharField(label='Confirm Password')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2', 'active', 'writer', 'staff', 'admin')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("The Email is already associated with an account!")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name').strip().capitalize()
        if first_name.isalpha():
            return first_name
        else:
            raise forms.ValidationError("Check your first name.")

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name').strip().capitalize()
        if last_name.isalpha():
            return last_name
        else:
            raise forms.ValidationError("Check your last name.")

    def clean(self):
        form = self.cleaned_data
        if form.get('password') != form.get('password2'):
            self.add_error('password2', 'Passwords do not match.')
        return form

    def save(self, commit=True):
        user = super(UserAdminCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'active', 'staff', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# only for admin site use
class WriterApplicationForm(forms.ModelForm):
    class Meta:
        model = WriterApplication
        fields = ('user', 'bio', 'writings', 'approved',)

    def clean_user(self):

        # initial user can be got by id from self.initial['user']
        initial_user = get_user_from_id(self.initial.get('user'))

        user = self.cleaned_data.get('user')

        if initial_user is not None:
            if initial_user.email != user.email:
                reset_to_initial(self, 'user', initial_user)
                raise forms.ValidationError("Cannot change user!")

        if initial_user is None and user.writer:
            raise forms.ValidationError("User is already a writer")

        return self.cleaned_data.get('user')

    def clean_approved(self):

        initial_status = self.initial.get('approved')
        status = self.cleaned_data.get('approved')

        if initial_status is True and initial_status != status:
            # if user is approved as writer then the status cannot be changed by this form
            reset_to_initial(self, 'approved', initial_status)
            raise forms.ValidationError("Cannot change writer status. Use demotion form")

        return status

    def clean(self):
        user = self.cleaned_data.get('user')
        bio = self.cleaned_data.get('bio')
        writings = self.cleaned_data.get('writings')
        init_writings = self.initial.get('writings')
        init_bio = self.initial.get('bio')

        if user and user.writer:
            reset_to_initial(self, 'bio', init_bio)
            reset_to_initial(self, 'writings', init_writings)
            if bio != init_bio:
                raise forms.ValidationError("Bio cannot be changed.")
            if writings != init_writings:
                raise forms.ValidationError("Writings cannot be changed.")


# only for admin site use
class EmailActivationForm(forms.ModelForm):
    class Meta:
        model = EmailActivation
        fields = ['user', 'validity', 'activated']

    def clean_user(self):

        init_user = get_user_from_id(self.initial.get('user'))

        user = self.cleaned_data.get('user')

        if init_user and init_user.email != user.email:
            # do not allow to change user associated with email activation
            reset_to_initial(self, 'user', init_user)
            raise forms.ValidationError("Cannot change user.")

        if user and not init_user and user.active:
            raise forms.ValidationError("User is already active.")

        return user

    def clean_activated(self):
        init_activated = self.initial.get('activated')
        activated = self.cleaned_data.get('activated')

        if init_activated and init_activated != activated:
            # do not allow deactivate a user using this form
            reset_to_initial(self, 'activated', init_activated)
            raise forms.ValidationError("Cannot change activated.")

        return activated


class ForgotPasswordAdminForm(forms.ModelForm):
    class Meta:
        model = ForgotPasswordKey
        fields = '__all__'

    def clean_user(self):

        init = self.initial.get('user')
        user = self.cleaned_data.get('user')
        if init:
            init_user = get_user_from_id(init)

            if init_user and init_user.email != user.email:
                # do not allow to change user associated with forgot password key
                reset_to_initial(self, 'user', init_user)
                raise forms.ValidationError("Cannot change user.")

        return user

    def clean_validity(self):

        # cannot change validity after password was changed
        if 'validity' in self.changed_data and self.instance is not None and self.instance.password_changed is True:
            reset_to_initial(self, 'validity', self.initial.get('validity'))
            raise forms.ValidationError("Cannot change validity after password was changed using this key")

        return self.cleaned_data.get('validity')
