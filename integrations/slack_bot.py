"""
Integration: Slack Bot

AI agent integrated with Slack using Bolt framework.
"""

import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI

# Initialize Bolt app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
client = OpenAI()

# Store conversation context per channel
conversations = {}


@app.event("app_mention")
def handle_mention(event, say):
    """Handle when bot is mentioned"""
    try:
        channel = event["channel"]
        user_message = event["text"]
        
        # Get conversation history
        history = conversations.get(channel, [])
        history.append({"role": "user", "content": user_message})
        
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful Slack assistant."},
                *history
            ]
        )
        
        assistant_message = response.choices[0].message.content
        history.append({"role": "assistant", "content": assistant_message})
        
        # Store conversation (keep last 10 messages)
        conversations[channel] = history[-10:]
        
        # Reply
        say(assistant_message)
        
    except Exception as e:
        say(f"Sorry, I encountered an error: {str(e)}")


@app.command("/agent")
def handle_agent_command(ack, command, say):
    """Handle /agent slash command"""
    ack()
    
    user_input = command["text"]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        
        say(response.choices[0].message.content)
        
    except Exception as e:
        say(f"Error: {str(e)}")


@app.event("message")
def handle_message(event, say):
    """Handle direct messages"""
    # Only respond to DMs
    if event.get("channel_type") == "im":
        user_message = event.get("text", "")
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a friendly Slack bot."},
                    {"role": "user", "content": user_message}
                ]
            )
            
            say(response.choices[0].message.content)
            
        except Exception as e:
            say(f"Sorry, error: {str(e)}")


if __name__ == "__main__":
    # Start the app
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    
    print("⚡️ Slack bot is running!")
    handler.start()
