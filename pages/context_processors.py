from events.models import RemindMeUpcomingEvent
from payments.models import CartPaymentCases,CartPayment
def cart_and_notifications(request):
    if request.user.is_authenticated:
        #user cart count
        cart = CartPayment.objects.filter(user=request.user).first()
        cart_count = CartPaymentCases.objects.filter(user=cart.user).count()
        
        #notification count
        notification_count = RemindMeUpcomingEvent.objects.filter(your_name=request.user, is_passed=False).count()
    else:
        cart_count = 0
        notification_count = 0
    
    return {
        'cart_count': cart_count,
        'notification_count': notification_count,
    }
