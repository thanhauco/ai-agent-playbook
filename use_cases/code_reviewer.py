"""
Real-World Use Case: Code Reviewer Agent

An automated code review agent that:
- Analyzes code for bugs and issues
- Checks best practices
- Provides improvement suggestions
- Uses structured outputs for consistency
"""

from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Literal
import json

client = OpenAI()


class CodeIssue(BaseModel):
    """A single code issue"""
    severity: Literal["critical", "warning", "info"]
    line_number: int
    issue_type: str
    description: str
    suggestion: str


class CodeReview(BaseModel):
    """Structured code review output"""
    overall_score: int = Field(ge=0, le=100, description="Overall code quality score")
    issues: List[CodeIssue]
    strengths: List[str]
    summary: str
    approved: bool


def analyze_code(code: str, language: str = "python") -> CodeReview:
    """Analyze code and return structured review"""
    
    response = client.beta.chat.completions.parse(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are a senior software engineer conducting code reviews.

Analyze code for:
- Bugs and potential errors
- Security vulnerabilities  
- Performance issues
- Code style and readability
- Best practices

Provide constructive feedback with specific suggestions."""
            },
            {
                "role": "user",
                "content": f"Review this {language} code:\n\n```{language}\n{code}\n```"
            }
        ],
        response_format=CodeReview
    )
    
    return response.choices[0].message.parsed


def format_review(review: CodeReview) -> str:
    """Format review for display"""
    output = []
    output.append(f"{'=' * 70}")
    output.append(f"CODE REVIEW REPORT")
    output.append(f"{'=' * 70}")
    output.append(f"\n📊 Overall Score: {review.overall_score}/100")
    output.append(f"✅ Approved: {'Yes' if review.approved else 'No'}\n")
    
    if review.strengths:
        output.append("💪 Strengths:")
        for strength in review.strengths:
            output.append(f"  • {strength}")
        output.append("")
    
    if review.issues:
        output.append(f"🔍 Issues Found ({len(review.issues)}):\n")
        for i, issue in enumerate(review.issues, 1):
            severity_emoji = {"critical": "🔴", "warning": "🟡", "info": "🔵"}
            emoji = severity_emoji.get(issue.severity, "⚪")
            output.append(f"{i}. {emoji} Line {issue.line_number} - {issue.issue_type}")
            output.append(f"   {issue.description}")
            output.append(f"   💡 Suggestion: {issue.suggestion}\n")
    
    output.append(f"\n📝 Summary:\n{review.summary}")
    output.append(f"\n{'=' * 70}")
    
    return "\n".join(output)


def demo():
    """Demo the code reviewer"""
    
    # Sample code with intentional issues
    sample_code = '''
def process_user_data(data):
    # No input validation
    user_id = data["id"]
    
    # SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    
    # No error handling
    result = execute_query(query)
    
    # Inefficient loop
    for i in range(len(result)):
        print(result[i])
    
    return result
'''
    
    print("=== Code Reviewer Agent Demo ===\n")
    print("Analyzing code...\n")
    
    try:
        review = analyze_code(sample_code)
        print(format_review(review))
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: This example uses OpenAI's structured outputs.")
        print("Requires OPENAI_API_KEY and gpt-4 model access.")


if __name__ == "__main__":
    demo()
