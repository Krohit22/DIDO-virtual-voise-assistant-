from keywords import get_keywords_Dic
Keywords = get_keywords_Dic()
def detect_command(user_input):
    """Detect which command the user is requesting based on keywords"""
    if not user_input:  # 🛑 Prevent None from being processed
        return None
   
    
    for command, phrases in Keywords.items():
        if any(phrase in user_input for phrase in phrases):
            return command 
    return None