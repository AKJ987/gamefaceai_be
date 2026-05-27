import io
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from openai import OpenAI

class GameFaceAIAPIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            visual_style = request.data.get('visual_style')
            if not visual_style or visual_style not in ["ghibili", "action_figure", "lego"]:
                return Response(data={"status": "failed", "error": "Invalid Visual Style"}, status=400)

            name = request.data.get('name')
            if not name:
                return Response(data={"status": "failed", "error": "Invalid Name"}, status=400)
            
            gender = request.data.get('gender')
            if not gender or gender not in ["male", "female"]:
                return Response(data={"status": "failed", "error": "Invalid Gender"}, status=400)
                        
            image = request.FILES.get('image')
            if not image:
                return Response(data={"status": "failed", "error": "Invalid Image"}, status=400)
            
            game_details = {
                "uncharted": "Nathan Drake",
                "ghost_of_tsushima": "Jin Sakai",
                "mafia": "Lincoln Clay",
                "red_dead_redemption": "Arthur Morgan",
                "gta_vice_city": "Tommy Vercetti",
                "total_overdose": "Ramiro Cruz",
                "sleeping_dogs": "Wei Shen",
                "assassins_creed": "Edward Kenway",
                "cyberpunk": "Vincent"
            }
            game = request.data.get('game')
            if not game and game not in game_details.keys():
                return Response(data={"status": "failed", "error": "Invalid Game"}, status=400)

            # Read the bytes
            image_bytes = image.read()
            # Convert to BytesIO stream
            image_file = io.BytesIO(image_bytes)
            image_file.name = f"{name}.png"

            game_name = game.replace("_", " ").title()
            game_character = game_details.get(game)
            style = visual_style.replace("_", " ").title()
            hashtag = game.replace("_", "").upper()

            prompt = (
                f"Capture the image added to create a full-body cinematic illustration of {game_name} character {game_character} in {style} style. "
                f"The character must be centered and shown head-to-toe in a heroic pose. "
                f"At the top of the image, display the name {name} in bold cinematic typography. "
                f"On both sides of the character, include thematic tools and effects related to the character. "
                f"The background should be cinematic and immersive, matching the character's universe. "
                f"At the bottom footer, create a clean aligned layout: Game logo in the center, developer's logo on the left, and “#{hashtag}” on the right, all equal size and perfectly balanced. "
            )

            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            result = client.images.edit(
                model="gpt-image-1",
                image=[image_file],
                prompt=prompt,
                quality="medium",
                size="1024x1536"
            )

            image_base64 = result.data[0].b64_json
            return Response(data={"status": "success", "image": image_base64}, status=200)

        except Exception as e:
            # Catch and return any unexpected errors
            return Response(data={"status": "failed", "error": str(e)}, status=400)
