"""
LlamaIndex - Workflow Example

Workflows in LlamaIndex allow sophisticated orchestration with loops,
branches, and complex control flow.
"""

from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    step,
    Event
)
from typing import Optional

# Note: Install with: pip install llama-index-core


class ProcessDataEvent(Event):
    """Event for data processing step"""
    data: str


class AnalyzeEvent(Event):
    """Event for analysis step"""
    processed_data: str


class DecisionEvent(Event):
    """Event for decision making"""
    analysis_result: str
    needs_review: bool


class ResearchWorkflow(Workflow):
    """
    A workflow that:
    1. Receives a research topic
    2. Processes it
    3. Analyzes the topic
    4. Makes a decision (simple or complex)
    5. Returns final result
    """
    
    @step
    async def start(self, ev: StartEvent) -> ProcessDataEvent:
        """Entry point - receive topic"""
        topic = ev.get("topic", "AI agents")
        print(f"📝 Starting research on: {topic}")
        return ProcessDataEvent(data=topic)
    
    @step
    async def process_data(self, ev: ProcessDataEvent) -> AnalyzeEvent:
        """Process the research topic"""
        processed = f"Processed: {ev.data} - gathering sources..."
        print(f"⚙️  {processed}")
        return AnalyzeEvent(processed_data=processed)
    
    @step
    async def analyze(self, ev: AnalyzeEvent) -> DecisionEvent:
        """Analyze the processed data"""
        # Simple analysis logic
        is_complex = "AI" in ev.processed_data or "agent" in ev.processed_data
        analysis = f"Analysis complete - Complexity: {'High' if is_complex else 'Low'}"
        print(f"🔍 {analysis}")
        return DecisionEvent(
            analysis_result=analysis,
            needs_review=is_complex
        )
    
    @step
    async def make_decision(self, ev: DecisionEvent) -> StopEvent:
        """Make final decision and return result"""
        if ev.needs_review:
            result = f"✅ {ev.analysis_result} - Requires expert review"
        else:
            result = f"✅ {ev.analysis_result} - Auto-approved"
        
        print(f"🎯 Decision: {result}")
        return StopEvent(result=result)


async def run_workflow_example():
    """Run the LlamaIndex workflow"""
    try:
        workflow = ResearchWorkflow(timeout=60, verbose=True)
        
        # Run workflow with different topics
        topics = [
            "AI agents and automation",
            "Simple data analysis",
            "Machine learning agents"
        ]
        
        for topic in topics:
            print(f"\n{'='*60}")
            print(f"WORKFLOW: {topic}")
            print('='*60)
            result = await workflow.run(topic=topic)
            print(f"Final Result: {result}\n")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires 'llama-index-core'.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_workflow_example())
