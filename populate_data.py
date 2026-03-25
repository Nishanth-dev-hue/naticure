import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naticurve.settings')
django.setup()

from remedies.models import Remedy

remedies_data = [
    {
        "symptom_english": "cough",
        "symptom_telugu": "దగ్గు",
        "symptom_hindi": "खांसी",
        "remedy_name": "Honey and Ginger Juice",
        "ingredients": "1 tbsp Honey, 1 tsp Ginger juice",
        "preparation_steps": "1. Grate ginger and squeeze out the juice.\n2. Mix with honey.\n3. Take this mixture twice a day.",
        "relief_time": "1-2 days",
        "remedy_type": "Traditional",
        "verified": True
    },
    {
        "symptom_english": "fever",
        "symptom_telugu": "జ్వరం",
        "symptom_hindi": "बुखार",
        "remedy_name": "Tulsi Tea",
        "ingredients": "10-15 Tulsi leaves, 2 cups water, 1 tsp Honey",
        "preparation_steps": "1. Boil Tulsi leaves in water until it reduces to half.\n2. Strain and add honey.\n3. Drink warm.",
        "relief_time": "Few hours",
        "remedy_type": "Ayurvedic",
        "verified": True
    },
    {
        "symptom_english": "cold",
        "symptom_telugu": "జలుబు",
        "symptom_hindi": "सर्दी",
        "remedy_name": "Turmeric Milk (Haldi Doodh)",
        "ingredients": "1 cup milk, 1/2 tsp Turmeric powder, Black pepper",
        "preparation_steps": "1. Boil milk with turmeric and a pinch of black pepper.\n2. Drink hot before bedtime.",
        "relief_time": "Overnight",
        "remedy_type": "Home Remedy",
        "verified": True
    },
    {
        "symptom_english": "headache",
        "symptom_telugu": "తలనొప్పి",
        "symptom_hindi": "सिरदर्द",
        "remedy_name": "Peppermint Oil Massage",
        "ingredients": "2-3 drops Peppermint oil, 1 tsp Coconut oil",
        "preparation_steps": "1. Mix peppermint oil with coconut oil.\n2. Massage gently on temples and forehead.",
        "relief_time": "15-30 mins",
        "remedy_type": "Aromatherapy",
        "verified": True
    },
    {
        "symptom_english": "indigestion",
        "symptom_telugu": "అజీర్ణం",
        "symptom_hindi": "अपच",
        "remedy_name": "Ajwain Water",
        "ingredients": "1 tsp Ajwain (Carom seeds), 1 cup water",
        "preparation_steps": "1. Boil ajwain in water for 5 minutes.\n2. Strain and drink warm after meals.",
        "relief_time": "30 mins",
        "remedy_type": "Traditional",
        "verified": True
    },
    {
        "symptom_english": "stomach ache",
        "symptom_telugu": "కడుపు నొప్పి",
        "symptom_hindi": "पेट दर्द",
        "remedy_name": "Asafoetida (Hing) Paste",
        "ingredients": "Pinch of Hing, warm water",
        "preparation_steps": "1. Mix hing with a few drops of warm water to make a paste.\n2. Apply around the navel area.",
        "relief_time": "15-20 mins",
        "remedy_type": "Home Remedy",
        "verified": True
    },
    {
        "symptom_english": "sore throat",
        "symptom_telugu": "గొంతు నొప్పి",
        "symptom_hindi": "गले में खराश",
        "remedy_name": "Salt Water Gargle",
        "ingredients": "1/2 tsp Salt, 1 cup warm water",
        "preparation_steps": "1. Dissolve salt in warm water.\n2. Gargle 3-4 times a day.",
        "relief_time": "Immediate relief",
        "remedy_type": "Traditional",
        "verified": True
    },
    {
        "symptom_english": "acidity",
        "symptom_telugu": "యాసిడిటీ",
        "symptom_hindi": "एसिडिटी",
        "remedy_name": "Cold Milk",
        "ingredients": "1 cup cold milk (no sugar)",
        "preparation_steps": "1. Sip a cup of cold milk slowly when feeling acidity.",
        "relief_time": "10-15 mins",
        "remedy_type": "Home Remedy",
        "verified": True
    },
    {
        "symptom_english": "constipation",
        "symptom_telugu": "మలబద్ధకం",
        "symptom_hindi": "कब्ज",
        "remedy_name": "Triphala Churna",
        "ingredients": "1 tsp Triphala powder, 1 cup warm water",
        "preparation_steps": "1. Mix Triphala powder in warm water.\n2. Drink before bedtime.",
        "relief_time": "Next morning",
        "remedy_type": "Ayurvedic",
        "verified": True
    },
    {
        "symptom_english": "skin rash",
        "symptom_telugu": "చర్మంపై దద్దుర్లు",
        "symptom_hindi": "त्वचा पर लाल चकत्ते",
        "remedy_name": "Aloe Vera Gel",
        "ingredients": "Fresh Aloe Vera leaf",
        "preparation_steps": "1. Extract fresh gel from the leaf.\n2. Apply directly on the affected area.",
        "relief_time": "30 mins",
        "remedy_type": "Natural",
        "verified": True
    }
]

for r in remedies_data:
    Remedy.objects.get_or_create(**r)

print("Sample data populated successfully!")
