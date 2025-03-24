import re
import logging
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER Lexicon (only required once)
nltk.download('vader_lexicon', quiet=True)

# Initialize Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

# Enable logging for debugging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Financial sentiment keywords
financial_keywords = {

    #  STRONG NEGATIVE KEYWORDS (High Impact, Score: -2.0 to -3.0)
    'layoff': -3.0, 'layoffs': -3.0, 'job cut': -3.0, 'job cuts': -3.0, 'bankrupt': -3.0,
    'bankruptcy': -3.0, 'shutdown': -3.0, 'fraud': -3.0, 'scam': -3.0, 'lawsuit': -2.5,
    'lawsuits': -2.5, 'scandal': -2.5, 'recall': -2.5, 'recalled': -2.5, 'data breach': -3.0,
    'hacked': -2.5, 'cyberattack': -3.0, 'exploit': -2.5, 'vulnerability': -2.0,
    'financial crisis': -2.5, 'downturn': -2.0, 'recession': -3.0, 'earnings miss': -2.5,
    'stock crash': -3.0, 'plummet': -2.5, 'collapse': -3.0, 'default': -3.0, 'delisting': -3.0,
    'insolvency': -3.0, 'liquidation': -3.0, 'foreclosure': -3.0, 'sued': -2.5, 'penalty': -2.5,
    'fine': -2.0, 'regulatory violation': -2.5, 'whistleblower': -2.0, 'outage': -2.0,
    'downgrade': -2.0, 'credit risk': -2.5, 'malware': -2.5, 'ransomware': -3.0, 'phishing': -2.0,
    'leak': -2.5, 'unauthorized access': -2.5, 'dispute': -2.0, 'strike': -2.0, 'boycott': -2.0,
    'protest': -1.5, 'corruption': -3.0, 'bribery': -3.0, 'misconduct': -2.5, 'negligence': -2.5,
    'unsafe': -2.5, 'defect': -2.0, 'failure': -2.5, 'recall': -2.5, 'withdrawal': -2.0,
    'suspended': -2.0, 'blackout': -2.0, 'downtime': -1.5, 'glitch': -1.5, 'bug': -1.5,
    'malfunction': -2.0, 'recall': -2.5, 'crisis': -3.0, 'turmoil': -2.5, 'volatility': -2.0,
    'decline': -2.0, 'slump': -2.0, 'plunge': -2.5, 'dip': -1.5, 'crash': -3.0, 'freefall': -3.0,
    'selloff': -2.5, 'panic': -2.5, 'distress': -2.5, 'chaos': -2.5, 'disaster': -3.0,
    'catastrophe': -3.0, 'fiasco': -2.5, 'debacle': -2.5, 'setback': -2.0, 'loss': -2.0,
    'write-down': -2.5, 'impairment': -2.0, 'default': -3.0, 'delinquency': -2.5, 'breach': -2.5,
    'violation': -2.0, 'infringement': -2.0, 'hacking': -2.5, 'cybercrime': -2.5, 'theft': -2.5,
    'sabotage': -3.0, 'espionage': -2.5, 'misleading': -2.0, 'deceptive': -2.0, 'manipulation': -3.0,
    'insider trading': -3.0, 'money laundering': -3.0, 'sanctions': -2.5, 'embargo': -2.5,

    #  MODERATE NEGATIVE KEYWORDS (Score: -1.0 to -1.9)
    'slowdown': -1.5, 'weak demand': -1.5, 'reduced forecast': -1.5, 'soft sales': -1.5,
    'declining revenue': -1.5, 'profit warning': -1.5, 'underperform': -1.5, 'downgrade': -1.5,
    'delays': -1.5, 'backlog': -1.5, 'supply chain issues': -1.5, 'shortage': -1.5,
    'inflation risk': -1.5, 'higher costs': -1.5, 'margin pressure': -1.5, 'competition': -1.0,
    'price war': -1.5, 'negative review': -1.5, 'poor feedback': -1.5, 'dissatisfaction': -1.5,
    'complaints': -1.5, 'controversy': -1.5, 'investigation': -1.5, 'probe': -1.5, 'audit': -1.0,
    'restructuring': -1.5, 'cost cutting': -1.5, 'headcount reduction': -1.5, 'attrition': -1.0,
    'turnover': -1.0, 'resignation': -1.0, 'exit': -1.0, 'departure': -1.0, 'downtime': -1.5,
    'outage': -1.5, 'latency': -1.0, 'bug': -1.0, 'glitch': -1.0, 'error': -1.0, 'flaw': -1.0,
    'weakness': -1.0, 'uncertainty': -1.5, 'risk': -1.0, 'concerns': -1.0, 'fears': -1.5,
    'headwinds': -1.5, 'challenges': -1.0, 'obstacles': -1.0, 'hurdles': -1.0, 'setback': -1.5,
    'adjustment': -1.0, 'revision': -1.0, 'missed target': -1.5, 'underestimation': -1.0,
    'overestimation': -1.0, 'miscalculation': -1.0, 'volatility': -1.5, 'fluctuation': -1.0,
    'instability': -1.5, 'unrest': -1.5, 'tension': -1.0, 'disagreement': -1.0, 'conflict': -1.5,
    'disruption': -1.5, 'interruption': -1.0, 'bottleneck': -1.0, 'congestion': -1.0,
    'inefficiency': -1.0, 'waste': -1.0, 'excess': -1.0, 'overcapacity': -1.0, 'oversupply': -1.0,
    'shortfall': -1.5, 'deficit': -1.5, 'debt': -1.5, 'leverage': -1.0, 'liquidity issue': -1.5,
    'cash flow problem': -1.5, 'solvency risk': -1.5, 'credit downgrade': -1.5, 'rating cut': -1.5,
    'negative outlook': -1.5, 'caution': -1.0, 'warning': -1.5, 'alert': -1.0, 'advisory': -1.0,
    'recall': -1.5, 'withdrawal': -1.5, 'suspension': -1.5, 'ban': -1.5, 'restriction': -1.0,
    'limitation': -1.0, 'regulation': -1.0, 'compliance issue': -1.5, 'governance risk': -1.5,
    'oversight': -1.0, 'scrutiny': -1.0, 'transparency issue': -1.5, 'accounting issue': -1.5,
    'audit finding': -1.5, 'control weakness': -1.5, 'fraud risk': -2.0, 'misstatement': -1.5,
    'restatement': -1.5, 'irregularity': -1.5, 'anomaly': -1.0, 'deviation': -1.0, 'variance': -1.0,
    'discrepancy': -1.0, 'inconsistency': -1.0, 'non-compliance': -1.5, 'violation': -1.5,
    'penalty': -1.5, 'sanction': -1.5, 'fine': -1.5, 'legal action': -1.5, 'litigation': -1.5,
    'dispute': -1.5, 'arbitration': -1.0, 'mediation': -1.0, 'settlement': -1.0, 'judgment': -1.5,
    'ruling': -1.5, 'verdict': -1.5, 'indictment': -2.0, 'charges': -2.0, 'allegations': -1.5,
    'accusations': -1.5, 'whistleblower': -1.5, 'leak': -1.5, 'expose': -1.5, 'revelation': -1.5,
    'investigation': -1.5, 'probe': -1.5, 'inquiry': -1.0, 'review': -1.0, 'audit': -1.0,
    'examination': -1.0, 'scrutiny': -1.0, 'oversight': -1.0, 'monitoring': -1.0, 'surveillance': -1.0,
    'inspection': -1.0, 'assessment': -1.0, 'evaluation': -1.0, 'appraisal': -1.0, 'analysis': -1.0,
    'diagnosis': -1.0, 'report': -1.0, 'finding': -1.0, 'conclusion': -1.0, 'recommendation': -1.0,
    'suggestion': -1.0, 'advice': -1.0, 'guidance': -1.0, 'direction': -1.0, 'instruction': -1.0,
    'order': -1.0, 'command': -1.0, 'decree': -1.0, 'mandate': -1.0, 'requirement': -1.0,
    'obligation': -1.0, 'duty': -1.0, 'responsibility': -1.0, 'accountability': -1.0,
    'liability': -1.5, 'culpability': -1.5, 'blame': -1.5, 'fault': -1.5, 'error': -1.0,
    'mistake': -1.0, 'oversight': -1.0, 'omission': -1.0, 'neglect': -1.5, 'carelessness': -1.5,
    'recklessness': -1.5, 'irresponsibility': -1.5, 'incompetence': -1.5, 'ineptitude': -1.5,
    'unprofessionalism': -1.5, 'misconduct': -1.5, 'wrongdoing': -1.5, 'malpractice': -1.5,
    'negligence': -1.5, 'breach': -1.5, 'violation': -1.5, 'infraction': -1.5, 'offense': -1.5,
    'crime': -2.0, 'criminal': -2.0, 'illegal': -2.0, 'unlawful': -2.0, 'unauthorized': -1.5,
    'unapproved': -1.5, 'unlicensed': -1.5, 'unregistered': -1.5, 'unregulated': -1.5,
    'noncompliant': -1.5, 'defiant': -1.5, 'rebellious': -1.5, 'insubordinate': -1.5,
    'disobedient': -1.5, 'uncooperative': -1.5, 'unresponsive': -1.5, 'uncommunicative': -1.5,
    'evasive': -1.5, 'secretive': -1.5, 'deceptive': -1.5, 'misleading': -1.5, 'dishonest': -1.5,
    'fraudulent': -2.0, 'corrupt': -2.0, 'bribary': -2.0, 'kickback': -2.0, 'embezzlement': -2.0,
    'theft': -2.0, 'larceny': -2.0, 'robbery': -2.0, 'burglary': -2.0, 'shoplifting': -2.0,
    'vandalism': -2.0, 'sabotage': -2.0, 'arson': -2.0, 'terrorism': -3.0, 'cyberterrorism': -3.0,
    'hactivism': -2.5, 'espionage': -2.5, 'spying': -2.5, 'eavesdropping': -2.0, 'wiretapping': -2.0,
    'surveillance': -1.5, 'monitoring': -1.0, 'tracking': -1.0, 'stalking': -2.0, 'harassment': -2.0,
    'bullying': -2.0, 'intimidation': -2.0, 'threat': -2.0, 'blackmail': -2.0, 'extortion': -2.0,
    'coercion': -2.0, 'duress': -2.0, 'pressure': -1.5, 'influence': -1.0, 'manipulation': -2.0,
    'exploitation': -2.0, 'abuse': -2.0, 'misuse': -1.5, 'waste': -1.5, 'mismanagement': -1.5,
    'mishandling': -1.5, 'misallocation': -1.5, 'diversion': -1.5, 'siphoning': -1.5,
    'laundering': -2.0, 'concealment': -1.5, 'cover-up': -2.0, 'falsification': -2.0,
    'fabrication': -2.0, 'forgery': -2.0, 'counterfeiting': -2.0, 'piracy': -2.0, 'plagiarism': -2.0,
    'infringement': -1.5, 'violation': -1.5, 'breach': -1.5, 'noncompliance': -1.5,
    'nonconformance': -1.5, 'deviation': -1.0, 'variance': -1.0, 'discrepancy': -1.0,
    'inconsistency': -1.0, 'anomaly': -1.0, 'irregularity': -1.5, 'abnormality': -1.0,
    'outlier': -1.0, 'exception': -1.0, 'oddity': -1.0, 'peculiarity': -1.0, 'curiosity': -1.0,
    'aberration': -1.0, 'fluke': -1.0, 'coincidence': -1.0, 'accident': -1.5, 'mishap': -1.5,
    'incident': -1.5, 'event': -1.0, 'occurrence': -1.0, 'situation': -1.0, 'circumstance': -1.0,
    'condition': -1.0, 'state': -1.0, 'status': -1.0, 'position': -1.0, 'posture': -1.0,
    'stance': -1.0, 'attitude': -1.0, 'behavior': -1.0, 'conduct': -1.0, 'action': -1.0,
    'activity': -1.0, 'operation': -1.0, 'performance': -1.0, 'execution': -1.0, 'implementation': -1.0,
    'enforcement': -1.0, 'administration': -1.0, 'management': -1.0, 'supervision': -1.0,
    # Negative terms
    'layoff': -3.0, 'layoffs': -3.0, 'job cut': -3.0, 'slashed': -2.5, 'recession': -2.5,
    'plunge': -2.0, 'crash': -3.0, 'defaults': -2.5, 'crisis': -3.0, 'bankrupt': -3.0,
    'scandal': -2.5, 'investigation': -1.5, 'lawsuit': -1.5, 'fine': -1.5, 'fraud': -3.0,
    'decline': -1.5, 'fell': -1.5, 'loss': -2.0, 'shortfall': -1.5, 'underperform': -1.5,
    'downturn': -1.5, 'failure': -2.0, 'volatile': -1.0, 'warning': -1.5, 'risk': -1.0,

     # Moderate Positive Terms
    'stable growth': 1.5, 'positive outlook': 1.5, 'secured funding': 1.5,
    'new partnership': 1.5, 'steady performance': 1.5, 'solid earnings': 1.5,
    'brand loyalty': 1.5, 'customer expansion': 1.5, 'rising market': 1.5,
    'successful expansion': 1.5, 'improving demand': 1.5, 'digital transformation': 1.5,
    'enhanced security': 1.5, 'technological upgrade': 1.5, 'automation': 1.5,
    'cost efficiency': 1.5, 'operational improvement': 1.5,

    #  Neutral Terms
    'update': 0.0, 'review': 0.0, 'report': 0.0, 'conference': 0.0,
    'announcement': 0.0, 'standard': 0.0, 'meeting': 0.0, 'forecast': 0.0,
    'assessment': 0.0, 'guideline': 0.0, 'recommendation': 0.0,
    'protocol': 0.0, 'strategy': 0.0, 'evaluation': 0.0, 'policy': 0.0,
    'agreement': 0.0, 'procedure': 0.0, 'audit': 0.0, 'presentation': 0.0,
    'industry trends': 0.0, 'white paper': 0.0, 'market update': 0.0,
    'company statement': 0.0,
    # Positive terms
    'surge': 2.0, 'profit': 2.0, 'growth': 1.5, 'recovered': 1.5, 'strong earnings': 2.0,
    'record high': 2.0, 'bull market': 2.0, 'innovation': 1.5, 'merger': 1.5, 'acquisition': 1.5,
    'boom': 2.0, 'thrived': 1.5, 'successful': 2.0, 'breakthrough': 2.0, 'top performer': 2.0
}

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using VADER and financial keywords.

    Args:
        text (str): The text to analyze.

    Returns:
        str: The sentiment of the text ('Positive', 'Negative', or 'Neutral').
    """
    # Preprocess text: Remove punctuation and convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    words = text.split()

    # Calculate custom financial keyword score
    custom_score = sum(financial_keywords.get(word, 0) for word in words)

    # Get the VADER sentiment score
    vader_score = sia.polarity_scores(text)['compound']

    # Combine scores (80% weight to financial terms, 20% to VADER)
    combined_score = (custom_score * 0.8) + (vader_score * 0.2)

    # Debugging Output
    logging.info(f"Text: {text}\nVADER Score: {vader_score}, Custom Score: {custom_score}, Combined: {combined_score}\n")

    # Determine sentiment based on the combined score
    if combined_score >= 0.05:
        return 'Positive'
    elif combined_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def generate_sentiment_report(data):
    """
    Generates a sentiment report for a list of data items.

    Args:
        data (list): A list of dictionaries, where each dictionary contains 'Summary' and any other relevant fields.

    Returns:
        dict: A dictionary containing the sentiment analysis results and comparative analysis.
    """
    report = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for item in data:
        sentiment = analyze_sentiment(item['Summary'])
        report.append({
            'Summary': item['Summary'],
            'Sentiment': sentiment,
            **{k: v for k, v in item.items() if k != 'Summary'}
        })
        if sentiment == 'Positive':
            positive_count += 1
        elif sentiment == 'Negative':
            negative_count += 1
        else:
            neutral_count += 1

    comparative_analysis = {
        'Sentiment Distribution': {
            'Positive': positive_count,
            'Negative': negative_count,
            'Neutral': neutral_count,
        }
    }

    return {'report': report, 'comparative_analysis': comparative_analysis}


if __name__ == '__main__':
    # Example testing data (Replace with actual news data)
    data = [
        {"Summary": "IBM Layoffs: 1000s Of Jobs Could Be Slashed Amid Stocks Slowown"},
        {"Summary": "Bad news for this IT company employees, mass layoffs due to..."},
        {"Summary": "IBM CEO Arvind Krishna may have just 'disagreed' with his 'AI warning' for techies"},
        {"Summary": "What Indian enterprises can learn from IBM’s digital transformation"},
        {"Summary": "Veeam and IBM Release Patches for High-Risk Flaws in Backup and AIX Systems"},
        {"Summary": "IBM Cuts From Roles In Neudesic, Cloud Classic Operations"},
        {"Summary": "Why IBM (IBM) Stock Is Trading Lower Today"},
        {"Summary": "IBM lays off thousands of employees again in new round of layoffs"},
        {"Summary": "IBM's Krishna sees pay surge 23% to $25mn"},
        {"Summary": "IBM’s ACP is an ‘Extension’ of Anthropic’s MCP"},
    ]

    # Run the sentiment analysis
    report = generate_sentiment_report(data)
    print(report)
