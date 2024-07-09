from django.shortcuts import render, redirect
from django.views import View
from api.forms import SignInForm, LoginInForm, NotesForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from api.models import CustomUser, Notes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.paginator import Paginator


# create a signin class with get method
class SignupView(View):
    template = "signup.html"

    def get(self, request):
        """
        Get method for the SignupView class.

        This method renders the 'signup.html' template with a SignInForm instance
        initialized in the context.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object with the rendered template.
        """
        self.form = SignInForm()
        context = {"form": self.form}
        return render(request, "signup.html", context)

    def post(self, request):
        """
        This function handles the HTTP POST request to sign in a user.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: A redirect response to 'signup' page if the user already exists.
            HttpResponseRedirect: A redirect response to 'login' page if the user is successfully signed up.

        Description:
            This function first validates the POST parameters using the `SignInForm` form.
            If the form is valid, it creates a new user using the `CustomUser.objects.create_user` method.
            If the user already exists, it redirects the request to the 'signup' page with an error message.
            In both cases, it redirects the request to the appropriate page and displays an error message.
        """
        post_params = request.POST
        form = SignInForm(post_params)
        print(form)
        user = CustomUser.objects.filter(username=post_params.get("username"))
        if user:
            messages.error(request, "User already exists")
            return redirect("signup")

        if form.is_valid():
            # create user
            user = CustomUser.objects.create_user(
                username=post_params.get("username"),
                email=post_params.get("email"),
                password=post_params.get("password"),
            )
            messages.error(request, "You have successfully signed up!")
            return redirect("login")
        messages.error(request, form.errors)
        return redirect("signup")


class LoginView(View):
    template = "login.html"

    def get(self, request):
        """
        This method handles the HTTP GET request for the login page.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object with the rendered login.html template.

        Description:
            This method initializes a new instance of the LoginInForm form and stores it in the `self.form` attribute.
            It then creates a context dictionary with the form as a value for the key 'form'.
            Finally, it renders the login.html template with the context and returns the rendered template as an HttpResponse.
        """
        self.form = LoginInForm()
        context = {"form": self.form}
        return render(request, "login.html", context)

    def post(self, request):
        """
        This function handles the HTTP POST request to log in a user.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: A redirect response to 'login' page if the form is not valid or the user does not exist.
            HttpResponseRedirect: A redirect response to 'home' page if the user is successfully logged in.

        Description:
            This function first validates the POST parameters using the `LoginInForm` form.
            If the form is valid, it attempts to authenticate the user using the `authenticate` function.
            If the user is authenticated, it logs the user in using the `login` function and redirects to the 'home' page.
            If the user is not authenticated, it redirects to the 'login' page with an error message.
        """
        post_params = request.POST
        form = LoginInForm(post_params)
        if form.is_valid():
            user = authenticate(
                username=post_params.get("username"),
                password=post_params.get("password"),
            )
            if user:
                login(request, user)
                messages.success(request, "You have successfully logged in!")
                return redirect("home")
        if form.errors:
            messages.error(request, form.errors)
        elif user is None:
            messages.error(request, "User does not exist")
        return redirect("login")


class LogoutView(View):
    def get(self, request):
        """
        This function handles the HTTP GET request to log out a user.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: A redirect response to the 'home' page.

        Description:
            This function calls the `logout` function to log out the user associated with the request.
            After logging out the user, it redirects the request to the 'home' page.
        """
        logout(request)
        return redirect("home")


class HomeView(LoginRequiredMixin, View):
    template = "home.html"

    def get(self, request, *args, **kwargs):
        """
        This method handles the HTTP GET request for the home page.

        Parameters:
            request (HttpRequest): The HTTP request object.
            args (tuple): Additional positional arguments.
            kwargs (dict): Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response object with the rendered home.html template.

        Description:
            This method checks if the request contains an 'id' parameter and an 'action' parameter set to 'delete'.
            If so, it retrieves the corresponding Note object and deletes it from the database.
            A success message is then displayed and the request is redirected to the home page.

            If the request does not contain the 'id' and 'action' parameters, it initializes a new instance
            of the NotesForm form and stores it in the `self.form` attribute.
            It retrieves the username of the authenticated user and uses it to filter the Notes objects.
            The notes are then paginated using the Paginator class with 10 notes per page.
            The current page number is extracted from the request's GET parameters and used to retrieve
            the corresponding page object.

            Finally, a context dictionary is created with the form, notes, and page object as values for the
            corresponding keys. This context is then used to render the home.html template and return
            the rendered template as an HttpResponse.
        """
        get_params = request.GET
        if get_params.get("id") and get_params.get("action") == "delete":
            note = Notes.objects.get(id=int(get_params.get("id")))
            note.delete()
            messages.success(request, "Note deleted successfully")
            return redirect("home")

        self.form = NotesForm()
        user_name = request.user.username
        notes = Notes.objects.filter(user=CustomUser.objects.get(username=user_name))

        paginator = Paginator(notes, 10)  # 10 notes per page
        page_number = request.GET.get("page", "1")
        page_obj = paginator.get_page(page_number)

        context = {"form": self.form, "notes": notes, "page_obj": page_obj}
        return render(request, "home.html", context)

    def post(self, request):
        """
        This function handles the HTTP POST request to add a new note to the database.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: A redirect response to the 'home' page after adding the note.

        Description:
            This function first validates the POST parameters using the `NotesForm` form.
            If the form is valid, it creates a new note in the database using the `Notes.objects.create` method.
            The note's title, body, and the user associated with the note are obtained from the POST parameters.
            The user is obtained using the `CustomUser.objects.get` method.
            After adding the note, a success message is displayed using the `messages.success` function.
            Finally, a redirect response to the 'home' page is returned.
            If the form is not valid, an error message is displayed using the `messages.error` function.
        """
        post_params = request.POST

        # get the user name
        user_name = request.user.username
        form = NotesForm(post_params)
        if form.is_valid():
            # save the note in model
            Notes.objects.create(
                title=post_params.get("title"),
                body=post_params.get("body"),
                user=CustomUser.objects.get(username=user_name),
            )
            messages.success(request, "Note added successfully")
            return redirect("home")
        messages.error(request, form.errors)
        return redirect("home")


class UpdateNoteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        """
        This function handles the HTTP POST request to update a note in the database.

        Parameters:
            request (HttpRequest): The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            JsonResponse: A JSON response with a success flag indicating the note was updated successfully.

        Description:
            This function first retrieves the POST parameters from the request.
            It then retrieves the note object associated with the given note_id from the database.
            The title and body of the note are updated with the values from the POST parameters.
            Finally, the note object is saved to the database and a success message is displayed using the `messages.success` function.
            A JSON response with a success flag indicating the note was updated successfully is returned.
        """
        post_params = request.POST
        note_id = post_params.get("note_id")
        note = Notes.objects.get(id=note_id)
        note.title = post_params.get("title")
        note.body = post_params.get("body")
        note.save()
        messages.success(request, "Note updated successfully")
        return JsonResponse({"success": True})
