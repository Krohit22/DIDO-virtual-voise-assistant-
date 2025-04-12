from keywords import get_keywords_Dic
Keywords = get_keywords_Dic()
def detect_command(user_input):
    """Detect which command the user is requesting based on keywords"""
    if not user_input:  # 🛑 Prevent None from being processed
        return None
    user_input = user_input.lower()
    
    for command, phrases in Keywords.items():

        if any(phrase.lower() in user_input for phrase in phrases):
            return command 
    return None