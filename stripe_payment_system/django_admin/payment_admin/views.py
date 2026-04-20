from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import StripePayment
import json

@csrf_exempt
@require_http_methods(["POST"])
def sync_transaction(request):
    """Sync transaction from FastAPI to Django"""
    try:
        data = json.loads(request.body)
        
        payment, created = StripePayment.objects.get_or_create(
            transaction_id=data.get('transaction_id'),
            defaults={
                'user_id': data.get('user_id'),
                'user_email': data.get('user_email'),
                'amount': data.get('amount'),
                'currency': data.get('currency', 'USD'),
                'status': data.get('status', 'pending'),
                'payment_type': data.get('payment_type'),
                'item_id': data.get('item_id'),
                'item_name': data.get('item_name', '')
            }
        )
        
        return JsonResponse({'status': 'success', 'created': created})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def transactions_list(request):
    """List all transactions"""
    transactions = StripePayment.objects.all()
    data = [{
        'id': t.id,
        'transaction_id': t.transaction_id,
        'user_email': t.user_email,
        'amount': float(t.amount),
        'status': t.status,
        'created_at': t.created_at.isoformat()
    } for t in transactions]
    return JsonResponse({'transactions': data})