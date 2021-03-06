from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from django.views.generic import ListView
from django.db.models import Q

# Contact list

class ContactList(ListView):
    context_object_name = "contacts"
    paginate_by = 4  # add this

    def get_queryset(self):
        user = self.request.user
        search = self.request.GET.get("q")
        contacts = Contact.objects.all()
        
        if user.is_authenticated:
            contacts = contacts.filter(created_by=self.request.user)
        else:
            contacts = contacts.filter(created_by=None)

# search contact(s) by phone or last_name       
        if search:
            contacts = contacts.filter(Q(phone__icontains=search) | Q(last_name__icontains=search))
        return contacts





# detail contact


@login_required(login_url="/login/")
def contact_details(request, id):
    contact = get_object_or_404(Contact, id=id)
    context = {"contact": contact}
    return render(request, "contact/contact_details.html", context)

# Add new contact


@login_required(login_url="/login/")
def new_contact(request):
    if request.method == "POST":
        created_by = request.user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        contact = Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            created_by=created_by
        )
        contact.save()
        return redirect("/contacts/")

    return render(request, "contact/new_contact.html")


# Update a contact
@login_required(login_url="/login/")
def update_contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        Contact.objects.filter(pk=contact.id).update(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email
        )
        return redirect("/contacts/")
    context = {"contact": contact}
    return render(request, "contact/update_contact.html", context)

# Remove a contact
@login_required(login_url="/login/")
def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    if request.method == "POST":
        contact.delete()
        return redirect("/contacts/")
    context = {"contact": contact}
    return render(request, "contact/delete_contact.html", context)

class Search(ListView):
    def get_queryset(self):
        return Contact.objects.filter(last_name__icontains=self.request.GET.get("q")).all()
    # def get_queryset(self): # new
    #     query = self.request.GET.get('q')
    #     object_list = Contact.objects.filter(
    #         Q(phone__icontains=query) | Q(last_name__icontains=query)
    #     )
    #     return object_list