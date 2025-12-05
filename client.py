import xmlrpc.client
import time

# Configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 8000
SERVER_URL = f'http://{SERVER_HOST}:{SERVER_PORT}/RPC2'

def display_status(message):
    """Helper function to display status messages with timestamp"""
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{timestamp}] {message}")

def analyze_user_input():
    """Main client function for interactive sentiment analysis"""
    display_status("🔵 Starting Khmer Sentiment Analysis Client")
    display_status(f"🖥️  Connecting to server at {SERVER_URL}")

    try:
        # Connect to the server
        with xmlrpc.client.ServerProxy(SERVER_URL) as proxy:
            display_status("✅ Successfully connected to the server")
            print("\n" + "="*50)
            display_status("Type 'exit' to quit the program")
            
            while True:
                # Get user input
                print("\n" + "-"*50)
                khmer_text = input("Enter Khmer text to analyze sentiment: ").strip()
                
                if khmer_text.lower() == 'exit':
                    break
                
                if not khmer_text:
                    display_status("⚠️  Please enter some text")
                    continue
                
                display_status(f"📩 Sending text for analysis: '{khmer_text}'")
                
                try:
                    # Call the remote procedure
                    display_status("🔄 Processing sentiment analysis...")
                    start_time = time.time()
                    result = proxy.analyze_sentiment(khmer_text)
                    elapsed_time = time.time() - start_time
                    
                    # Display results
                    display_status(f"⏱️  Analysis completed in {elapsed_time:.2f} seconds")
                    print("\n🔍 Analysis Result:")
                    print(f"Input: {khmer_text}")
                    print(f"Result: {result}")
                    
                except Exception as e:
                    display_status(f"🔴 Error during analysis: {str(e)}")
                
    except ConnectionError:
        display_status("🔴 Error: Could not connect to the server. Is it running?")
    except Exception as e:
        display_status(f"🔴 Unexpected error: {str(e)}")
    
    display_status("🔵 Client session ended")

if __name__ == "__main__":
    analyze_user_input()

# សម្ដេចពុកលោកវាយកូនហ្គោល ស៊ុតឡបញ្ចូលពូកែខ្លាំងណាស់ (ទិចនិចពិតជាត្រង់ច្បាស់ ទឹកដៃជើងចាស់រហ័សរហួន)
# Stop doing that, you stupid shit. I don't want to see that again.
# ឈប់ឆ្គួតទៅ គេមិនស្រលាញ់យើងទេ