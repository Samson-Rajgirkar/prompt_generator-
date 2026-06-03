"""
dataset.py – Sample dataset for training the intent/category classifier.

Categories:
  - creative    : creative writing, storytelling, imagination
  - technical   : coding, engineering, debugging, systems
  - analytical  : data analysis, research, reasoning, logic
  - educational : teaching, explaining, learning, tutoring
  - business    : marketing, strategy, sales, entrepreneurship
  - conversational: casual chat, advice, opinion
"""

# ---------------------------------------------------------------------------
# Labelled training data  (text, category)
# ---------------------------------------------------------------------------
TRAINING_DATA = [
    # ── creative ────────────────────────────────────────────────────────────
    ("write a short story about a dragon", "creative"),
    ("help me write a poem about the ocean", "creative"),
    ("create a fantasy world with magic", "creative"),
    ("I need lyrics for a love song", "creative"),
    ("write a screenplay scene for a thriller", "creative"),
    ("describe a futuristic city in detail", "creative"),
    ("give me ideas for a science fiction novel", "creative"),
    ("write a haiku about spring", "creative"),
    ("create a character backstory for my RPG", "creative"),
    ("write a horror story opening", "creative"),
    ("compose a limerick about coffee", "creative"),
    ("describe a sunset over the mountains beautifully", "creative"),
    ("write dialogue between two time travelers", "creative"),
    ("create a myth about the origin of thunder", "creative"),
    ("help me name my fantasy kingdom", "creative"),
    ("write an alternate history where Rome never fell", "creative"),
    ("create a villain with a compelling motivation", "creative"),
    ("write a children's bedtime story", "creative"),
    ("describe an alien landscape", "creative"),
    ("write a mystery story hook", "creative"),

    # ── technical ───────────────────────────────────────────────────────────
    ("fix my Python function that returns wrong output", "technical"),
    ("how do I implement a binary search tree", "technical"),
    ("explain REST API design best practices", "technical"),
    ("debug this JavaScript async/await code", "technical"),
    ("how to set up Docker for a Django project", "technical"),
    ("write a SQL query to join three tables", "technical"),
    ("help me optimize this database query", "technical"),
    ("explain how recursion works with examples", "technical"),
    ("create a CI/CD pipeline configuration", "technical"),
    ("how do I handle authentication in React", "technical"),
    ("write a bash script to automate backups", "technical"),
    ("explain microservices architecture", "technical"),
    ("help me design a RESTful endpoint", "technical"),
    ("what is the difference between TCP and UDP", "technical"),
    ("how to implement rate limiting in Django", "technical"),
    ("write unit tests for this class", "technical"),
    ("explain big O notation with examples", "technical"),
    ("how to secure a web application against SQL injection", "technical"),
    ("help me implement a caching layer with Redis", "technical"),
    ("debug my CSS flexbox layout issue", "technical"),

    # ── analytical ──────────────────────────────────────────────────────────
    ("analyze the trends in this dataset", "analytical"),
    ("compare the pros and cons of solar vs nuclear energy", "analytical"),
    ("what factors contributed to the 2008 financial crisis", "analytical"),
    ("evaluate this business model for weaknesses", "analytical"),
    ("help me interpret these survey results", "analytical"),
    ("what statistical method should I use for this study", "analytical"),
    ("analyze the sentiment of customer reviews", "analytical"),
    ("give a logical breakdown of this argument", "analytical"),
    ("research the impact of social media on mental health", "analytical"),
    ("compare Python and R for data science", "analytical"),
    ("what are the key performance indicators for this metric", "analytical"),
    ("analyze competitor pricing strategies", "analytical"),
    ("identify patterns in this time series data", "analytical"),
    ("evaluate the risks of this investment", "analytical"),
    ("how does correlation differ from causation", "analytical"),
    ("give a SWOT analysis for a startup", "analytical"),
    ("what does this p-value mean in my research", "analytical"),
    ("compare cloud providers for a data pipeline", "analytical"),
    ("analyze the efficiency of this algorithm", "analytical"),
    ("what are the logical fallacies in this argument", "analytical"),

    # ── educational ─────────────────────────────────────────────────────────
    ("explain quantum mechanics to a beginner", "educational"),
    ("teach me how photosynthesis works", "educational"),
    ("what is the difference between mitosis and meiosis", "educational"),
    ("explain the French Revolution in simple terms", "educational"),
    ("how does the stock market work", "educational"),
    ("teach me the basics of machine learning", "educational"),
    ("explain Newton's laws of motion", "educational"),
    ("what is blockchain and how does it work", "educational"),
    ("how do I learn to play guitar", "educational"),
    ("explain the human digestive system", "educational"),
    ("what is climate change and why does it matter", "educational"),
    ("teach me basic Spanish phrases", "educational"),
    ("how does the immune system fight infections", "educational"),
    ("explain the theory of relativity simply", "educational"),
    ("what is the difference between classical and operant conditioning", "educational"),
    ("teach me how to read financial statements", "educational"),
    ("explain how vaccines work", "educational"),
    ("what are the causes and effects of World War II", "educational"),
    ("how does GPS navigation work", "educational"),
    ("explain the periodic table to me", "educational"),

    # ── business ────────────────────────────────────────────────────────────
    ("write a product launch email campaign", "business"),
    ("help me create a pitch deck for investors", "business"),
    ("write a business plan for a coffee shop", "business"),
    ("create social media content for my brand", "business"),
    ("help me write a job description for a developer", "business"),
    ("what is the best pricing strategy for a SaaS product", "business"),
    ("write a customer onboarding email sequence", "business"),
    ("create a sales funnel for my e-commerce store", "business"),
    ("write a professional LinkedIn post", "business"),
    ("help me negotiate a vendor contract", "business"),
    ("create a marketing strategy for a new app", "business"),
    ("write an executive summary for my report", "business"),
    ("how do I reduce customer churn", "business"),
    ("write a cold outreach email to potential clients", "business"),
    ("create an OKR framework for my startup", "business"),
    ("help me write performance review feedback", "business"),
    ("what is a go-to-market strategy", "business"),
    ("write a press release for a product update", "business"),
    ("create a customer persona for my target audience", "business"),
    ("help me calculate unit economics for my business", "business"),

    # ── conversational ───────────────────────────────────────────────────────
    ("what do you think about artificial intelligence", "conversational"),
    ("give me advice on work life balance", "conversational"),
    ("what should I watch on Netflix tonight", "conversational"),
    ("help me decide between two job offers", "conversational"),
    ("what are your thoughts on remote work", "conversational"),
    ("give me motivation to go to the gym", "conversational"),
    ("what is a good hobby to pick up", "conversational"),
    ("help me plan a weekend trip", "conversational"),
    ("what are some fun facts about space", "conversational"),
    ("recommend a good book to read", "conversational"),
    ("help me write a toast speech for a wedding", "conversational"),
    ("give me tips for better sleep", "conversational"),
    ("what are the best productivity hacks", "conversational"),
    ("recommend healthy meal prep ideas", "conversational"),
    ("how do I deal with a difficult coworker", "conversational"),
    ("give me advice on saving money", "conversational"),
    ("what is a good morning routine", "conversational"),
    ("help me choose a gift for my friend", "conversational"),
    ("how do I improve my public speaking", "conversational"),
    ("what are some stress relief techniques", "conversational"),
]

# ---------------------------------------------------------------------------
# Tone detection dataset
# ---------------------------------------------------------------------------
TONE_DATA = [
    ("Write this formally and professionally", "formal"),
    ("Can you make it more casual and friendly", "casual"),
    ("I need this to be very detailed and thorough", "detailed"),
    ("Keep it short and to the point", "concise"),
    ("Make it creative and imaginative", "creative"),
    ("Write it technically with precise language", "technical"),
    ("Make it persuasive and convincing", "persuasive"),
    ("Keep it simple and easy to understand", "simple"),
]
