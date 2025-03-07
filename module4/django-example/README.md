# Django Examples

## BEFORE THE LAB

[Django](https://www.djangoproject.com/) is a python web framework that allows you to quickly develop web applications. This tutorial is loosely based on a set of introductory Django tutorials, also available [here](https://docs.djangoproject.com/en/5.1/intro/tutorial01/).

### Install Django

['pip'](https://pip.pypa.io/en/stable/) is a popular package manager for python. We used it in previous labs when we created a virtual environment and install packages. This lab, we will use it to install Django.

1. Open VS code, then open command palette (View -> Command Palette)
2. Type `Python: Select Interpreter`. You should see the one with `.venv` as we created it during the lab 2. Click it.
3. Open the new terminal (Terminal -> New Terminal). The VS code will activate your virtual environment automatically.
4. Type following command to the terminal

```bash
pip install django
```

### Watch this tutorial video

Introduction to Django: https://cs50.harvard.edu/web/2020/weeks/3/

This tutorial covers some of the things we will do in this lab, plus a few extra things. I strongly recommend following along with the video as going through these concepts a couple of times will help you make sense of the framework and how the different files and components fit together.

## 1. Creating a skeleton web application

> This section is a customized version of [part 1 of this Django tutorial](https://docs.djangoproject.com/en/5.1/intro/tutorial01/).

### Create a 'myapp' project

Open your terminal! Navigate to the place (using the `cd` command) where you would like to create your project. We'll create a skeleton project called `myapp`. You will find the complete code for this project in module4 -> django-example folder for your reference.

```
django-admin startproject myapp
```

The `django-admin` is our main command line tool for administrative tasks. We'll use this a fair bit in conjunction with other commands as you will see later. This first command automatically create a set of files that are your core project skeleton:

```
myapp/
  manage.py
  myapp/
    __init__.py
    settings.py
    urls.py
    asgi.py
    wsgi.py
```

These files determine the way in which your python is "run". For now, we won't worry most of these files. I'll explain these as we begin to interact with them.

First, let's check that our project `myapp` works. Run the following command:

```
cd myapp
python manage.py runserver
```

The first part, `python`, tells the terminal that we're about to run a python python file, in this case, we're running the python file `manage.py`. **[manage.py](https://docs.djangoproject.com/en/5.1/ref/django-admin/)** is itself a python-based command-line tool that can be used to run the django web server, manage the database, and range of other things. We pass the argument `runserver` to tell manage.py, that we'd like to activate the code required to... run the server!

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
September 28, 2024 - 22:42:10
Django version 5.1.1, using settings 'myapp.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

If you go to the URL: http://127.0.0.1:8000/ in your browser, you should see a "Congratulations!" page. This means your django project works and is running on the server.

Once you're satisfied, hit CTL-C and stop the server.

### Create our "farmnotes" Web App

We're going to create a basic web application called **farmnotes** to allow a farmer to create quick observations and make notes about what they see as they are walking around their fields doing day to day activities.

Make sure you're inside the 'myapp' folder. Run the following command:

`python manage.py startapp farmnotes`

As we run the manage.py tool this time, we provide the argument `startapp` followed by our app name `farmnotes`. This will create a skeleton web app inside the project folder 'myapp'. For future reference, remember that a project can contain multiple apps, hence the nesting.

Your 'farmnotes' _app_ folder should look like this inside your 'myapp' _project_ folder:

```
myapp/
  manage.py
  myapp/
  farmnotes/
      __init__.py
      admin.py
      apps.py
      migrations/
          __init__.py
      models.py
      tests.py
      views.py
  db.sqlite3
```

Start the server back up using `python manage.py runserver`.

If you go to the URL: http://127.0.0.1:8000/farmnotes in your browser, you should see an "404 Page not found" error page. Your django project is running, but your app is empty! Makes sense that it found no pages :)

### Create our first view

Open your project in an editor of your choosing. The **'views.py'** file contains python commands to "render" web pages.

Insert the following code into your **'myapp/farmnotes/views.py'** file:

**farmnotes/views.py**

```python
from django.http import HttpResponse

#Show all the fields in my farm
def index(request):
    return HttpResponse("Hello, world! You're at the farmnotes index, or 'home' page.")
```

Next we will map this file to URL. Inside **'myapp/farmnotes'** create a file called **'urls.py'**. Inside this file, insert the following code:

**farmnotes/urls.py**

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

This file will be used to tell the server where different files are located. Django works by using a [URL dispatcher](https://docs.djangoproject.com/en/5.1/topics/http/urls/), a tool that tells the webserver how different URLs map to python functions (written inside views.py). So every time someone makes an HTTP request in the browser (by navigating to a URL), Django will point them to the correct python function that renders the appropriate web page, that is, the "**view**".

In this instance, we're pointing the server to the `index` function as specified inside the file 'views.py'. We now need to point the root URLconf file at the project level to this application.

Open the **'myapp/myapp/urls.py'** file. It will contain some code already, with two import statements and one item in the `urlpatterns` list regarding the admin site. Edit the file to import the package `include` from `django.urls` and add a line to route the server to the **'farmnotes'** app.

**myapp/myapp/urls.py**

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('farmnotes/', include('farmnotes.urls')),
    path('admin/', admin.site.urls),
]
```

If you closed it, start the server back up using `python manage.py runserver`.

If you go to the URL: http://127.0.0.1:8000/farmnotes in your browser, you should see message saying "Hello, world! You're at the farmnotes index, or 'home' page.". Congrats! Technically, you've got a working Django web app.

## 2. Creating the data model

> This section is a customized version of [part 2 of this Django tutorial](https://docs.djangoproject.com/en/5.1/intro/tutorial02/).

Now that we have a basic web application, let's create a structure to allow us to store and manage data.

In Django, a MODEL describes the structure of your data, as well as your database. Since models are written in python, we are essentially creating python OBJECTS, or CLASSES, that Django processes and converts into the database itself. This means we don't actually leave python, even though we are in effect creating the model of a database.

### Create models to represent Fields and Observations.

> Creating the models is similar to what we did in lab 3.

Open the **'models.py'**. Create two classes, one titled "Field" and one titled "Observation", based on the class diagram below. The model classes are "child" classes of `models.Model`.

![ClassDiagram](img/classdiag.png)

**farmnotes/models.py**

```python
from django.db import models

OBSERVATION_TYPES = [
  ('weather', 'Weather'),
  ('crop', 'Crop'),
  ('soil', 'Soil'),
  ('water', 'Water'),
  ('pest', 'Pest'),
  ('other', 'Other'),
]

#class definitions below
class Field(models.Model):
	field_name = models.CharField(max_length=200)
	date_planted = models.DateTimeField('date planted')


class Observation(models.Model):
	field = models.ForeignKey(Field, on_delete=models.CASCADE)
	observation_title = models.CharField(max_length=200)
	author = models.CharField(max_length=100)
	observation_content = models.CharField(max_length=1000)
	observation_type = models.CharField(choices=OBSERVATION_TYPES, max_length=100)
	observation_date = models.DateTimeField('date observed')

```

Now, let's make sure that we register our **'farmnotes'** app with the **'myapp'** project. Navigate to the **'myapp/myapp/settings.py'**. In the section titled #Application definition, insert the line marked in the code below:

**myapp/myapp/settings.py**

```python
# Application definition

INSTALLED_APPS = [
    'farmnotes.apps.FarmnotesConfig',     ### ADD THIS LINE! Don't forget the comma :)
    'django.contrib.admin',
    ...
    ...
    ...
  ]
```

There is a `INSTALLED_APPS` already. You DO NOT need to create. You only need to add one line into that list.

Once you are done, save the file and open your terminal. Make sure you are inside your Django 'myapp' project folder. Run the following command:

`python manage.py makemigrations farmnotes`

You will see a message similar to the following:

```
Migrations for 'farmnotes':
  farmnotes/migrations/0001_initial.py
    - Create model Field
    - Create model Observation

```

You've now created a set of instructions to Django stating that you'd like it to change your model, and store it as a _migration_. You can think of this step as the Django version of `git add` and `git commit`, where you are simply indexing the changes you'd like to make.

Next, run:

`python manage.py migrate`

Django will now actually alter your database as instructed by your model: creating (create table in SQL), editing, and deleting things as necessary. This is like the Django equivalent of `git push` -- it actually makes the changes you desire.

If you made a mistake in your original model, just change it, run the `makemigrations` command to tell Django to make the changes, and run `migrate` to actually push the changes to the database. Remember:

1. Edit your models in the file **'models.py'**
2. Run `python manage.py makemigrations farmnotes` to create the migration for the changes you make in `farmnotes` app.
3. Run `python manage.py migrate` to push the changes to the database.

### Using the Django API

Django has an Application Programming Interface (API) that allows you to do things interactively. This will feel a lot like what we did in the Jupyter Notebooks module, where you interactively played with a Pandas dataframe. Instead, we'll be interactively playing with the Django model in your **'farmnotes'** application.

Run the command:

`python manage.py shell`

This starts puts us inside the application - more technically, the `manage.py` command sets the environment variable in python to be your Django application so you can import your newly created model and interact with your basic application.

Try out the following commands. Remember anything after the `#` symbol is a comment. You'll be typing in the commands written after the `>>>` prompts, and the response you get from python when you hit enter is shown below it.

```python
>>> from farmnotes.models import Field, Observation  # Import the model classes we just wrote.

# No fields are in the system yet so it returns an empty QuerySet
>>> Field.objects.all()
<QuerySet []>

# Create a new Field.
# We'll import use the timezone library,
# so that we can use timezone.now()
# to automatically detect the date and time right now.
>>> from django.utils import timezone
>>> my_field = Field(field_name="North Field", date_planted=timezone.now())

# Save the object into the database. You have to call save() explicitly.
>>> my_field.save()

# Now it has an ID.
>>> my_field.id
1

# Access model field values via Python attributes.
>>> my_field.field_name
"North Field"
>>> my_field.date_planted
datetime.datetime(2021, 9, 18, 3, 10, 37, 528878, tzinfo=<UTC>)

# Change values by changing the attributes, then calling save().
>>> my_field.field_name = "South Field"
>>> my_field.save()

# objects.all() displays all the questions in the database.
>>> Field.objects.all()
<QuerySet [<Field: Field object (1)>]>

```

When we called `objects.all()` requesting a list of all `Field` objects in the database, we got an unhelpful list -- what we wanted was the actual names of the field. This means we need to edit our model to actually have a **function** that returns `field_name`.

We'll use a special Django helper method, `__str__` to instruct our application to return a human readable representation of the model.

Inside your `Field` class add the following code at the end:

**farmnotes/models.py**

```python
  def __str__(self): #this is the function declaration
    return f"{self.field_name} planted on {self.date_planted.date()}"

```

Inside your `Observation` class add the following code at the end:

**farmnotes/models.py**

```python
  def __str__(self):
    return f"{self.observation_title} by {self.author} on {self.observation_date.date()}"

```

Try to run `Field.objects.all()` inside your app's shell (remember: `python manage.py shell`). You should now get a nice little list that includes the field name. Play around with creating and deleting objects inside your database via the shell!

Note: To exit from the shell mode, type `exit()`.

### The Django Admin Portal

Django has a friendly little admin site already built into it, so we'll set that up for now so that we can play around with our data without worrying about the shell for now. Let's quickly set it up. This is a back-end tool, that is, this portal is not typically end-user facing. We will only use this to create test data and inspect our database.

In your terminal, make sure you are inside your **'myapp'** folder before you proceed.

First, we need to set up a `super user`, that is, and admin account:

`python manage.py createsuperuser`

It will ask you to enter an admin username, email address, and password. We're not going to be deploying our site anywhere, so for now keep these simple. Remember, in the real world, this actually matters :)

Start your application's web server:

`python manage.py runserver`

Open http://127.0.0.1:8000/admin/ in your browser. You should see the admin login screen. Use your credentials to log in. It should look like this:

![Admin](img/admin02.png)

As always with Django, if you don't add it to the python model or view, it won't show up in the browser. So let's add our `Field` and `Observeration` models to the **'admin.py'** file by adding the following code:

**farmnotes/admin.py**

```python
from .models import Field, Observation

admin.site.register(Field)
admin.site.register(Observation)

```

Save your file. If you had left the server running, notice that your admin web page simply updated after you changed things. If not, spin the server back up and go to the admin site. It should now look like the image below:

![Admin](img/admin03.png)

Go ahead and create some fields in the admin site. Create at some observations, and associate them with different fields. This will populate our database with some test data as we continue. Use the admin page for ease of creation.

## 3. Creating the front-end

We will create a total of three views, or web pages, for our site:

1. Field `index` page - displays all the fields in my farm.

2. Field `notes` page - displays all the observations related to a particular field.

3. A Field `observation` page - displays the details of a specific observation related to a field.

### Stub Views & Routing

We've already created a 'stub' (that is, a small piece of code that does a minimal set of actions) for our 'index' page view. We'll create each of these views in turn and iterate on our original 'index' view. Let's quickly put together a few more stubs so that we can set up the URLs for each of the pages.

Add the following view functions to **'farmnotes/views.py'**.

**farmnotes/views.py**

```python
#List all notes related to a particular field
def notes(request, field_id):
    return HttpResponse("You're looking at the notes related to field %s." % field_id)

#View the details of a single observation
def observation(request, field_id, observation_id):
        return HttpResponse("You're looking at observation %s related to field %s." % (observation_id, field_id))
```

Edit **'farmnotes/urls.py'** to look like the code snippet below:

**farmnotes/urls.py**

```python
from django.urls import path

from . import views

urlpatterns = [

    # /farmnotes
    path('', views.index, name='index'),

    # /farmnotes/field_id
    # /farmnotes/5/
    path('<int:field_id>/', views.notes, name='notes'),

    #farmnotes/field_id/observation_id/
    #3rd observation for my 4th field
    #farmnotes/4/3/
    path('<int:field_id>/<int:observation_id>/', views.observation, name='observation'),
]
```

Let's try each of our web pages to make sure things are routing correctly.

1. Index page: 127.0.0.1:8000/farmnotes/

2. Field 1's notes page: http://127.0.0.1:8000/farmnotes/1/

3. Field 1, observation 1 page: http://127.0.0.1:8000/farmnotes/1/1/

Right now, our code's a little simplistic. For example, it doesn't check to see if there actually is an observation 1 for field 1, or do much of anything really. But, it does demonstrate that the URL routing works. Routing is how we point the HTTP request from the user to the correct Django view: a critical component of a Django application.

### Real Views & HTML Templates!

Django uses [templates](https://docs.djangoproject.com/en/5.1/topics/templates/) to separate the design of the user interface from Python that manages the conversation between the front and back-end.

Create a folder called **'templates'** inside the **'farmnotes'** app folder. Because of how Django template loader functionality works, you'll have to create another folder inside **'templates'** that is the name of the app. Inside THAT you wil put your actual templates, in this case, create a file called **'index.html'**. Your folder structure will look something like this:

```
farmnotes/
  templates/
    farmnotes/
      index.html
  models.py
  views.py
  ...etc.
```

Confirm that your template path is: **'farmnotes/templates/farmnotes/index.html'**. Insert the following code into this template HTML file.

**farmnotes/templates/farmnotes/index.html**

```HTML
<!DOCTYPE html>
<html>
<head>
    <title>Farmnotes App</title>
</head>

<body>
    <h1>My Farm Fields</h1>
    {% if latest_fields %}
        <ul>
        {% for field in latest_fields %}
            <li><a href="/farmnotes/{{ field.id }}/">{{ field.field_name }}</a></li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No fields are available.</p>
    {% endif %}
</body>
</html>

```

Some things to note:

1.

```
   {% for field in latest_fields %}
    .....
   {% endfor %}
```

Above the syntax for 'tags' in the Django template language ([here's a quick reference for it](https://docs.djangoproject.com/en/5.1/ref/templates/language/). It allows us to perform some logic e.g., loops to iterate through a list, like shown above in `for field in latest fields`.

2. We can also use variables in our template. Consider the line `{{ field.field_name }}`. Anything inside `{{ }}` is a variable. In this case, we're calling the variable `field`, and specifically accessing the attribute `field_name`.

3. We've inserted a reference to a relative URL inside around the `field.field_name` variable. It appears here: `<a href="/farmnotes/{{ field.id }}/">`. Think back to the **'urls.py'**. The format of this URL follows that! In this case, we are pointing to the `notes` URL and subsequently the notes function in views.py. The intent is that if the user clicks on the field name it takes them to the page that shows them all the notes for that particular field.

This **'index.html'** template, when rendered, should display a list of all the fields in our **'farmnotes'** database. But first, we need to update the python function `index()` inside **'views.py'** to point here correctly.

**farmnotes/views.py**

```python
from .models import Field

#Show all the fields in my farm
def index(request):
    latest_fields = Field.objects.all()
    context = {'latest_fields': latest_fields}
    return render(request, 'farmnotes/index.html', context)
```

We use the function `render()`, a [Django shortcut function](https://docs.djangoproject.com/en/5.1/topics/http/shortcuts/#django.shortcuts.render). It has three arguments: - `request` which is the HTTP request object that was passed into the `index(request)` function in the first place. - the name of the template that we want to render, in this case `'farmnotes/index.html'`. - and an optional third argument: a dictionary referencing the object that we want to pass to the template. This allows us to pass the object `'latest_fields'` from this view to the template as shown in the previous code block. That's how come we could use the argument `{% if latest_fields %}` in the **'index.html'** file.

While your webserver is running, navigate to http://127.0.0.1:8000/farmnotes/. You should see output that looks like the image below. You can see the five fields I had created in the image (you won't have a black border, that's just the picture here).

![Index](img/index01.png)

> Reminder: if you made any changes to your model, make sure you `makemigrations` and `migrate`, or you will get an error!

### 404 page not found errors

Let's create field `notes` page that will display all the observations related to a particular field. First, we will update the `notes` function inside our **'views.py'** file. In this case, we want the function to check to see if the field actually exists, otherwise throw a 404 page not found error. Let's look at two ways in which you can do it.

The long way would be...

```python
from django.http import Http404

def notes(request, field_id):
    try:
        field = Field.objects.get(pk=field_id)
    except Field.DoesNotExist:
        raise Http404("Field does not exist")
    return render(request, 'farmnotes/notes.html', {'field': field})

```

I show you this so that you can (a) see how one would typically use the `try` clause, and (b) see the `get` function in action since it allows us to actually obtain an object by passing the primary key, or ID of the object as an argument `pk=field_id`.

Since this is a common enough thing that people need to do, there is a Django shortcut function for it - `get_object_or_404()`. So we will actually use this instead. Edit the `notes` function in **'views.py'** as follows:

**views.py**

```python
from django.shortcuts import get_object_or_404

#List all notes related to a particular field
def notes(request, field_id):
    field = get_object_or_404(Field, pk=field_id)
    return render(request, 'farmnotes/notes.html', {'field': field})
```

Now let's create the corresponding **'notes.html'** template file. The file will be placed in **'farmnotes/templates/farmnotes/notes.html'**.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Farmnotes App</title>
  </head>

  <body>
    <div>
      <h1>{{ field.field_name }}</h1>
      <h2>Observations:</h2>
      <ul>
        {% for observation in field.observation_set.all %}
        <li>
          <a href="/farmnotes/{{ field.id }}/{{ observation.id }}/"
            >{{ observation.observation_title }}</a
          >
        </li>
        {% endfor %}
      </ul>
    </div>
  </body>
</html>
```

![notes](img/notes01.png)

## View a single observation

Now that we've had experience with a few, it is time for creating the `observation` function in **'views.py'** and the associated **'observation.html'** template file.

When we click on one of the links to an observation in the previous image, it should give us a detailed view of the observation. That is, when we visit the URL http://127.0.0.1:8000/farmnotes/1/1/, weI should see the details of Field 1's Observation 1. The page should display the following:

1. The name of the field
2. A prefix "Observation:" followed by the observation_title.
3. The observation_content itself.
4. The author of the observation.
5. The timestamp of when the observation was made.

**views.py**

```python
from .models import Field, Observation

# View the details of a single observation
def observation(request, field_id, observation_id):
    observation = get_object_or_404(Observation, pk=observation_id)
    return render(request, 'farmnotes/observation.html',{'observation': observation})
```

**'farmnotes/templates/farmnotes/observation.html'**.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Farmnotes App</title>
  </head>

  <body>
    <header>Farmnotes</header>
    <div>
      <h1>{{observation.field.field_name}}</h1>
      <h2>Observation: {{observation.observation_title}}</h2>
      <ul style="list-style-type:none;">
        <li>{{observation.observation_content}}</li>
        <li>{{observation.author}}</li>
        <li>{{observation.observation_date}}</li>
        <li>{{observation.observation_type}}</li>
      </ul>
    </div>
  </body>
</html>
```

![observation](img/observation01.png)

## 4. Styling your web app

Inside your **'farmnotes'** folder: create a folder called **'static'**. Inside that, create a folder called **'farmnotes'**. Inside that create a file called **'style.css'**. (This is that same Django quirk we dealt with earlier when we created the templates folder). Inside your newly created stylesheet, enter a little color code so that we can test that everything works:

**farmnotes/static/farmnotes/style.css**

```css
body {
  background: green;
}
```

Go to your template files, and link the style sheet in the `<head>` section of **'index.html'**, **'notes.html'**, **'observation.html'**.

```HTML
    <head>
      <title>Farmnotes Application</title>
      {% load static %}
      <link rel="stylesheet" type="text/css" href="{% static 'farmnotes/style.css' %}">
    </head>
```

Start your server (or restart it if it was already running). You should now see a green background.

By now, your file structure should look like this:

```
myapp/
  manage.py
  myapp/
  farmnotes/
      static
        farmnotes
          style.css
      templates
        farmnotes
          index.html
          notes.html
          observation.html
      __init__.py
      admin.py
      apps.py
      migrations/
      models.py
      tests.py
      views.py
  db.sqlite3
```

## Future Learning Pathways

Mozilla server-side programming overview: https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Introduction

Mozilla Django overview: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django

Full Django documentation (with tutorials!): https://docs.djangoproject.com/en/5.1/

## License

[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

<!-- This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa] -->

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png

[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

"Introduction to Agricultural Informatics Course" by [Ankita Raturi, Purdue University](https://github.com/ag-informatics/ag-informatics-course) is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.](http://creativecommons.org/licenses/by-nc-sa/4.0/)
