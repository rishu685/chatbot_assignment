#!/usr/bin/env python3
"""
Website Content Chatbot using Google Gemini API

This chatbot fetches content from a given website URL and uses it as context
to answer user questions via the Google Gemini API.

Author: AI Assistant
Date: September 9, 2025
"""

import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
import sys
import re
from urllib.parse import urljoin, urlparse
import time
from typing import Optional, Dict, List


class WebsiteContentExtractor:
    """Handles web scraping and content extraction from websites."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_website_content(self, url: str) -> Optional[Dict[str, str]]:
        """
        Fetch and extract content from a website URL.
        
        Args:
            url (str): The website URL to scrape
            
        Returns:
            Dict containing extracted content or None if failed
        """
        try:
            print(f"Fetching content from: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
            
            # Extract different content types
            content = {
                'title': self._extract_title(soup),
                'main_content': self._extract_main_content(soup),
                'headings': self._extract_headings(soup),
                'links': self._extract_links(soup, url),
                'meta_description': self._extract_meta_description(soup),
                'url': url
            }
            
            return content
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching website content: {e}")
            return None
        except Exception as e:
            print(f"Error processing website content: {e}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        title = soup.find('title')
        return title.get_text().strip() if title else "No title found"
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main textual content from the page."""
        # Try to find main content areas
        main_selectors = ['main', 'article', '.content', '#content', '.main', '#main']
        main_content = ""
        
        for selector in main_selectors:
            elements = soup.select(selector)
            if elements:
                main_content = " ".join([elem.get_text().strip() for elem in elements])
                break
        
        # Fallback to body content if no main content found
        if not main_content:
            body = soup.find('body')
            if body:
                main_content = body.get_text()
        
        # Clean up the text
        main_content = re.sub(r'\s+', ' ', main_content).strip()
        return main_content[:5000]  # Limit content length for API efficiency
    
    def _extract_headings(self, soup: BeautifulSoup) -> List[str]:
        """Extract all headings (h1-h6) from the page."""
        headings = []
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                text = heading.get_text().strip()
                if text:
                    headings.append(f"H{i}: {text}")
        return headings[:20]  # Limit number of headings
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract important links from the page."""
        links = []
        for link in soup.find_all('a', href=True)[:10]:  # Limit to first 10 links
            href = link['href']
            full_url = urljoin(base_url, href)
            link_text = link.get_text().strip()
            if link_text:
                links.append(f"{link_text}: {full_url}")
        return links
    
    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description."""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        return "No meta description found"


class GeminiBot:
    """Handles interaction with Google Gemini API."""
    
    def __init__(self, api_key: str):
        """
        Initialize the Gemini bot.
        
        Args:
            api_key (str): Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.conversation_history = []
        self.website_content = None
        self.max_history = 10  # Limit conversation history
    
    def set_website_context(self, content: Dict[str, str]):
        """
        Set website content as context for the chatbot.
        
        Args:
            content (Dict): Extracted website content
        """
        self.website_content = content
        
        # Create a structured context from the website content
        context_parts = [
            f"Website Title: {content['title']}",
            f"URL: {content['url']}",
            f"Meta Description: {content['meta_description']}",
        ]
        
        if content['headings']:
            context_parts.append("Key Headings:")
            context_parts.extend(content['headings'][:10])
        
        if content['main_content']:
            context_parts.append(f"Main Content: {content['main_content']}")
        
        if content['links']:
            context_parts.append("Important Links:")
            context_parts.extend(content['links'][:5])
        
        self.context = "\n".join(context_parts)
    
    def chat(self, user_message: str) -> str:
        """
        Process user message and generate response using Gemini API.
        
        Args:
            user_message (str): User's input message
            
        Returns:
            str: Gemini's response
        """
        try:
            # Create the prompt with website context
            prompt = f"""You are a helpful assistant that can answer questions about a specific website. 
            Here is the website content for context:
            
            {self.context}
            
            Please answer user questions based on this website content. If the question cannot be answered 
            from the website content, politely let the user know and provide general helpful information if possible.
            
            User Question: {user_message}
            
            Please provide a helpful response:"""
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            if response.text:
                bot_response = response.text.strip()
                
                # Add to conversation history for context
                self.conversation_history.append({"user": user_message, "bot": bot_response})
                
                # Keep only recent history
                if len(self.conversation_history) > self.max_history:
                    self.conversation_history = self.conversation_history[-self.max_history:]
                
                return bot_response
            else:
                return "I'm sorry, I couldn't generate a response. Please try rephrasing your question."
            
        except Exception as e:
            error_msg = str(e).lower()
            if "api key" in error_msg or "authentication" in error_msg:
                return "Error: Invalid Google Gemini API key. Please check your API key and try again."
            elif "quota" in error_msg or "limit" in error_msg:
                return "Error: API quota exceeded. Please check your Google Cloud account."
            elif "safety" in error_msg:
                return "Error: Content was blocked by safety filters. Please try rephrasing your question."
            else:
                return f"Error: An unexpected error occurred - {e}"


class WebsiteChatbot:
    """Main chatbot class that orchestrates web scraping and ChatGPT interaction."""
    
    def __init__(self):
        self.content_extractor = WebsiteContentExtractor()
        self.chatbot = None
        self.website_url = None
    
    def setup(self):
        """Setup the chatbot with API key and website URL."""
        print("=" * 60)
        print("🤖 Website Content Chatbot (Powered by Google Gemini)")
        print("=" * 60)
        print("This chatbot can answer questions about any website content!")
        print()
        
        # Get Google Gemini API key
        api_key = self._get_api_key()
        if not api_key:
            print("❌ Cannot proceed without API key.")
            return False
        
        # Initialize chatbot with API key
        self.chatbot = GeminiBot(api_key)
        
        # Get website URL
        url = self._get_website_url()
        if not url:
            print("❌ Cannot proceed without website URL.")
            return False
        
        # Extract website content
        print("\n📥 Extracting website content...")
        content = self.content_extractor.fetch_website_content(url)
        if not content:
            print("❌ Failed to extract website content.")
            return False
        
        # Set website context for chatbot
        self.chatbot.set_website_context(content)
        self.website_url = url
        
        print("✅ Website content extracted successfully!")
        print(f"📄 Title: {content['title']}")
        print(f"📝 Content length: {len(content['main_content'])} characters")
        print(f"🔗 Found {len(content['links'])} links")
        print(f"📋 Found {len(content['headings'])} headings")
        
        return True
    
    def _get_api_key(self) -> Optional[str]:
        """Get Google Gemini API key from user or environment."""
        # First check environment variable
        api_key = os.environ.get('GOOGLE_API_KEY')
        if api_key:
            print("✅ Found Google Gemini API key in environment variable.")
            return api_key
        
        # Ask user for API key
        print("🔑 Google Gemini API Key Required")
        print("You can get your API key from: https://makersuite.google.com/app/apikey")
        print("Or set the GOOGLE_API_KEY environment variable.")
        print()
        
        api_key = input("Please enter your Google Gemini API key: ").strip()
        if not api_key:
            return None
        
        # Basic validation
        if not api_key.startswith('AI'):
            print("⚠️  Warning: Google API key typically starts with 'AI'")
        
        return api_key
    
    def _get_website_url(self) -> Optional[str]:
        """Get website URL from user."""
        print("\n🌐 Website URL Required")
        print("Enter the URL of the website you want the chatbot to learn about.")
        print("Example: https://www.example.com")
        print()
        
        while True:
            url = input("Enter website URL: ").strip()
            if not url:
                return None
            
            # Add https:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Basic URL validation
            parsed = urlparse(url)
            if parsed.netloc:
                return url
            else:
                print("❌ Invalid URL format. Please try again.")
    
    def run(self):
        """Main chatbot interaction loop."""
        if not self.setup():
            return
        
        print("\n" + "=" * 60)
        print("💬 Chat Started! Type 'quit', 'exit', or 'bye' to end the conversation.")
        print(f"🌐 Current website: {self.website_url}")
        print("=" * 60)
        print()
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\n👋 Goodbye! Thanks for using the Website Content Chatbot!")
                    break
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Special commands
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif user_input.lower() == 'info':
                    self._show_website_info()
                    continue
                elif user_input.lower().startswith('new url'):
                    self._change_website()
                    continue
                
                # Generate and display response
                print("\n🤖 Bot: ", end="")
                response = self.chatbot.chat(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Website Content Chatbot!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again.\n")
    
    def _show_help(self):
        """Display help information."""
        print("\n📖 Available Commands:")
        print("• Type any question about the website content")
        print("• 'help' - Show this help message")
        print("• 'info' - Show current website information")
        print("• 'new url' - Change to a different website")
        print("• 'quit', 'exit', 'bye' - End the conversation")
        print()
    
    def _show_website_info(self):
        """Display current website information."""
        if self.chatbot and self.chatbot.website_content:
            content = self.chatbot.website_content
            print(f"\n📋 Current Website Information:")
            print(f"🌐 URL: {content['url']}")
            print(f"📄 Title: {content['title']}")
            print(f"📝 Description: {content['meta_description']}")
            print(f"🔗 Links found: {len(content['links'])}")
            print(f"📋 Headings found: {len(content['headings'])}")
            print()
    
    def _change_website(self):
        """Allow user to change to a different website."""
        print("\n🔄 Changing website...")
        url = self._get_website_url()
        if url:
            print("📥 Extracting new website content...")
            content = self.content_extractor.fetch_website_content(url)
            if content:
                self.chatbot.set_website_context(content)
                self.website_url = url
                print("✅ Website changed successfully!")
                print(f"📄 New title: {content['title']}")
            else:
                print("❌ Failed to extract content from new website.")
        print()


def main():
    """Main function to run the chatbot."""
    try:
        chatbot = WebsiteChatbot()
        chatbot.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
