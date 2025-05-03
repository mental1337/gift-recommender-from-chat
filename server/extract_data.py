from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import json
import re
import litellm
from litellm import completion

class WishSignal(BaseModel):
    item: str = Field(description="The item the person wants")
    quote: str = Field(description="The exact quote expressing desire for something")
    date: str = Field(description="Date of the conversation")
    sentiment_strength: int = Field(description="Strength of desire from 1-5, with 5 being strongest")

class ProblemStatement(BaseModel):
    quote: str = Field(description="The exact quote describing a problem or complaint")
    date: str = Field(description="Date of the conversation")
    severity: int = Field(description="How severe the problem is, from 1 (annoying) to 5 (critical)")

class EnthusiasmMarker(BaseModel):
    topic: str = Field(description="The specific topic, activity, or item generating enthusiasm")
    quotes: List[str] = Field(description="The quotes showing enthusiasm")
    intensity: int = Field(description="Intensity of enthusiasm from 1 (slight) to 5 (strong)")

class ValueIndication(BaseModel):
    value: str = Field(description="Values the person explicitly or implicitly expresses")
    quotes: List[str] = Field(description="The quotes showing the value")
    intensity: int = Field(description="Intensity of value from 1 (slight) to 5 (strong)")

class FriendSignals(BaseModel):
    direct_wish_signals: List[WishSignal] = Field(
        default_factory=list,
        description="Explicit mentions of things the person wants, needs, or wishes for"
    )
    
    problems: List[ProblemStatement] = Field(
        default_factory=list,
        description="Complaints, frustrations, or challenges mentioned that could be addressed by a gift"
    )
    
    enthusiasm_signals: List[EnthusiasmMarker] = Field(
        default_factory=list,
        description="Topics, activities, or items the person shows strong positive emotion about"
    )

    values: List[ValueIndication] = Field(
        default_factory=list,
        description="Personal values that could inform thoughtful gift selection"
    )

def create_conversation_chunks(messages: List[tuple[datetime, str]], chunk_size: int) -> List[str]:
    """
    Create chunks of conversation for processing.
    
    Args:
        messages: List of tuples containing (timestamp, message_text)
        chunk_size: Number of messages per chunk
        
    Returns:
        List of formatted conversation string chunks
    """
    chunks = []
    
    for i in range(0, len(messages), chunk_size):
        chunk_messages = messages[i:i + chunk_size]
        
        # Format the chunk as a readable conversation
        chunk_text = ""
        for timestamp, message in chunk_messages:
            date_str = timestamp.strftime("%Y-%m-%d")
            chunk_text += f"[{date_str}] {message}\n\n"
            
        chunks.append(chunk_text)
        
    return chunks

def get_format_instructions(model_class: BaseModel) -> str:
    """
    Generate format instructions for the model.
    
    Args:
        model_class: Pydantic model class
        
    Returns:
        String with formatting instructions
    """
    schema = model_class.model_json_schema()
    schema_str = json.dumps(schema, indent=2)
    
    return f"""
    Return the data in the following JSON format:
    
    {schema_str}
    
    Ensure the output is valid JSON that adheres to this schema.
    """

def extract_information(
    messages: List[tuple[datetime, str]],
    chunk_size: int = 10,
    model: str = "anthropic/claude-3-haiku-20240307"
) -> FriendSignals:
    """
    Process conversation history to extract gift-related signals using LiteLLM.
    
    Args:
        messages: List of tuples containing (timestamp, message_text)
        chunk_size: Number of messages to process in each chunk
        model: LLM model to use
        
    Returns:
        FriendSignals object containing all extracted information
    """
    # Format instructions for the model
    format_instructions = get_format_instructions(FriendSignals)
    
    # Create conversation chunks
    conversation_chunks = create_conversation_chunks(messages, chunk_size)
    
    # Initialize the results object
    all_signals = FriendSignals()
    
    # Process each chunk
    for chunk in conversation_chunks:
        try:
            # Craft the prompt
            prompt = f"""
            You are an AI specializing in analyzing conversations to extract information useful for selecting thoughtful gifts.
            
            Analyze the following conversation history and extract specific signals that could help with gift selection.
            
            CONVERSATION CHUNK:
            ```
            {chunk}
            ```
            
            For each category below, extract relevant information ONLY if it exists in the text:
            
            1. DIRECT WISH SIGNALS: When the person explicitly mentions wanting something
            2. PROBLEMS: Complaints or frustrations that could be addressed with a gift
            3. ENTHUSIASM SIGNALS: Topics or activities the person shows excitement about
            4. VALUES: Personal values that could inform gift selection
            
            {format_instructions}
            
            If a category has no valid examples in this conversation chunk, return an empty list for that category.
            Only include items with clear supporting evidence in the conversation.
            """
            
            # Get the LLM response using LiteLLM
            response = litellm.completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            # Extract the content from the response
            content = response.choices[0].message.content
            
            # Parse the response as JSON
            chunk_signals = FriendSignals.model_validate_json(content)
            
            # Add unique signals from this chunk to our full results
            # Direct wish signals
            for wish in chunk_signals.direct_wish_signals:
                if wish.quote not in [w.quote for w in all_signals.direct_wish_signals]:
                    all_signals.direct_wish_signals.append(wish)
                    
            # Problems
            for problem in chunk_signals.problems:
                if problem.quote not in [p.quote for p in all_signals.problems]:
                    all_signals.problems.append(problem)
                    
            # Enthusiasm signals - merge by topic
            for enthusiasm in chunk_signals.enthusiasm_signals:
                existing = next((e for e in all_signals.enthusiasm_signals if e.topic == enthusiasm.topic), None)
                if existing:
                    # Merge quotes and take the higher intensity
                    for quote in enthusiasm.quotes:
                        if quote not in existing.quotes:
                            existing.quotes.append(quote)
                    existing.intensity = max(existing.intensity, enthusiasm.intensity)
                else:
                    all_signals.enthusiasm_signals.append(enthusiasm)
                    
            # Values - merge by value
            for value_indication in chunk_signals.values:
                existing = next((v for v in all_signals.values if v.value == value_indication.value), None)
                if existing:
                    # Merge quotes and take the higher intensity
                    for quote in value_indication.quotes:
                        if quote not in existing.quotes:
                            existing.quotes.append(quote)
                    existing.intensity = max(existing.intensity, value_indication.intensity)
                else:
                    all_signals.values.append(value_indication)
                
        except Exception as e:
            print(f"Error processing chunk: {e}")
            continue
    
    return all_signals

def generate_gift_recommendations(
    signals: FriendSignals, 
    budget_range: str = "any",
    model: str = "anthropic/claude-3-opus-20240229"
) -> List[Dict]:
    """
    Generate gift recommendations based on the extracted signals using LiteLLM.
    
    Args:
        signals: FriendSignals object with extracted information
        budget_range: String indicating budget constraints (e.g., "under $50", "$100-$200")
        model: LLM model to use
        
    Returns:
        List of gift recommendations with reasoning
    """
    # Format the signals for the prompt
    wish_signals_text = "\n".join([f"- {wish.item}: \"{wish.quote}\" (Desire strength: {wish.sentiment_strength}/5)" 
                                 for wish in signals.direct_wish_signals])
    
    problems_text = "\n".join([f"- \"{problem.quote}\" (Severity: {problem.severity}/5)" 
                             for problem in signals.problems])
    
    enthusiasm_text = "\n".join([f"- {enthusiasm.topic} (Intensity: {enthusiasm.intensity}/5)\n  Example: \"{enthusiasm.quotes[0] if enthusiasm.quotes else ''}\"" 
                               for enthusiasm in signals.enthusiasm_signals])
    
    values_text = "\n".join([f"- {value.value} (Intensity: {value.intensity}/5)\n  Example: \"{value.quotes[0] if value.quotes else ''}\"" 
                           for value in signals.values])
    
    # Handle empty cases
    if not wish_signals_text: wish_signals_text = "None detected"
    if not problems_text: problems_text = "None detected"
    if not enthusiasm_text: enthusiasm_text = "None detected"
    if not values_text: values_text = "None detected"
    
    # Craft the recommendation prompt
    recommendation_prompt = f"""
    Based on the following information extracted from conversations with a friend, 
    suggest 5 thoughtful gift ideas within a {budget_range} budget.
    
    DIRECT WISH SIGNALS:
    {wish_signals_text}
    
    PROBLEMS THEY'VE MENTIONED:
    {problems_text}
    
    TOPICS THEY'RE ENTHUSIASTIC ABOUT:
    {enthusiasm_text}
    
    VALUES THEY CARE ABOUT:
    {values_text}
    
    For each recommendation:
    1. Describe the gift
    2. Explain why it would be meaningful based on the signals
    3. Rate how well it matches their expressed interests (1-5)
    4. Suggest personalization options
    
    Return a JSON array where each item has these keys:
    - gift_name: The name of the gift
    - description: Brief description
    - reasoning: Why this gift matches their signals
    - match_score: 1-5 rating of how well it matches
    - personalization: Ideas to make it more special
    """
    
    # Get gift recommendations using LiteLLM
    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": recommendation_prompt}],
        temperature=0.7,
        max_tokens=2000,
        response_format={"type": "json_object"}
    )
    
    # Extract the content from the response
    content = response.choices[0].message.content
    
    # Parse the recommendations from the response
    recommendations = []
    try:
        response_json = json.loads(content)
        
        # Check if the response has a "recommendations" key or is an array directly
        if "recommendations" in response_json:
            recommendations = response_json["recommendations"]
        elif isinstance(response_json, list):
            recommendations = response_json
        else:
            # Look for any key that contains a list of recommendations
            for key, value in response_json.items():
                if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                    if "gift_name" in value[0]:
                        recommendations = value
                        break
            
    except Exception as e:
        print(f"Error parsing recommendations: {e}")
        
    return recommendations

# Function to create a complete gift intelligence system
def analyze_conversation_for_gifts(
    messages: List[tuple[datetime, str]],
    friend_name: str,
    budget_range: str = "any",
    chunk_size: int = 10
) -> Dict:
    """
    Complete pipeline to analyze conversations and generate gift recommendations.
    
    Args:
        messages: List of tuples containing (timestamp, message_text)
        friend_name: Name of the friend
        budget_range: Budget constraint for gift recommendations
        chunk_size: Number of messages per processing chunk
        
    Returns:
        Dictionary with signals and recommendations
    """
    print(f"Analyzing conversations with {friend_name}...")
    signals = extract_information(messages, chunk_size)
    
    print(f"Generating gift recommendations within {budget_range} budget...")
    recommendations = generate_gift_recommendations(signals, budget_range)
    
    return {
        "friend_name": friend_name,
        "signals": signals.model_dump(),
        "recommendations": recommendations
    }

# Example usage
if __name__ == "__main__":
    # Configure LiteLLM (optional)
    # litellm.set_verbose=True
    
    # Sample conversation history
    sample_messages = [
        (datetime(2025, 3, 1), "I really want to get into rock climbing but all the gear is so expensive!"),
        (datetime(2025, 3, 2), "My coffee maker broke yesterday. Starting the day without coffee is the worst."),
        (datetime(2025, 3, 5), "I'm so excited about that new Thai restaurant. The food was amazing!"),
        (datetime(2025, 3, 10), "Have you read that new book on sustainable living? I'm thinking of changing how I shop."),
        (datetime(2025, 3, 15), "I hate how cold my apartment gets in the evening. I'm always freezing."),
        (datetime(2025, 3, 20), "Just saw an amazing documentary on marine conservation. We need to do more to protect the oceans."),
        (datetime(2025, 3, 25), "I love these handmade ceramics! So much better than mass-produced stuff."),
        (datetime(2025, 4, 1), "My birthday is coming up next month. No big plans yet."),
        (datetime(2025, 4, 5), "My hands are so dry from all this hand washing. Nothing seems to help."),
        (datetime(2025, 4, 10), "I would love to visit Japan next year. The cherry blossoms look incredible!")
    ]
    
    # Run the complete analysis
    results = analyze_conversation_for_gifts(
        messages=sample_messages,
        friend_name="Alex",
        budget_range="$20-$100"
    )
    
    # Print the results
    print(json.dumps(results, indent=2))
