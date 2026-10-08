import requests
import pandas as pd
import time
import re
from collections import Counter
import random

class CatFactAnalyzer:
    def __init__(self):
        self.base_url = "https://catfact.ninja/fact"
        self.facts = []
        
    def crawl_cat_facts(self, num_facts=20):
        print("🐱 Starting the Great Cat Fact Expedition...")
        print(f"📊 Collecting {num_facts} scientifically important cat facts...")
        
        for i in range(num_facts):
            try:
                response = requests.get(self.base_url, timeout=10)
                if response.status_code == 200:
                    fact_data = response.json()
                    self.facts.append({
                        'fact': fact_data['fact'],
                        'length': fact_data['length']
                    })
                    print(f"✅ Fact {i+1}/{num_facts} acquired: {fact_data['fact'][:50]}...")
                else:
                    print(f"❌ Fact {i+1} failed to load (Status: {response.status_code})")
                
                # Be nice to the API
                time.sleep(0.5)
                
            except requests.RequestException as e:
                print(f"🚫 Network error getting fact {i+1}: {e}")
                continue
    
    def analyze_facts(self):
        if not self.facts:
            print("❌ No facts to analyze! The cats are disappointed.")
            return
            
        df = pd.DataFrame(self.facts)
        
        print("\n" + "="*60)
        print("🔬 CAT FACT SCIENTIFIC ANALYSIS REPORT 🔬")
        print("="*60)
        
        # Basic stats
        print(f"\n📊 BASIC STATISTICS:")
        print(f"   Total facts collected: {len(df)}")
        print(f"   Average fact length: {df['length'].mean():.1f} characters")
        print(f"   Shortest fact: {df['length'].min()} characters")
        print(f"   Longest fact: {df['length'].max()} characters")
        
        # Find the longest and shortest facts
        shortest_fact = df.loc[df['length'].idxmin(), 'fact']
        longest_fact = df.loc[df['length'].idxmax(), 'fact']
        
        print(f"\n🏆 RECORD HOLDERS:")
        print(f"   Most concise cat wisdom: \"{shortest_fact}\"")
        print(f"   Most verbose cat knowledge: \"{longest_fact[:100]}{'...' if len(longest_fact) > 100 else ''}\"")
        
        # Word analysis
        all_text = ' '.join(df['fact'].str.lower())
        words = re.findall(r'\b[a-z]{3,}\b', all_text)
        word_counts = Counter(words)
        
        print(f"\n🎯 WORD FREQUENCY ANALYSIS:")
        print("   Top 5 most important cat-related words:")
        for word, count in word_counts.most_common(5):
            print(f"   • '{word}': mentioned {count} times")
        
        # Fun metrics
        self.calculate_fun_metrics(df, all_text)
        
        # Display some random facts
        print(f"\n🎲 RANDOM CAT WISDOM SAMPLES:")
        sample_facts = df.sample(min(3, len(df)))
        for i, (_, row) in enumerate(sample_facts.iterrows(), 1):
            print(f"   {i}. {row['fact']}")
    
    def calculate_fun_metrics(self, df, all_text):
        print(f"\n😸 FUN METRICS & SCIENTIFIC ASSESSMENTS:")
        
        # Cuteness factor
        cute_words = ['cute', 'adorable', 'sweet', 'purr', 'kitten', 'fluffy', 'soft']
        cute_score = sum(all_text.count(word) for word in cute_words)
        print(f"   💖 Cuteness Factor: {cute_score}/10 (based on cute word density)")
        
        # Mysterious cat behavior mentions
        mystery_words = ['behavior', 'mysterious', 'strange', 'weird', 'unknown']
        mystery_score = sum(all_text.count(word) for word in mystery_words)
        print(f"   🔮 Mystery Level: {mystery_score}/10 (cats remain enigmatic)")
        
        # Historical importance
        history_words = ['ancient', 'egypt', 'worship', 'goddess', 'pharaoh', 'temple']
        history_score = sum(all_text.count(word) for word in history_words)
        print(f"   🏺 Historical Significance: {history_score}/10 (cats ruled ancient world)")
        
        # Practical usefulness
        practical_words = ['hunt', 'mouse', 'rat', 'pest', 'useful', 'work']
        practical_score = sum(all_text.count(word) for word in practical_words)
        print(f"   🎯 Practical Utility: {practical_score}/10 (actual job performance)")
        
        # Calculate overall cat appreciation index
        total_score = cute_score + mystery_score + history_score + practical_score
        appreciation_level = "MAXIMUM" if total_score > 15 else "HIGH" if total_score > 10 else "MODERATE" if total_score > 5 else "DEVELOPING"
        print(f"   🌟 Overall Cat Appreciation Index: {appreciation_level}")
        print(f"      (Based on {total_score} total cat-positive indicators)")

def main():
    print("🚀 Initializing Docker Cat Fact Analysis System...")
    print("🐾 This is a completely serious scientific endeavor...")
    
    analyzer = CatFactAnalyzer()
    
    try:
        # Crawl facts
        analyzer.crawl_cat_facts(15)  # Reduced for demo purposes
        
        # Analyze the data
        analyzer.analyze_facts()
        
        print("\n" + "="*60)
        print("✅ Analysis complete! The cats approve of this research.")
        print("🐱 Docker container has successfully processed feline data!")
        print("="*60)
        
    except Exception as e:
        print(f"💥 Something went wrong in cat fact analysis: {e}")
        print("🐱 The cats are not amused...")

if __name__ == "__main__":
    main()