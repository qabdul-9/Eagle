with open('keywords.txt', 'r') as f:
    keywords = []
    for line in f:
        keyword = line.strip()
        keywords.append(keyword)
print(keywords)

class KeywordManager:    
    def __init__(self):
        self.keywords = set()

    def is_keyword_valid(self, keyword):
        if not isinstance(keyword, str) or not keyword.strip():
            return False
        return True
    
    def is_invalid_keyword(self, keyword):
        return not self.is_keyword_valid(keyword)

