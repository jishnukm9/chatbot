



import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from .models import Conversation
import json
import uuid





@csrf_exempt
@require_http_methods(["POST"])
def chat_view(request):

    template = """
    You are a helpful AI assistant engaged in a natural conversation. Always maintain a consistent and friendly personality.

    Here is your personality and behavior guide:
    - Be concise but friendly in responses
    - Remember and use the user's name when appropriate
    - Maintain context from previous messages
    - Ask follow-up questions when relevant
    - Provide direct, clear answers

    Previous conversation:
    {context}

    Current message: {question}

    Respond naturally as you would in a terminal conversation:"""


    model = OllamaLLM(
    model="llama3.2:3b",)
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        # Get or create conversation with improved error handling
        try:
            conversation = Conversation.objects.get(session_id=session_id)
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create(
                session_id=session_id,
                context="System: Conversation started. Remember to be helpful and maintain context."
            )

        # Get recent conversation history with improved formatting
        conversation_history = get_recent_history(conversation.context)
        
        # Generate response with error handling and timeout
        try:
            result = chain.invoke({
                "context": conversation_history,
                "question": user_message
            })
        except Exception as e:
            print(f"Model inference error: {str(e)}")
            return JsonResponse({
                'error': 'Failed to generate response. Please try again.'
            }, status=500)

        # Clean and format the response
        cleaned_result = result.strip()
        
        # Update conversation context with improved formatting
        new_exchange = (
            f"User: {user_message}\n"
            f"Assistant: {cleaned_result}"
        )
        
        if not conversation.context:
            conversation.context = new_exchange
        else:
            conversation.context = f"{conversation.context}\n\n{new_exchange}"

        # Trim context if it gets too long (prevent database issues)
        if len(conversation.context) > 10000:  # Adjust based on your needs
            conversation.context = get_recent_history(conversation.context, max_exchanges=5)

        conversation.save()

      

        return JsonResponse({
            'response': cleaned_result,
            'session_id': session_id
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)







@csrf_exempt
@require_http_methods(["POST"])
def chat_doc_view(request):

    template = """
    You are a helpful AI assistant engaged in a natural conversation. Always maintain a consistent and friendly personality.

    Here is your personality and behavior guide:
    - Be concise but friendly in responses
    - Remember and use the user's name when appropriate
    - Maintain context from previous messages
    - Ask follow-up questions when relevant
    - Provide direct, clear answers

    Previous conversation:
    {context}

    Here is the content you should use to answer questions:
    {content}

    Current message: {question}

    Instructions:
    1. If the question can be answered using the provided content, provide a clear and relevant answer
    2. If the question cannot be answered using the provided content, politely inform the user that the question is outside the scope of the available information and ask them to ask questions about the provided content
    3. You may use specific quotes or references from the content to support your answers

    Response:"""


    model = OllamaLLM(
    model="llama3.2:3b",)
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model



    current_dir = os.path.dirname(os.path.abspath(__file__))

    data_file_path = os.path.join(current_dir, 'data.txt')

    with open(data_file_path, "r", encoding='utf-8') as file:
            content = file.read()


    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        # Get or create conversation with improved error handling
        try:
            conversation = Conversation.objects.get(session_id=session_id)
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create(
                session_id=session_id,
                context="System: Conversation started. Remember to be helpful and maintain context."
            )

        # Get recent conversation history with improved formatting
        conversation_history = get_recent_history(conversation.context)
        
        # Generate response with error handling and timeout
        try:
            result = chain.invoke({
                "context": conversation_history,
                "content":content,
                "question": user_message
            })
        except Exception as e:
            print(f"Model inference error: {str(e)}")
            return JsonResponse({
                'error': 'Failed to generate response. Please try again.'
            }, status=500)

        # Clean and format the response
        cleaned_result = result.strip()
        
        # Update conversation context with improved formatting
        new_exchange = (
            f"User: {user_message}\n"
            f"Assistant: {cleaned_result}"
        )
        
        if not conversation.context:
            conversation.context = new_exchange
        else:
            conversation.context = f"{conversation.context}\n\n{new_exchange}"

        # Trim context if it gets too long (prevent database issues)
        if len(conversation.context) > 10000:  # Adjust based on your needs
            conversation.context = get_recent_history(conversation.context, max_exchanges=5)

        conversation.save()

      

        return JsonResponse({
            'response': cleaned_result,
            'session_id': session_id
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)



def get_recent_history(context, max_exchanges=10):
    """
    Keep only the most recent conversation exchanges with improved formatting
    """
    if not context:
        return ""
    
    # Split by double newline to separate exchanges
    exchanges = context.split('\n\n')
    
    # Keep only complete exchanges
    valid_exchanges = [
        exchange for exchange in exchanges
        if 'User:' in exchange and 'Assistant:' in exchange
    ]
    
    # Get recent exchanges
    recent_exchanges = valid_exchanges[-max_exchanges:] if len(valid_exchanges) > max_exchanges else valid_exchanges
    
    return '\n\n'.join(recent_exchanges)










@csrf_exempt
@require_http_methods(["POST"])
def answer_view(request):
    model = OllamaLLM(
    model="llama3.2:3b",)

    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        # session_id = data.get('session_id', str(uuid.uuid4()))

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

    
        
        # Generate response with error handling and timeout
        try:
            result = model.invoke(input=user_message)
        except Exception as e:
            print(f"Model inference error: {str(e)}")
            return JsonResponse({
                'error': 'Failed to generate response. Please try again.'
            }, status=500)

        return JsonResponse({
            'response': result,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)











@csrf_exempt
@require_http_methods(["POST"])
def answer_from_doc_view(request):
    template = """
    You are a helpful AI assistant that answers questions based on the provided content.
    
    Here is your personality and behavior guide:
    - Be concise but friendly in responses
    - Provide direct, clear answers
    
    Here is the content you should use to answer questions:
    {context}
    
    The user's question is: {question}
    
    Instructions:
    1. If the question can be answered using the provided content, provide a clear and relevant answer
    2. If the question cannot be answered using the provided content, politely inform the user that the question is outside the scope of the available information and ask them to ask questions about the provided content
    3. You may use specific quotes or references from the content to support your answers
    
    Response:
    """
    model = OllamaLLM(
    model="llama3.2:3b",)
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    

    current_dir = os.path.dirname(os.path.abspath(__file__))

    data_file_path = os.path.join(current_dir, 'data.txt')

    with open(data_file_path, "r", encoding='utf-8') as file:
            content = file.read()

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        # session_id = data.get('session_id', str(uuid.uuid4()))

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        # Generate response with error handling and timeout
        try:
            result = chain.invoke({
                "context": content,
                "question": user_message
            })
        except Exception as e:
            print(f"Model inference error: {str(e)}")
            return JsonResponse({
                'error': 'Failed to generate response. Please try again.'
            }, status=500)

        return JsonResponse({
            'response': result,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)