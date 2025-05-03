from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from parser import parse_whatsapp_messages
from extract_data import analyze_conversation_for_gifts
from api import GiftRecommendationRequest, GiftRecommendationResponse

app = FastAPI(title="Gift Recommender API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Gift Recommender API"}

@app.post("/recommend")
async def recommend(request: GiftRecommendationRequest) -> GiftRecommendationResponse:
    messages = parse_whatsapp_messages(request.messages, request.friend_name)
    recommendations = analyze_conversation_for_gifts(messages)
    return GiftRecommendationResponse(
        notes=recommendations["notes"],
        gift_ideas=recommendations["gift_ideas"]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 