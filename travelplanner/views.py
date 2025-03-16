from django.shortcuts import render
from django.http import JsonResponse
from gradio_client import Client

def index(request):
    """Renders the main AI Travel Planner UI."""
    return render(request, "planner/index.html")

def plan_trip(request):
    """Handles user input and returns an AI-generated travel itinerary in JSON format."""
    
    if request.method == "POST":
        start_location = request.POST.get("start_location", "").strip()
        destination = request.POST.get("destination", "").strip()
        duration = request.POST.get("duration", "").strip()

        # Validate inputs
        if not start_location or not destination or not duration:
            return JsonResponse({"error": "All fields are required!"}, status=400)

        try:
            # Call AI Travel API
            client = Client("wolf1997/travel_agent")
            response = client.predict(
                message=f"I want to travel from {start_location} to {destination} for {duration}. Suggest an itinerary.",
                api_name="/chat"
            )

            return JsonResponse({"response": response})

        except Exception as e:
            return JsonResponse({"error": f"API Error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
