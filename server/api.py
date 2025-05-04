import pydantic

class GiftRecommendationRequest(pydantic.BaseModel):
    messages: str
    my_name: str
    friend_name: str

class GiftIdea(pydantic.BaseModel):
    name: str
    link: str
    description: str

class GiftRecommendationResponse(pydantic.BaseModel):
    notes: str
    gift_ideas: list[GiftIdea]
