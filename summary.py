from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


# Example text

def summ(text) :
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
# Parse the input text
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)
    ans=""
    ans=' '.join(map(str,summary))
    return ans
   




# Initialize the LSA summarizer

# Generate the summary
  # Number of sentences in summary

