import json
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

from .models import Remedy, SuggestedRemedy, Feedback, UnknownSymptom
from .utils import translate_text


# ---------------------------
# AUTH CHECK
# ---------------------------

def is_superuser(user):
    return user.is_authenticated and user.is_superuser


# ---------------------------
# TEMPLATE VIEWS
# ---------------------------

def home(request):
    return render(request, 'remedies/home.html')


def search_remedy(request):
    return render(request, 'remedies/search_remedy.html')


def suggest_remedy(request):
    return render(request, 'remedies/suggest_remedy.html')




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')

            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'remedies/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# ---------------------------
# ADMIN PAGES
# ---------------------------

@user_passes_test(is_superuser, login_url='/login/')
def admin_dashboard(request):
    return render(request, 'remedies/admin/dashboard.html', {
        'total_remedies': Remedy.objects.count(),
        'pending_suggestions': SuggestedRemedy.objects.filter(status='pending').count(),
        'total_feedback': Feedback.objects.count(),
    })


@user_passes_test(is_superuser, login_url='/login/')
def admin_manage_remedies(request):
    return render(request, 'remedies/admin/manage_remedies.html')


@user_passes_test(is_superuser, login_url='/login/')
def admin_review_suggestions(request):
    return render(request, 'remedies/admin/review_suggestions.html')


@user_passes_test(is_superuser, login_url='/login/')
def admin_view_feedback(request):
    return render(request, 'remedies/admin/view_feedback.html')


@user_passes_test(is_superuser, login_url='/login/')
def admin_unknown_symptoms(request):
    return render(request, 'remedies/admin/unknown_symptoms.html')


# ---------------------------
# USER APIs
# ---------------------------

def api_get_remedies(request):
    symptom = request.GET.get('symptom', '').strip()
    lang = request.GET.get('lang', 'english').lower()

    # Auto-detect language from input text if user typed Telugu/Hindi
    telugu_pattern = re.compile(r'[\u0C00-\u0C7F]')
    hindi_pattern = re.compile(r'[\u0900-\u097F]')

    if symptom:
        if telugu_pattern.search(symptom):
            lang = 'telugu'
        elif hindi_pattern.search(symptom):
            lang = 'hindi'

    # Translate input to English for search (only if not English)
    original_symptom = symptom

    if lang == "telugu":
        symptom = translate_text(original_symptom, 'en')
    elif lang == "hindi":
        symptom = translate_text(original_symptom, 'en')

    # FIX: allow empty → return all remedies
    if not symptom:
        remedies = Remedy.objects.all().order_by('-id')
    else:
        query = (
            Q(symptom_english__icontains=symptom) |
            Q(symptom_telugu__icontains=symptom) |
            Q(symptom_hindi__icontains=symptom)
        )
        remedies = Remedy.objects.filter(query).order_by('-id')

    # If no results → store unknown
    if symptom and not remedies.exists():
        UnknownSymptom.objects.create(symptom_text=symptom, language=lang)
        return JsonResponse({'remedies': []})
    remedies = remedies[:20]
    results = []
    for r in remedies:
        name = r.remedy_name or ""
        ingredients = r.ingredients or ""
        steps = r.preparation_steps or ""

        # Skip translation completely if English
        if lang == "english":
            results.append({
                'id': r.id,
                'remedy_name': name,
                'ingredients': ingredients,
                'preparation_steps': steps,
                'relief_time': r.relief_time,
                'remedy_type': r.remedy_type,
                'verified': r.verified
            })
            continue

        # Ensure we always return in detected language (fallback handled below)

        # Telugu caching
        if lang == "telugu":
            if r.remedy_name_te and r.ingredients_te and r.preparation_steps_te:
                name = r.remedy_name_te
                ingredients = r.ingredients_te
                steps = r.preparation_steps_te
            else:
                name = translate_text(r.remedy_name, 'te')
                ingredients = translate_text(r.ingredients, 'te')
                steps = translate_text(r.preparation_steps, 'te')

                r.remedy_name_te = name
                r.ingredients_te = ingredients
                r.preparation_steps_te = steps
                r.save(update_fields=['remedy_name_te', 'ingredients_te', 'preparation_steps_te'])

        # Hindi caching
        elif lang == "hindi":
            if r.remedy_name_hi and r.ingredients_hi and r.preparation_steps_hi:
                name = r.remedy_name_hi
                ingredients = r.ingredients_hi
                steps = r.preparation_steps_hi
            else:
                name = translate_text(r.remedy_name, 'hi')
                ingredients = translate_text(r.ingredients, 'hi')
                steps = translate_text(r.preparation_steps, 'hi')

                r.remedy_name_hi = name
                r.ingredients_hi = ingredients
                r.preparation_steps_hi = steps
                r.save(update_fields=['remedy_name_hi', 'ingredients_hi', 'preparation_steps_hi'])

        results.append({
            'id': r.id,
            'remedy_name': name,
            'ingredients': ingredients,
            'preparation_steps': steps,
            'relief_time': r.relief_time,
            'remedy_type': r.remedy_type,
            'verified': r.verified
        })

    return JsonResponse({'remedies': results})


@csrf_exempt
def api_suggest_remedy(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        suggestion = SuggestedRemedy.objects.create(
            symptom=data.get('symptom'),
            remedy_name=data.get('remedy_name'),
            ingredients=data.get('ingredients'),
            preparation_steps=data.get('preparation_steps'),
            language=data.get('language'),
            status='pending'
        )

        return JsonResponse({'status': 'success', 'id': suggestion.id})

    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def api_feedback(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        remedy = get_object_or_404(Remedy, id=data.get('remedy_id'))

        fb = Feedback.objects.create(
            remedy=remedy,
            rating=int(data.get('rating', 0)),
            feedback_text=data.get('feedback_text'),
            language=data.get('language')
        )

        return JsonResponse({'status': 'success', 'id': fb.id})

    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def api_unknown_symptom(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        us = UnknownSymptom.objects.create(
            symptom_text=data.get('symptom_text'),
            language=data.get('language')
        )

        return JsonResponse({'status': 'success', 'id': us.id})

    return JsonResponse({'status': 'error'}, status=400)


# ---------------------------
# ADMIN APIs
# ---------------------------

@user_passes_test(is_superuser)
def api_admin_get_remedies(request):
    remedies = Remedy.objects.all().order_by('-id')

    results = []
    for r in remedies:
        results.append({
            'id': r.id,
            'symptom_english': r.symptom_english,
            'symptom_telugu': r.symptom_telugu,
            'symptom_hindi': r.symptom_hindi,
            'remedy_name': r.remedy_name,
            'ingredients': r.ingredients,
            'preparation_steps': r.preparation_steps,
            'relief_time': r.relief_time,
            'remedy_type': r.remedy_type,
            'verified': r.verified
        })

    return JsonResponse({'remedies': results})


@csrf_exempt
@user_passes_test(is_superuser)
def api_admin_remedy_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        remedy = Remedy.objects.create(**data)
        return JsonResponse({'status': 'success', 'id': remedy.id})

    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
@user_passes_test(is_superuser)
def api_admin_remedy_update(request, pk):
    remedy = get_object_or_404(Remedy, pk=pk)

    if request.method == 'PUT':
        data = json.loads(request.body)

        for key, value in data.items():
            setattr(remedy, key, value)

        remedy.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
@user_passes_test(is_superuser)
def api_admin_remedy_delete(request, pk):
    remedy = get_object_or_404(Remedy, pk=pk)

    if request.method == 'DELETE':
        remedy.delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


@user_passes_test(is_superuser)
def api_admin_get_suggestions(request):
    suggestions = SuggestedRemedy.objects.filter(status='pending').order_by('-created_at')

    results = []
    for s in suggestions:
        results.append({
            'id': s.id,
            'symptom': s.symptom,
            'remedy_name': s.remedy_name,
            'ingredients': s.ingredients,
            'preparation_steps': s.preparation_steps,
            'language': s.language,
            'created_at': s.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({'suggestions': results})


@csrf_exempt
@user_passes_test(is_superuser)
def api_admin_approve_suggestion(request, pk):
    suggestion = get_object_or_404(SuggestedRemedy, pk=pk)

    if request.method == 'POST':
        remedy = Remedy.objects.create(
            symptom_english=suggestion.symptom,
            symptom_telugu=suggestion.symptom if suggestion.language == 'telugu' else '',
            symptom_hindi=suggestion.symptom if suggestion.language == 'hindi' else '',
            remedy_name=suggestion.remedy_name,
            ingredients=suggestion.ingredients,
            preparation_steps=suggestion.preparation_steps,
            relief_time="N/A",
            remedy_type="Traditional",
            verified=True
        )

        suggestion.status = 'approved'
        suggestion.save()

        return JsonResponse({'status': 'success', 'remedy_id': remedy.id})

    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
@user_passes_test(is_superuser)
def api_admin_reject_suggestion(request, pk):
    suggestion = get_object_or_404(SuggestedRemedy, pk=pk)

    if request.method == 'POST':
        suggestion.status = 'rejected'
        suggestion.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


@user_passes_test(is_superuser)
def api_admin_get_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')

    results = []
    for f in feedbacks:
        results.append({
            'id': f.id,
            'remedy_name': f.remedy.remedy_name,
            'rating': f.rating,
            'feedback_text': f.feedback_text,
            'language': f.language,
            'created_at': f.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({'feedback': results})


@user_passes_test(is_superuser)
def api_admin_get_unknown_symptoms(request):
    symptoms = UnknownSymptom.objects.all().order_by('-created_at')

    results = []
    for s in symptoms:
        results.append({
            'id': s.id,
            'symptom_text': s.symptom_text,
            'language': s.language,
            'created_at': s.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({'unknown_symptoms': results})


# ---------------------------
# PWA
# ---------------------------

def manifest(request):
    return render(request, 'remedies/manifest.json', content_type='application/json')


def service_worker(request):
    return render(request, 'remedies/service-worker.js', content_type='application/javascript')