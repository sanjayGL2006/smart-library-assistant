import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import AIConversation, AIMessage
from .services.rag import retrieve_context
from .services.mode_parser import parse_mode
from .services.modes import MODES_CONFIG

@login_required
def ai_chat_page(request):
    return render(request, "knowledge/ai_chat.html")

@login_required
@require_POST
def ask_ai(request):
    try:
        data = json.loads(
            request.body
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "Invalid JSON."
            },
            status=400
        )

    question = data.get(
        "question",
        ""
    ).strip()

    if not question:
        return JsonResponse(
            {
                "error": "Question is required."
            },
            status=400
        )
        
    if len(question) > 1000:
        return JsonResponse(
            {
                "error": "Question is too long. Maximum length is 1000 characters."
            },
            status=400
        )

    conversation_id = data.get(
        "conversation_id"
    )

    if conversation_id:
        try:
            conversation = AIConversation.objects.get(
                id=conversation_id,
                user=request.user
            )
        except AIConversation.DoesNotExist:
            return JsonResponse(
                {
                    "error": "Conversation not found."
                },
                status=404
            )
    else:
        conversation = AIConversation.objects.create(
            user=request.user,
            title=question[:100]
        )

    parsed = parse_mode(question)
    mode = parsed["mode"]
    cleaned_question = parsed["question"]
    
    mode_config = MODES_CONFIG.get(mode, MODES_CONFIG["default"])
    retrieval_limit = mode_config.get("retrieval_limit", 5)

    context, results = retrieve_context(
        cleaned_question,
        limit=retrieval_limit
    )

    sources = []

    for result in results:
        metadata = result["metadata"]

        sources.append({
            "filename": metadata.get(
                "filename"
            ),
            "subject": metadata.get(
                "subject"
            ),
            "topic": metadata.get(
                "topic"
            ),
            "page": metadata.get(
                "page_number"
            )
        })

    AIMessage.objects.create(
        conversation=conversation,
        role="user",
        content=question
    )

    # Temporary response.
    # Replace this with the actual LLM provider.
    answer = (
        f"Mode Detected: [{mode_config['display_name']}]\n"
        f"Question parsed: {cleaned_question}\n"
        f"Retrieval Limit: {retrieval_limit}\n\n"
        "Knowledge retrieved successfully.\n\n"
        f"{context[:5000]}"
    )

    AIMessage.objects.create(
        conversation=conversation,
        role="assistant",
        content=answer,
        sources=sources
    )

    return JsonResponse({
        "conversation_id": conversation.id,
        "mode": mode,
        "mode_display_name": mode_config["display_name"],
        "answer": answer,
        "sources": sources
    })
