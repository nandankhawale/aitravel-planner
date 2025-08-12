from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load local .env only if running locally (Render uses environment variables)
if os.environ.get("RENDER") is None:  
    load_dotenv()

# Get API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


def index(request):
    """Renders the main AI Travel Planner UI."""
    return render(request, "planner/index.html")


def plan_trip(request):
    """Handles user input and returns structured itinerary data."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    start_location = request.POST.get("start_location", "").strip()
    destination = request.POST.get("destination", "").strip()
    duration = request.POST.get("duration", "").strip()

    # Validate inputs
    if not all([start_location, destination, duration]):
        return JsonResponse({"error": "All fields are required!"}, status=400)

    try:
        prompt = (
    f"You are a professional travel planner and storyteller. "
    f"Create a concise {duration}-day travel itinerary for a trip from {start_location} to {destination}.\n\n"
    f"**Part 1 — Travel Route (1–2 sentences):** Briefly describe the best route (air/train/bus) including travel time.\n\n"
    f"**Part 2 — Daily Plans:** For each day:\n"
    f"• Write about 70-100 words per day.\n"
    f"• Label sections as **Morning**, **Afternoon**, and **Evening**.\n"
    f"• Mention main attractions and food recommendations briefly.\n\n"
    f"**Part 3 — Travel Notes:** Include 3-4 quick bullet points on safety, customs, and packing tips.\n\n"
    f"Keep the tone clear, friendly, and to the point."
)


        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert travel itinerary creator who writes vivid, detailed, and structured trip plans."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        full_response = response.choices[0].message.content.strip()

        # Try to split notes from main itinerary
        headers = ["Important Travel Notes", "Important travel notes", "Travel Notes", "Notes"]
        notes_index = None
        for h in headers:
            if h in full_response:
                notes_index = full_response.index(h)
                break

        if notes_index is not None:
            itinerary = full_response[:notes_index].strip()
            notes = full_response[notes_index:].strip()
        else:
            itinerary = full_response
            notes = None

        return JsonResponse({
            "response": itinerary,
            "notes": notes
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
def destinations(request):
    """Renders the popular destinations page with images from the internet."""
    popular_destinations = [
        {
            "name": "Kathmandu, Nepal",
            "image": "https://images.unsplash.com/photo-1580502304784-8985b7eb7260?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8a2F0aG1hbmR1fGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60",
            "description": "Explore the rich cultural heritage and stunning mountain views.",
            "highlights": ["Pashupatinath Temple", "Boudhanath Stupa", "Swayambhunath"]
        },
        {
            "name": "Bali, Indonesia",
            "image": "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YmFsaXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60",
            "description": "A tropical paradise with beautiful beaches and vibrant culture.",
            "highlights": ["Ubud", "Seminyak", "Mount Batur"]
        },
        {
            "name": "Paris, France",
            "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cGFyaXN8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
            "description": "The city of love, known for its art, fashion, and iconic landmarks.",
            "highlights": ["Eiffel Tower", "Louvre Museum", "Notre-Dame"]
        },
        {
            "name": "Tokyo, Japan",
            "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dG9reW98ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
            "description": "A blend of traditional culture and modern technology.",
            "highlights": ["Shibuya Crossing", "Tokyo Tower", "Asakusa Temple"]
        },
        {
            "name": "New York, USA",
            "image": "https://images.unsplash.com/photo-1499092346589-b9b6be3e94b2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3JTIweW9ya3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60",
            "description": "The city that never sleeps, famous for its skyscrapers and vibrant culture.",
            "highlights": ["Statue of Liberty", "Central Park", "Times Square"]
        },
        {
            "name": "Dubai, UAE",
            "image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZHViYWl8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
            "description": "A futuristic city with stunning architecture and luxury experiences.",
            "highlights": ["Burj Khalifa", "Palm Jumeirah", "Dubai Mall"]
        }
    ]

    return render(request, "planner/destinations.html", {
        "destinations": popular_destinations
    })

def guides(request):
    """Renders the travel guides page."""
    travel_guides = [
        {
            "title": "Packing Tips",
            "image": "https://images.unsplash.com/photo-1503220317375-aaad61436b1b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dHJhdmVsJTIwcGFja2luZ3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60",
            "description": "Learn how to pack efficiently for any trip.",
            "tips": [
                "Make a packing list",
                "Use packing cubes",
                "Roll clothes to save space",
                "Pack versatile clothing"
            ]
        },
        {
            "title": "Budget Travel",
            "image": "https://images.unsplash.com/photo-1500835556837-99ac94a94552?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dHJhdmVsJTIwYnVkZ2V0fGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60",
            "description": "Tips for traveling on a budget.",
            "tips": [
                "Book flights in advance",
                "Stay in hostels or budget hotels",
                "Use public transportation",
                "Eat at local restaurants"
            ]
        },
        {
            "title": "Cultural Etiquette",
            "image": "https://images.unsplash.com/photo-1523905330026-b8bd1f5f320e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y3VsdHVyYWwlMjBldGlxdWV0dGV8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
            "description": "How to respect local cultures while traveling.",
            "tips": [
                "Learn basic phrases in the local language",
                "Dress modestly in conservative areas",
                "Respect local customs and traditions",
                "Ask before taking photos of people"
            ]
        },
        {
            "title": "Solo Travel",
            "image": "https://images.unsplash.com/photo-1501554728187-ce583db33af7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c29sbyUyMHRyYXZlbHxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60",
            "description": "Tips for safe and enjoyable solo travel.",
            "tips": [
                "Stay in well-reviewed accommodations",
                "Keep your belongings secure",
                "Share your itinerary with someone",
                "Trust your instincts"
            ]
        },
        {
            "title": "Travel Safety",
            "image": "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dHJhdmVsJTIwc2FmZXR5fGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60",
            "description": "Stay safe while exploring the world.",
            "tips": [
                "Keep copies of important documents",
                "Be aware of your surroundings",
                "Avoid risky areas at night",
                "Use trusted transportation services"
            ]
        }
    ]

    return render(request, "planner/guides.html", {
        "guides": travel_guides
    })


def testimonials(request):
    """Renders the testimonials page."""
    user_testimonials = [
        {
            "name": "Rahul Sharma",
            "image": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dXNlciUyMHByb2ZpbGV8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
            "feedback": "JourneyAI helped me plan the perfect trip to Bali. The itinerary was spot on, and I didn't have to worry about a thing!",
            "rating": 5
        },
        {
            "name": "Priya Patel",
            "image": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dXNlciUyMHByb2ZpbGV8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
            "feedback": "The travel guides were incredibly helpful. I learned so much about cultural etiquette before my trip to Japan.",
            "rating": 4
        },
        {
            "name": "Amit Singh",
            "image": "https://images.unsplash.com/photo-1527980965255-d3b416303d12?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dXNlciUyMHByb2ZpbGV8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
            "feedback": "I used JourneyAI for my solo trip to Nepal. The recommendations were perfect, and I felt safe throughout my journey.",
            "rating": 5
        },
   
    ]

    return render(request, "planner/testimonials.html", {
        "testimonials": user_testimonials
    })

def help(request):
    """Renders the help page with FAQs and contact information."""
    faqs = [
        {
            "question": "How do I create a travel itinerary?",
            "answer": "Go to the 'Create Your Trip' section, fill in your travel details, and click 'Generate Plan'. Our AI will create a personalized itinerary for you."
        },
        {
            "question": "How do I contact customer support?",
            "answer": "You can reach us via email at support@journeyai.com or call us at +91-1234567890."
        },
        {
            "question": "Is JourneyAI free to use?",
            "answer": "Yes, JourneyAI is completely free to use. We may introduce premium features in the future."
        },
        {
            "question": "How accurate are the travel recommendations?",
            "answer": "Our recommendations are based on advanced AI algorithms and user feedback. However, always double-check details like visa requirements and local regulations."
        }
    ]

    return render(request, "planner/help.html", {
        "faqs": faqs
    })