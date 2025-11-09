class KeywordManager:    
    def __init__(self):
        self.keywords = []

    def load_keywords(self, filepath):
        with open(filepath, 'r') as f:
            self.keywords = [line.strip() for line in f if line.strip()]

    def is_keyword_valid(self, keyword):
        if not isinstance(keyword, str):
            return False
        if not keyword.strip():
            return False
        return True
    
    def is_invalid_keyword(self, keyword):
        return not self.is_keyword_valid(keyword)
    
    def get_keywords(self):
        return self.keywords



