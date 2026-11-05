#!/usr/bin/env python3
"""
Exercise 3: Text Processing and Word Count
Level: Intermediate-Advanced

Learning Objectives:
- Process text files in HDFS
- Implement word count algorithms
- Handle large text processing
- Use regex for text cleaning
- Create text analysis reports

Tasks:
1. Read text file from HDFS
2. Clean and preprocess text
3. Implement word count functionality
4. Find most common words
5. Analyze text patterns
6. Generate comprehensive text analysis report
"""

from hdfs import InsecureClient
import re
from collections import Counter
import json

def exercise3():
    """Complete the text processing tasks"""
    
    # Initialize HDFS connection
    hdfs = InsecureClient('http://namenode:9870')
    
    # TODO: Task 1 - Read text file from HDFS
    # Read /data/sample_text.txt from HDFS
    
    # TODO: Task 2 - Clean and preprocess text
    # Convert to lowercase
    # Remove punctuation and special characters
    # Split into words
    
    # TODO: Task 3 - Implement word count
    # Count frequency of each word
    # Remove common stop words (the, and, is, etc.)
    
    # TODO: Task 4 - Find most common words
    # Get top 10 most frequent words
    # Calculate average word length
    
    # TODO: Task 5 - Analyze patterns
    # Count sentences and paragraphs
    # Find longest and shortest words
    # Calculate text statistics
    
    # TODO: Task 6 - Generate report
    # Create comprehensive analysis report
    # Save results to HDFS
    
    print("Exercise 3 completed!")

def solution_exercise3():
    """Solution for exercise 3"""
    hdfs = InsecureClient('http://namenode:9870')
    
    # Task 1: Read text file
    with hdfs.open('/data/sample_text.txt', 'rt') as f:
        text_content = f.read()
    
    print("Original text:")
    print(text_content[:200] + "..." if len(text_content) > 200 else text_content)
    
    # Task 2: Clean and preprocess text
    # Convert to lowercase and clean
    cleaned_text = text_content.lower()
    
    # Remove punctuation and split into words
    words = re.findall(r'\b[a-z]+\b', cleaned_text)
    
    print(f"\nTotal words found: {len(words)}")
    
    # Task 3: Word count with stop words removal
    stop_words = {
        'the', 'and', 'is', 'to', 'of', 'a', 'an', 'in', 'on', 'at', 'for', 'with',
        'by', 'it', 'are', 'be', 'or', 'as', 'that', 'have', 'has', 'will', 'from',
        'they', 'them', 'their', 'this', 'these', 'those', 'was', 'were', 'been'
    }
    
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    word_counts = Counter(filtered_words)
    
    print(f"Words after filtering: {len(filtered_words)}")
    print(f"Unique words: {len(word_counts)}")
    
    # Task 4: Most common words
    most_common = word_counts.most_common(10)
    print("\nTop 10 most common words:")
    for word, count in most_common:
        print(f"  {word}: {count}")
    
    # Calculate average word length
    avg_length = sum(len(word) for word in filtered_words) / len(filtered_words)
    print(f"\nAverage word length: {avg_length:.2f}")
    
    # Task 5: Text pattern analysis
    sentences = len(re.findall(r'[.!?]+', text_content))
    paragraphs = len([p for p in text_content.split('\n') if p.strip()])
    
    longest_word = max(filtered_words, key=len) if filtered_words else ""
    shortest_word = min(filtered_words, key=len) if filtered_words else ""
    
    print(f"\nText Statistics:")
    print(f"  Sentences: {sentences}")
    print(f"  Paragraphs: {paragraphs}")
    print(f"  Longest word: {longest_word} ({len(longest_word)} chars)")
    print(f"  Shortest word: {shortest_word} ({len(shortest_word)} chars)")
    
    # Task 6: Generate comprehensive report
    hdfs.mkdir('/exercises/exercise3/')
    
    # Save word counts as JSON
    word_count_data = {
        'total_words': len(words),
        'unique_words': len(word_counts),
        'filtered_words': len(filtered_words),
        'most_common_words': dict(most_common),
        'statistics': {
            'average_word_length': round(avg_length, 2),
            'sentences': sentences,
            'paragraphs': paragraphs,
            'longest_word': longest_word,
            'shortest_word': shortest_word
        }
    }
    
    with hdfs.open('/exercises/exercise3/word_analysis.json', 'wt') as f:
        json.dump(word_count_data, f, indent=2)
    
    # Save detailed report
    report = f"""
Text Analysis Report
===================

File Analyzed: /data/sample_text.txt

Basic Statistics:
- Total Words: {len(words)}
- Unique Words: {len(word_counts)}
- Words after filtering: {len(filtered_words)}
- Average Word Length: {avg_length:.2f} characters
- Sentences: {sentences}
- Paragraphs: {paragraphs}

Word Length Analysis:
- Longest Word: "{longest_word}" ({len(longest_word)} characters)
- Shortest Word: "{shortest_word}" ({len(shortest_word)} characters)

Top 10 Most Frequent Words:
"""
    for i, (word, count) in enumerate(most_common, 1):
        report += f"{i:2d}. {word:15s} ({count:2d} occurrences)\n"
    
    report += f"""
Word Frequency Distribution:
- Words appearing once: {sum(1 for count in word_counts.values() if count == 1)}
- Words appearing 2+ times: {sum(1 for count in word_counts.values() if count >= 2)}
- Most frequent word appears: {most_common[0][1] if most_common else 0} times

Analysis completed successfully!
"""
    
    with hdfs.open('/exercises/exercise3/text_analysis_report.txt', 'wt') as f:
        f.write(report)
    
    # Save word frequency list
    word_freq_content = "Word,Frequency\n"
    for word, count in sorted(word_counts.items()):
        word_freq_content += f"{word},{count}\n"
    
    with hdfs.open('/exercises/exercise3/word_frequencies.csv', 'wt') as f:
        f.write(word_freq_content)
    
    print("\nAnalysis results saved to /exercises/exercise3/")
    print("Files created:")
    print("  - word_analysis.json (structured data)")
    print("  - text_analysis_report.txt (detailed report)")
    print("  - word_frequencies.csv (word frequency table)")
    print("Exercise 3 completed!")

if __name__ == "__main__":
    # Run your solution here
    exercise3()
    
    # Uncomment to see the complete solution
    # solution_exercise3()

# Expected Output:
"""
Original text:
This is a sample text file for HDFS operations.
It contains multiple lines of text data.
Students will learn how to:
1. Upload files to HDFS...

Total words found: 89
Words after filtering: 45
Unique words: 38

Top 10 most common words:
  hdfs: 4
  data: 3
  files: 2
  applications: 2
  ...

Text Statistics:
  Sentences: 9
  Paragraphs: 4
  Longest word: applications (12 chars)
  Shortest word: low (3 chars)

Analysis results saved to /exercises/exercise3/
Exercise 3 completed!
"""
