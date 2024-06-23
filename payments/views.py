from django.views.generic import ListView,DetailView
from django.shortcuts import redirect
from .models import PaymentCase

class PaymentCaseListView(ListView):
    model = PaymentCase
    template_name = 'payments/payment_case_list.html'  # Specify your template name
    context_object_name = 'payment_cases'  # Specify the context object name to use in the template
    paginate_by = 10  # Optional: to paginate the list if there are many items



class PaymentCaseDetailView(DetailView):
    model = PaymentCase
    template_name = 'payments/payment_case_detail.html'  # Specify your detail view template
    context_object_name = 'payment_case'



def add_to_cart(request, slug):
    payment_case = PaymentCase.objects.get(slug=slug)
    # Implement the logic to add the payment_case to the cart
    # For example, you might have a Cart model and you add the payment_case to it
    # cart = request.user.cart  # Assuming the user has a cart
    # cart.items.add(payment_case)
    # return redirect('cart_view')  # Redirect to the cart view or wherever you need
    return redirect('payments:payment_case_list')  # Redirect to the list view for simplicity
