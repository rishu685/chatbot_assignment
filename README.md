# Website Content Chatbot (Google Gemini)

A sophisticated chatbot that uses Google's Gemini AI to answer questions about any website's content. Simply provide a URL, and the chatbot will scrape the website content and be able to answer questions about it using Google's powerful AI model.

#  Features

- **Smart Web Scraping**: Extracts title, content, headings, links, and metadata from any website
- **Google Gemini Integration**: Uses Google's latest Gemini 1.5 Flash model for intelligent responses
- **Interactive Console**: User-friendly command-line interface with helpful commands
- **Error Handling**: Robust error handling for network issues, API problems, and invalid inputs
- **Conversation Memory**: Maintains conversation context for natural dialogue
- **Multiple Commands**: Built-in help, info, and website switching capabilities

# Requirements

- Python 3.9 or higher
- Google Gemini API key (get one at https://makersuite.google.com/app/apikey)
- Internet connection for web scraping and API calls

## 🛠️ Installation

1. **Clone or download the project files**
   ```bash
   cd bot_assignment
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Google Gemini API key** (Optional but recommended)
   ```bash
   export GOOGLE_API_KEY="your-api-key-here"
   ```

# Usage

1. **Run the chatbot**
   ```bash
   python website_chatbot.py
   ```

2. **Follow the prompts:**
   - Enter your Google Gemini API key (if not set as environment variable)
   - Enter the website URL you want to analyze
   - Start asking questions about the website content!

3. **Available Commands:**
   - Type any question about the website
   - `help` - Show available commands
   - `info` - Display current website information
   - `new url` - Switch to a different website
   - `quit`, `exit`, or `bye` - End the conversation

##  Example Session

```
🤖 Website Content Chatbot (Powered by Google Gemini)
============================================================
This chatbot can answer questions about any website content!

🔑 Google Gemini API Key Required
Please enter your Google Gemini API key: AIza...

🌐 Website URL Required
Enter website URL: https://github.com/torvalds/linux

📥 Extracting website content...
✅ Website content extracted successfully!
📄 Title: GitHub - torvalds/linux: Linux kernel source tree
📝 Content length: 5000 characters
🔗 Found 10 links
📋 Found 8 headings

============================================================
💬 Chat Started! Type 'quit', 'exit', or 'bye' to end the conversation.
🌐 Current website: https://github.com/torvalds/linux
============================================================

You: What is this repository about?

🤖 Bot: This is the official GitHub repository for the Linux kernel source tree, 
maintained by Linus Torvalds. It contains the complete source code for the Linux 
operating system kernel, which is the core component that manages system resources 
and provides the foundation for Linux-based operating systems...

You: Who maintains this project?

🤖 Bot: Based on the repository information, this project is maintained by Linus 
Torvalds (torvalds), who is the original creator of Linux. The repository shows 
his username as the owner, indicating he has primary responsibility for this 
official Linux kernel source tree...

You: help

📖 Available Commands:
• Type any question about the website content
• 'help' - Show this help message
• 'info' - Show current website information
• 'new url' - Change to a different website
• 'quit', 'exit', 'bye' - End the conversation
```

## Architecture

The chatbot consists of three main components:

## 1. WebsiteContentExtractor
- Handles HTTP requests with proper headers
- Extracts content using BeautifulSoup
- Processes and cleans website data
- Manages different content types (title, headings, links, etc.)

### 2. GeminiBot
- Integrates with Google Gemini API
- Manages conversation context
- Handles API errors and edge cases
- Formats responses appropriately

### 3. WebsiteChatbot
- Orchestrates the entire application
- Manages user interface and interactions
- Handles setup and configuration
- Provides command processing

## Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key

### Supported Website Types
- News websites
- Blogs and articles
- Documentation sites
- E-commerce pages
- Educational content
- GitHub repositories
- Wikipedia articles
- And many more!

#Limitation
- Some websites may block automated requests
- JavaScript-heavy sites might not be fully scraped
- Very large websites are limited to first 5000 characters
- API rate limits may apply based on your Google Cloud plan

## Troubleshooting

### Common Issues

1. **"Invalid API key" error**
   - Verify your Google Gemini API key is correct
   - Check if the key starts with 'AI'
   - Ensure the key has proper permissions

2. **"Website content extraction failed"**
   - Check if the URL is accessible
   - Try adding 'https://' prefix
   - Some websites may block automated requests

3. **"API quota exceeded"**
   - Check your Google Cloud billing and quotas
   - Wait for quota reset or upgrade your plan

4. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.9+ required)

## License

This project is provided for educational purposes. Please ensure you comply with website terms of service when scraping content.

##  Contributing

This is an assignment project, but suggestions and improvements are welcome!

## 🔗 Useful Links

- [Google AI Studio](https://makersuite.google.com/app/apikey) - Get your API key
- [Google Gemini Documentation](https://ai.google.dev/docs) - API documentation
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web scraping guide

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This chatbot is designed for educational purposes to demonstrate web scraping and AI integration. Always respect robots.txt and website terms of service when scraping content.
