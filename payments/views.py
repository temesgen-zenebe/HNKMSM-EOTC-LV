from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,DetailView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from .models import PaymentCase, PaymentCaseCartList,BillingInformation, Payment
from members.models import MembersUpdateInformation
from django.views.generic import FormView
from .forms import BillingForm, CardInformationForm
import uuid
class PaymentCaseListView(ListView):
    model = PaymentCase
    template_name = 'payments/payment_case_list.html'  # Specify your template name
    context_object_name = 'payment_cases'  # Specify the context object name to use in the template
    paginate_by = 10  # Optional: to paginate the list if there are many items



class PaymentCaseDetailView(DetailView):
    model = PaymentCase
    template_name = 'payments/payment_case_detail.html'  # Specify your detail view template
    context_object_name = 'payment_case'



# def add_to_cart(request, slug):
#     payment_case = PaymentCase.objects.get(slug=slug)
#     # Implement the logic to add the payment_case to the cart
#     # For example, you might have a Cart model and you add the payment_case to it
#     # cart = request.user.cart  # Assuming the user has a cart
#     # cart.items.add(payment_case)
#     # return redirect('cart_view')  # Redirect to the cart view or wherever you need
#     return redirect('payments:payment_case_list')  # Redirect to the list view for simplicity


class AddToPaymentCaseCartView(View):
    
    def post(self, request, slug):
        payment_case = get_object_or_404(PaymentCase, slug=slug)
        cart_item, created = PaymentCaseCartList.objects.get_or_create(user=request.user, payment_case=payment_case)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('payments:paymentCaseCart_view')
    
class PaymentCaseCartListView(LoginRequiredMixin,ListView):
    model = PaymentCaseCartList
    template_name = 'payments/paymentCaseCart_list.html'
    context_object_name = 'paymentCaseCart_items'

    def get_queryset(self):
        return PaymentCaseCartList.objects.filter(user=self.request.user)
    


class CheckoutView(FormView):
    template_name = 'payments/checkout.html'
    form_class = BillingForm
    success_url = reverse_lazy('payments:payment_confirmation') # Redirect to a confirmation page after successful payment

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs
    
    
    def form_valid(self, form):
        # Save billing information
        billing_info = form.save(commit=False)
        billing_info.user = self.request.user
        billing_info.save()
        
        # Use the payment_case value from the form
        payment_case_value = form.cleaned_data.get('payment_case')   
        # Process the payment using Stripe
        # This is where you would use Stripe's API to create a charge
        # Mocking Stripe payment for simplicity
        payment = Payment(
            user=self.request.user,
            billing_info=billing_info,
            payment_case = payment_case_value,
            amount=100.00,  # Replace with the actual amount from your cart
            payment_id=str(uuid.uuid4()),  # Use actual Stripe payment ID
            status='Success'
        )
        payment.save()
        
       
        

        if payment_case_value == 'membership':
            try:
                membership = MembersUpdateInformation.objects.get(user=self.request.user)
                membership.member_status = 'active'
                membership.save()

            except MembersUpdateInformation.DoesNotExist:
                # Handle the case where the user does not have a membership info record
                pass
        
        # Clear the cart
        PaymentCaseCartList.objects.filter(user=self.request.user).delete()
        
        return super().form_valid(form)


class PaymentConfirmationView(TemplateView):
    template_name = 'payments/payment_confirmation.html'
    
