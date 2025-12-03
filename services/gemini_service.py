"""
Gemini LLM Service
Handles all interactions with Google's Gemini API
"""

import google.generativeai as genai
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        """Initialize Gemini API with API key from environment"""
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        # Initialize the model - Gemini 2.5 Flash (latest fast model)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Configure generation settings
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 1024,
        }
        
        logger.info("Gemini service initialized successfully")
    
    def generate_response(self, user_query: str, language: str = 'english', 
                         context: Optional[str] = None) -> str:
        """
        Generate a response to user query using Gemini
        
        Args:
            user_query: The user's question or message
            language: Preferred response language
            context: Optional conversation context
        
        Returns:
            Generated response text
        """
        try:
            # Construct the prompt with language and context
            system_prompt = self._build_system_prompt(language)
            
            full_prompt = f"{system_prompt}\n\nUser Query: {user_query}"
            
            if context:
                full_prompt = f"Context: {context}\n\n{full_prompt}"
            
            # Generate response
            response = self.model.generate_content(
                full_prompt,
                generation_config=self.generation_config
            )
            
            # Extract text from response
            response_text = response.text
            
            logger.info(f"Generated response for query: {user_query[:50]}...")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._get_fallback_response(language)
    
    def _build_system_prompt(self, language: str) -> str:
        """Build system prompt based on language and use case"""
        
        language_instructions = {
            'tamil': 'தயவுசெய்து தமிழில் பதிலளிக்கவும். (Please respond in Tamil)',
            'telugu': 'దయచేసి తెలుగులో సమాధానం ఇవ్వండి. (Please respond in Telugu)',
            'hindi': 'कृपया हिंदी में जवाब दें। (Please respond in Hindi)',
            'english': 'Please respond in English.'
        }
        
        base_prompt = """You are a helpful AI assistant for farmers and agricultural workers.
You provide practical advice on:
- Farming techniques and best practices
- Crop management and pest control
- Weather and seasonal recommendations
- Market prices and selling tips
- Government schemes and subsidies

Keep your responses:
- Clear and concise (2-3 sentences)
- Practical and actionable
- Friendly and supportive
- In the requested language
"""
        
        lang_instruction = language_instructions.get(language, language_instructions['english'])
        
        return f"{base_prompt}\n\n{lang_instruction}"
    
    def _get_fallback_response(self, language: str) -> str:
        """Return a fallback response if API fails"""
        fallback_messages = {
            'tamil': 'மன்னிக்கவும், எனக்கு இப்போது பதிலளிக்க முடியவில்லை. மீண்டும் முயற்சிக்கவும்.',
            'telugu': 'క్షమించండి, నేను ప్రస్తుతం సమాధానం ఇవ్వలేను. దయచేసి మళ్లీ ప్రయత్నించండి.',
            'hindi': 'क्षमा करें, मैं अभी जवाब नहीं दे सकता। कृपया पुनः प्रयास करें।',
            'english': 'Sorry, I am unable to respond right now. Please try again.'
        }
        
        return fallback_messages.get(language, fallback_messages['english'])
