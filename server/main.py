import random
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
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

async def recommend(request: GiftRecommendationRequest) -> GiftRecommendationResponse:
    messages = parse_whatsapp_messages(request.messages, request.friend_name)
    recommendations = analyze_conversation_for_gifts(messages)
    return GiftRecommendationResponse(
        notes=recommendations["notes"],
        gift_ideas=recommendations["gift_ideas"]
    )


@app.post("/api/analyze-chat", response_model=GiftRecommendationResponse)
async def analyze_chat(
    file: UploadFile = File(...),
    user_name: str = Form(...),
    friend_name: str = Form(...)
):
    """
    Upload a chat history file and get gift recommendations.
    
    This endpoint accepts a text file containing chat history and returns
    personalized gift recommendations based on the content.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Check if the file is a valid format
    if not file.filename.endswith(('.txt')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .txt file")
    
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Log the user and friend names (in a real app, you would use these for personalized recommendations)
        print(f"Analyzing chat between You ({user_name}) and friend ({friend_name})")
        
        # In a real application, this is where you would:
        # 1. Parse the chat history from the uploaded file
        # 2. Process the text using NLP or send to a language model
        # 3. Generate personalized gift recommendations for the specified friend
        
        # # For this demo, we'll just return a random selection of mock recommendations
        # # Number of recommendations to return (between 3 and 6)
        # num_recommendations = random.randint(3, 6)
        
        # # Randomly select recommendations and sort by confidence
        # selected_recommendations = random.sample(MOCK_GIFT_IDEAS, num_recommendations)
        # selected_recommendations.sort(key=lambda x: x.confidence, reverse=True)
        
        recommendations = await recommend(GiftRecommendationRequest(messages=content_str, my_name=user_name, friend_name=friend_name))
        return recommendations

        # # Return the recommendations
        # return RecommendationsResponse(recommendations=selected_recommendations)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 